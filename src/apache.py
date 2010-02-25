#!/usr/bin/env python
"""
apache.* scripts item

Params:
    $1 - metric name. Supported:
        accesses - number of accesses since server start
        traffic - number of bytes sent since server start
        workers_busy - current number of busy workers
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