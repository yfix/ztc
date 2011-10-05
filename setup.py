#!/usr/bin/env python
"""
ZTC setup file
"""

from distutils.core import setup
import os
import glob
import sys

setup(
      name='ztc',
      version = '11.10',
      description = 'Zabbix Template Collection',
      author = 'Vladimir Rusinov',
      author_email = 'vladimir@greenmice.info',
      url = 'https://bitbucket.org/rvs/ztc/wiki/Home',
      
      home = '/opt/ztc/',
      
      package_dir = {'': 'src'},
      packages = ['ztc', 'ztc.system', 'ztc.apache', 'ztc.mysql', 'ztc.nginx', 'ztc.vm', 'ztc.pgsql', 'ztc.net', 'ztc.hw', 'ztc.java', 'ztc.php', 'ztc.lib'],
      
      scripts = glob.glob('src/*.py'),
      
      data_files=[
            ('/etc/zabbix-agent.d/', glob.glob('./conf/zabbix-agent.d/*.conf') + glob.glob('./conf/zabbix-agent.d/*.ini')),
            ('/etc/ztc',  glob.glob('./conf/etc/*.conf')),
            ('/opt/ztc/templates', glob.glob('templates/*.xml')),
            ('/opt/ztc/doc/', ('README', 'REQUIREMENTS')),
            ('/opt/ztc/lib/', glob.glob('lib/*.jar'))
            ('/opt/ztc/contrib/2gis/bin/*', glob.glob('contrib/2gis/bin/*')),
            ('/opt/ztc/contrib/2gis/conf/zabbix-agent.d/*', glob.glob('contrib/2gis/conf/zabbix-agent.d/*')),
            ('/opt/ztc/contrib/2gis/templates/*', glob.glob('contrib/2gis/templates/*')),
            ('/opt/ztc/contrib/2gis/README', glob.glob('contrib/2gis/README')),
      ],
)
