import sys, os
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from qtcode.sourceview import SourceView
from qtcode.mainview import MainView
from features.alloc import *

import logging
import datetime

def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)

if sys.executable.endswith("pythonw.exe"):
  sys.stdout = open(os.devnull, "w");
  sys.stderr = open(os.path.join(os.getenv("TEMP"), "stderr-"+os.path.basename(sys.argv[0])), "w")
  
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("root_%s.log"%(datetime.datetime.now().strftime("%Y-%m-%d")))
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

if __name__ == '__main__':
    sys._excepthook = sys.excepthook

    # Set the exception hook to our wrapping function
    sys.excepthook = my_exception_hook
    app = QApplication(sys.argv)
    Main = MainView()
    Main.show()    
    app.exec_()
