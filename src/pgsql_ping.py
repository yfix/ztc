#!/usr/bin/env python
'''
Created on 21.12.2009

@author: Vladimir Rusinov <vladimir@greenmice.info>

PgSQL ping script
Connects to db and executes trivial query

Copyright (c) 2010 Vladimir Rusinov <vladimir@greenmice.info>
Licensed under GNU GPL v.3
'''

from pgsql import PgSQL

p = PgSQL()
if p.query('SELECT 1'):
    print("1")
else:
    print("0")