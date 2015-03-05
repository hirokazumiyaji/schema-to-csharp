# coding: utf-8
from __future__ import absolute_import, unicode_literals, print_function

__all__ = [
    'BooleanField', 'NullableBooleanField',
    'IntegerField', 'NullableIntegerField',
    'FloatField', 'NullableFloatField',
    'DateTimeField', 'NullableDateTimeField',
    'ObjectField', 'ArrayField', 'StringField',
    'gen_field',
]

from operator import attrgetter

import cache
from utils import *
from schema import *


class Field(object):
    schema_type = None

    def __init__(self, name, value):
        self.name = name
        self.value = value

    @property
    def camel_name(self):
        return snake_to_camel(self.name)

    @property
    def field(self):
        return 'public {} {}'.format(self.schema_type, self.camel_name)

    @property
    def initialize(self):
        return '{} = ({})data["{}"];'.format(
            self.camel_name, self.schema_type, self.name)


class NullableField(Field):

    @property
    def initialize(self):
        return '{} = data["{}"] == null ? ({})null : ({})data["{}"];'.format(
            self.camel_name, self.name, self.schema_type, self.schema_type, self.name)


class BooleanField(Field):
    schema_type = 'bool'


class NullableBooleanField(NullableField):
    schema_type = 'bool?'


class IntegerField(Field):
    schema_type = 'int'


class NullableIntegerField(NullableField):
    schema_type = 'int?'


class FloatField(Field):
    schema_type = 'double'


class NullableFloatField(NullableField):
    schema_type = 'double?'


class StringField(NullableField):
    schema_type = 'string'


class DateTimeField(Field):
    schema_type = 'DateTime'

    @property
    def initialize(self):
        return '{} = DateTime.parse((string)data["{}"]);'.format(self.camel_name. self.name)


class NullableDateTimeField(Field):
    schema_type = 'DateTime?'

    @property
    def initialize(self):
        return '{0} = data["{1}"] == null ? ({2})null : ({2})DateTime.parse((string)data["{1}"]);'.format(
            self.camel_name, self.name, self.schema_type)


class ArrayField(Field):

    @property
    def field(self):
        if self.item_schema_type is SchemaType.Boolean:
            return 'public bool[] {};'.format(self.camel_name)
        if self.item_schema_type is SchemaType.Integer:
            return 'public int[] {};'.format(self.camel_name)
        if self.item_schema_type is SchemaType.Float:
            return 'public double[] {};'.format(self.camel_name)
        if self.item_schema_type is SchemaType.DateTime:
            return 'public DateTime[] {};'.format(self.camel_name)
        if self.item_schema_type is SchemaType.NullableBoolean:
            return 'public bool?[] {};'.format(self.camel_name)
        if self.item_schema_type is SchemaType.NullableInteger:
            return 'public int?[] {};'.format(self.camel_name)
        if self.item_schema_type is SchemaType.NullableFloat:
            return 'public double?[] {};'.format(self.camel_name)
        if self.item_schema_type is SchemaType.NullableDateTime:
            return 'public DateTime?[] {};'.format(self.camel_name)
        if self.item_schema_type is SchemaType.Object:
            class_name = camel_to_class_name(self.camel_name)
            return 'public {}[] {};'.format(class_name, self.camel_name)

    @property
    def item_schema_type(self):
        result = self.__dict__['item_schema_type'] = get_schema_type(self.value['items'])
        return result

    @property
    def initialize(self):
        if self.item_schema_type is SchemaType.Boolean:
            return '{} = ((IList<object>)data["{}"]).Select(x => (bool)x).ToArray();'.format(
                self.camel_name, self.name)
        if self.item_schema_type is SchemaType.Integer:
            return '{} = ((IList<object>)data["{}"]).Select(x => (int)x).ToArray();'.format(
                self.camel_name, self.name)
        if self.item_schema_type is SchemaType.Float:
            return '{} = ((IList<object>)data["{}"]).Select(x => (double)x).ToArray();'.format(
                self.camel_name, self.name)
        if self.item_schema_type is SchemaType.DateTime:
            return '{} = ((IList<object>)data["{}"]).Select(x => DateTime.parse((string)x)).ToArray();'.format(
                self.camel_name, self.name)

        if self.item_schema_type is SchemaType.NullableBoolean:
            return '{} = ((IList<object>)data["{}"]).Select(x => x == null ? (bool?)null : (bool?)x).ToArray();'.format(
                self.camel_name, self.name)
        if self.item_schema_type is SchemaType.NullableInteger:
            return '{} = ((IList<object>)data["{}"]).Select(x => x == null ? (int?)null : (int?)x).ToArray();'.format(
                self.camel_name, self.name)
        if self.item_schema_type is SchemaType.NullableFloat:
            return '{} = ((IList<object>)data["{}"]).Select(x => x == null ? (double?)null : (double?)x).ToArray();'.format(
                self.camel_name, self.name)
        if self.item_schema_type is SchemaType.NullableDateTime:
            return '{} = ((IList<object>)data["{}"]).Select(x => x == null ? (DateTime?)null : (DateTime?)DateTime.parse((string)x)).ToArray();'.format(
                self.camel_name, self.name)
        if self.item_schema_type is SchemaType.Object:
            class_name = camel_to_class_name(self.camel_name)
            return '{} = ((IList<object>)data["{}"]).Select(x => x == null ? null : new {}((Dictionary<string, object>)x)).ToArray();'.format(
                self.camel_name, self.name, class_name)


class ObjectField(NullableField):

    @property
    def schema_type(self):
        camel_name = self.camel_name[0].upper() + self.camel_name[1:]
        return camel_name

    @property
    def initialize(self):
        return '{0} = data["{1}"] == null ? ({2})null : new ({2})(Dictionary<string, object>)data["{1}"]);'.format(
            self.camel_name, self.name, self.schema_type)


def gen_field(schema):
    assert schema.get('type', 'object') == 'object'

    fields = []

    for name, value in schema['properties'].iteritems():
        if not isinstance(value, dict):
            raise Exception('InValid: {}={}'.format(name, value))

        if 'type' not in value:
            raise Exception('InValid: {}={}'.format(name, value))

        schema_type = get_schema_type(value)

        if schema_type is SchemaType.Boolean:
            field = BooleanField(name, value)
        elif schema_type is SchemaType.NullableBoolean:
            field = NullagleBooleanField(name, value)
        elif schema_type is SchemaType.Integer:
            field = IntegerField(name, value)
        elif schema_type is SchemaType.NullableInteger:
            field = NullableIntegerField(name, value)
        elif schema_type is SchemaType.Float:
            field = FloatField(name, value)
        elif schema_type is SchemaType.NullableFloat:
            field = NullableFloatField(name, value)
        elif schema_type is SchemaType.DateTime:
            field = DateTimeField(name, value)
        elif schema_type is SchemaType.NullableDateTime:
            field = NullableDateTimeField(name, value)
        elif schema_type is SchemaType.Object:
            value['name'] = name
            field = ObjectField(name, value)
            gen_field(value)
        elif schema_type is SchemaType.Array:
            field = ArrayField(name, value)
            if 'object' == value['items']['type']:
                value['items']['name'] = name
                gen_field(value['items'])
        elif schema_type is SchemaType.String:
            field = StringField(name, value)

        fields.append(field)

    fields.sort(key=attrgetter('field'))

    cache.set(schema['name'], fields)
