#!/usr/bin/env python
"""
    Terracotta check class for ZTC. Licensed under the same terms as ZTC.
    
    Copyright (c) 2011 Wrike, Inc. [http://www.wrike.com]
    Copyright (c) 2011 Vladimir Rusinov <vladimir@greenmice.info>
    
Terracotta beans:

#domain = JMImplementation:
JMImplementation:type=MBeanServerDelegate
#domain = com.sun.management:
com.sun.management:type=HotSpotDiagnostic
#domain = java.lang:
java.lang:name=Code Cache,type=MemoryPool
java.lang:name=CodeCacheManager,type=MemoryManager
java.lang:name=PS Eden Space,type=MemoryPool
java.lang:name=PS MarkSweep,type=GarbageCollector
java.lang:name=PS Old Gen,type=MemoryPool
java.lang:name=PS Perm Gen,type=MemoryPool
java.lang:name=PS Scavenge,type=GarbageCollector
java.lang:name=PS Survivor Space,type=MemoryPool
java.lang:type=ClassLoading
java.lang:type=Compilation
java.lang:type=Memory
java.lang:type=OperatingSystem
java.lang:type=Runtime
java.lang:type=Threading
#domain = java.util.logging:
java.util.logging:type=Logging
#domain = org.terracotta:
org.terracotta:name=DSO,type=Terracotta Server
org.terracotta:name=ObjectManagement,subsystem=Object Management,type=Terracotta Server
org.terracotta:name=Terracotta Statistics Gatherer,subsystem=Statistics,type=Terracotta Server
#domain = org.terracotta.internal:
org.terracotta.internal:name=Application Events,type=Terracotta Server
org.terracotta.internal:name=L2Dumper,type=Terracotta Server
org.terracotta.internal:name=Logger,type=Terracotta Server
org.terracotta.internal:name=Terracotta Lock Statistics,type=Terracotta Server
org.terracotta.internal:name=Terracotta Server,type=Terracotta Server
org.terracotta.internal:name=Terracotta Statistics Emitter,subsystem=Statistics,type=Terracotta Agent
org.terracotta.internal:name=Terracotta Statistics Gateway,subsystem=Statistics,type=Terracotta Server
org.terracotta.internal:name=Terracotta Statistics Manager,subsystem=Statistics,type=Terracotta Agent    
"""

from ztc.java.jmx import JMXCheck
from ztc.check import CheckFail
from ztc.store import ZTCStore

class JMXTerracotta(JMXCheck):
    """ Generic JMX check """
    
    name = 'terracotta'
    
    OPTPARSE_MIN_NUMBER_OF_ARGS = 2
    OPTPARSE_MAX_NUMBER_OF_ARGS = 3
    
    def __init__(self):
        """ constructor override """
        JMXCheck.__init__(self)
        # override default url
        self.jmx_url = self.config.get('jmx_url',
                                       'service:jmx:jmxmp://localhost:9520')
        
    def _get(self, metric, *args, **kwargs):
        if metric == 'get_prop':
            # get jmx property
            return self.get_prop(*args)
        elif metric == 'heap':
            # get java heap memory info
            # supported metric under heap: commited, init, max, used
            return self.get_heap(args[0])
        else:
            raise CheckFail('unsupported metric')
    
    def get_heap(self, metric):
        st = ZTCStore('java.terracotta.heap', self.options)
        st.ttl = 60
        data = st.get()
        if not data:
            # no cache, get from jmx
            data = self.get_prop('java.lang:type=Memory', 'HeapMemoryUsage')
            st.set(data)
        # example of prop value:
        # { 
        #  committed = 257294336;
        #  init = 268435456;
        #  max = 257294336;
        #  used = 59949552;
        # }
        for line in data.splitlines():
            line = line.strip()
            if line.startswith(metric):
                return int(line.split()[-1][:-1])
        raise CheckFail('no such memory mertic')