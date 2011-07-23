#!/usr/bin/env python
"""
<description>

This file is part of ZTC and distributed under the same license.
http://bitbucket.org/rvs/ztc/

Copyright (c) 2011 Vladimir Rusinov <vladimir@greenmice.info>
"""

from ztc.check import ZTCCheck, CheckFail

class PHPFPMCheck(ZTCCheck):
    name = "php-fpm"
    
    OPTPARSE_MIN_NUMBER_OF_ARGS = 1
    OPTPARSE_MAX_NUMBER_OF_ARGS = 1    
    
    def _get(self, metric, *arg, **kwarg):
        if metric == 'ping':
            return self.ping()
        else:
            raise CheckFail("uncknown metric")
        
    @property
    def ping(self):
        pass            