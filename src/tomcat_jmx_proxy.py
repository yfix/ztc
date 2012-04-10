#!/usr/bin/env python
"""
tomcat jmx proxy script

Copyright (c) 2012 Wrike, Inc.
"""

from ztc.java.tomcat import TomcatJMXProxy

t = TomcatJMXProxy()
m = t.args[0]
t.get(m, *t.args[1:])
