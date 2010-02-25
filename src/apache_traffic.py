#!/usr/bin/env python
'''
Number of bytes returned by accesses since start
'''

from ztc.apache import ApacheStatus
from ztc import notsupported

try:
    st = ApacheStatus()
    ret = st.bytes
    if ret is None:
        notsupported("There is no info about traffic on apache status page")
    else:
        print ret
except Exception, e:
    notsupported(e)
