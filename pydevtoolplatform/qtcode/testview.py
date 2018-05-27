from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QEventLoop, QPoint 
from os.path import join, basename, dirname

import sys
import unittest
import time

qtdesignpath = "./qtdesign"
form_class = uic.loadUiType(join(qtdesignpath,"testview.ui"))[0]

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

class TestResult(unittest.TestResult):
    def __init__(self, *argv):
        super(TestResult, self).__init__(*argv)
        self.success = list()
        self.executetime = {}
        self._starttime = 0
        
    def addSuccess(self, test):
        super(TestResult, self).addSuccess(test)
        self.success.append(test)
        
    def startTest(self, test):
        super(TestResult, self).startTest(test)
        self._starttime = time.time()
        
    def stopTest(self, test):
        super(TestResult, self).stopTest(test)
        self.executetime[test] = (time.time()-self._starttime)*1000
        
class TestView(QWidget, form_class):
    def __init__(self, parent = None):
        super(TestView, self).__init__(parent)
        self.setupUi(self)

        # member variable
        self._leftdefaultsize = 200
        self.splitter.setSizes([self._leftdefaultsize,(self.size().width()) - self._leftdefaultsize])
        self.__rollbackImporter = RollbackImporter()
        
        # treeView model create
        self.model = QFileSystemModel()
        self.model.setNameFilters(["*.py"])        
        self.testmodel = QStandardItemModel()
        
        # button icons
        self.btnAdd.setFlat(True)
        self.btnAdd.setIcon(QIcon(join(qtdesignpath,"makefg.png")));        
        self.btnRun.setFlat(True)
        self.btnRun.setIcon(QIcon(join(qtdesignpath,"start.png")));        
        self.btnDel.setFlat(True)
        self.btnDel.setIcon(QIcon(join(qtdesignpath,"delete.png")));        
        
        # treeView setting
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.setRootPath('./testscript'))
        self.treeView.setAnimated(True)
        self.treeView.setSortingEnabled(True)
        [self.treeView.hideColumn(ii) for ii in range(1,5)]
        self.treeView.header().setStretchLastSection(False)
        self.treeView.header().setSectionResizeMode(0,QHeaderView.Stretch)           
        
        self.listView.setModel(self.testmodel)
        
        # signal connect        
        self.btnAdd.clicked.connect(self._btnAdd_clicked)
        self.btnRun.clicked.connect(self._btnRun_clicked)
        self.btnDel.clicked.connect(self._btnDel_clicked)
        self.treeView.activated.connect(self._btnAdd_clicked)
        self.listView.activated.connect(self._btnRun_clicked)
        
    def __extract_testunit(self, testsuite, testunits):
        """ extract unittest from testsuite discover was used"""
        if type(testsuite._tests[0]) == unittest.suite.TestSuite:
            self.__extract_testunit(testsuite._tests[0], testunits)
        else:
            for ii in testsuite._tests:
                testunits.append(ii) 
       
    def _btnDel_clicked(self):
        """ delete selected unittest list """
        selectedIndex = self.listView.selectedIndexes()
        deleteRow = list()
        for select in selectedIndex:
            deleteRow.append((select.row(), select.parent()))
        deleteRow.sort(reverse=True)
        for selectRow in deleteRow:
            self.testmodel.removeRow(selectRow[0], selectRow[1])
        
    def _btnRun_clicked(self):
        """ unittest run start """
        self.__rollbackImporter.rollbackImports() # clearly make sure test modules    
    
        selectedIndex = self.listView.selectedIndexes()
        selectedItems = [self.testmodel.itemFromIndex(ii) for ii in selectedIndex]
        
        suite = unittest.TestSuite()
        for testcase in selectedItems:
            if testcase.data() is not None:
                suite.addTest(testcase.data())
            else:
                """ parents (filename) is not runnable """

        if suite.countTestCases() != 0:          
            report = TestResult()
            suite.run(report)
            print(report)
            for success in report.success:
                print("%s %d ms" %(success, report.executetime[success]))
                
            for failures in report.failures:
                print("%s %d ms" %(failures, report.executetime[failures[0]]))
        else:
            """ there are not selected item """
            print("there are not selected item")

#        print(report.failures)
#        print(report.skipped)
        
#        runner = unittest.TextTestRunner(verbosity = 2)
#        
#        if suite.countTestCases() != 0:
#            runner.run(suite)
#        else:
#            """ there are not selected item """
#            print("there are not selected item")
       
    def _btnAdd_clicked(self):
        selectedIndex = self.treeView.selectedIndexes()
        selectedItems = [self.model.filePath(ii) for ii in selectedIndex]
        
        testloader = unittest.TestLoader()        
        
        for ii in selectedItems:
            if (ii[-3:] != ".py"):
                """ python script only can be added """
                continue
            else:
                try:
                    suite = testloader.discover(dirname(ii), pattern = basename(ii))
                except ImportError as e:
                    sys.stderr.write("don't duplicated unittest althought there are in other folder")
                    return
                    
                testunits = list()
                self.__extract_testunit(suite,testunits)
                for testname in testunits:
                    child = QStandardItem(str(testname))
                    child.setData(testname)
                    self.testmodel.insertRow(0, child)
