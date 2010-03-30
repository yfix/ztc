#!/usr/bin/env python
'''
PostgreSQL connections metrics for ZTC

Copyright (c) Vladimir Rusinov <vladimir@greenmice.info>

Params:
    $1 - name of metric. Supported:
        'idle_tnx' - number of clear buffers
'''

import sys

from ztc.pgsql import PgDB
from ztc import notsupported

if len(sys.argv) <> 2:
    notsupported("not enough arguments")

metric = sys.argv[1]

if metric == 'idle_tnx':
    q = "SELECT COUNT(*) FROM pg_stat_activity WHERE current_query = '<IDLE> in transaction'"
else:
    notsupported("unknown metric")

p = PgDB()
r = p.query(q)
if not r:
    notsupported(p.lasterr)
print r[0][0]