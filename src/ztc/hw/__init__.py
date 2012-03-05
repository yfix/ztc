#!/usr/bin/env python

"""
    ZTC Hardware monitoring package
    
    Copyright (c) 2010-2011 Vladimir Rusinov <vladimir@greenmice.info>
    Copyright (c) 2010 Murano Software [http://muranosoft.com]
    Copyright (c) 2011 Parchment Inc. [http://www.parchment.com]
"""

#from ztc.commons import mypopen, get_config

from ztc.check import ZTCCheck, CheckFail
from ztc.myos import popen

class RAID_3Ware(ZTCCheck):
    """
        Class for monitoring 3ware raid.
        Requirements:
            * tw_cli tool installed
            * run as root, or have permissions to run tw_cli
    """
    
    name = 'hw_raid_3ware'
    
    _tw_out = {}
    
    def _get(self, metric):
        if metric == 'status':
            return self.get_status()
        else:
            raise CheckFail('uncknown metric')
    
    def _read_tw_status(self, c=0, u=0, cmd='status'):
        key = (c, u, cmd)
        if key in self._tw_out:
            # already executed
            return self._tw_out[key]
        else:
            command = "%s info c%i u%i %s" \
                % (self.config.get('tw_cli_path', '/opt/3ware/tw_cli'), c, u, cmd)
            retcode, ret = popen(command, self.logger)
            self._tw_out[key] = ret
            return ret
    
    def get_status(self, c=0, u=0):
        ret = "ZTC_FAIL"
        try:
            st = self._read_tw_status(c, u, 'status')
            ret = st.splitlines()[0].split()[3]
        except IndexError:
            self.logger.exception("problem with tw_cli output. Make sure it's installed correctly")
            ret = "ZTC_FAIL: TW_CLI"
        except AttributeError:
            self.logger.exception("popen returned incorrect type. Please, report a bug")
            ret = "ZTC_FAIL: popen"
        except:
            self.logger.exception("uncknown exception")
            ret = "ZTC_FAIL"
        return ret

if __name__ == '__main__':
    # test
    tw = RAID_3Ware()
    print tw.get_status()
