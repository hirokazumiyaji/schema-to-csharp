# coding: utf-8
from __future__ import absolute_import, unicode_literals, print_function


def snake_to_camel(snake_string):
    camel_string = ''
    for i, s in enumerate(snake_string.split('_')):
        if i == 0:
            camel_string = s.lower()
        else:
            camel_string += s.capitalize()
    return camel_string


def camel_to_class_name(camel_string):
    return '{}{}'.format(camel_string[0].upper(), camel_string[1:])


def format(fields, attrname, indent):
    string = '\n' + ' ' * indent
    return string.join([getattr(field, attrname) for field in fields])
