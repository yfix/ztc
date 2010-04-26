#!/usr/bin/env python
'''
PostgreSQL buffers metrics for ZTC

Copyright (c) Vladimir Rusinov <vladimir@greenmice.info>

Params:
    $1 - name of metric. Supported:
        'clear' - number of clear buffers
        'dirty' - number of dirty buffers
        'used' - number of used buffers
'''

import sys

from ztc.pgsql import PgDB
from ztc import notsupported

if len(sys.argv) <> 2:
    notsupported("not enough arguments")

metric = sys.argv[1]

if metric == 'clear':
    q = "SELECT COUNT(*) FROM pg_buffercache WHERE isdirty='f'"
elif metric == 'dirty':
    q = "SELECT COUNT(*) FROM pg_buffercache WHERE isdirty='t'"
elif metric == 'used':
    q = "SELECT COUNT(*) FROM pg_buffercache WHERE reldatabase IS NOT NULL;"
else:
    notsupported("unknown buffers type")

p = PgDB()
r = p.query(q)
if not r:
    notsupported(p.lasterr)
print r[0][0]