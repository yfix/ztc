#!/usr/bin/env python
'''
NTP service metrics for ZTC

Copyright (c) 2010 Vladimir Rusinov <vladimir@greenmice.info>
Copyright (c) 2010 Murano Software [http://muranosoft.com]
Copyright (c) 2010 Docufide, Inc. [http://docufide.com]
License: GNU GPL v3

Requirements:
    * ntp
    * run as root or have permissions to 'ntpq -c readvar localhost'
'''

from ztc.commons import mypopen

class Ntpq(object):
    def __init__(self):
        self.ntpq_vars = mypopen("ntpq -c readvar localhost").readlines()
    
    def get_jitter(self):
        j = 0
        for line in self.ntpq_vars:
            if line.startswith('clk_jitter='): # line ="clk_jitter=3.829, clk_wander=0.719"
                j = line.split()[0] # j = "line ="clk_jitter=3.829,"
                j = j.split('=')[1] # j = "3.829,"
                j = j[:-1] # j = 3.829
                j = float(j)
        return j
    jitter = property(get_jitter)
    
if __name__ == '__main__':
    n = Ntpq()
    print "Jitter = ", n.jitter