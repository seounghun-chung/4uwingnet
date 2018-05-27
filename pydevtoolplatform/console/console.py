""" console.py is used to connect GUI and FEATURE
    It provides API for controlling GUI / FEATURE """

from PyQt5.QtCore import QObject, pyqtSignal, Qt, QEventLoop    
from features.example import Example

import os
import traceback
import sys
import inspect


class PyQtSignalConnect(QObject):
    consoleview_clear = pyqtSignal()
    script_run = pyqtSignal()
    exampleview = pyqtSignal(str)
    
    def __init__(self, *param):
        QObject.__init__(self, None)
    
        
# it will be allocated in mainview.py from calling ConnectPytQtSignalBothCommandWithGui
cPyQtSignalConnect = None
classObjectList = dict()

def cexec(arg1):
    """ it is used in consoleview """
    try:
        c = compile(arg1, "<string>", "single")
        exec(c, globals())
    except:  # (OverflowError, ValueError, SyntaxError, NameError):
        info = sys.exc_info()
        backtrace = traceback.format_exception(*info)
        for line in backtrace:
            sys.stderr.write(line)
            
def ConnectPytQtSignalBothCommandWithGui():
    """ it is for mainview.py. Signal must be used in GUI app """
    
    global cPyQtSignalConnect
    cPyQtSignalConnect = PyQtSignalConnect()

def RegisterCommandClassObjectMap(o):
    """ Register class object for controlling in console """    
    global classObjectList        
    name = str(o.__class__.__name__)
    if (name in classObjectList) is True:
        print("Already class object (%s) was assigned" % name)
    else:
        classObjectList[name] = o            
        print("class object (%s) is assigned" % name) 
        
def GetPyQtSignalFromConsole():
    """ GUI components will connected it with here """    
    return cPyQtSignalConnect


def clear():
    """ clear console view """
    cPyQtSignalConnect.consoleview_clear.emit()
    
def run():
    """ run script """
    cPyQtSignalConnect.script_run.emit()
    
def exampleview(s):
    """ set text example view """
    cPyQtSignalConnect.exampleview.emit(s)
    
def func1():
    """ example.func1() """
    classObjectList["Example"].func1()
    
def func2():
    """ example2.func2() """
    classObjectList["Example2"].func2()

def help():
    RegisterCommandClassObjectMap.__doc__ = "private"
    ConnectPytQtSignalBothCommandWithGui.__doc__ = "private"
    GetPyQtSignalFromConsole.__doc__ = "private"    
    cexec.__doc__ = "private"
    help.__doc__ = "private"
    
    func = inspect.getmembers(sys.modules[__name__],
                              predicate=lambda f: inspect.isfunction(f) and f.__module__ == __name__)
    print("========== Console Command List ============")
    func = sorted(func, key = lambda x : x[1].__doc__.lower()
                                if type(x[1].__doc__) is not type(None) \
                                else "z")    
    for ii in func:
        if (ii[1].__doc__ != "private"):
            print("  ", end="")
            print(ii[0], end="")
            print(inspect.formatargspec(*inspect.getfullargspec(ii[1])), end=" : ")
            print(ii[1].__doc__)    
    