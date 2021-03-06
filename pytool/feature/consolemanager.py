# next command list is not controlled by consolemanager.py
# so then, directly handle these in lineEdit_returnPressed() of consolewindows.py
# if (cmd == ""):
#     pass
# elif (cmd == "help()"):  # help() occurs error in GUI console widget
#     consolemanager.cexec("info()")
# elif (cmd == "exit()"):  # exit() occurs error in exec module
#     exit(0)

import threading
import os
import traceback
import sys
import inspect

from PyQt5.QtCore import QObject, pyqtSignal

from feature.dummymanager import *
from gui.consolewindows import ConsoleWindows
from feature.command import Command

class GuiControlSignal(QObject):
    clearOccur = pyqtSignal(int, name="control")

    def __init__(self, *param):
        QObject.__init__(self, None)

    def clear(self):
        self.clearOccur.emit(1)
        
    def test(self):
        print("hello?")

ClassConsoleWindows = None
ClassCommand = None
C = DummyManager()
ClassGuiControlSignal = GuiControlSignal()

        
def help(module):
    print(module.__doc__)

def cexec(s):
    """private functions"""
    try:
        if (os.path.isfile(s) is True):
            f = open(s).read()
            f = "from feature import dummymanager\r" + f
            
            # gui class is not worked in thread ....
#            t1 = threading.Thread(target=exec, args=(f, globals(),))
#            t1.daemon = True
#            t1.start()
            exec(f, globals())
        else:
            c = compile(s, "<string>", "single")
            exec(c, globals())

    except:  # (OverflowError, ValueError, SyntaxError, NameError):
        info = sys.exc_info()
        backtrace = traceback.format_exception(*info)
        for line in backtrace:
            sys.stderr.write(line)


def connect(c):
    """private functions"""
    global ClassConsoleWindows
    global ClassCommand

    if (type(c) == ConsoleWindows):
        ClassConsoleWindows = c
    elif (type(c) == Command):
        ClassCommand = c


def clear():
    """clear console windows"""
    ClassGuiControlSignal.clear()
#    if ClassConsoleWindows is not None:
#        ClassConsoleWindows.clear()
        


def WaitForResponse(msg, timeout = 1):
    """Wait for serial reponse during timeout"""
    ret = False
    if ClassCommand is not None:
        ret = ClassCommand.InterfaceSerial.WaitForResponse(msg, timeout)
    return ret

def RequestRoutineControl():
    ClassCommand.InterfaceCan.RequestRoutineControl()

def serial():
    if ClassCommand is not None:
        ClassCommand.InterfaceSerial.test()


def setinfo(s):
    C.setinfo(s)


def getinfo():
    return C.getinfo()


def info():
    func = inspect.getmembers(sys.modules[__name__],
                              predicate=lambda f: inspect.isfunction(f) and f.__module__ == __name__)
    print("command list")
    func = sorted(func, key = lambda x : x[1].__doc__.lower()
                                if type(x[1].__doc__) is not type(None) \
                                else "z")
    
    for ii in func:
        if (ii[1].__doc__ != "private functions"):
            print("  ", end="")
            print(ii[0], end="")
            print(inspect.formatargspec(*inspect.getfullargspec(ii[1])), end=" : ")
            print(ii[1].__doc__)
