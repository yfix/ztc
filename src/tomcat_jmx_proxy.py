#!/usr/bin/env python
"""
tomcat jmx proxy script

Copyright (c) 2012 Wrike, Inc.
"""

from ztc.java.tomcat import TomcatJMXProxy

t = TomcatJMXProxy()
t.get('jmx_attr', 'java.lang:type=Memory', 'HeapMemoryUsage', 'used')
