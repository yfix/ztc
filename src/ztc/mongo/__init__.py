#!/usr/bin/env python
"""
ZTC Mongodb check class

Copyright (c) 2011 Vladimir Rusinov <vladimir@greenmice.info>
"""

import pymongo
import time

from ztc.check import ZTCCheck, CheckFail

class Mongo(ZTCCheck):
    name = "mongo"
    
    OPTPARSE_MAX_NUMBER_OF_ARGS = 1
    
    def _connect(self):
        """ connect to mongodb """
        if not self.connection:
            host = self.config.get('host', 'localhost')
            port = int(self.config.get('port', 27017))
            db = self.config.get('db', 'ztc')
            self.connection = pymongo.Connection(host, port)
            self.db = self.connection[db]

    def _get(self, metric, *arg):
        if metric == 'ping':
            return self.get_ping()
        else:
            raise CheckFail("uncknown metric: %s" % metric)
    
    def get_ping(self):
        """ get ping to mongo db - time required to make a connection and
        execute simple query.
        Returns:
            float - number of seconds required to do a query
            0 - if mongodb failed
        """
        self.connection = None
        st = time.time()
        try:
            self._connect()
            #print dir(self.db)
            #print dir(self.connection)
            info = self.connection.server_info()
            if info and info.has_key('ok'):
                return time.time() - st
        except:
            self.logger.exception("failed to connect to mongodb")
        return 0