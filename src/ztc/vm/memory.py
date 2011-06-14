#!/usr/bin/env python

from ztc.check import ZTCCheck, CheckFail
from ztc.store import ZTCStore

class Memory(ZTCCheck):
    name = 'memory'
    OPTPARSE_MIN_NUMBER_OF_ARGS = 1
    OPTPARSE_MAX_NUMBER_OF_ARGS = 1    
    
    def _get(self, metric=None, *args, **kwargs):
        if metric == 'used':
            return self.get_used()
        else:
            return self._get_amount(metric)
    
    def _get_amount(self, name):
        """ Get amount of %name% memory from /proc/meminfo
            @param name: memory metric name (string)
            @return: amount of requested memory metric, in bytes
        """
        name = name.lower()
        f = open('/proc/meminfo', 'r')
        for l in f.readlines():
            if l.lower().startswith('%s: ' % name):
                r = l.split()[-2]
        return int(r)*1024
    
    def get_used(self):
        """ Get amount of used (by apps) memory """
        return self._get_amount('MemTotal') - self._get_amount('MemFree') - \
            self._get_amount('Buffers') - self._get_amount('Cached')
    used = property(get_used)