# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test2.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QEventLoop
from PyQt5.QtWidgets import QApplication, QFileDialog

from copytoolui import Ui_Form
from datetime import date
from pathlib import Path

import os  
import shutil
import configparser
import ast

class DiaglogSample(Ui_Form):
    def __init__(self, *argv):
        super().setupUi(*argv)
        
#        self.comboBox.currentTextChanged.connect(lambda x : self._maketext(version = x))
#        self.comboBox_2.currentTextChanged.connect(lambda x : self._maketext(rev = x))
#        self.lineEdit.textChanged.connect(lambda x : self._maketext( desc = x ))
#        self.lineEdit_2.textChanged.connect(lambda x: self._findgitpath( x ) )
        self.pushButton_4.clicked.connect(lambda : self._btn_copytree())
        self.pushButton_3.clicked.connect(lambda : self._btn_loadexcludeconfig())
        self.pushButton_2.clicked.connect(lambda : self.lineEdit_2.setText(QFileDialog.getExistingDirectory(None, "Set src directory")))
        self.pushButton.clicked.connect(lambda : self.lineEdit.setText(QFileDialog.getExistingDirectory(None, "Set dest directory")))

        self.exclude_dir = list()
        self.exclude_pattern = list()   
        
        config = configparser.ConfigParser()
        config.read("default.ini")
        self.exclude_dir = config.get("default","exclude_dir").split('\n')
        self.exclude_pattern = config.get("default","exclude_pattern").split('\n')    
        
        self.listWidget.addItems(self.exclude_dir)
        self.listWidget.addItems(self.exclude_pattern)
        
    def _btn_loadexcludeconfig(self):
        filename, _filter = QtWidgets.QFileDialog.getOpenFileName(None, "Open exclude pattern ini", '.', "(*.ini)")
        if (os.path.isfile(filename) == True):
            self.listWidget.clear()
            config = configparser.ConfigParser()
            config.read(filename)
            self.exclude_dir = config.get("default","exclude_dir").split('\n')
            self.exclude_pattern = config.get("default","exclude_pattern").split('\n')    
            
            self.listWidget.addItems(self.exclude_dir)
            self.listWidget.addItems(self.exclude_pattern)
        else:
            self.listWidget.clear()
            self.exclude_dir = list()
            self.exclude_pattern = list() 
            pass        

    def _btn_copytree(self):
        src = str(Path(self.lineEdit.displayText()))
        dest = str(Path(self.lineEdit_2.displayText()))
        
        search = self.__searchtree(src,exclude_dir=self.exclude_dir, exclude_pattern = self.exclude_pattern)
        self.progressBar.setRange(0,len(search))  
        self.progressBar.setValue(0)        
        self.__coptyree(src,dest,exclude_dir=self.exclude_dir, exclude_pattern = self.exclude_pattern, search=search,callback=self.progressBar.setValue)        
        
    def __searchtree(self, src, exclude_dir=[".git"], exclude_pattern = ["**/*.pyc"]):
        # search to pattern for excluding
        o = list()
        for ex in exclude_pattern:
            o += Path(src).glob(ex)

        all_files_in_src = set(Path(src).glob("**/*")) -  set(o)
        all_exclude_files_in_src = list(Path(src,ex).glob("**/*") for ex in exclude_dir)

        for x in all_exclude_files_in_src:
            all_files_in_src = set(all_files_in_src) - set(x)

        # remove exclude dir
        all_files_in_src = set(all_files_in_src) - set(Path(src,ex) for ex in exclude_dir)
        return all_files_in_src

    def __changefilepath(self, src, dest, filepath):
        return Path(str(filepath).replace(src, dest))
        
    def __coptyree(self, src, dest, exclude_dir=[".git"], exclude_pattern = ["**/*.pyc"], search=None, callback = None):
        count = 0
        callback = (lambda x : None) if callback is None else callback
        
        if search is None:
            search =  self.__searchtree(src,exclude_dir=exclude_dir, exclude_pattern=exclude_pattern)
            
        dir = sorted(list(x for x in search if x.is_dir() is True))
        files = sorted(list(x for x in search if x.is_file() is True))
        
        if not os.path.exists(dest):
            os.mkdir(dest)
        else:
            shutil.rmtree(dest)
            os.mkdir(dest)
            
        for path in dir:
            dst = self.__changefilepath(src,dest,path)
            if not os.path.exists(dst):
                os.mkdir(dst)
                count += 1                
                callback(count)

        for path in files:        
            dst = self.__changefilepath(src,dest,path)
            shutil.copy(path, dst)
            count += 1                
            callback(count)            
            print("Success : ", path)
            
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = DiaglogSample(Form)
    Form.show()
    sys.exit(app.exec_())

