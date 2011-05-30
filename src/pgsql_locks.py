#!/usr/bin/env python
'''
PostgreSQL locks stats

Copyroght (c) 2011 Wrike, Inc. [http://wrike.com]
Copyright (c) 2011 Vladimir Rusinov <vladimir@greenmice.info>
Licensed under GPL v.3

Params:
    $1 - name of metric. Supported:
        all - total number of locks
        granted - number of granted locks
        not_granted - number of not granted locks
'''

import sys

from ztc.pgsql import PgDB
from ztc import notsupported

if len(sys.argv) <> 2:
    notsupported("not enough arguments")

metric = sys.argv[1]

if metric == 'all':
    q = "SELECT COUNT(*) FROM pg_locks"
elif metric == 'granted':
    q = "SELECT COUNT(*) FROM pg_locks WHERE granted='t'"
elif metric == 'not_granted':
    q = "SELECT COUNT(*) FROM pg_locks WHERE granted<>'t'"    
else:
    notsupported("unknown metric")

p = PgDB()
r = p.query(q)
if not r:
    notsupported(p.lasterr)
print r[0][0]
