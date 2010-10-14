#!/usr/bin/env python
'''
VFS Device metrics module for ZTC

Copyright (c) 2010 Vladimir Rusinov <vladimir@greenmice.info>
Parts of mdstat parsing copyright (c) Michal Ludvig <michal@logix.cz> http://www.logix.cz/michal/devel/nagios
License: GNU GPL v3

Requirements:
    * Linux 2.6
    * proc filesystem mounted on /proc/
    * smartmontools (for smart checks)
'''

import os
import stat
import re

class DiskStats(object):
    major = 0
    minor = 0
    devname = None
    reads = 0
    reads_merged = 0
    sectors_read = 0
    time_read = 0
    writes = 0
    writes_merged = 0
    sectors_written = 0
    time_write = 0
    cur_ios = 0
    time_io = 0
    time_io_weidged = 0
    
    def __repr__(self):
        r = self
        return str( (r.major, r.minor, r.devname, r.reads, r.reads_merged, r.sectors_read,
            r.time_read, r.writes, r.writes_merged, r.sectors_written, r.time_write,
            r.cur_ios, r.time_io, r.time_io_weidged) )
    
    def __str__(self):
        r = self
        ret = """major number: %i
minor mumber: %i
device name: %s
reads completed succesfully: %i
reads merged: %i
sectors read: %i
time spent reading (ms): %i
writes completed: %i
writes merged: %i
sectors written: %i
time spent writing (ms): %i
I/Os currently in progress: %i
time spent doing I/Os (ms): %i
weighted time spent doing I/Os (ms): %i
""" % (r.major, r.minor, r.devname, r.reads, r.reads_merged, r.sectors_read,
            r.time_read, r.writes, r.writes_merged, r.sectors_written, r.time_write,
            r.cur_ios, r.time_io, r.time_io_weidged)
        return ret                 
        

class DiskStatsParser(object):
    """ Class to read and parse /proc/diskstats """
    
    def __init__(self, device):
        """ IN:
            device (string) - device name, e.g. 'sda'
        """
        self.device = device
    
    def parse(self):
        return self._read_diskstats()
    
    def _read_diskstats(self):
        f = open('/proc/diskstats', 'r')
        ret = None
        for l in f.readlines():
            d = self._parse_diskstats_line(l)
            if d.devname == self.device:
                ret = d
        f.close()
        return ret
    
    def _parse_diskstats_line(self, l):
        """ Parse line from /proc/disktats
                The /proc/diskstats file displays the I/O statistics
                of block devices. Each line contains the following 14
                fields:
                 1 - major number
                 2 - minor mumber
                 3 - device name
                 4 - reads completed succesfully
                 5 - reads merged
                 6 - sectors read
                 7 - time spent reading (ms)
                 8 - writes completed
                 9 - writes merged
                10 - sectors written
                11 - time spent writing (ms)
                12 - I/Os currently in progress
                13 - time spent doing I/Os (ms)
                14 - weighted time spent doing I/Os (ms)
                For more details refer to Documentation/iostats.txt
        (for kernel 2.6)        
        """
        r = DiskStats()
        t = l.split()
        (r.major, r.minor, r.devname, r.reads, r.reads_merged, r.sectors_read,
            r.time_read, r.writes, r.writes_merged, r.sectors_written, r.time_write,
            r.cur_ios, r.time_io, r.time_io_weidged) = \
            map(int, t[:2]) + [t[2], ] + map(int, t[3:])
        
        return r
    
class SmartStatus(object):
    """ Disk smart status, using smartmontools """
    def __init__(self, dev):
        self.device = dev
    
    def get_health(self):
        dev = '/dev/%s' % (self.device, )
        if not os.path.exists(dev):
            return 'NO_DEVICE'
        cmd = 'smartctl -H %s' % (dev, )
        #print cmd
        c = os.popen(cmd)        
        return c.readlines()[-2].split()[-1]
    health = property(get_health)

class MDStatus(object):
    """ Staus of linux software RAID
    Sample /proc/mdstat output:
    
    Personalities : [raid1] [raid5]
    md0 : active (read-only) raid1 sdc1[1]
          2096384 blocks [2/1] [_U]
    
    md1 : active raid5 sdb3[2] sdb4[3] sdb2[4](F) sdb1[0] sdb5[5](S)
          995712 blocks level 5, 64k chunk, algorithm 2 [3/2] [U_U]
          [=================>...]  recovery = 86.0% (429796/497856) finish=0.0min speed=23877K/sec
    
    unused devices: <none>
    """
    
    def get_failed_devs(self):
        failed_devs = []
        active_devs = []
        spare_devs = []
        
        md_re = re.compile('^(md\d+)+\s*:') # pattern to detect md1: bla-bla-bla lines
        dev_re = re.compile('(\w+)\[\d+\](\(.\))*') # pattern to detect sda1[1] (F) in bla-bla-bla md descriptions
        
        f = open('/proc/mdstat', 'r')
        for l in f.readlines():
            if not md_re.match(l):
                continue # skipping lines which are not md status
            #print l
            for d in l.split():
                st = dev_re.match(d)
                if not st:
                    continue # skip 'active', ':' and other
                (dev, status) = st.groups()
                if status == "(F)":
                    failed_devs.append(dev)
                elif status == "(S)":
                    spare_devs.append(dev)
                else:
                    active_devs.append(dev)
        return failed_devs
    failed_devs = property(get_failed_devs)
            
            
            

if __name__ == '__main__':
    #st = DiskStatsParser('sda')
    #print st.parse()
    
    #ss = SmartStatus('sda')
    #print ss.health

    #ss = SmartStatus('sdq')
    #print ss.health
    
    md = MDStatus()
    print md.failed_devs    
    
    pass