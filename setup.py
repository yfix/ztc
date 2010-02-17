#!/usr/bin/env python

from distutils.core import setup
import os
import glob

setup(name='ztc',
      version = '10.2',
      description = 'Zabbix Template Collection',
      author = 'Vladimir Rusinov',
      author_email = 'vladimir@greenmice.info',
      url = 'http://trac.greenmice.info/ztc/',
      
      package_dir = {'': 'src'},
      packages = ['ztc', 'ztc.system'],
      
      scripts = glob.glob('src/*.py'),  
)