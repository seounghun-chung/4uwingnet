from PyQt5.QtWidgets import QWidget, QFileSystemModel, QHeaderView, QFileDialog, QMessageBox, QPlainTextEdit
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtCore import QSize, Qt
from PyQt5 import uic
from os.path import join
from console import console
from threading import Thread

import os

qtdesignpath = "./qtdesign"
form_class = uic.loadUiType(join(qtdesignpath,"sourceview.ui"))[0]

def ismodified(fn):
    """ if code view was changed, ask which the file save """
    def decorator(self, *args, **kwargs):
        if self.modfiedstate is True:
            msgBox = QMessageBox()
            msgBox.setText("The document has been modified.");
            msgBox.setInformativeText("Do you want to save your changes?");
            msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel);
            msgBox.setDefaultButton(QMessageBox.Save);        
            ret = msgBox.exec()

            if ret == QMessageBox.Save:
                ret = self._save_script()
                if ret != "":
                    return fn(self, *args, **kwargs)
                else:   # fail to save file
                    return
            elif ret == QMessageBox.Discard:    # not save
                return fn(self, *args, **kwargs)
            else:   # cancle
                return
        else:   # not modified, so then don't ask which file is saved.
            return fn(self, *args, **kwargs)
    return decorator

class SourceView(QWidget, form_class):
    def __init__(self, parent=None):
        super(SourceView, self).__init__(parent)
        self.setupUi(self)

        # private variable
        self.__currentpath = ""
        self.modfiedstate = False
        
        self._leftdefaultsize = 200
        self.splitter.setSizes([self._leftdefaultsize,(self.size().width()) - self._leftdefaultsize])
        self._PyQtSignalConnect = console.GetPyQtSignalFromConsole()
        
        # button icon
        self.pushButton.setFlat(True)
#        self.pushButton.setAutoFillBackground(True)
        self.pushButton.setIcon(QIcon(join(qtdesignpath,"save-30169.png")));
        self.pushButton_2.setFlat(True)
#        self.pushButton_2.setAutoFillBackground(True)
        self.pushButton_2.setIcon(QIcon(join(qtdesignpath,"iconmonstr-file-2.png")));
        self.pushButton_3.setFlat(True)
#        self.pushButton_3.setAutoFillBackground(True)
        self.pushButton_3.setIcon(QIcon(join(qtdesignpath,"zoomin.png")));
        self.pushButton_4.setFlat(True)
#        self.pushButton_4.setAutoFillBackground(True)
        self.pushButton_4.setIcon(QIcon(join(qtdesignpath,"zoomout.png")));
        self.pushButton_5.setFlat(True)
#        self.pushButton_5.setAutoFillBackground(True)
        self.pushButton_5.setIcon(QIcon(join(qtdesignpath,"run.png")));
        self.btnOpen.setFlat(True)
        self.btnOpen.setIcon(QIcon(join(qtdesignpath,"open.png")));
        
        
        # treeView model create
        self.model = QFileSystemModel()
        self.model.setNameFilters(["*.py"])
        
        # treeView setting
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.setRootPath('./'))
        self.treeView.setAnimated(True)
        self.treeView.setSortingEnabled(True)
        [self.treeView.hideColumn(ii) for ii in range(1,5)]
        self.treeView.header().setStretchLastSection(False)
        self.treeView.header().setSectionResizeMode(0,QHeaderView.Stretch)      

        # signal connect
        self.lineEdit.returnPressed.connect(self._change_root)
        self.treeView.activated.connect(lambda e : \
                        self._open_script(self.model.filePath(e)))
        self.pushButton_4.clicked.connect(lambda : self.plainTextEdit.zoomOut(2))
        self.pushButton_3.clicked.connect(lambda : self.plainTextEdit.zoomIn(2))
        self.pushButton.clicked.connect(lambda : self._save_script())
        self.pushButton_2.clicked.connect(lambda : self._new_script())       
        self.pushButton_5.clicked.connect(lambda : self._run_script())       
        self.btnOpen.clicked.connect(lambda : self._btnOpen_clicked())       
        
        self.fontComboBox.currentFontChanged.connect(lambda x : self.plainTextEdit.setFont(x))
        self.plainTextEdit.keyPressEvent = self._plainTextEdit_keyPressEvent            
        self.plainTextEdit.wheelEvent = self._plainTextEdit_wheelEvent            
        self.plainTextEdit.setAcceptDrops(True)
        self.plainTextEdit.dropEvent = lambda e : self._open_script(e.mimeData().urls()[0].toLocalFile())
        self.plainTextEdit.modificationChanged.connect(lambda x : self._change_modified_state(x))
        self._PyQtSignalConnect.script_run.connect(lambda : self.pushButton_5.animateClick())


    def _change_modified_state(self, param):
        self.modfiedstate = param
        
    def _btnOpen_clicked(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if (os.path.isfile(fileName) == True):
            self._open_script(fileName)
        else:
            pass    

    @ismodified    
    def _new_script(self):    
        self.plainTextEdit.clear()
        self._change_modified_state(False)
        
    def _save_script(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", self.__currentpath,
                                                  "Python Files (*.py)", options=options)
        if fileName == "":
            pass
        else:
            with open(fileName,"w") as f:
                f.write(self.plainTextEdit.toPlainText())
                self.__currentpath = fileName    # when re save occurs, it will be used in default path
            self._change_modified_state(False)
        return fileName
        
    @ismodified
    def _open_script(self, path):
        try:
            with open(path) as f:
                self.__currentpath = path
                self.plainTextEdit.clear();           
                self.plainTextEdit.setPlainText(f.read())         
        except UnicodeDecodeError as e:
            pass
        except PermissionError as e:
            pass
        
    def _change_root(self):
        text = self.lineEdit.displayText()
        self.treeView.setRootIndex(self.model.setRootPath(text))
        self.lineEdit.clear()      

    def _plainTextEdit_keyPressEvent(self, event):
        # this is monkey.......
        # how to change tab to 4 space ?
        if (event.key() == Qt.Key_Tab):
            self.plainTextEdit.insertPlainText(" "*4)
        else:
            QPlainTextEdit.keyPressEvent(self.plainTextEdit, event)
                
    def _plainTextEdit_wheelEvent(self, event):
        if (event.modifiers() & Qt.ControlModifier):
            self._plainTextEdit_zoom(event.angleDelta().y())
        else:
            QPlainTextEdit.wheelEvent(self.plainTextEdit, event)              

    def _plainTextEdit_zoom(self, delta):
        if delta < 0:
            self.plainTextEdit.zoomOut(2)
        elif delta > 0:
            self.plainTextEdit.zoomIn(2)            
                
                
    def _run_script(self):
        console.cexec(self.plainTextEdit.toPlainText(), isfile = True)

    