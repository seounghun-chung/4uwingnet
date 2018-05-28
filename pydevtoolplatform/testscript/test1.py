from unittest.case import TestCase
import unittest
import time


class MyTestCase(TestCase):
    def testTrue(self):
        '''
        Always true
        '''
        assert True
    def testTrue2(self):
        '''Always true'''
        assert True
    def testFail(self):
        '''
        Always fails
        '''
        assert False   
        
    def testSleep(self):
        time.sleep(1)
        print("sleepaaaa...")
        time.sleep(1)
        print("sleep...")        
        assert True
   
if __name__ == '__main__':    
    from pprint import pprint
    runner = unittest.TextTestRunner()
    result = runner.run(unittest.makeSuite(MyTestCase))
    print (result.testsRun)
    pprint(result.failures)

    for ii in result.failures:
        pprint(ii)