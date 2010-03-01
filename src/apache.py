#!/usr/bin/env python
"""
apache.* scripts item

This file is part of ZTC and distributed under GNU GPL v.3
Copyright (c) 2010 Vladimir Rusinov
Copyright (c) 2010 Murano Software [http://muranosoft.com/]

Params:
    $1 - metric name. Supported:
        accesses - number of accesses since server start
        traffic - number of bytes sent since server start
        workers_busy - current number of busy workers
        workers_closingconn - current number of workers closing connection
        workers_dns - current number of workers doing dns query
        workers_finishing - cunnrent number of workers finishing
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