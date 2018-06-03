from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5 import uic
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QEventLoop
from os.path import join
from console.console import RegisterObjectInConsole, GetPyQtSignalFromConsole
from features.example import Example
from features.example2 import Example2
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
        self.cExample = Example()
        self.cExample2 = Example2()    
        
        self.pushButton.clicked.connect(lambda : self.cExample.func1())
        self._commandSignal.exampleview.connect(lambda x : self.lineEdit.setText(x))  
        
        RegisterObjectInConsole(self, "exampleview")
        RegisterObjectInConsole(self.cExample, "example")
        RegisterObjectInConsole(self.cExample2, "example2")
        
    def text(self, x):
        """set test"""
        logger.debug("text() is called")        
        self.lineEdit.setText(x)