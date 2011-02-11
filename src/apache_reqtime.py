#!/usr/bin/env python
'''
Gets average apache request time

Copyright (c) 2010-2011 Vladimir Rusinov <vladimir@greenmice.info>

Params:
    $1 - metric name. Supported: avg, min, max. Defaults to avg

Usage:

1. Configure apache:
   `LogFormat "%D <whatever>" timelog` in modules.d/00_mod_log_config.conf (or enywhere else, this is distro-specific)
   `CustomLog /var/log/apache2/time.log timelog` there and in every vhost
    TODO
'''

import sys

from ztc.apache import ApacheTimeLog
from ztc import notsupported

if len(sys.argv) == 1:
    m = 'avg'
else:
    m = sys.argv[1]

try:
    tl = ApacheTimeLog()
    ret = tl.__getattribute__('%s_request_time' % (m, ))
    print ret
except Exception, e:
    notsupported(e)    