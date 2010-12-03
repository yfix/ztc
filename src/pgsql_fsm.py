#!/usr/bin/env python
'''
PostgreSQL fsm items.
Requires pg_freespacemap contrib to be installed on configured database.
Does not supports PostgreSQL >= 8.4, as it manages fsm automatically,

Copyright (c) 2010 Murano Software [http://muranosoft.com]
Copyright (c) 2010 Vladimir Rusinov <vladimir@greenmice.info>

Thanks to:
    * sn00p - reporting typos in SQL

Params:
    $1 - name of metric. Supported:
        pages - percent of used fsm_pages
        relations - percent of used fsm_relations
'''

import sys

from ztc.pgsql import PgDB
from ztc import notsupported

if len(sys.argv) <> 2:
    notsupported("not enough arguments")

metric = sys.argv[1]

if metric == 'pages':
    q = """
        SELECT
            pages,
            maxx,
            ROUND(100*(pages/maxx)) AS percent
        FROM
            (SELECT
                (sumrequests+numrels)*chunkpages AS pages
            FROM
                (SELECT
                    SUM(CASE WHEN avgrequest IS NULL THEN interestingpages/32 ELSE interestingpages/16 END) AS sumrequests,
                    COUNT(relfilenode) AS numrels, 16 AS chunkpages FROM pg_freespacemap_relations
                ) AS foo
            ) AS foo2,
            (SELECT setting::NUMERIC AS maxx FROM pg_settings WHERE name = 'max_fsm_pages') AS foo3
        """
elif metric == 'relations':
    q = """
        SELECT
            maxx,
            cur,
            ROUND(100*(cur/maxx))\n
        FROM (SELECT
              (SELECT COUNT(*) FROM pg_freespacemap_relations) AS cur,
              (SELECT setting::NUMERIC FROM pg_settings WHERE name='max_fsm_relations') AS maxx) x    
    """    
else:
    notsupported("unknown metric")

p = PgDB()
r = p.query(q)
if not r:
    notsupported(p.lasterr)
print r[0][2]
