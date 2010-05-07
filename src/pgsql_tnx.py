#!/usr/bin/env python
'''
PostgreSQL transaction metrics for ZTC

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

if metric == 'idle_time':
    q = """SELECT max(COALESCE(ROUND(EXTRACT(epoch FROM now()-query_start)),0))
        FROM pg_stat_activity WHERE current_query = '<IDLE> in transaction'"""
elif metric == 'max_time':
    q = """SELECT max(COALESCE(ROUND(EXTRACT(epoch FROM now()-query_start)),0))
        FROM pg_stat_activity WHERE xact_start IS NOT NULL"""
else:
    notsupported("unknown metric")

p = PgDB()
r = p.query(q)
if not r:
    notsupported(p.lasterr)
print r[0][0]