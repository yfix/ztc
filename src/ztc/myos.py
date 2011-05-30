#!/usr/bin/env python
""" ZTC os helper functions

Copyright (c) 2011 Wrike, Inc. [http://www.wrike.com]
"""

import os
import sys
if sys.version_info >= (2, 6):
    import subprocess
else:
    import popen2    

def mypopen(cmd, logger=None, input=None):
    os.putenv('LC_ALL', 'POSIX')
    if logger:
        logger.debug("mypopen: executing %s", cmd)
    if sys.version_info >= (2, 6):
        pipe = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)
        (ret, err) = pipe.communicate(input)
    else:
        #ret = os.popen(cmd)
        (o, i, e) = popen2.popen3(cmd)
        if input:
            i.write(input)
            i.close()
        ret = o.read()
        err = e.read()
        o.close()
        e.close()
        
    if err:
        if logger:
            logger.warn("Stderr while executing '%s': '%s'" % (cmd, err))        
    return ret