#!/usr/bin/env python
"""
MySQL module for ZTC
"""

import ztc.commons

class MySQL(object):
    database='postgres'
    host='localhost'
    user='postgres'
    password=''
    
    def __init__(self):
        self.config = ztc.commons.get_config('mysql')
        self.database = self.config.get('database', self.database)
        self.host = self.config.get('host', self.host)
        self.user = self.config.get('user', self.user)
        self.password = self.config.get('password', self.password)
        
        self._connect()        
        
    def _connect(self):
        pass