#!/usr/bin/env python
"""
MySQL module for ZTC

Copyright (c) 2010 Vladimir Rusinov <vladimir@greenmice.info>
Licensed under GNU GPL v.3
"""

import MySQLdb

import ztc.commons

class MyDB(object):
    database='mysql'
    host='localhost'
    user='root'
    password=''
    
    lasterr = None
    
    def __init__(self):
        self.config = ztc.commons.get_config('mysql')
        self.database = self.config.get('database', self.database)
        self.host = self.config.get('host', self.host)
        self.user = self.config.get('user', self.user)
        self.password = self.config.get('password', self.password)
        
        self._connect()        
        
    def _connect(self):
        try:
            self.conn =  MySQLdb.connect (host = self.host,
                           user = self.user,
                           passwd = self.password,
                           db = self.database)
            self.cursor = self.conn.cursor();
        except:
            self.conn = None
            self.cursor = None
    
    def query(self, query):
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception, e:
            self.lasterr = e
            return None
    
    def escape(self, str):
        return MySQLdb.escape_string(str)

if __name__ == '__main__':
    m = MyDB()
    print m.query("SELECT 1")