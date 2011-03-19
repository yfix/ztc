#!/usr/bin/env python
'''
ZTC url_ping item script - print specified url

Copyright (c) 2010 Vladimir Rusinov <vladimir@greenmice.info>
Licensed under GPL v.3
'''

import sys

from ztc.url import URL
from ztc import notsupported

if len(sys.argv) <> 2:
    notsupported("not enough arguments")

url = sys.argv[1]
if not (url.startswith('http://') or url.startswith('https://')):
    notsupported("incorrect url")

try:
    u = URL(url, 30)

    print u.ping
except Exception, e:
    notsupported(e)