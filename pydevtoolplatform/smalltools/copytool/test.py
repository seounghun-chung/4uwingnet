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
from pathlib import Path

import os  
import shutil
import glob


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
    
def __coptyree(self, src, dest,exclude_dir=[".git"], exclude_pattern = ["**/*.pyc"]):
    search =  __searchtree(1,src,exclude_dir=[".git","test"], exclude_pattern=["gui/*.ui","pydevtoolplatform/qtcode/*.py","**/__pycache__/*.pyc"])
    dir = sorted(list(x for x in search if x.is_dir() is True))
    files = sorted(list(x for x in search if x.is_file() is True))
    
    if not os.path.exists(dest):
        os.mkdir(dest)
    else:
        print("Already copied.... ")
        return
        
    for path in dir:
        dst = __changefilepath(1,src,dest,path)
        if not os.path.exists(dst):
            os.mkdir(dst)

    for path in files:        
        dst = __changefilepath(1,src,dest,path)
        shutil.copy('\\\\?\\'+str(path), dst)
        print("Success : ", path)

        
__coptyree(1,"C:\\Users\\seoung\\workspace\\pytool","C:\\Users\\seoung\\workspace\\test",exclude_dir=[".git","test"], exclude_pattern=["gui/*.ui","pydevtoolplatform/qtcode/*.py"])        
#a = __searchtree(1,"C:\\Users\\seoung\\workspace\\pytool","./",exclude_dir=[".git","test"], exclude_pattern=["gui/*.ui","pydevtoolplatform/qtcode/*.py"])

dir = sorted(list(x for x in a if x.is_dir() is True))
files = sorted(list(x for x in a if x.is_file() is True))
for x in a:
    print((x))
print("")
for x in dir:
    print((x))
print("")
#for x in files:
#    print(x)
