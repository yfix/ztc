#!/usr/bin/env python
"""
vfs.mdstat.failed_devs scripts item


This file is part of ZTC and distributed under GNU GPL v.3
Copyright (c) 2010 Vladimir Rusinov <vladimir@greenmice.info>
"""

from ztc.system.vfs import  MDStatus
from ztc import notsupported

try:
    md = MDStatus()
    d = md.failed_devs
    if d:
        print str(d)
    else:
        print 'OK'
except Exception, e:
    notsupported(e)