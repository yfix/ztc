#!/usr/bin/env python
'''
ZTC URL class - used to query url

TODO: use this class on nginx and apache templates

Copyright (c) 2010 Vladimir Rusinov <vladimir@greenmice.info>
Licensed under GPL v.3
'''

import urllib2
import time

class URL(object):
    _data = None
    _ping = 0
    
    def __init__(self, url, timeout=30):
        self.url = url
        self.timeout = timeout
        
    def _open(self):
        if self._data is not None:
            return 1
        s = time.time()
        try:
            u = urllib2.urlopen(self.url, None, self.timeout)
        except TypeError:
            # Changed in version 2.6: timeout was added, versions < 2.6 does not have last param
            u = urllib2.urlopen(self.url, None)
        self._data = u.readlines()
        self._ping = time.time()- s
    
    def get_ping(self):
        try:
            self._open()
        except:
            pass
        return self._ping
    ping = property(get_ping)
    
if __name__ == '__main__':
    # tests
    u = URL('http://google.com/', 60)
    print u.ping