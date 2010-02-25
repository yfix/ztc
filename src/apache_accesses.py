#!/usr/bin/env python
'''
Number of apache accesses since start
'''

from ztc.apache import ApacheStatus
from ztc import notsupported

try:
    st = ApacheStatus()
    ret = st.accesses
    if ret is None:
        notsupported("There is no info about accesses on apache status page")
    else:
        print ret
except Exception, e:
    notsupported(e)