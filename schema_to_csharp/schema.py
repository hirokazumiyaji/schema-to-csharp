# coding: utf-8
from __future__ import absolute_import, unicode_literals, print_function

import enum


class SchemaType(enum.IntEnum):
    Array = 1
    Boolean = 2
    Integer = 3
    Float = 4
    Null = 5
    Object = 6
    String = 7
    DateTime = 8
    NullableBoolean = 9
    NullableInteger = 10
    NullableFloat = 11
    NullableDateTime = 12


def _get_schema_type(schema_type, nullable=False, format=None):
    if 'array' == schema_type:
        return SchemaType.Array
    if 'boolean' == schema_type:
        return SchemaType.Boolean if not nullable else SchemaType.NullableBoolean
    if 'integer' == schema_type:
        return SchemaType.Integer if not nullable else SchemaType.NullableInteger
    if 'number' == schema_type:
        return SchemaType.Float if not nullable else SchemaType.NullableFloat
    if 'object' == schema_type:
        return SchemaType.Object
    if 'string' == schema_type:
        if format and format == 'date-time':
            return SchemaType.DateTime if not nullable else SchemaType.NullableDateTime
        else:
            return SchemaType.String


def get_schema_type(value):
    schema_type = value['type']
    if isinstance(schema_type, list):
        if 'null' not in schema_type:
            raise Exception('not found null')

        if len(schema_type) != 2:
            raise Exception('schema type is not 2 elements.')

        _schema_type = schema_type[0] if schema_type[0] != 'null' else schema_type[1]
        return _get_schema_type(_schema_type, True, value.get('format'))
    else:
        return _get_schema_type(schema_type, format=value.get('format'))
