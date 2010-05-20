#!/usr/bin/env python
'''
MySQL ping script for ztc (mysql.ping item)
Connects to db and executes trivial query

Copyright (c) 2009-2010 Vladimir Rusinov <vladimir@greenmice.info>
Licensed under GNU GPL v.3
'''

from ztc.mysql import MyDB

m = MyDB()
if m.query('SELECT 1'):
    print("1")
else:
    print("0")