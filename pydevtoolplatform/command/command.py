""" command.py is used to connect GUI and FEATURE
    It provides API for controlling GUI / FEATURE """

from PyQt5.QtCore import QObject, pyqtSignal, Qt, QEventLoop    

class PyQtSignalConnect(QObject):
    consoleview_clear = pyqtSignal()
    script_run = pyqtSignal()
    
    
    def __init__(self, *param):
        QObject.__init__(self, None)

    def clear(self):
        self.consoleview_clear.emit()
        
    def run(self):
        self.script_run.emit()
        
        
# it will be allocated in mainview.py from calling ConnectPytQtSignalBothCommandWithGui
cPyQtSignalConnect = None


def ConnectPytQtSignalBothCommandWithGui():
    """ it is for mainview.py. Signal must be used in GUI app """
    global cPyQtSignalConnect
    cPyQtSignalConnect = PyQtSignalConnect()

def GetPyQtSignalFromConsole():
    """ GUI components will connected it with here """
    return cPyQtSignalConnect
    
def clear():
    """ clear console view """
    cPyQtSignalConnect.clear()
    
def run():
    """ run script """
    cPyQtSignalConnect.run()