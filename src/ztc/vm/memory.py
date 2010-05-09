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