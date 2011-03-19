#!/usr/bin/env python
"""
system_cpu_temp - get cpu temperature

This file is part of ztc, http://greenmice.info/trac/ztc/
Licensed under GPL v.3
Copyright (c) 2010 Vladimir Rusinov <vladimir@greenmice.info>
"""

import sys
import re

from ztc import notsupported
from ztc.commons import mypopen

# try 0: read /proc/acpi/thermal_zone/THRM/temperature
# contains something like "temperature:             52 C"
try:
    f = open('/proc/acpi/thermal_zone/THRM/temperature', 'r')
    lines = f.readlines()
    print int(lines[-1].split()[-2])
    f.close()
    sys.exit(0)
except Exception, e:
    #notsupported(e)
    # try another method
    pass

# try2: using lm_sensors
try:
    n = 0
    tot_temp = 0.0
    temp_re = re.compile('(\d+.\d+) C')
    cmd = 'sensors -A'
    for l in mypopen(cmd).readlines():
        temps = temp_re.findall(l)
        if temps:
            temp = float(temps[0])
            tot_temp += temp
            n+=1
    print tot_temp/n
except Exception, e:
    notsupported(e)