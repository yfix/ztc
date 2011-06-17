#!/usr/bin/env python
"""
vm.memory.* scripts item


This file is part of ZTC and distributed under GNU GPL v.3
Copyright (c) 2010 Vladimir Rusinov <vladimir@greenmice.info>

Params:
    $1 - metric name. Supported:
        active - amount of active (recently accessed) memory
        inavtive - amount of inactive (not accessed recently) memory
"""

from ztc.vm.memory import Memory

m = Memory()
c = m.args[0]
m.get(c, *m.args[1:])