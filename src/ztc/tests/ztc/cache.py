'''
Created on 17.12.2009

@author: vrusinov
'''
import unittest
import time

import ztc.cache

class CacheTest(unittest.TestCase):
    def testSaveLoad(self):
        """ cache save-load test """
        o1 = ztc.cache.CacheObject()
        o1.data = "Here is the test"
        c = ztc.cache.Cache()
        c.save('test', o1)
        
        o2 = c.load('test')
        
        self.assertEqual(o1.data, o2.data)
    
    def testAge(self):
        """ cache entry age test """
        o1 = ztc.cache.CacheObject()
        time.sleep(1)
        self.assert_(o1.age < 2 and o1.age > 1)
        
if __name__ == '__main__':
    unittest.main()