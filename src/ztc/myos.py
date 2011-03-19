#!/usr/bin/env python
""" ZTC os helper functions

Copyright (c) 2011 Wrike, Inc. [http://www.wrike.com]
"""

import os
import sys

def mypopen(cmd):
    # TODO: catch stderr
    os.putenv('LC_ALL', 'POSIX')
    if sys.version_info >= (2, 6):
        # TODO: use subprocess on 2.6+
        ret = os.popen(cmd)
    else:
        ret = os.popen(cmd)
    return ret