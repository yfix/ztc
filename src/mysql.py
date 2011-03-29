#!/usr/bin/env python
'''
MySQL script for ztc (mysql.ping item)
Connects to db and executes trivial query

Copyright (c) 2009-2011 Vladimir Rusinov <vladimir@greenmice.info>
Licensed under GNU GPL v.3
'''

from ztc.mysql import MyDB

my = MyDB()
m = my.args[0]
my.get(m)