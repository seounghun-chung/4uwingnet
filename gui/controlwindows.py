from feature.dummymanager import DummyManager

from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import uic

import os
import sys
qtDesignerPath = os.path.dirname(__file__)
form_class = uic.loadUiType(os.path.join(qtDesignerPath, "ControlWindows.ui"))[0]


class ControlWindows(QWidget, form_class):
    def __init__(self, parent = None):
        super(ControlWindows, self).__init__(parent)
        self.setupUi(self)

        self.pushButton_2.clicked.connect(self.pushButton_2_clicked)
        self.pushButton.clicked.connect(self.pushButton_clicked)
        self.pushButton_3.clicked.connect(self.pushButton_3_clicked)
        self.pushButton_13.clicked.connect(self.pushButton_13_clicked)
        self.pushButton_16.clicked.connect(self.pushButton_16_clicked)

        self.checkBox.stateChanged.connect(self.checkBox_stateChanged)
        self.ClassDummyManager = DummyManager()

        self.cnt = 0
        self.command = None
    def pushButton_13_clicked(self):
        self.command.InterfaceSerial.run()
        print("test")
        pass
    def pushButton_16_clicked(self):
        self.command.InterfaceSerial.WaitForResponse(1,0.05)
        self.command.InterfaceSerial.stop()

    def getCommandInstance(self, instance):
        self.command = instance
        self.pushButton_9.clicked.connect(self.command.InterfaceCan.RequestRoutineControl)


    def checkBox_stateChanged(self, e):
        self.cnt += 1
        print(self.comboBox.currentText())
        print(e)
        if (e == QtCore.Qt.Checked):
            print("try to connect")
            self.checkBox.setCheckState(QtCore.Qt.Unchecked)
            pass
        else:
            print("try to disconnect")
            pass

    def pushButton_clicked(self):
        print(self.lineEdit.displayText())
        self.lineEdit.clear()

    def pushButton_2_clicked(self):
        r = self.ClassDummyManager.run()
        self.ClassDummyManager.callback =lambda x : self.label_3.setText(str(x))

        print(self.lineEdit_2.displayText())
        self.lineEdit_2.clear()

    def pushButton_3_clicked(self):
        self.label_3.setText("version1 : " + str(self.ClassDummyManager.getrnd()))
        self.label_4.setText("version2 : " + str(self.ClassDummyManager.getrnd()))
        self.label_5.setText("helloaaaaaaaasdafwefwefweaaaaaaaaaaaa")
        self.label_6.setText("hello")
        self.label_7.setText("hello")