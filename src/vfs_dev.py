#!/usr/bin/env python
"""
vfs_dev_* scripts item


This file is part of ZTC and distributed under GNU GPL v.3
Copyright (c) 2010 Murano Software [http://muranosoft.com/]

Params:
    $1 - metric name. Supported:
        major: major number
        minor: minor mumber
        devname: device name
        reads: reads completed succesfully
        reads_merged: reads merged
        sectors_read: sectors read
        time_read: time spent reading (ms)
        writes: writes completed
        writes_merged: writes merged
        sectors_written: sectors written
        time_write: time spent writing (ms)
        cur_ios: I/Os currently in progress
        time_io: time spent doing I/Os (ms)
        time_io_weidged: weighted time spent doing I/Os (ms)
    $2 - device name, e.g. 'sda'
"""

import sys

from ztc.system.vfs import  DiskStatsParser
from ztc import notsupported

if len(sys.argv) <> 3:
    notsupported("not enough arguments")

metric = sys.argv[1]
dev = sys.argv[2]

try:
    p = DiskStatsParser(dev)
    stats = p.parse()

    print stats.__getattribute__(metric)
except Exception, e:
    notsupported(e)