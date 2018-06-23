from unittest.case import TestCase
import unittest
import time
#from HTMLTestRunner import HTMLTestRunner

class MyTestCase(TestCase):
    def testTrue(self):
        '''Always true'''
        print("hello1")
        assert True
    def testTrue2(self):
        '''
        Always true
        it is coneected
        test method
        '''
        print("hello2")        
        assert True
    @unittest.skip("demonstrating skipping")
    def testFail(self):
        '''Always fails
        '''
        assert False   
    @unittest.skip("demonstrating skipping")    
    def testSleep(self):
        time.sleep(1)
        print("sleepaaaa...")
        time.sleep(1)
        print("sleep...")        
        assert True
   
if __name__ == '__main__':    

    loader = unittest.TestLoader()
    suite = unittest.makeSuite(MyTestCase)
    outfile = open('Report.html', 'w')
    runner = HTMLTestRunner(stream=outfile,
                            verbosity=2,
                            title='LinkedIn Report',
                            description='This is a demo report')
    runner.run(suite)
    
    
#    from pprint import pprint
#    runner = unittest.TextTestRunner()
#    result = runner.run(unittest.makeSuite(MyTestCase))
#    print (result.testsRun)
#    pprint(result.failures)

#    for ii in result.failures:
#        pprint(ii)