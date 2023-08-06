# -*- coding: utf-8 -*-
import six
from kikimr.public.sdk.python.client import credentials
try:
    import ticket_parser2.api.v1 as tvm
except ImportError:
    try:
        import ticket_parser2_py3.api.v1 as tvm

    except ImportError:
        raise ImportError("Failed to import ticket parser module!")


class TvmCredentialsProvider(credentials.Credentials):
    """
    TVM Auth Adapter

    Usage example:

    def tvm_credentials():
        from kikimr.public.sdk.python import tvm
        return tvm.TvmCredentialsProvider(
            self_client_id=int(os.getenv('TVM_CLIENT_ID')),
            self_secret=os.getenv('TVM_SECRET'),
            destination_alias='ydb',
            dsts={
                'ydb': 2002490,
            }
        )

    """
    def __init__(self, self_client_id, self_secret, dsts, destination_alias):
        self._settings = tvm.TvmApiClientSettings(
            self_client_id=self_client_id, self_secret=self_secret, dsts=dsts)
        self._client = tvm.TvmClient(self._settings)
        self._destination_alias = destination_alias

    def _get_service_ticket(self):
        return six.text_type(self._client.get_service_ticket_for(self._destination_alias))

    def expired(self):
        return True

    def auth_metadata(self):
        return [
            (
                credentials.YDB_AUTH_TICKET_HEADER, self._get_service_ticket()
            )
        ]
