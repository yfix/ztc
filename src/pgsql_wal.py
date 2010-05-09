#!/usr/bin/env python
'''
Number of postgreSQL wal files

Copyright (c) Vladimir Rusinov <vladimir@greenmice.info>
'''

from ztc.pgsql import PgDB
from ztc import notsupported

q = "SELECT count(*) FROM pg_ls_dir('pg_xlog') WHERE pg_ls_dir ~ E'^[0-9A-F]{24}$'" 

p = PgDB()
r = p.query(q)
if not r:
    notsupported(p.lasterr)
print r[0][0]