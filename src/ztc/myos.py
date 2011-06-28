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
import logging    

def popen(cmd, logger, input=None):
    os.putenv('LC_ALL', 'POSIX')
    logger.debug("mypopen: executing %s", cmd)
    if sys.version_info >= (2, 6):
        pipe = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)
        (ret, err) = pipe.communicate(input)
        pipe.wait()
        retcode = pipe.returncode
    else:
        pipe = popen2.Popen3(cmd, True)
        i = pipe.tochild
        o = pipe.fromchild
        e = pipe.childerr
        if input:
            i.write(input)
            i.close()
        ret = o.read()
        err = e.read()
        o.close()
        e.close()
        retcode = pipe.wait()
        
    if err:
        logger.warn("Stderr while executing '%s': '%s'" % (cmd, err))        
    return retcode, ret

def mypopen(cmd, logger=None, input=None):
    if not logger:
        logger = logging.getLogger('mypopen')
        logger.setLevel(logging.FATAL)
    logger.warn("mypopen is deprecated, please use ztc.myos.popen instead")
    return popen(cmd, logger, input)[1]