#!/usr/bin/env python

import urllib2

import ztc.commons

class ApacheStatus(object):
    """ Process apache status page """
    
    _page_data = None # data from status page
    
    def __init__(self):
        self.config = ztc.commons.get_config('apache')
    
    def _read_status(self):
        """ urlopen and save to _page_data text of status page """
        if self._page_data is not None:
            return 1
        url = self.config = "%s://%s:%s%s?auto" % (
                                              self.config.get('proto', 'http'),
                                              self.config.get('host', 'localhost'),
                                              self.config.get('port', '80'),
                                              self.config.get('resource', '/server-status')
                                              )
        u = urllib2.urlopen(url, None, 1)
        self._page_data = u.read()
        u.close()
    
    def alive(self):
        """ Check if apache is alive """
        ret = True
        try:
            self._read_status()
        except:
            ret = False
        return ret
    
    def _get_info(self, name):
        """ Extracts info from status """
        self._read_status()
        ret = None
        for l in self._page_data.split("\n"):
            if l.find(name + ": ") == 0:
                ret = int(l.split()[-1])
                break
        return ret        
    
    def get_accesses(self):
        return self._get_info('Total Accesses')
    def get_bytes(self):
        return self._get_info('Total kBytes') * 1024

if __name__ == '__main__':
    st = ApacheStatus()
    print "accesses:", st.get_accesses()