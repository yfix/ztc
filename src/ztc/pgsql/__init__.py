#!/usr/bin/env python
"""
ZTC pgsql package

Used in PostgreSQL-related templates

Copyright (c) 2010-2011 Vladimir Rusinov <vladimir@greenmice.info>
"""

import sys

import psycopg2 as pg

from ztc.check import ZTCCheck, CheckFail
import queries as pgq

class PgDB(ZTCCheck):
    """ Connection to single database """
    
    _database = None
    
    def __init__(self, database=None):
        ZTCCheck.__init__(self)
        self._database = database
    
    name= 'pgsql'
    
    OPTPARSE_MIN_NUMBER_OF_ARGS = 0
    
    dbh = None # database handler
    cur = None # database cursor
    
    def _get(self, metric, *args, **kwargs):
        if metric == 'query':
            q = args[0]
            return self.query(q)
        elif metric == 'autovac_freeze':
            return self.get_autovac_freeze()
        else:
            raise CheckFail('uncknown metric')
    
    # queries:
    def get_autovac_freeze(self):
        """ Checks how close each database is to the Postgres
            autovacuum_freeze_max_age setting. This action will only work for
            databases version 8.2 or higher. The 'age' of the transactions in
            each database is compared to the autovacuum_freeze_max_age setting
            (200 million by default) to generate a rounded percentage.
        
        Returns: (float) maximum age of transaction from all databases, in %
            (compared to autovacuum_freeze_max_age)
        """
        max_percent = 0
        q = pgq.AUTOVAC_FREEZE
        ret = self.query(q)
        for (freeze, age, percent, dbname) in ret:
            if self.debug:
                self.logger.info("Freeze %% for %s: %s" % (dbname, percent))
            max_percent = max(max_percent, percent)        
        return max_percent
    
    # postgresql-related
    def _connect(self):
        """ Connect to database """
        if self.dbh:
            return True
        connect_dict = {
            'host': self.config.get('host', None), # none = connect via socket
            'user': self.config.get('user', 'postgres'),
            'password': self.config.get('password', None),
            'database': self.config.get('database', 'postgres')
        }
        if self._database:
            connect_dict['database'] = self._database
        # filtering connect_dict to remove all Nones:
        connect_dict = dict((k, v) for k, v in connect_dict.iteritems() if v is not None)
        try:
            self.dbh = pg.connect(**connect_dict)
            self.cur = self.dbh.cursor()
            return True
        except  Exception, e:
            raise
            self.lasterr = e
            self.dbh = None
            self.cur = None
            return False
    
    def query(self, sql):
        self._connect()
        if self.debug:
            self.logger.debug("running query '%s'" % sql)        
        self.cur.execute(sql)
        ret = self.cur.fetchall()
        if self.debug:
            self.logger.debug("result:\n%s" % self.fineprint_results(ret))
        return ret
        
    def fineprint_results(self, rets):
        """ Fine print query results """
        ret = ''
        for row in rets:
            for cell in row:
                ret += (str(cell) + ' | ')
            ret += "\n"
        return ret
    
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

if __name__ == '__main__':
    # some test
    p = PgDB()
    ret = p.get('query', "SELECT * FROM pg_tables")
    p.fineprint_results(ret)
