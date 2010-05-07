#!/usr/bin/env python
'''
PostgreSQL slony item script

Copyright (c) 2010 Murano Software [http://muranosoft.com]

Params:
    $1 - name of metric. Supported:
        'lag' - lag time
'''

import sys

from ztc.pgsql import PgDB
from ztc import notsupported

from ztc.commons import get_config

if len(sys.argv) <> 2:
    notsupported("not enough arguments")

metric = sys.argv[1]

conf = get_config('slony')
custername = conf.get('cluster', 'Slonik')

if metric == 'lag':
    q = "SELECT cast(extract(epoch from st_lag_time) as int8) FROM \"_%\".sl_status" % (custername, )
else:
    notsupported("unknown metric")

p = PgDB('slony')
r = p.query(q)
if not r:
    notsupported(p.lasterr)
print r[0][0]