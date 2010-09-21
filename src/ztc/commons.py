#!/usr/bin/env python
'''
ZTC commons classes

Copyright (c) 2010 Vladimir Rusinov <vladimir@greenmice.info>
Licensed under GPL v.3
'''

import os
import optparse
import ConfigParser

class MyConfigParser(ConfigParser.ConfigParser):
    def get(self, option, default):
        try:
            return ConfigParser.ConfigParser.get(self, 'main', option)
        except:
            return default

parser = optparse.OptionParser()
parser.add_option("-v", "--version",
                  action="store_true", dest="version", default=False,
                  help="show version and exit")
parser.add_option("-t", "--tmpdir",
                  action="store", type="str", dest="tmpdir", default="/tmp/ztc/",
                  help="Temp direcroty path")
parser.add_option("-c", "--confdir",
                  action="store", type="str", dest="confdir", default="/etc/ztc/",
                  help="ZTC Config dir")
(options, args) = parser.parse_args()

# TODO: version() function

def get_config(name):
    """
    Get config object for template with given name
    """
    config = MyConfigParser()
    config.read(os.path.join(options.confdir, name+".conf"))
    return config

def get_tmpdir():
    s = options.tmpdir
    if not os.path.isdir(s):
        os.makedirs(s)
    return s

def mypopen(cmd):
    # TODO: use subprocess on 2.6+
    os.putenv('LC_ALL', 'POSIX')
    return os.popen(cmd)

if __name__ == '__main__':
    # test
    c = get_config('nginx')
    print c.get('port', 123)