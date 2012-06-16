#!/usr/bin/env python
"""
ZTC setup file

Copyright (c) 2009-2012 Vladimir Rusinov <vladimir.rusinov@muransofot.com>
Copyright (c) 2012 Murano Software [http://www.muranosoft.com]
"""

import os
import glob
import sys

if sys.version_info > (3, 3):
    from packaging.core import setup
    print("Using packaging")
else:
    try:
        from distutils2.core import setup
        print("Using distutils2")
    except ImportError:
        from distutils.core import setup

setup(
      name='ztc',
      version='12.04',
      description='Zabbix Template Collection',
      author='Vladimir Rusinov',
      author_email='vladimir@greenmice.info',
      url='https://bitbucket.org/rvs/ztc/wiki/Home',

      package_dir={'': 'src'},
      packages=[
          'ztc', 'ztc.lib',
          'ztc.system', 'ztc.system.vfs',
          'ztc.apache', 'ztc.mysql', 'ztc.nginx',
          'ztc.vm',
          'ztc.pgsql',
          'ztc.net', 'ztc.net.icmp', 'ztc.net.http',
          'ztc.hw',
          'ztc.java', 'ztc.java.tomcat', 'ztc.php',
          'ztc.mongo',
          'ztc.ldap'],

      scripts=glob.glob('src/*.py'),

      data_files=[
            ('/etc/zabbix-agent.d/',
                  glob.glob('./conf/zabbix-agent.d/*.conf') + \
                  glob.glob('./conf/zabbix-agent.d/*.ini')),
            ('/etc/ztc', glob.glob('./conf/etc/*.conf')),
            ('/opt/ztc/templates', glob.glob('templates/*.xml')),
            ('/opt/ztc/doc/', ('README', 'REQUIREMENTS')),
            ('/opt/ztc/lib/', glob.glob('lib/*.jar')),
            ('/opt/ztc/contrib/2gis/bin/', glob.glob('contrib/2gis/bin/*')),
            ('/opt/ztc/contrib/2gis/conf/zabbix-agent.d/',
                  glob.glob('contrib/2gis/conf/zabbix-agent.d/*')),
            ('/opt/ztc/contrib/2gis/templates/',
                  glob.glob('contrib/2gis/templates/*')),
            ('/opt/ztc/contrib/2gis/', glob.glob('contrib/2gis/README')),
      ],
)
