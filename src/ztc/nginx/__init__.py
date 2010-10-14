#!/usr/bin/env python
"""
    ztc.nginx package
    Used in nginx Apache template
    
    Copyright (c) 2010 Vladimir Rusinov <vladimir@greenmice.info>
    License: GNU GPL v.3
"""

import urllib2

import ztc.commons

class NginxStatus(object):
    """ Nginx status page reader and parser """
    
    _page_data = None # data from status page
    
    def __init__(self):
        self.config = ztc.commons.get_config('nginx')
    
    def _read_status(self):
        """ urlopen and save to _page_data text of status page """
        if self._page_data is not None:
            # we've already retrieved it
            return 1
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
        #print self._page_data
    
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
        st = ztc.commons.MyStore('nginx.accepts')
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
        st = ztc.commons.MyStore('nginx.handled')
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
        st = ztc.commons.MyStore('nginx.requests')
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
    
if __name__ == '__main__':
    st = NginxStatus()
    print "accepts:", st.get_accepts()