#!/usr/bin/env python
"""
system_cpu_temp - get cpu temperature
"""

from ztc import notsupported

# try 0: read /proc/acpi/thermal_zone/THRM/temperature
# contains something like "temperature:             52 C"
try:
    f = open('/proc/acpi/thermal_zone/THRM/temperature', 'r')
    lines = f.readlines()
    print int(lines[-1].split()[-2])
    f.close()
except Exception, e:
    notsupported(e)

# no other methods supported (yet)