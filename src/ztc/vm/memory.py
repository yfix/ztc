#!/usr/bin/env python

class Memory(object):
    def get_active(self):
        """ Get amount of active memory """
        f = open('/proc/meminfo', 'r')
        for l in f.readlines():
            if l.find('Active: ') == 0:
                r = l.split()[-2]
        return int(r)*1024
    active = property(get_active)
    
    def get_inactive(self):
        """ Get amount of inactive memory """
        f = open('/proc/meminfo', 'r')
        for l in f.readlines():
            if l.find('Inactive: ') == 0:
                r = l.split()[-2]
        return int(r)*1024
    inactive = property(get_inactive)    