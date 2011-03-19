#!/usr/bin/env python
'''
MySQL ping script for ztc (mysql.ping item)
Connects to db and executes trivial query

Copyright (c) 2009-2011 Vladimir Rusinov <vladimir@greenmice.info>
Licensed under GNU GPL v.3
'''

import time

from ztc.mysql import MyDB

st = time.time()
m = MyDB()
if m.query('SELECT 1'):
    print time.time() - st
else:
    print("0")