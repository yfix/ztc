#!/usr/bin/env python
'''
PgSQL ping script
Connects to db and executes trivial query

Copyright (c) 2009 Vladimir Rusinov <vladimir@greenmice.info>
Licensed under GNU GPL v.3
'''

from ztc.pgsql import PgDB

p = PgDB()
if p.query('SELECT 1'):
    print("1")
else:
    print("0")