# -*- coding: utf-8 -*-
import abc
import enum
from . import _utilities, _apis


@enum.unique
class PrimitiveType(enum.Enum):
    """
    Enumerates all available primitive types that can be used
    in computations.
    """
    Int32 = _apis.primitive_types.INT32, 'int32_value'
    Uint32 = _apis.primitive_types.UINT32, 'uint32_value'
    Int64 = _apis.primitive_types.INT64, 'int64_value'
    Uint64 = _apis.primitive_types.UINT64, 'uint64_value'
    Int8 = _apis.primitive_types.INT8, 'int32_value'
    Uint8 = _apis.primitive_types.UINT8, 'uint32_value'
    Int16 = _apis.primitive_types.INT16, 'int32_value'
    Uint16 = _apis.primitive_types.UINT16, 'uint32_value'
    Bool = _apis.primitive_types.BOOL, 'bool_value'
    Double = _apis.primitive_types.DOUBLE, 'double_value'
    Float = _apis.primitive_types.FLOAT, 'float_value'

    String = _apis.primitive_types.STRING, 'bytes_value'
    Utf8 = _apis.primitive_types.UTF8, 'text_value', _utilities.from_bytes

    Yson = _apis.primitive_types.YSON, 'bytes_value'
    Json = _apis.primitive_types.JSON, 'text_value', _utilities.from_bytes
    JsonDocument = _apis.primitive_types.JSON_DOCUMENT, 'text_value', _utilities.from_bytes

    Date = _apis.primitive_types.DATE, 'uint32_value'
    Datetime = _apis.primitive_types.DATETIME, 'uint32_value'
    Timestamp = _apis.primitive_types.TIMESTAMP, 'uint64_value'
    Interval = _apis.primitive_types.INTERVAL, 'int64_value'

    DyNumber = _apis.primitive_types.DYNUMBER, 'text_value', _utilities.from_bytes

    def __init__(self, idn, proto_field, to_obj=None):
        self._idn_ = idn
        self._to_obj = to_obj
        self._proto_field = proto_field

    def get_value(self, value_pb):
        """
        Extracts value from protocol buffer
        :param value_pb: A protocol buffer
        :return: A valid value of primitive type
        """
        if self._to_obj is not None:
            return self._to_obj(getattr(value_pb, self._proto_field))
        return getattr(value_pb, self._proto_field)

    def set_value(self, pb, value):
        """
        Sets value in a protocol buffer
        :param pb: A protocol buffer
        :param value: A valid value to set
        :return: None
        """
        setattr(pb, self._proto_field, value)

    def __str__(self):
        return self._name_

    @property
    def proto(self):
        """
        Returns protocol buffer representation of a primitive type
        :return: A protocol buffer representation
        """
        return _apis.ydb_value.Type(type_id=self._idn_)


class DataQuery(object):
    __slots__ = ('yql_text', 'parameters_types', 'name')

    def __init__(self, query_id, parameters_types, name=None):
        self.yql_text = query_id
        self.parameters_types = parameters_types
        self.name = _utilities.get_query_hash(self.yql_text) if name is None else name


#######################
# A deprecated alias  #
#######################
DataType = PrimitiveType


class AbstractTypeBuilder(object):
    __metaclass__ = abc.ABCMeta

    @property
    @abc.abstractmethod
    def proto(self):
        """
        Returns protocol buffer representation of a type
        :return: A protocol buffer representation
        """
        pass


class DecimalType(AbstractTypeBuilder):
    __slots__ = ('_proto', '_precision', '_scale')

    def __init__(self, precision=22, scale=9):
        """
        Represents a decimal type
        :param precision: A precision value
        :param scale: A scale value
        """
        self._precision = precision
        self._scale = scale
        self._proto = _apis.ydb_value.Type()
        self._proto.decimal_type.MergeFrom(
            _apis.ydb_value.DecimalType(precision=self._precision, scale=self._scale))

    @property
    def precision(self):
        return self._precision

    @property
    def scale(self):
        return self._scale

    @property
    def proto(self):
        """
        Returns protocol buffer representation of a type
        :return: A protocol buffer representation
        """
        return self._proto

    def __eq__(self, other):
        return self._precision == other.precision and self._scale == other.scale

    def __str__(self):
        """
        Returns string representation of a type
        :return: A string representation
        """
        return 'Decimal(%d,%d)' % (self._precision, self._scale)


class OptionalType(AbstractTypeBuilder):
    __slots__ = ('_repr', '_proto', '_item')

    def __init__(self, optional_type):
        """
        Represents optional type that wraps inner type
        :param optional_type: An instance of an inner type
        """
        self._repr = "%s?" % str(optional_type)
        self._proto = _apis.ydb_value.Type()
        self._item = optional_type
        self._proto.optional_type.MergeFrom(
            _apis.ydb_value.OptionalType(item=optional_type.proto))

    @property
    def item(self):
        return self._item

    @property
    def proto(self):
        """
        Returns protocol buffer representation of a type
        :return: A protocol buffer representation
        """
        return self._proto

    def __eq__(self, other):
        return self._item == other.item

    def __str__(self):
        return self._repr


class ListType(AbstractTypeBuilder):
    __slots__ = ('_repr', '_proto')

    def __init__(self, list_type):
        """
        :param list_type: List item type builder
        """
        self._repr = "List<%s>" % str(list_type)
        self._proto = _apis.ydb_value.Type(
            list_type=_apis.ydb_value.ListType(
                item=list_type.proto
            )
        )

    @property
    def proto(self):
        """
        Returns protocol buffer representation of type
        :return: A protocol buffer representation
        """
        return self._proto

    def __str__(self):
        return self._repr


class DictType(AbstractTypeBuilder):
    __slots__ = ('__repr', '__proto')

    def __init__(self, key_type, payload_type):
        """
        :param key_type: Key type builder
        :param payload_type: Payload type builder
        """
        self._repr = "Dict<%s,%s>" % (str(key_type), str(payload_type))
        self._proto = _apis.ydb_value.Type(
            dict_type=_apis.ydb_value.DictType(
                key=key_type.proto,
                payload=payload_type.proto,
            )
        )

    @property
    def proto(self):
        return self._proto

    def __str__(self):
        return self._repr


class TupleType(AbstractTypeBuilder):
    __slots__ = ('__elements_repr', '__proto')

    def __init__(self):
        self.__elements_repr = []
        self.__proto = _apis.ydb_value.Type(tuple_type=_apis.ydb_value.TupleType())

    def add_element(self, element_type):
        """
        :param element_type: Adds additional element of tuple
        :return: self
        """
        self.__elements_repr.append(str(element_type))
        element = self.__proto.tuple_type.elements.add()
        element.MergeFrom(element_type.proto)
        return self

    @property
    def proto(self):
        return self.__proto

    def __str__(self):
        return "Tuple<%s>" % ",".join(self.__elements_repr)


class StructType(AbstractTypeBuilder):
    __slots__ = ('__members_repr', '__proto')

    def __init__(self):
        self.__members_repr = []
        self.__proto = _apis.ydb_value.Type(struct_type=_apis.ydb_value.StructType())

    def add_member(self, name, member_type):
        """
        :param name:
        :param member_type:
        :return:
        """
        self.__members_repr.append("%s:%s" % (name, str(member_type)))
        member = self.__proto.struct_type.members.add()
        member.name = name
        member.type.MergeFrom(member_type.proto)
        return self

    @property
    def proto(self):
        return self.__proto

    def __str__(self):
        return "Struct<%s>" % ",".join(self.__members_repr)


class BulkUpsertColumns(AbstractTypeBuilder):
    __slots__ = ('__columns_repr', '__proto')

    def __init__(self):
        self.__columns_repr = []
        self.__proto = _apis.ydb_value.Type(struct_type=_apis.ydb_value.StructType())

    def add_column(self, name, column_type):
        """
        :param name: A column name
        :param column_type: A column type
        """
        self.__columns_repr.append("%s:%s" % (name, column_type))
        column = self.__proto.struct_type.members.add()
        column.name = name
        column.type.MergeFrom(column_type.proto)
        return self

    @property
    def proto(self):
        return self.__proto

    def __str__(self):
        return "BulkUpsertColumns<%s>" % ",".join(self.__columns_repr)
