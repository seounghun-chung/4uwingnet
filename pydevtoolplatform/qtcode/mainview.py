from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5 import uic
from os.path import join
from command.command import *

import sys
import os
import traceback

#logging.basicConfig(level = logging.DEBUG)

qtdesignpath = "./qtdesign"
form_class = uic.loadUiType(join(qtdesignpath,"mainview.ui"))[0]


class MainView(QMainWindow, form_class):
    def __init__(self):
        ConnectPytQtSignalBothCommandWithGui()    # signal is only connected in GUI app    
        super().__init__()
        self.setupUi(self)        
        self.dockWidget_2.visibilityChanged.connect(self._stdout_redirect)
        
    def _stdout_redirect(self, s):
        """ stdout redirection true / false """
        self.dockWidgetContents_2.stdout_redirect(s)