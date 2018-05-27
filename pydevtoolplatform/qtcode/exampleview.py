from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5 import uic
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QEventLoop
from os.path import join
from console import console
from features.example import Example
from features.example2 import Example2

import sys
import traceback

qtdesignpath = "./qtdesign"
form_class = uic.loadUiType(join(qtdesignpath,"exampleview.ui"))[0]

class ExampleView(QWidget, form_class):
    def __init__(self, parent = None):
        super(ExampleView, self).__init__(parent)
        self.setupUi(self)
    
        self._commandSignal = console.GetPyQtSignalFromConsole()
        self.cExample = Example()
        self.cExample2 = Example2()        
        
        self.pushButton.clicked.connect(lambda : self.cExample.func1())
        self._commandSignal.exampleview.connect(lambda x : self.lineEdit.setText(x))
        
        