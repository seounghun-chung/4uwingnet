"""
    console.py is used to connect GUI and FEATURE
    It provides API for controlling GUI / FEATURE
    Never uses multiple class because API function is only connected to
    one class object (e.g. func1() is only callble on the one of class objects.
    There no way of multiple class objects.
        >>> a = Example(1)
        >>> b = Example(2)
        >>> a.func1()   # ok
        1
        >>> b.func1()   # ok
        2
        >>> func1()     # only can controll a.func1()
        1
"""

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

def get_name_of_obj(obj, except_word = ""):

    for name, item in globals().items():
        if item == obj and name != except_word:
            return name
def RegisterCommandClassObjectMap(o):
    """ Register class object for controlling in console """    
    global classObjectList        
    name = str(o.__class__.__name__)
    
    if (name in classObjectList) is True:
        print("Already class object (%s) was assigned in console API" % name)
    else:
        classObjectList[name] = o
        print("class object (%s) is assigned in console API" % name) 
        
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
    