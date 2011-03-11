#!/usr/bin/env python
'''
ZTC commons classes

Copyright (c) 2010 Vladimir Rusinov <vladimir@greenmice.info>
Licensed under GPL v.3
'''

import os
import optparse
import ConfigParser
import time
import cPickle as pickle

class MyConfigParser(ConfigParser.ConfigParser):
    def get(self, option, default):
        try:
            return ConfigParser.ConfigParser.get(self, 'main', option)
        except:
            return default

# TODO: deprecate
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
#(options, args) = parser.parse_args()

class MyStore(object):
    """ class for storing data in key files """
    def __init__(self, name):
        self.mydir = os.path.join(get_tmpdir(), 'store')
        self.myfile = os.path.join(self.mydir, name)
        try:
            os.makedirs(self.mydir)
            # TODO: better makedirs: fail when it's really impossible to create dir 
        except:
            pass
    
    def get(self):
        if time.time() - os.stat(self.myfile).st_mtime > 7200:
            # do not store for more then 2 hours
            self.clear()        
        f = open(self.myfile, 'r')
        ret = pickle.load(f)
        f.close()
        return ret
    
    def set(self, val):
        try:
            f = open(self.myfile, 'w')
            pickle.dump(val, f)
            f.close()
        except:
            pass # set should never fail
    
    def clear(self):
        os.unlink(self.myfile)

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
    print "Config test:"
    c = get_config('nginx')
    print c.get('port', 123)
    
    print "store test:"
    s = MyStore('test')
    s.set('test_val')
    print s.get()