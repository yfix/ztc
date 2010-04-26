#!/usr/bin/env python
'''
PostgreSQL database stats

Copyright (c) Vladimir Rusinov <vladimir@greenmice.info>

Params:
    $1 - name of metric. Supported:
        blks_hit - number of cache hits
'''

import sys

from ztc.pgsql import PgDB
from ztc import notsupported

if len(sys.argv) <> 2:
    notsupported("not enough arguments")

metric = sys.argv[1]

if metric == 'blks_hit':
    q = "SELECT SUM(blks_hit) FROM pg_stat_database"
elif metric == 'blks_read':
    q = "SELECT SUM(blks_read) FROM pg_stat_database"
elif metric == 'commits':
    q = "SELECT SUM(xact_commit) FROM pg_stat_database"
elif metric == 'rollbacks':    
    q = "SELECT SUM(xact_rollback) FROM pg_stat_database"
elif metric == 'tup_deleted':
    q = "SELECT SUM(tup_deleted) FROM pg_stat_database"
elif metric == 'tup_inserted':
    q = "SELECT SUM(tup_inserted) FROM pg_stat_database"
elif metric == 'tup_fetched':
    q = "SELECT SUM(tup_fetched) FROM pg_stat_database"
elif metric == 'tup_updated':
    q = "SELECT SUM(tup_updates) FROM pg_stat_database"
elif metric == 'tup_returned':
    q = "SELECT SUM(tup_teturned) FROM pg_stat_database"
else:
    notsupported("unknown metric")

p = PgDB()
r = p.query(q)
if not r:
    notsupported(p.lasterr)
print r[0][0]