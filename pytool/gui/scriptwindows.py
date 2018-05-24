""" this code is spagetti code .... if you have a problem,
    don't try analize this file. just remove!"""


from feature import consolemanager

from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem 
import os

#logging.basicConfig(level = logging.DEBUG)

qtDesignerPath = os.path.dirname(__file__)
xmlconfigPath = os.path.join(os.path.dirname(__file__),"../config/")

form_class = uic.loadUiType(os.path.join(qtDesignerPath, "ScriptWindows.ui"))[0]

class ScriptWindows(QWidget, form_class):
    def __init__(self, parent = None):
        super(ScriptWindows, self).__init__(parent)
        self.setupUi(self)

        self._defaultdir = "./script"
        self._currentname = "./script"
        
        self.pushButton_5.clicked.connect(self._pushButton_5_connect)
        self.pushButton_4.clicked.connect(self._pushButton_4_connect)
        self.pushButton_2.clicked.connect(self._pushButton_2_connect)
        self.pushButton_3.clicked.connect(self._pushButton_3_connect)

        self.listWidget.itemActivated.connect(self.listWidget_itemDoubleClicked)
        self.listWidget.setAlternatingRowColors(True)   
        self.plainTextEdit.keyPressEvent = self.plainTextEdit_keyPressEvent            
        self._find_script_directory()
        self._leftdefaultsize = 200
        self.splitter.setSizes([self._leftdefaultsize,(self.size().width()) - self._leftdefaultsize])
        
    def _pushButton_3_connect(self):    # loadUiType
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if (os.path.isfile(fileName) == True):
            self._open_script(fileName)
        else:
            pass
        
    def _pushButton_2_connect(self):    # save
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", self._currentname,
                                                  "Python Files (*.py)", options=options)
        if fileName == "":
            pass
        else:
            with open(fileName,"w") as f:
                f.write(self.plainTextEdit.toPlainText())
            self._currentname = fileName    # when re save occurs, it will be used in default path
            self._find_script_directory()
            
    def plainTextEdit_keyPressEvent(self, event):
        # this is monkey.......
        # how to change tab to 4 space ?
        if (event.key() == Qt.Key_Tab):
            self.plainTextEdit.insertPlainText(" "*4)
        else:
            QPlainTextEdit.keyPressEvent(self.plainTextEdit, event)
        
    def _open_script(self, path):
        if not os.path.exists(path):
            print("fine not exist")
            return
            
        with open(path) as f:
            self.plainTextEdit.clear();           
            self.plainTextEdit.setPlainText(f.read())         
            
            # when re save occurs, it will be used in default path                         
            self._currentname = path
        
    def listWidget_itemDoubleClicked(self, e):
        self._open_script(os.path.join(self._defaultdir, e.text()))

    def _pushButton_4_connect(self):    # run btn
        with open("_temp.py", "w") as f:
            f.write(self.plainTextEdit.toPlainText())        
        consolemanager.cexec("_temp.py")  
        os.remove("_temp.py")
        
    def _find_script_directory(self):     # find directory 
        self.listWidget.clear();    
        dir = QDir(self._defaultdir)
        dir.setFilter(QDir.Files | QDir.Hidden | QDir.NoSymLinks)        
        dirlist = dir.entryInfoList();
        
        for ii in dirlist:
            if (ii.fileName()[-3:] == ".py"):
                self.listWidget.addItem(ii.fileName())   
            else:
                pass
        abspath = os.path.abspath(self._defaultdir)
        relativepath = abspath.split("\\")
        
        self.label_2.setText(os.path.join(*relativepath[-3:]))
        self.label_2.setToolTip(os.path.join(*relativepath))
        
    def _pushButton_5_connect(self):    # direcotry btn
        dir = QFileDialog()
        dir = dir.getExistingDirectory(self, "Select script folder", self._defaultdir);          
        if dir == "":   # cancle select folder
            pass
        else:   # add python script to listwidget
            self._defaultdir = dir
            self._find_script_directory()
