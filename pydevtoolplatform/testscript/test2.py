from unittest.case import TestCase
import unittest

class MyTestCase(TestCase):
    def tearDown(self):
        print("teadown class....")
    def testTrue(self):
        '''
        Always true
        '''
        assert True
    def testTrue2(self):
        '''
        Always true
        '''
        assert True
    def testFail(self):
        '''
        Always fails
        '''
        assert False
    def testFail2(self):
        '''
        Always fails
        '''
        assert False
    def testFail3(self):
        '''
        Always fails
        '''
        assert False        
    
if __name__ == '__main__':    
    from pprint import pprint
    runner = unittest.TextTestRunner()
    result = runner.run(unittest.makeSuite(MyTestCase))
    print (result.testsRun)
    pprint(result.failures)

    for ii in result.failures:
        pprint(ii)