#!/usr/bin/env python
"""
ZTC pgsql package

Used in PostgreSQL-releated templates
"""

import psycopg2 as pg
import ztc.commons

class PgSQL(object):
    database='postgres'
    host='localhost'
    user='postgres'
    password=''
    
    my_name='pgsql'
    
    dbh = None # database handler
    cur = None # database cursor
    
    lasterr = None # last error 
    
    def __init__(self, my_name='pgsql'):
        self.my_name = my_name
        self.config = ztc.commons.get_config(self.my_name)
        self.database = self.config.get('database', self.database)
        self.host = self.config.get('host', self.host)
        self.user = self.config.get('user', self.user)
        self.password = self.config.get('password', self.password)
        
        self._connect()
    
    def _connect(self):
        """ Connect to database """
        try:
            self.dbh = pg.connect(database=self.database, host=self.host, user=self.user, password=self.password)
            self.cur = self.dbh.cursor()
        except:
            self.dbh = None
            self.cur = None
    
    def query(self, sql):
        try:
            self.cur.execute(sql)
            return self.cur.fetchall()
        except Exception, e:
            self.lasterr = e
            return None
    
    def close(self):
        self.cur.close()
        self.dbh.close()