"""
    console.py is used to connect GUI and FEATURE
    It provides API for controlling GUI / FEATURE
    It can used class object through from features.alloc import *
"""

from PyQt5.QtCore import QObject, pyqtSignal, Qt, QEventLoop, QTimer   
from features.alloc import *

import os
import traceback
import sys
import inspect
import logging

logger = logging.getLogger("console.console")

# it will be allocated in mainview.py from calling ConnectPytQtSignalBothCommandWithGui
_PyQtSignalConnect = None

class PyQtSignalConnect(QObject):
    consoleview_clear = pyqtSignal()
    script_run = pyqtSignal()
    exampleview = pyqtSignal(str)
    consoleview_print = pyqtSignal(str, str)
    
    def __init__(self, *param):
        QObject.__init__(self, None)

def cexec(arg1, isfile = False):
    """ it is used in consoleview """
    try:
        if isfile is False:
            c = compile(arg1, "<string>", "single")
        else:
            c = arg1
        exec(c, globals())
    except:  # (OverflowError, ValueError, SyntaxError, NameError):
        info = sys.exc_info()
        backtrace = traceback.format_exception(*info)
        for line in backtrace:
            sys.stderr.write(line)
            
def ConnectPytQtSignalBothCommandWithGui():
    """ it is for mainview.py. Signal must be used in GUI app """
    global _PyQtSignalConnect
    _PyQtSignalConnect = PyQtSignalConnect()

def GetPyQtSignalFromConsole():
    """ GUI components will connected it with here """    
    return _PyQtSignalConnect

def settext(s):
    _PyQtSignalConnect.exampleview.emit(s)
    
def clear():
    """ clear console view """
    _PyQtSignalConnect.consoleview_clear.emit()
    
def run():
    """ run script """
    _PyQtSignalConnect.script_run.emit()

#def print(msg, color="black"):
#    _PyQtSignalConnect.consoleview_print.emit(msg, color)    
    
def msleep(t):
    loop = QEventLoop()
    QTimer.singleShot(t, loop.quit)
    loop.exec_()
    
def help(obj = None):
#    RegisterObjectInConsole.__doc__ = "private"
    ConnectPytQtSignalBothCommandWithGui.__doc__ = "private"
    GetPyQtSignalFromConsole.__doc__ = "private"    
    cexec.__doc__ = "private"
    help.__doc__ = "private"
    
    if obj is None:
        func = inspect.getmembers(sys.modules[__name__],
                                  predicate=lambda f: inspect.isfunction(f) and f.__module__ == __name__)
        print("========== Console Command List ============")
        func = sorted(func, key = lambda x : x[1].__doc__.lower()
                                    if type(x[1].__doc__) is not type(None) \
                                    else "z")    
        for ii in func:
            if (ii[1].__doc__ != "private"):
                out = "  %s%s : %s" %(ii[0], inspect.formatargspec(*inspect.getfullargspec(ii[1])), ii[1].__doc__)
                print(out)

        for ii in listOfAllocatedClassObject:
            print(" %s : object , for getting more information help(%s)" % (ii, ii))
    else:
        func = inspect.getmembers(obj, predicate = inspect.ismethod)  
        if len(func) == 0:
            try:
                inspect.getfullargspec(obj) # pass not support help()
                out = "parameter %s : %s" % (inspect.formatargspec(*inspect.getfullargspec(obj)), obj.__doc__)    
                print(out)
            except:
                print("Not support help()")
                pass
        else:
            print("Class method = ")
            for ii in func:
                if ii[0] == "__init__":
                    continue
                out = "  %s%s : %s" % (ii[0], inspect.formatargspec(*inspect.getfullargspec(ii[1]))
                                    , ii[1].__doc__)
                print(out)
    print("")
        