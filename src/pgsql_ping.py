#!/usr/bin/env python
'''
PgSQL ping script for ztc (pgsql.ping item)
Connects to db and executes trivial query

Copyright (c) 2009-2011 Vladimir Rusinov <vladimir@greenmice.info>
Licensed under GNU GPL v.3
'''

import time

from ztc.pgsql import PgDB

st = time.time()
try:
    p = PgDB()
    if p.query('SELECT 1'):
        print time.time() - st
    else:
        print("0")
except:
    print 0