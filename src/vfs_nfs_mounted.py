#!/usr/bin/env python
"""
NFS template items script

Copyright (c) 2011 Vladimir Rusinov <vladimir@greenmice.info>
Copyright (c) 2011 Wrike, Inc. [http://www.wrike.com]
Copyright (c) 2011 Murano Software [http://muranosoft.com]


This file is part of ZTC and distributed under GNU GPL v.3
Copyright (c) 2010 Vladimir Rusinov <vladimir@greenmice.info>
"""

from ztc.system.vfs import  MountStatus
import ztc.commons
from ztc import notsupported

conf = ztc.commons.get_config('nfs')
mount_point = conf.get('mountpoint', '/mnt/nfs')



try:
    ms = MountStatus(mount_point)
    print int(ms.checkmount('nfs'))
except Exception, e:
    notsupported(e)