# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test2.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QEventLoop
from PyQt5.QtWidgets import QApplication

from diaglogsampleui import Ui_Form
from datetime import date
import os  
import shutil
import glob

class DiaglogSample(Ui_Form):
    def __init__(self, *argv):
        super().setupUi(*argv)
        self.pushButton.setEnabled(False)
        
        self.comboBox.currentTextChanged.connect(lambda x : self._maketext(version = x))
        self.comboBox_2.currentTextChanged.connect(lambda x : self._maketext(rev = x))
        self.lineEdit.textChanged.connect(lambda x : self._maketext( desc = x ))
        self.lineEdit_2.textChanged.connect(lambda x: self._findgitpath( x ) )
        self.pushButton.clicked.connect(lambda : self._generate())
        
        self.version = self.comboBox.currentText()
        self.rev = self.comboBox_2.currentText()
        self.desc = "" 
        self.date = ("%s%s%s" % (str(date.today().year)[2:], str(date.today().month).zfill(2) , str(date.today().day).zfill(2)))      
        self.info = ""
        self._maketext(version = self.version, rev = self.rev, desc = self.desc)
        
        self.totalfiles = 0
        
    def _findgitpath(self, path):
        if (os.path.isdir(os.path.join(path,".git"))) is True:
            self.label_5.setStyleSheet('color: lightgreen; font: bold')                  
            self.label_5.setText("Valid")
            self._maketext(info = "11.12")
            self.pushButton.setEnabled(True)    
        else:
            self.label_5.setStyleSheet('color: red; font: bold')                  
            self.label_5.setText("Not Valid")
            self._maketext(info = "")
#            self.pushButton.setEnabled(False)
                                
    def _maketext(self,**argv):        
        self.version = argv.get('version') if argv.get('version') is not None else self.version
        self.rev = argv.get('rev') if argv.get('rev') is not None else self.rev
        self.desc = argv.get('desc') if argv.get('desc') is not None else self.desc
        self.info = argv.get('info') if argv.get('info') is not None else self.info
        
        self.label_3.setText("%s_%s_%s_%s_%s" % (self.version, self.rev, self.desc, self.date,self.info))        
        self.lineEdit_3.setText(os.path.abspath(os.path.join(self.lineEdit_2.displayText(),'../',self.label_3.text())))

    def __countfiles(self, src, exclude_dir):
        files = []
        exclude_dir = [os.path.join(src,x) for x in exclude_dir]
        for path, dirs, filenames in os.walk(src):    
            isignore = [path.find(exclude) >= 0 for exclude in exclude_dir]
            if not(True in isignore):
                files.extend(filenames)
            else:
                pass
        return len(files)
    
    def __count(self, src, dst,follow_symlinks=True):
        self.totalfiles += 1
    
    def __copy2(self,src, dst,follow_symlinks=True):
        shutil.copy2(src,dst)
        self.progressBar.setValue(self.progressBar.value()+1)   
        QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
        
    def _generate(self):
        self.totalfiles = len([x for x in glob.iglob(os.path.join(self.lineEdit_2.displayText(),'**/*.*'),recursive=True)])
        self.totalfiles = self.totalfiles - len([x for x in glob.iglob(os.path.join(self.lineEdit_2.displayText(),'.git/**/*.*'),recursive=True)])
        
        self.progressBar.setRange(0,self.totalfiles)        
        shutil.copytree(self.lineEdit_2.displayText(), self.lineEdit_3.displayText(),ignore=shutil.ignore_patterns('.git/**/*.*'),copy_function=self.__copy2)    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = DiaglogSample(Form)
    Form.show()
    sys.exit(app.exec_())

