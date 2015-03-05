# coding: utf-8
from __future__ import absolute_import, unicode_literals, print_function

from optparse import OptionParser

import ujson

import cache
from format import *
from utils import *
from field import *

parser = OptionParser()
parser.add_option('-i', '--input', type=str, dest='input', help='input schema json file')
parser.add_option('-o', '--output', type=str, dest='output', help='output cs file')


if __name__ == "__main__":
    args, _ = parser.parse_args()
    if not args.input:
        raise Exception('require arg -i or --input')
    if not args.output:
        raise Exception('require arg -o or --output')

    gen_field(ujson.loads(open(args.input).read()))

    with open(args.output, 'w') as f:
        f.write(header.encode('utf-8-sig'))

        for klassname, fields in cache.all().iteritems():
            f.write(klass.format(CLASS_NAME=camel_to_class_name(snake_to_camel(klassname)),
                                 FIELDS=format(fields, 'field', 4),
                                 INITIALIZE=format(fields, 'initialize', 8)))

        f.write(footer.encode('utf-8-sig'))
