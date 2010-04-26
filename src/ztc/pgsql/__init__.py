#!/usr/bin/env python
"""
ZTC pgsql package

Used in PostgreSQL-releated templates
"""

import psycopg2 as pg
import ztc.commons

class PgDB(object):
    """ Connection to single database """
    database='postgres'
    host='localhost'
    user='postgres'
    password=None
    
    my_name='pgsql'
    
    dbh = None # database handler
    cur = None # database cursor
    
    lasterr = None # last error 
    
    def __init__(self, my_name='pgsql', database=None):
        self.my_name = my_name
        self.config = ztc.commons.get_config(self.my_name)
        if database:
            self.database = database
        else:
            self.database = self.config.get('database', self.database)
        self.host = self.config.get('host', self.host)
        self.user = self.config.get('user', self.user)
        self.password = self.config.get('password', self.password)
        
        self._connect()
    
    def _connect(self):
        """ Connect to database """
        try:
            if self.host == None or self.host == 'localhost':
                if self.password:
                     self.dbh = pg.connect(database=self.database, user=self.user, password=self.password)
                else:
                     self.dbh = pg.connect(database=self.database, user=self.user)
            else:
                if self.password:
                     self.dbh = pg.connect(database=self.database, host=self.host, user=self.user, password=self.password)
                else:
                     self.dbh = pg.connect(database=self.database, host=self.host, user=self.user)
            # ^^^ I hate myself, TODO: rewrite this please
            self.cur = self.dbh.cursor()
        except  Exception, e:
            self.lasterr = e
            self.dbh = None
            self.cur = None
    
    def query(self, sql):
        if not self.cur: return None
        try:
            self.cur.execute(sql)
            return self.cur.fetchall()
        except Exception, e:
            self.lasterr = e
            return None
    
    def close(self):
        self.cur.close()
        self.dbh.close()

class PgCluster(object):
    """ Class represent database cluster """
    
    dbs = []
    
    def get_dblist(self):
        d = PgDB()
        dbs = d.query("SELECT datname FROM pg_database")
        self.dbs = [x[0] for x in dbs]
    
    def query_eachdb(self, sql, exclude=[]):
        """ execure query on each database of the cluster
        Params:
            sql (string): query text
            exclude (list of strings): database names to exclude
        Out:
            { dbname: query_result, ...  }
        """
        
        ret = {}
        if not self.dbs: self.get_dblist()
        for db in self.dbs:
            if db in exclude:
                continue
            pdb = PgDB(database=db)
            ret[db] = pdb.query(sql)
        return ret
