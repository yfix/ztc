#!/usr/bin/env python
"""
    ztc.apache package
    Used in ztc Apache template
    
    Copyright (c) 2010 Vladimir Rusinov <vladimir@greenmice.info>
    Copyright (c) 2010 Murano Software [http://muranosoft.com/]
    License: GNU GPL v.3
"""

import os
import urllib2

import ztc.commons

class ApacheStatus(object):
    """ Apache status page reader and parser """
    
    _page_data = None # data from sta 
    def __init__(self):
        self.config = ztc.commons.get_config('apache')
    
    def _read_status(self):
        """ urlopen and save to _page_data text of status page """
        if self._page_data is not None:
            # we've already retrieved it
            return 1
        url  = "%s://%s:%s%s?auto" % (
                                      self.config.get('proto', 'http'),
                                      self.config.get('host', 'localhost'),
                                      self.config.get('port', '80'),
                                      self.config.get('resource', '/server-status')
                                      )
        u = urllib2.urlopen(url, None, 1)
        self._page_data = u.read()
        u.close()
    
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
    def get_alive(self):
        """ Check if apache is alive """
        ret = True
        try:
            self._read_status()
        except:
            ret = False
        return ret
    alive = property(get_alive)

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
    """ Processes Apache time log (LogFormat %T) """
    
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
    
    def get_avg(self):
        """ Calculates average request processing time """
        total_time = 0
        total_lines = 0
        self._openlog()
        for l in self.log.readlines():
            if not l.strip():
                continue
            time= l.split()[0]
            total_time += int(time)
            total_lines += 1
        self._truncatelog()
        self._closelog()
        if total_lines == 0:
            return 0
        else:
            return float(total_time) / total_lines
    average_request_time = property(get_avg)        

if __name__ == '__main__':
    st = ApacheStatus()
    print "accesses:", st.get_accesses()
    tl = ApacheTimeLog()
    print "average time: ", tl.get_avg()    