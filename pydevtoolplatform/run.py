import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from qtcode.sourceview import SourceView
from qtcode.mainview import MainView
from features.alloc import *

import logging
import datetime

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("root_%s.log"%(datetime.datetime.now().strftime("%Y-%m-%d")))
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Main = MainView()
    Main.show()
    app.exec_()
