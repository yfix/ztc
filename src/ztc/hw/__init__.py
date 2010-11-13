#!/usr/bin/env python

"""
    ZTC Hardware monitoring package
    
    Copyright (c) 2010 Vladimir Rusinov <vladimir@greenmice.info>
    Copyright (c) 2010 Murano Software [http://muranosoft.com]
"""

from ztc.commons import mypopen, get_config

class RAID_3Ware(object):
    """
        Class for monitoring 3ware raid.
        Requirements:
            * tw_cli tool installed
            * run as root, or have permissions to run tw_cli
    """
    def __init__(self):
        self.config = get_config('hw_raid_3ware')
    
    def get_status(self, c=0, u=0):
        cmd = "%s info c%i u%i status" % (self.config.get('tw_cli_path', '/opt/3ware/tw_cli'), c, u)
        ret = mypopen(cmd).readlines()[0]
        return ret.split()[3]

if __name__ == '__main__':
    # test
    tw = RAID_3Ware()
    print tw.get_status()