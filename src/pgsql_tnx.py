#!/usr/bin/env python
'''
PostgreSQL transactions metrics for ZTC

Copyright (c) 2010 Murano Software [http://muranosoft.com/
Licensed under GPL v. 3

Params:
    $1 - name of metric. Supported:
        'idle_tnx'
        'running'
Returns:
    Current max time of transaction in given status (in seconds), type: float
'''

import sys

from ztc.pgsql import PgDB
from ztc import notsupported

if len(sys.argv) <> 2:
    notsupported("not enough arguments")

metric = sys.argv[1]

if metric == 'idle_tnx':
    q = "SELECT EXTRACT (EPOCH FROM MAX(age(NOW(), query_start))) as d FROM pg_stat_activity WHERE current_query='<IDLE> in transaction'"
elif metric == 'running':
    q = "SELECT EXTRACT (EPOCH FROM MAX(age(NOW(), query_start))) as d FROM pg_stat_activity WHERE current_query<>'<IDLE> in transaction' AND current_query<>'<IDLE>'"    
else:
    notsupported("unknown metric")

p = PgDB()
r = p.query(q)
if not r:
    notsupported(p.lasterr)
if not r[0][0]:
    print 0
else:
    if r[0][0] < 0: # sometimes happens
        print 0
    else:
        print "%.5f" % (r[0][0], )