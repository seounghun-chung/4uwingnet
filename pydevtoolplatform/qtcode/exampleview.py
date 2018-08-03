from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QEventLoop
from PyQt5.QtCore import QSettings, QPoint, QSize
from os.path import join
from console.console import GetPyQtSignalFromConsole
from features import alloc
import logging
import sys
import traceback

logger = logging.getLogger("qtcode.exampleview")

qtdesignpath = "./qtdesign"
form_class = uic.loadUiType(join(qtdesignpath,"exampleview.ui"))[0]

class ExampleView(QWidget, form_class):
    def __init__(self, parent = None):
        super(ExampleView, self).__init__(parent)
        self.setupUi(self)
        logger.debug("exampleview created")
        
        self._commandSignal = GetPyQtSignalFromConsole()
        self.cExample = alloc.example
        self.cExample2 = alloc.example2  
        
        self.pushButton.clicked.connect(lambda : self._test1())
#        self.pushButton_2.clicked.connect(self._test1)
        
        self._commandSignal.exampleview.connect(lambda x : self.lineEdit.setText(x))  

        self.settings = QSettings('test.ini', QSettings.IniFormat)  
        self.groupBox.setChecked(True if self.settings.value("checkbox1", True) == "true" else False)
        self.groupBox.clicked.connect(lambda : self.settings.setValue("checkbox1", self.groupBox.isChecked()))

    def _test1(self):
        b

    def _test2(self, prog):
        import time
        prog.setRange(0,10)
        for ii in range(0,10):
            time.sleep(0.5)
            prog.setValue(ii)
            
    def text(self, x):
        """set test"""
        logger.debug("text() is called")        
        self.lineEdit.setText(x)