#!/usr/bin/env python
'''
Checks if apache is alive

Copyright (c) 2009-2010 Vladimir Rusinov <vladimir@greenmice.info>

apache.alive item from Apache2 template
Out:
    0 if apache is failed
    1 if apache is alive

TODO: convert to ping item
'''

from ztc.apache import ApacheStatus
from ztc import notsupported

try:
    st = ApacheStatus()
    ret = st.alive
    print int(ret)
except Exception, e:
    notsupported(e)