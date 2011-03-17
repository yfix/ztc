#!/usr/bin/env python
""" ZTC Store class
Used for storing temporary values & cache

Copyright (c) 2010-2011 Vladimir Rusinov <vladimir@greenmice.info>
"""

import os
import time
import cPickle as pickle

class ZTCStore(object):
    """ class for storing data in key files """
    def __init__(self, name, options):
        """ Args:
        * name - name of store item
        * options = optparse options object. Needed for getting path of tmpdir
        """
        self.mydir = os.path.join(options.tmpdir, 'store')
        self.myfile = os.path.join(self.mydir, name)
        if not os.path.isdir(self.mydir):
            os.makedirs(self.mydir)
    
    def _mktmpdir(self, dir):
        """ check & make tmp dir """
        if not os.path.isdir(dir):
            os.makedirs(dir)        
    
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
