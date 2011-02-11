#!/usr/bin/env python
"""
MySQL module for ZTC

Copyright (c) 2010-2011 Vladimir Rusinov <vladimir@greenmice.info>
Copyright (c) 2011 Murano Software [http://muranosoft.com]
Licensed under GNU GPL v.3
"""

import MySQLdb

import ztc.commons

class MyDB(object):
    database='mysql'
    host='localhost'
    user='root'
    password=''
    unix_socket = None
    
    lasterr = None
    
    def __init__(self):
        self.config = ztc.commons.get_config('mysql')
        self.database = self.config.get('database', self.database)
        self.host = self.config.get('host', self.host)
        self.user = self.config.get('user', self.user)
        self.password = self.config.get('password', self.password)
        self.unix_socket = self.config.get('unix_socket', self.unix_socket)
        
        self._connect()        
        
    def _connect(self):
        try:
            # TODO: remove this if, filter arguments instead
            if self.unix_socket:
                self.conn =  MySQLdb.connect (host = self.host,
                           user = self.user,
                           passwd = self.password,
                           db = self.database,
                           unix_socket = self.unix_socket,
                           connect_timeout = 2
                           )
            else:
                self.conn =  MySQLdb.connect (host = self.host,
                           user = self.user,
                           passwd = self.password,
                           db = self.database,
                           connect_timeout = 2
                           )                
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