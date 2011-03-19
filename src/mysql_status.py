#!/usr/bin/env python
'''
MySQL status items for ztc (mysql.status.* and other items)
Executes SHOW STATUS LIKE '$1' 

Copyright (c) 2010 Vladimir Rusinov <vladimir@greenmice.info>
Licensed under GNU GPL v.3

Params:
    $1 - status item name
'''

import sys

from ztc.mysql import MyDB
from ztc import notsupported

if len(sys.argv) <> 2:
    notsupported("not enough arguments")

metric = sys.argv[1]

m = MyDB()
r = m.query('SHOW GLOBAL STATUS LIKE "%s"' % (m.escape(metric)))
if r:
    print r[0][1]
else:
    notsupported(m.lasterr)