#!/usr/bin/env python
"""
apache.* scripts item

Params:
    $1 - metric name. Supported:
"""

import sys

from ztc.apache import ApacheStatus
from ztc import notsupported

if len(sys.argv) <> 2:
    notsupported("not enough arguments")

metric = sys.argv[1]

try:
    st = ApacheStatus()

    print st.__getattribute__(metric)
except Exception, e:
    notsupported(e)