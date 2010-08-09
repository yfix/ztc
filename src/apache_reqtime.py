#!/usr/bin/env python
'''
Gets average apache request time

Copyright (c) 2010 Vladimir Rusinov <vladimir@greenmice.info>

Usage:

1. Configure apache:
   `LogFormat "%D <whatever>" timelog` in modules.d/00_mod_log_config.conf (or enywhere else, this is distro-specific)
   `CustomLog /var/log/apache2/time.log timelog` there and in every vhost

'''

from ztc.apache import ApacheTimeLog
from ztc import notsupported

try:
    tl = ApacheTimeLog()
    ret = tl.average_request_time
    print ret
except Exception, e:
    notsupported(e)    