#!/usr/bin/env python
"""
    ztc.apache package
    Used in ztc Apache template
    
    Copyright (c) 2010-2011 Vladimir Rusinov <vladimir@greenmice.info>
    Copyright (c) 2010 Murano Software [http://muranosoft.com/]
    License: GNU GPL v.3
"""

import os
import time
import urllib2

import ztc.commons

class ApacheStatus(object):
    """ Apache status page reader and parser """
    
    ping = 0
    
    _page_data = None # data from sta 
    def __init__(self):
        self.config = ztc.commons.get_config('apache')
    
    def _read_status(self):
        """ urlopen and save to _page_data text of status page """
        st = time.time()
        if self._page_data is not None:
            # we've already retrieved it
            return 1
        url  = "%s://%s:%s%s?auto" % (
                                      self.config.get('proto', 'http'),
                                      self.config.get('host', 'localhost'),
                                      self.config.get('port', '80'),
                                      self.config.get('resource', '/server-status')
                                      )
        try:
            u = urllib2.urlopen(url, None, 1)
        except TypeError:
            u = urllib2.urlopen(url, None)
        self._page_data = u.read()
        u.close()
        self.ping = time.time() - st
    
    def _get_info(self, name):
        """ Extracts info from status """
        self._read_status()
        ret = None
        for l in self._page_data.split("\n"):
            if l.find(name + ": ") == 0:
                ret = l.split()[-1]
                break
        return ret
    
    def get_scoreboard(self):
        return self._get_info('Scoreboard')
    
    ####################################################################
    ## Properties ######################################################            
    def get_ping(self):
        """ Check if apache is alive """
        try:
            self._read_status()
        except:
            pass
        return self.ping
    prig = property(get_ping)

    def get_accesses(self):
        return int(self._get_info('Total Accesses'))
    accesses = property(get_accesses)
    
    def get_bytes(self):
        return int(self._get_info('Total kBytes')) * 1024
    bytes = property(get_bytes)
    
    def get_workers_busy(self):
        return int(self._get_info('BusyWorkers'))
    workers_busy = property(get_workers_busy)
    
    def get_workers_idle(self):
        return int(self._get_info('IdleWorkers'))
    workers_idle = property(get_workers_idle)    
    
    def get_workers_closingconn(self):
        return self.get_scoreboard().count('C')
    workers_closingconn = property(get_workers_closingconn)
    
    def get_workers_dns(self):
        return self.get_scoreboard().count('D')
    workers_dns = property(get_workers_dns)
                
    def get_workers_finishing(self):
        return self.get_scoreboard().count('G')
    workers_finishing = property(get_workers_finishing)
                
    def get_workers_idlecleanup(self):
        return self.get_scoreboard().count('I')
    workers_idlecleanup = property(get_workers_idlecleanup)
    
    def get_workers_keepalive(self):
        return self.get_scoreboard().count('K')
    workers_keepalive = property(get_workers_keepalive)
    
    def get_workers_logging(self):
        return self.get_scoreboard().count('L')
    workers_logging = property(get_workers_logging)
    
    def get_workers_openslot(self):
        return self.get_scoreboard().count('.')
    workers_openslot = property(get_workers_openslot)
                
    def get_workers_reading(self):
        return self.get_scoreboard().count('R')
    workers_reading = property(get_workers_reading)
            
    def get_workers_starting(self):
        return self.get_scoreboard().count('S')
    workers_starting = property(get_workers_starting)
            
    def get_workers_waitingconn(self):
        return self.get_scoreboard().count('_')
    workers_waitingconn = property(get_workers_waitingconn)
            
    def get_workers_writing(self):
        return self.get_scoreboard().count('_')
    workers_writing = property(get_workers_writing)

class ApacheTimeLog(object):
    """ Processes Apache time log (LogFormat %D) """
    
    def __init__(self):
        self.config = ztc.commons.get_config('apache')
        
    def _openlog(self):
        """ Open Log File and save it as self.log file object """
        logdir = self.config.get('logdir', '/var/log/apache2/')
        logfile = self.config.get('timelog', 'time.log')    
        fn = os.path.join(logdir, logfile)
        self.log = open(fn, 'a+')
    
    def _closelog(self):
        self.log.close()
    
    def _truncatelog(self):
        self.log.truncate(0)
    
    def _get_metrics(self):
        """ Calculates average, max & min request processing time, in seconds """
        total_time = 0
        max_time = 0
        min_time = -1
        total_lines = 0
        self._openlog()
        ret = {'avg': 0, 'min': 0, 'max': 0 }
        for l in self.log.readlines():
            if not l.strip():
                # skip empty lines
                continue
            time = int(l.split()[0])
            total_time += time
            if max_time < time:
                max_time = time
            if min_time == -1 or min_time > time:
                min_time = time 
            total_lines += 1
        self._truncatelog()
        self._closelog()
        if total_lines != 0:
            ret = {
                   'avg': float(total_time) / total_lines * 0.000001, # convert to seconds
                   'min': float(min_time) * 0.000001,
                   'max': float(max_time) * 0.000001,
                   }
        self._save_metrics_to_cache(ret)
        return ret

    def _get_metrics_from_cache(self):
        st = ztc.commons.MyStore('apache_reqtime')
        return st.get()
    
    def _save_metrics_to_cache(self, data):
        st = ztc.commons.MyStore('apache_reqtime')
        st.set(data)        
    
    def get_avg(self):
        """ returns average request processing time """
        metrics = self._get_metrics()
        return metrics['avg']
    avg_request_time = property(get_avg)
    
    def get_min(self):
        metrics = self._get_metrics_from_cache()
        return metrics['min']
    min_request_time = property(get_min)
    
    def get_max(self):
        metrics = self._get_metrics_from_cache()
        return metrics['max']
    max_request_time = property(get_max)    
     
            

if __name__ == '__main__':
    #st = ApacheStatus()
    #print "accesses:", st.get_accesses()
    tl = ApacheTimeLog()
    print "average time: ", tl.avg_request_time
    print "max time", tl.max_request_time
    print 'min time', tl.min_request_time