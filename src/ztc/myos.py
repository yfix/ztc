#!/usr/bin/env python
""" ZTC os helper functions

Copyright (c) 2011 Wrike, Inc. [http://www.wrike.com]
"""

import os
import sys
if sys.version_info >= (2, 6):
    import popen2
else:
    import subprocess

def mypopen(cmd, logger=None, input=None):
    # TODO: catch stderr
    os.putenv('LC_ALL', 'POSIX')
    if sys.version_info >= (2, 6):
        # TODO: use subprocess on 2.6+
        #ret = os.popen(cmd)
        (i, o, err) = popen2.popen3(cmd)
        if input:
            i.write(input)
        ret = o.read()
        e = err.read()
        if e:
            if logger:
                logger.warn("Stderr while executing '%s': '%s'" % (cmd, e))
    else:
        (i, o, err) = popen2.popen3(cmd)
        #ret = os.popen(cmd)
        if input:
            i.write(input)
        ret = i.read()
    return ret