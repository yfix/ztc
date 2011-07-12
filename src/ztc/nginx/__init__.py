#!/usr/bin/env python
"""
    ztc.nginx package
    Used in nginx Apache template
    
    Copyright (c) 2010 Vladimir Rusinov <vladimir@greenmice.info>
    License: GNU GPL v.3
"""

import urllib2
import time

#import ztc.commons
from ztc.check import ZTCCheck, CheckFail
from ztc.store import ZTCStore

class NginxStatus(ZTCCheck):
    """ Nginx status page reader and parser """
    
    OPTPARSE_MIN_NUMBER_OF_ARGS = 1
    OPTPARSE_MAX_NUMBER_OF_ARGS = 1
    name = 'nginx'
    
    _page_data = None # data from status page
    ping_time = 0
    
    def _get(self, metric=None, *args, **kwargs):
        allowed_metrics = ('accepts', 'handled', 'requests',
            'connections_active', 'connections_reading', 'connections_waiting',
            'connections_writing', 'ping')
        if metric in allowed_metrics:
            return self.__getattribute__('get_' + metric)()
        else:
            raise CheckFail("Requested not allowed metric")   
        
    
    def _read_status(self):
        """ urlopen and save to _page_data text of status page """
        if self._page_data is not None:
            # we've already retrieved it
            return 1
        read_start = time.time()
        url = "%s://%s:%s%s?auto" % (
                                     self.config.get('proto', 'http'),
                                     self.config.get('host', 'localhost'),
                                     self.config.get('port', '8080'),
                                     self.config.get('resource', '/server-status')
                                     )
        try:
            u = urllib2.urlopen(url, None, 1)
        except TypeError:
            u = urllib2.urlopen(url, None)
        self._page_data = u.readlines()
        u.close()
        self.ping_time = time.time() - read_start # calulate how many time was required
    
    def _get_info(self, name):
        """ Extracts info from status """
        self._read_status()
        ret = None
        for l in self._page_data.split("\n"):
            if l.find(name + ": ") == 0:
                ret = l.split()[-1]
                break
        return ret
    
    def get_accepts(self):
        """ Number of accept()s since server start """
        st = ZTCStore('nginx.accepts', self.options)
        try:
            self._read_status()
            my_line = self._page_data[2]
            a = int(my_line.split()[0])
            st.set(a)
        except Exception, e:
            # if nginx status failed, do not become unsupported
            try: a = st.get()
            except: raise e 
        return a
    accepts = property(get_accepts)
    
    def get_handled(self):
        st = ZTCStore('nginx.handled', self.options)
        try:
            self._read_status()
            my_line= self._page_data[2]
            a = int(my_line.split()[1])
            st.set(a)
        except Exception, e:
            # if nginx status failed, do not become unsupported
            try: a = st.get()
            except: raise e 
        return a        
    handled = property(get_handled)
    
    def get_requests(self):
        """ get number of requests since server start """
        st = ZTCStore('nginx.requests', self.options)
        try:
            self._read_status()
            my_line= self._page_data[2]
            a = int(my_line.split()[2])
            st.set(a)
        except Exception, e:
            # if nginx status failed, do not become unsupported
            try: a = st.get()
            except: raise e 
        return a        
    requests = property(get_requests)
    
    def get_connections_active(self):
        """
        first line:
        Active connections: 123
        """
        try:
            self._read_status()
            my = self._page_data[0].split()[-1]
            return int(my)
        except:
            return 0
    connections_active = property(get_connections_active)
    
    def get_connections_reading(self):
        try:
            self._read_status()
            my = self._page_data[-1].split()[1]
            return int(my)
        except:
            return 0
    connections_reading = property(get_connections_reading)
    
    def get_connections_waiting(self):
        try:
            self._read_status()
            my = self._page_data[-1].split()[5]
            return int(my)
        except:
            return 0
    connections_waiting = property(get_connections_waiting)

    def get_connections_writing(self):
        try:
            self._read_status()
            my = self._page_data[-1].split()[3]
            return int(my)
        except:
            return 0
    connections_writing = property(get_connections_writing)
    
    def get_ping(self):
        try:
            self._read_status()
        finally:
            return self.ping_time
    ping = property(get_ping)
                
    
if __name__ == '__main__':
    st = NginxStatus()
    print "ping:", st.ping
    print "accepts:", st.get_accepts()
