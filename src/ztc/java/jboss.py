#!/usr/bin/env python
"""
    Jboss check class for ZTC. Licensed under the same terms as ZTC.
    
    Copyright (c) 2011 Wrike, Inc. [http://www.wrike.com]
    Copyright (c) 2011 Vladimir Rusinov <vladimir@greenmice.info>
    
Use jboss-remoting.sar from server/all/deploy/ to enable remote jmx support
"""

from ztc.java.jmx import JMXCheck

class JMXJboss(JMXCheck):
    """ Jboss JMX check """
    
    name = 'jboss'
    
    def __init__(self):
        """ constructor override """
        JMXCheck.__init__(self)
        # override default url
        self.jmx_url = self.config.get('jmx_url',
                                       'service:jmx:rmi://localhost/jndi/rmi://localhost:1090/jmxconnector')