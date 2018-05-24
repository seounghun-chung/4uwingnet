from feature import consolemanager
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5 import uic
from PyQt5.QtCore import QObject, pyqtSignal, Qt
from gui import syntax

import os
import sys
import threading
import traceback
import logging

#logging.basicConfig(level = logging.DEBUG)

qtDesignerPath = os.path.dirname(__file__)
form_class = uic.loadUiType(os.path.join(qtDesignerPath, "ConsoleWindows.ui"))[0]


class StdoutRedirect(QObject):
    printOccur = pyqtSignal(str, str, name="print")

    def __init__(self, *param):
        QObject.__init__(self, None)
        self.daemon = True
        self.sysstdout = sys.stdout.write
        self.sysstderr = sys.stderr.write

    def stop(self):
        sys.stdout.write = self.sysstdout
        sys.stderr.write = self.sysstderr

    def start(self):
        sys.stdout.write = self.write
        sys.stderr.write = lambda msg : self.write(msg, color="red")

    def write(self, s, color="black"):
        self.printOccur.emit(s, color)


class ConsoleWindows(QWidget, form_class):
    def __init__(self, parent = None):
        super(ConsoleWindows, self).__init__(parent)
        self.setupUi(self)

        # get class object for connecting GUI
        self._clear = consolemanager.ClassGuiControlSignal  
        self._clear.clearOccur.connect(lambda x : self.clear())
        
        self._stdout = StdoutRedirect()
        self._stdout.printOccur.connect(lambda x, y: self.append_text(x, y)) # print redirection

        self.comboBox.keyPressEvent = self.comboBox_keyPressEvent
        self.comboBox.addItems(self._GetConsoleManagerFunctionList())        
        self.comboBox.setCurrentText("")        
        self.fontComboBox.currentFontChanged.connect(lambda x : self.textBrowser.setFont(x))
        self.textBrowser.setFont(QtGui.QFont(self.fontComboBox.currentText(), 9))
        self.fmt = QtGui.QTextCharFormat();
    def stdout_redirect(self, s):
        if s is True:
            self._stdout.start()
        else:
            self._stdout.stop()
        
    def comboBox_keyPressEvent(self, e):
        QComboBox.keyPressEvent(self.comboBox, e)
        if e.key() == Qt.Key_Return:
            cmd = self.comboBox.currentText()
            self.textBrowser.moveCursor(QtGui.QTextCursor.End)
            self.comboBox.setCurrentText("")
            
            if (cmd == ""):
                pass
            elif (cmd == "help()"): # help() occurs error in GUI console widget
                consolemanager.cexec("info()")
            elif (cmd == "exit()"): # exit() occurs error in exec module
                exit(0)
            else:
                self.append_text(">>> " + cmd + "\n")
                consolemanager.cexec(cmd)        
        else:
            pass
            
    def _GetConsoleManagerFunctionList(self):
        from inspect import formatargspec, getfullargspec, getmembers, isfunction, getargspec
        import inspect
        
        # skip private functions in console manager
        functions_list = [o for o in getmembers(consolemanager) if isfunction(o[1]) and (o[1].__doc__ != "private functions")]
        # make function list and argv
        # o[0] is function name
        # o[1] is function address
        # formatargspec(getfullargspec(o[1])[0]) is argv of functions
        ret = [o[0] + (formatargspec(getfullargspec(o[1])[0])) for o in functions_list] 
        return ret
        
    def append_text(self, msg, color="black"):
        self.textBrowser.moveCursor(QtGui.QTextCursor.End)

        # set user color
        self.fmt.setForeground(QtGui.QBrush(QtGui.QColor(color)));
        self.textBrowser.mergeCurrentCharFormat(self.fmt);                
        self.textBrowser.insertPlainText(msg)

    def clear(self):
        self.textBrowser.clear()
        self.comboBox.clear()
