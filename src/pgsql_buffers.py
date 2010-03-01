#!/usr/bin/env python
'''
Pgsql buffers metrics for ztc
Params:
    $1 - name of metric. Supported:
        'clear' - number of clear buffers
'''

import sys

from ztc.pgsql import PgDB
from ztc import notsupported

if len(sys.argv) <> 2:
    notsupported("not enough arguments")

metric = sys.argv[1]

if metric == 'clear':
    q = "SELECT COUNT(*) FROM pg_buffercache WHERE isdirty='f'"
else:
    notsupported("uncknown buffers type")

p = PgDB()
r = p.query(q)
if not r:
    notsupported(p.lasterr)
print r[0][0]