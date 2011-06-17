#!/usr/bin/env python
"""
PgDB class - ZTCCheck for tracking single postgresql database
    
Copyright (c) 2010-2011 Vladimir Rusinov <vladimir@greenmice.info>
"""

import time

from ztc.check import ZTCCheck, CheckFail
import ztc.pgsql.queries as pgq
from ztc.pgsql.pgconn import PgConn

class PgDB(ZTCCheck):
    """ Connection to single database """
    
    name= 'pgsql'
    dbconn = None
    
    OPTPARSE_MIN_NUMBER_OF_ARGS = 1
    
    def _myinit(self):
        connect_dict = {
            'host': self.config.get('host', None), # none = connect via socket
            'user': self.config.get('user', 'postgres'),
            'password': self.config.get('password', None),
            'database': self.config.get('database', 'postgres')
        }
        self.dbconn = PgConn(connect_dict, self.logger)        
    
    def _get(self, metric, *args, **kwargs):
        if metric == 'query':
            q = args[0]
            return self.dbconn.query(q)
        elif metric == 'autovac_freeze':
            return self.get_autovac_freeze()
        elif metric == 'ping':
            st = time.time()
            try:
                if self.dbconn.query('SELECT 1'):
                    return time.time() - st
                else:
                    return 0
            except:
                return 0
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
        ret = self.dbconn.query(q)
        for (freeze, age, percent, dbname) in ret:
            if self.debug:
                self.logger.info("Freeze %% for %s: %s" % (dbname, percent))
            max_percent = max(max_percent, percent)        
        return max_percent