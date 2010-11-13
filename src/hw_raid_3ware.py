#!/usr/bin/env python

"""
    3ware raid monitoring item script
    
    Copyright (c) 2010 Vladimir Rusinov <vladimir@greenmice.info>
    Copyright (c) 2010 Murano Software [http://muranosoft.com]
"""

import ztc
import ztc.hw

try:
    tw = ztc.hw.RAID_3Ware()
    print tw.get_status()
except Exception, e:
    ztc.notsupported(e)