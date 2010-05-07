#!/usr/bin/env python

from distutils.core import setup
import os
import glob
import sys

#sys.prefix='/opt/ztc/'
#sys.exec_prefix='/opt/ztc/'

setup(
      name='ztc',
      version = '10.2',
      description = 'Zabbix Template Collection',
      author = 'Vladimir Rusinov',
      author_email = 'vladimir@greenmice.info',
      url = 'http://trac.greenmice.info/ztc/',
      
      home = '/opt/ztc/',
      
      package_dir = {'': 'src'},
      packages = ['ztc', 'ztc.system', 'ztc.apache', 'ztc.mysql', 'ztc.nginx'],
      
      scripts = glob.glob('src/*.py'),  
      
      data_files=[
            ('/etc/zabbix-agent.d/', glob.glob('./conf/zabbix-agent.d/*.conf')),
            ('/etc/ztc',  glob.glob('./conf/etc/*.conf'))
      ],
)
