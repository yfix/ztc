#!/usr/bin/env python
#
# CPU items module for ztc
# Copyright (c) 2010 Vladimir Rusinov <vladimir@greenmice.info>
# Copyright (c) 1999-2009 by Sebastien GODARD (sysstat <at> orange.fr)
#
# Requirements:
# * kernel 2.6.0+
# * /proc/ filesystem

import time

class CPUStats:
    """
        CPUStats: class to store cpu stats read from /proc/stat
    """
    
    stats = () # number of jiffies spent in the different modes
    # 0: cpu_user
    # 1: cpu_nice
    # 2: cpu_sys
    # 3: cpu_idle
    # 4: cpu_iowait
    # 5: cpu_hardirq
    # 6: cpu_softirq
    # 7: cpu_steal
    # 8: cpu_guest    
    capture_time = 0 # capture time
    
    def __init__(self, stats):
        """
        IN:
            stats (list): list of (cpu_user, cpu_nice, cpu_sys, cpu_idle, cpu_iowait,
                cpu_hardirq, cpu_softirq, cpu_steal, cpu_guest)
        """
        if len(stats) != 9:
            raise TypeError("Invalid list size")
        self.stats = tuple(map(int, stats))
        self.capture_time = time.time()
    
    def _get_iowait(self):
        return self.stats[4]
    iowait = property(_get_iowait)
    def _get_iowait_p(self): 
        return float(self.iowait) / self.jiffies 
    iowait_p = property(_get_iowait_p)
    
    
    def _get_jiffies(self):
        """ Returns total number of jiffies """
        sum = 0
        for i in self.stats: sum += i
        return sum
    jiffies = property(_get_jiffies)    
    
    def __str__(self):
        vals = (1, 2, 3, 4, 5, 6, 7, 8, 9)
        print self.stats
        ret = """user:    %i
nice:    %i
sys:     %i
idle:    %i
iowait:  %i
hardirq: %i
softirq: %i
steal:   %i
guest:   %i""" % self.stats
        return ret
        

def read_cpu_stats(cpu="cpu"):
    f = open("/proc/stat", 'r')
    for l in f.readlines():
        if l.find(cpu+' ') == 0:
            stats = l.strip().split(' ')
            stats = stats[-9:] # selecting only numbers
            st = CPUStats(stats)
            f.close()
            return st
    # ouch, no such cpu
    f.close()
    return None 
        
# tests
if __name__ == '__main__':
    s = read_cpu_stats()
    print("cpu stats:")
    print(str(s))
    print s.iowait_p
    print("iowait: %.2f%%" % (s.iowait_p*100, ))
    