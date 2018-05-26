from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QEventLoop, QPoint 
from os.path import join, basename, dirname

import sys
import unittest


qtdesignpath = "./qtdesign"
form_class = uic.loadUiType(join(qtdesignpath,"testview.ui"))[0]

class TestView(QWidget, form_class):
    def __init__(self, parent = None):
        super(TestView, self).__init__(parent)
        self.setupUi(self)

        # member variable
        self._leftdefaultsize = 200
        self.splitter.setSizes([self._leftdefaultsize,(self.size().width()) - self._leftdefaultsize])

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
        if type(testsuite._tests[0]) == unittest.suite.TestSuite:
            self.__extract_testunit(testsuite._tests[0], testunits)
        else:
            for ii in testsuite._tests:
                testunits.append(ii) 
       
    def _btnDel_clicked(self):
        selectedIndex = self.listView.selectedIndexes()
        deleteRow = list()
        for select in selectedIndex:
            deleteRow.append((select.row(), select.parent()))
        deleteRow.sort(reverse=True)
        for selectRow in deleteRow:
            self.testmodel.removeRow(selectRow[0], selectRow[1])
        
    def _btnRun_clicked(self):
        selectedIndex = self.listView.selectedIndexes()
        selectedItems = [self.testmodel.itemFromIndex(ii) for ii in selectedIndex]
        
        suite = unittest.TestSuite()
        for testcase in selectedItems:
            if testcase.data() is not None:
                suite.addTest(testcase.data())
            else:
                """ parents (filename) is not runnable """
                
        runner = unittest.TextTestRunner(verbosity = 2)
        
        if suite.countTestCases() != 0:
            runner.run(suite)
        else:
            """ there are not selected item """
            print("there are not selected item")
       
    def _btnAdd_clicked(self):
        selectedIndex = self.treeView.selectedIndexes()
        selectedItems = [self.model.filePath(ii) for ii in selectedIndex]
        
        testloader = unittest.TestLoader()        
        
        for ii in selectedItems:
            if (ii[-3:] != ".py"):
                """ python script only can be added """
                continue
            else:
                suite = testloader.discover(dirname(ii), pattern = basename(ii))
                testunits = list()
                self.__extract_testunit(suite,testunits)
                for testname in testunits:
                    child = QStandardItem(str(testname))
                    child.setData(testname)
                    self.testmodel.insertRow(0, child)
