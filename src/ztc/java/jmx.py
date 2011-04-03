#!/usr/bin/env python
"""
    JMX Check class for ZTC. Licensed under the same terms as ZTC.
    
    Copyright (c) 2011 Wrike, Inc. [http://www.wrike.com]
    Copyright (c) 2011 Vladimir Rusinov <vladimir@greenmice.info>

Usage example to jmxterm-*.jar:

java -Djava.endorsed.dirs=/opt/ztc/lib/ -jar /opt/ztc/lib/jmxterm-1.0-alpha-4-uber.jar -l service:jmx:jmxmp://localhost:9520
get -b java.lang:type=ClassLoading LoadedClassCount -s

automated version:

echo "get -b java.lang:type=ClassLoading LoadedClassCount -s" | java -Djava.endorsed.dirs=/opt/ztc/lib/ -jar /opt/ztc/lib/jmxterm-1.0-alpha-4-uber.jar -l service:jmx:jmxmp://localhost:9520 -e -n -v silent 

"""

from ztc.check import ZTCCheck, CheckFail

class JMXCheck(ZTCCheck):
    """ Generic JMX check """
    
    name = 'java'
    
    OPTPARSE_MIN_NUMBER_OF_ARGS = 3
    
    def _get(self, metric, *args, **kwargs):
        # TODO: implement
        if metric == 'get_prop':
            # get jmx property
            self.get_prop(*args)
        else:
            raise CheckFail('unsupported metric')
    
    def get_prop(self, mbean_name, attribute_name):
        popen_cmd = "java -Djava.endorsed.dirs=/opt/ztc/lib/ -jar " + \
            "/opt/ztc/lib/jmxterm-1.0-alpha-4-uber.jar -l %s -e -n -v silent" % \
            (self.jmx_url, )
        jmxterm_cmd = "get -b %s %s -s" % (mbean_name, attribute_name)
        self.logger.debug("Executing jmxterm command %s" % jmxterm_cmd)
        self.logger.debug("Jmxterm executable: %s" % popen_cmd)
        # TODO: mypopen function with input support            