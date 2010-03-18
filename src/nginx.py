#!/usr/bin/env python
"""
nginx.* scripts item

This file is part of ZTC and distributed under GNU GPL v.3
Copyright (c) 2010 Vladimir Rusinov

Params:
    $1 - metric name. Supported:
        accepts - number of connection accepted by nginx (since server start)
        connections_active - current number of active connections
        connections_reading - current number of connections reading request
        connections_writing - current number of connections writing response
"""

import sys

from ztc.nginx import NginxStatus
from ztc import notsupported

if len(sys.argv) <> 2:
    notsupported("not enough arguments")

metric = sys.argv[1]

try:
    st = NginxStatus()

    print st.__getattribute__(metric)
except Exception, e:
    notsupported(e)