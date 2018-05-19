from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtGui, QtCore
import sys
from gui.mainwindows import MainWindow
import xmltodict

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Main = MainWindow()
    Main.setWindowTitle("pytool")
    Main.show()
    app.exec_()
