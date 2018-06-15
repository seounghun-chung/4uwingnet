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

    def _generate(self):
        exclude_path = ['.git', 'pydevtoolplatform/console']
        
        self.totalfiles = self.__count(self.lineEdit_2.displayText(),exclude_path=exclude_path)
        self.progressBar.setRange(0,self.totalfiles)  
        self.progressBar.setValue(0)
        
        self.__copytree(self.lineEdit_2.displayText(), self.lineEdit_3.displayText(),exclude_path=exclude_path)        
        
    def __isexclude(self, path, abs_exclude_path):
        """ it must require abs path for checking which there are """
        for e in abs_exclude_path:
            if (path.find(e) == 0):
                return True
        return False
        
    def __count(self, root_src_dir, exclude_path = ['.git']):
        """ the total count of files is used for progress bar """
        _files = list()
        for src_dir, dirs, files in os.walk(root_src_dir):
            if self.__isexclude(src_dir, [os.path.abspath(os.path.join(root_src_dir,x)) for x in exclude_path]) is True:
                continue
            else:
                _files.extend(files)
        return len(_files)
        
    def __copytree(self, root_src_dir, root_target_dir, exclude_path = ['.git'], operation = 'copy'):
        
        # if the folder aready exists, remove it
        if os.path.exists(root_target_dir):
            shutil.rmtree(root_target_dir)
            
        for src_dir, dirs, files in os.walk(root_src_dir):
            dst_dir = src_dir.replace(root_src_dir, root_target_dir)
            
            if self.__isexclude(src_dir, [os.path.abspath(os.path.join(root_src_dir,x)) for x in exclude_path]) is True:
                continue

            if not os.path.exists(dst_dir):
                os.mkdir(dst_dir)
                
            for file_ in files:
                src_file = os.path.join(src_dir, file_)
                dst_file = os.path.join(dst_dir, file_)
                    
                # '\\\\?\\' is work around caused by windows bugs
                if operation is 'copy':
                    shutil.copy('\\\\?\\' + src_file, dst_dir)
                elif operation is 'move':
                    shutil.move('\\\\?\\' + src_file, dst_dir)
                    
                self.progressBar.setValue(self.progressBar.value()+1)   
                QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
                
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = DiaglogSample(Form)
    Form.show()
    sys.exit(app.exec_())

