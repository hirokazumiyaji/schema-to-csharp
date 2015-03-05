# coding: utf-8
from __future__ import absolute_import, unicode_literals, print_function

header = """
// -*- coding: utf-8-with-signature; -*-
/*
  This file is automaitically created.
  If you want to expand, please define a partial class in a separate file.
*/
using System;
using System.Collections;
using System.Collections.Generic;

"""

klass = """
[System.Serializable]
public partial class {CLASS_NAME}
{{
    {FIELDS}

    public {CLASS_NAME}() {{
    }}

    public {CLASS_NAME}(Dictionary<string, object> data)
    {{
        {INITIALIZE}
    }}
}}
"""

footer = """
"""
