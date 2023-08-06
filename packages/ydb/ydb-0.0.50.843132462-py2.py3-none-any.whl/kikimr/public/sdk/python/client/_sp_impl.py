# -*- coding: utf-8 -*-
import collections
from concurrent import futures
from six.moves import queue
import logging
import time
import threading
from . import settings, issues, _utilities

logger = logging.getLogger(__name__)


class SessionPoolImpl(object):
    def __init__(self, driver, size, workers_threads_count=4, initializer=None, min_pool_size=0):
        self._lock = threading.RLock()
        self._waiters = collections.OrderedDict()
        self._driver = driver
        self._active_queue = queue.PriorityQueue()
        self._active_count = 0
        self._size = size
        self._req_settings = settings.BaseRequestSettings().with_timeout(3)
        self._tp = futures.ThreadPoolExecutor(workers_threads_count)
        self._initializer = initializer
        self._should_stop = threading.Event()
        self._keep_alive_threshold = 4 * 60
        self._spin_timeout = 30
        self._event_queue = queue.Queue()
        self._driver_await_timeout = 3
        self._event_loop_thread = threading.Thread(target=self.events_loop)
        self._event_loop_thread.daemon = True
        self._event_loop_thread.start()
        self._logger = logger.getChild(self.__class__.__name__)
        self._min_pool_size = min_pool_size
        self._terminating = False
        if self._min_pool_size > self._size:
            raise ValueError("Invalid min pool size value!")
        for _ in range(self._min_pool_size):
            self._prepare(self._create())

    def stop(self, timeout):
        with self._lock:
            self._logger.debug("Requested session pool stop.")
            self._event_queue.put(self._terminate_event)
            self._should_stop.set()
            self._terminating = True

            self._logger.debug("Session pool is under stop, cancelling all in flight waiters.")
            while True:
                try:
                    _, waiter = self._waiters.popitem(last=False)
                    session = self._create()
                    waiter.set_result(session)
                    self._logger.debug(
                        "Waiter %s has been replied with empty session info. Session details: %s.", waiter, session)
                except KeyError:
                    break

            self._logger.debug("Destroying sessions in active queue")
            while True:
                try:
                    _, session = self._active_queue.get(block=False)
                    self._destroy(session)

                except queue.Empty:
                    break

            self._logger.debug("Destroyed active sessions")

        self._event_loop_thread.join(timeout)

    def _terminate_event(self):
        self._logger.debug("Terminated session pool.")
        raise StopIteration()

    def _delayed_prepare(self, session):
        try:
            self._driver.wait(self._driver_await_timeout)
        except futures.TimeoutError:
            pass

        self._prepare(session)

    def pick(self):
        with self._lock:
            try:
                priority, session = self._active_queue.get_nowait()
            except queue.Empty:
                return None

            till_expire = priority - time.time()
            if till_expire < self._keep_alive_threshold:
                return session
            self._active_queue.put((priority, session))
            return None

    def _create(self):
        with self._lock:
            session = self._driver.table_client.session()
            self._logger.debug("Created session %s", session)
            self._active_count += 1
            return session

    @property
    def active_size(self):
        with self._lock:
            return self._active_count

    @property
    def free_size(self):
        with self._lock:
            return self._active_queue.qsize()

    @property
    def busy_size(self):
        with self._lock:
            return self._active_count - self._active_queue.qsize()

    @property
    def max_size(self):
        return self._size

    @property
    def waiters_count(self):
        with self._lock:
            return len(self._waiters)

    def _is_min_pool_size_satisfied(self, delta=0):
        if self._terminating:
            return True
        return self._active_count + delta >= self._min_pool_size

    def _destroy(self, session):
        self._logger.debug("Requested session destroy: %s.", session)
        with self._lock:
            self._active_count -= 1
            self._logger.debug("Session %s is no longer active. Current active count %d.", session, self._active_count)
            cnt_waiters = len(self._waiters)
            if cnt_waiters > 0:
                self._logger.debug(
                    "In flight waiters: %d, preparing session %s replacement.", cnt_waiters, session)
                # we have a waiter that should be replied, so we have to prepare replacement
                self._prepare(self._create())
            elif not self._is_min_pool_size_satisfied():
                self._logger.debug("Current session pool size is less than %s, actual size %s", self._min_pool_size, self._active_count)
                self._prepare(self._create())

        if session.initialized():
            session.async_delete(self._req_settings)
            self._logger.debug("Sent delete on session %s", session)

    def put(self, session):
        with self._lock:
            self._logger.debug("Put on session %s", session)
            if session.pending_query():
                self._destroy(session)
                return False

            if not session.initialized() or self._should_stop.is_set():
                self._destroy(session)
                # we should probably prepare replacement session here
                return False

            try:
                _, waiter = self._waiters.popitem(last=False)
                waiter.set_result(session)
                self._logger.debug("Replying to waiter with a session %s", session)
            except KeyError:
                priority = time.time() + 10 * 60
                self._active_queue.put(
                    (priority, session))

    def _on_session_create(self, session, f):
        with self._lock:
            try:
                f.result()
                if self._initializer is None:
                    return self.put(session)
            except issues.Error:
                self._logger.error("Failed to create session. Put event to a delayed queue.")
                return self._event_queue.put(
                    lambda: self._delayed_prepare(
                        session
                    )
                )

            except Exception:
                self._logger.exception("Failed to create session. Put event to a delayed queue.")
                return self._event_queue.put(
                    lambda: self._delayed_prepare(
                        session
                    )
                )

        init_f = self._tp.submit(self._initializer, session)

        def _on_initialize(in_f):
            try:
                in_f.result()
                self.put(session)
            except Exception:
                self._prepare(session)

        init_f.add_done_callback(_on_initialize)

    def _prepare(self, session):
        if self._should_stop.is_set():
            self._destroy(session)
            return

        with self._lock:
            self._logger.debug("Preparing session %s", session)
            if len(self._waiters) < 1 and self._is_min_pool_size_satisfied(delta=-1):
                self._logger.info("No pending waiters, will destroy session")
                return self._destroy(session)

            f = session.async_create(self._req_settings)
            f.add_done_callback(
                lambda _: self._on_session_create(
                    session, _
                )
            )

    def _waiter_cleanup(self, w):
        with self._lock:
            try:
                self._waiters.pop(w)
            except KeyError:
                return None

    def subscribe(self):
        with self._lock:
            try:
                _, session = self._active_queue.get(block=False)
                return _utilities.wrap_result_in_future(session)
            except queue.Empty:
                self._logger.debug("Active session queue is empty, subscribe waiter for a session")
                waiter = _utilities.future()
                self._logger.debug("Subscribe waiter %s", waiter)
                if self._should_stop.is_set():
                    session = self._create()
                    self._logger.debug("Session pool is under stop, replying with empty session, %s", session)
                    waiter.set_result(session)
                    return waiter

                waiter.add_done_callback(self._waiter_cleanup)
                self._waiters[waiter] = waiter
                if self._active_count < self._size:
                    self._logger.debug(
                        "Session pool is not large enough (active_count < size: %d < %d). "
                        "will create a new session.", self._active_count, self._size)
                    session = self._create()
                    self._prepare(session)
                return waiter

    def unsubscribe(self, waiter):
        with self._lock:
            try:
                # at first we remove waiter from list of the waiters to ensure
                # we will not signal it right now
                self._logger.debug("Unsubscribe on waiter %s", waiter)
                self._waiters.pop(waiter)
            except KeyError:
                try:
                    session = waiter.result(timeout=-1)
                    self.put(session)
                except (futures.CancelledError, futures.TimeoutError):
                    # future is cancelled and not signalled
                    pass

    def _on_keep_alive(self, session, f):
        try:
            self.put(f.result())
            # additional logic should be added to check
            # current status of the session
        except issues.Error:
            self._destroy(
                session)
        except Exception:

            self._destroy(
                session)

    def acquire(self, blocking=True, timeout=None):
        waiter = self.subscribe()
        if blocking:
            try:
                session = waiter.result(timeout=timeout)
                return session
            except futures.TimeoutError:
                self.unsubscribe(waiter)
                raise issues.SessionPoolEmpty("Timeout on session acquire.")
            except Exception:
                self.unsubscribe(waiter)
                raise

        else:
            try:
                return waiter.result(timeout=-1)
            except futures.TimeoutError:
                self.unsubscribe(waiter)
                raise issues.SessionPoolEmpty("Session pool is empty.")
            except Exception:
                self.unsubscribe(waiter)
                raise

    def events_loop(self):
        while True:
            try:
                if self._should_stop.is_set():
                    break

                event = self._event_queue.get(timeout=self._spin_timeout)
                event()
            except StopIteration:
                break

            except queue.Empty:
                while True:
                    if not self.send_keep_alive():
                        break

    def send_keep_alive(self):
        session = self.pick()
        if session is None:
            return False

        if self._should_stop.is_set():
            self._destroy(session)
            return False

        f = session.async_keep_alive(self._req_settings)
        f.add_done_callback(lambda q: self._on_keep_alive(session, q))
        return True
