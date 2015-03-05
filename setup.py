#!/usr/bin/env python
# coding: utf-8
from __future__ import absolute_import, unicode_literals, print_function

import os
from setuptools import setup, find_packages

try:
    with open('README.md') as f:
        readme = f.read()
except IOError:
    readme = ''


setup(
    name='SchemaToCSharp',
    verion='0.0.1',
    url='',
    author='Hirokazu Miyaji',
    author_email='hirokazu.miyaji@gmail.com',
    description='Create CSharp File from JSON Schema.'
    long_description=readme,
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      schema_to_csharp = schema_to_csharp.scripts.main:main
    """,
)
