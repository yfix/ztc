#!/usr/bin/env python
""" ZTC os helper functions

Copyright (c) 2011 Wrike, Inc. [http://www.wrike.com]
"""

import os

def mypopen(cmd):
    # TODO: use subprocess on 2.6+
    # TODO: catch stderr
    os.putenv('LC_ALL', 'POSIX')
    return os.popen(cmd)