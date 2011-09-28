#!/usr/bin/env python
"""
Nginx TimeLog check class: calculates min/avg/max upstream response times.

Usage:
1. configure time_log log format in nginx config (http section):
log_format time_log '$upstream_response_time $request <anything you want>';

2. Add timelog log to all servers/locations you need to monitor:
access_log /var/log/nginx/time.log time_log;

3. Check log path on config file /etc/ztc/nginx.conf

4. Make sure zabbix can execute nginx_reqtime.py script under root (to allow
cleaning of the log)

5. It might be good idea to place this log to tmpfs.

This file is part of ZTC and distributed under the same license.
http://bitbucket.org/rvs/ztc/

Copyright (c) 2011 Vladimir Rusinov <vladimir@greenmice.info>
"""

from ztc.check import ZTCCheck, CheckFail
from ztc.store import ZTCStore

class NginxTimeLog(ZTCCheck):
    """ Nginx upsteam response min/avg/max calculation """
    name = 'nginx'
    
    OPTPARSE_MIN_NUMBER_OF_ARGS = 1
    OPTPARSE_MAX_NUMBER_OF_ARGS = 1    
    
    def _get(self, metric=None, *args, **kwargs):
        return self.get_resptime(metric)
        
    def get_resptime(self, metric):
        """ get min/avg/max response time """
        if metric == 'avg':
            data = self.read_timelog()
            self.save_to_store(data)
        else:
            data = self.read_from_store()
            if not data:
                data = self.read_timelog()
                self.save_to_store(data)
        return data[metric]

    def read_timelog(self):
        """ really open timelog and calculate data """
        mn = -1.0
        mx = -1.0
        avg = 0.0
        n = 0
        
        fn = self.config.get('timelog', '/var/log/nginx/time.log')
        f = open(fn, 'a+')
        
        for l in f.readlines():
            r = l.split()[0] # response time should be in first col
            if r == '-':
                # non-dynamic request
                continue
            else:
                r = float(r)
            if min == -1:
                mn = r
            else:
                mn = min(r, mn)
            mx = max(r, mx)
            avg += r
            n += 1
            
        f.truncate(0)
        f.close()            
        
        if n > 0:
            avg = avg / n
        if mn == -1:
            mn = 0
            
        return {
                'min': mn,
                'max': mx,
                'avg': avg
                }
    
    def save_to_store(self, data):
        st = ZTCStore('nginx_reqtime', self.options)
        st.set(data)        
    
    def read_from_store(self):
        st = ZTCStore('nginx_reqtime', self.options)
        return st.get()        