# coding: utf-8
from __future__ import absolute_import, unicode_literals, print_function

import threading

_local = threading.local()
_local._cache = {}


def all():
    return _local._cache


def get(name):
    return _local._cache.get(name)


def set(name, value):
    _local._cache[name] = value
