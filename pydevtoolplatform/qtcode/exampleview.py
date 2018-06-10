from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5 import uic
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QEventLoop
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
        
        self.pushButton.clicked.connect(lambda : self.cExample.func1())
        self._commandSignal.exampleview.connect(lambda x : self.lineEdit.setText(x))  
        
    def text(self, x):
        """set test"""
        logger.debug("text() is called")        
        self.lineEdit.setText(x)