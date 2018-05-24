"""
GUI framework for Python unit testing

This module is free software, and you may redistribute it and/or modify
it under the same terms as Python itself, so long as this copyright message
and disclaimer are retained in their original form.

IN NO EVENT SHALL THE AUTHOR BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OF
THIS CODE, EVEN IF THE AUTHOR HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH
DAMAGE.

THE AUTHOR SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE.  THE CODE PROVIDED HEREUNDER IS ON AN "AS IS" BASIS,
AND THERE IS NO OBLIGATION WHATSOEVER TO PROVIDE MAINTENANCE,
SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
"""
__author__ = "Seounghun, Chung (4uwingnet@naver.com)"
__version__ = "$Revision: 0.1 $"[11:-2]

import unittest
import os
import logging
import traceback
import time
import sys

logger = logging.getLogger("test.manager")
logger.setLevel(logging.DEBUG)
stream_hander = logging.StreamHandler()
logger.addHandler(stream_hander)

class UnittestReport(unittest.TestResult):
    def __init__(self, callback):
        unittest.TestResult.__init__(self)
        self.callback = callback
        self.timestamp = 0
        
    def addError(self, test, err):
        unittest.TestResult.addError(self, test, err)
        self.callback.notifyTestErrored(test, err)
        
    def addSuccess(self, test):
        unittest.TestResult.addSuccess(self, test)
        self.callback.notifyTestSuccessed(test)
        
    def addFailure(self, test, err):
        unittest.TestResult.addFailure(self, test, err)
        tracebackLines =  traceback.format_exception(*err)
        tracebackText = "".join(tracebackLines)
        self.callback.notifyTestFailed(test, tracebackText)

    def addSkip(self, test, reason):
        super(UnittestReport,self).addSkip(test, reason)
        self.callback.notifyTestSkipped(test, reason)

    def addExpectedFailure(self, test, err):
        super(UnittestReport,self).addExpectedFailure(test, err)
        self.callback.notifyTestFailedExpectedly(test, err)

    def stopTest(self, test):
        unittest.TestResult.stopTest(self, test)
        self.timestamp = time.time() - self.timestamp 
        self.callback.notifyTestFinished("%s : %.3lf ms" % (test, self.timestamp*1000))       
        
    def startTest(self, test):
        unittest.TestResult.startTest(self, test)
        self.callback.notifyTestStarted(test)
        self.timestamp = time.time()


class TestManager(object):
    def __init__(self, *args):
        self.test_suites = None # test suite dictionary
                                # {path : testsuites,}
        self.prepare_test_suites = unittest.TestSuite() # ready to test
        
        self.pyqt = args[0]     # for connecting GUI with testreport alert
        self.__rollbackImporter = RollbackImporter()
        
    def addTests(self, path):
        self.__rollbackImporter.rollbackImports() # clearly make sure test modules    
        this_dir = os.path.dirname(os.path.abspath(path))
        pattern = os.path.basename(path)
        tests = unittest.defaultTestLoader.discover(start_dir=this_dir, pattern=pattern)    

        if self.test_suites is None:
            self.test_suites = {path : tests}
        else:
            self.test_suites[path] = tests
    
        logger.debug("addTest is successful! ")
        
    def delTests(self, path):
        del self.test_suites[path]
        logger.debug("delTests is successful! ")
        
    def prepareTests(self, path):
        logger.debug("%s : prepared" % path)
        self.prepare_test_suites.addTests(self.test_suites[path])
        del self.test_suites[path]
            
    def run(self):
        # for callback functions test report
        result = UnittestReport(self.pyqt)
        self.prepare_test_suites.run(result)        
        self.prepare_test_suites = unittest.TestSuite() # initialize prepare test item


class RollbackImporter(object):
    """This tricky little class is used to make sure that modules under test
    will be reloaded the next time they are imported.
    """
    def __init__(self):
        self.previousModules = sys.modules.copy()

    def rollbackImports(self):
        for modname in sys.modules.copy().keys():
            if not modname in self.previousModules:
                # Force reload when modname next imported
                del(sys.modules[modname])