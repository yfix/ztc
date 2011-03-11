#!/usr/bin/env python
"""
    ZTCCheck class - wrapper for ztc checks
    provides logging, output formatting and error handling abilities
    
    This file is part of ZTC and distributed under same license.
    
    Copyright (c) 2011 Denis Seleznyov [https://bitbucket.org/xy2/]
    Copyright (c) 2011 Vladimir Rusinov <vladimir@greenmice.info>
"""

import os
import sys
import traceback
import optparse
import ConfigParser

import ztc.commons

class CheckFail(Exception):
    """Exception that should be raised to notify zabbix about failed check."""
    pass

class CheckTimeout(Exception):
    """Exception that should be raised to notify zabbix that check timeouted"""
    pass

class MyConfigParser(ConfigParser.ConfigParser):
    def get(self, option, default):
        try:
            return ConfigParser.ConfigParser.get(self, 'main', option)
        except:
            return default

class ZTCCheck(object):
    """Base class for ztc checks"""
    
    # shortened name of the class
    # being used for getting config
    name = 'ztccheck'
    version = "11.03"
    args = None # parsed command-line args 
    
    debug = False
    
    def __init__(self, name=None):
        if name:
            self.name = name
        if self.name == 'ztccheck':
            raise NotImplementedError("Class %s must redefine its name"
                                            % (self.__class__.__name__, ))
        self._parse_argv()
        self.config = self._get_config()
        # checking if we are running in debug mode
        if self.config.get('debug', False):
            self.debug = True
    
    def _parse_argv(self):
        parser = optparse.OptionParser()
        parser.add_option("-v", "--version",
                  action="store_true", dest="version", default=False,
                  help="show version and exit")
        parser.add_option("-d", "--debug",
                  action="store_true", dest="debug", default=False,
                  help="enable debug")        
        parser.add_option("-t", "--tmpdir",
                  action="store", type="str", dest="tmpdir", default="/tmp/ztc/",
                  help="Temp direcroty path")
        parser.add_option("-c", "--confdir",
                  action="store", type="str", dest="confdir", default="/etc/ztc/",
                  help="ZTC Config dir")
        (options, args) = parser.parse_args()
        
        if options.version:
            self.version()
            sys.exit(0)
        
        if options.debug:
            self.debug = True
        
        self.options = options
        self.args = args
    
    def version(self):
        print "ZTC version %s" % self.version
        print "http://trac.greenmice.info/ztc/"
    
    def _get_config(self):
        config = MyConfigParser()
        config.read(os.path.join(self.options.confdir, self.name+".conf"))
        return config

    def _get(self, *args, **kwargs):
        """This method MUST return exactly one string or integer or raise
        one of CheckFail or CheckTimeout exceptions. Multiple return values
        are not supported by zabbix yet."""
        raise NotImplementedError("Class %s must reimplement _get method"
                                            % (self.__class__.__name__, ))

    def get(self, metric=None, *args, **kwargs):
        """Perform a check and return data immediately with exit code
        expected by zabbix. Caller script will be not continued after this
        method call, so SomeFancyCheck.process(arg1, arg2, ...) line should
        be last in userparameter script. Exit codes are defined in enum
        ZBX_SYSINFO_RET (include/sysinfo.h)"""
        try:
            # TODO: run _get in another thread, terminate it when it's running
            # for too long.
            # This is required for zabbix agent not to hang
            ret = self._get(metric, *args, **kwargs)
            print(ret)
            sys.exit(0)
        except CheckFail, e:
            if self.debug:
                traceback.print_stack()
            for arg in e.args:
                print(arg)
            sys.exit(1)
        except CheckTimeout, e:
            if self.debug:
                traceback.print_stack()
            for arg in e.args:
                print(arg)
            sys.exit(2)
        except Exception, e:
            # totally unexpected fail: dump all data we know
            traceback.print_stack()
            sys.exit(1)
            