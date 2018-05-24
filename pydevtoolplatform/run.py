import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from qtcode.sourceview import SourceView

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    Main = SourceView()
    Main.show()
    app.exec_()
