from PyQt5.QtWidgets import QWidget, QFileSystemModel, QHeaderView, QFileDialog, QMessageBox, QPlainTextEdit
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtCore import QSize, Qt
from PyQt5 import uic
from os.path import join

from threading import Thread

qtdesignpath = "./qtdesign"
form_class = uic.loadUiType(join(qtdesignpath,"sourceview.ui"))[0]


class SourceView(QWidget, form_class):
    def __init__(self, parent=None):
        super(SourceView, self).__init__(parent)
        self.setupUi(self)

        self._leftdefaultsize = 200
        self.splitter.setSizes([self._leftdefaultsize,(self.size().width()) - self._leftdefaultsize])

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
        
        self.fontComboBox.currentFontChanged.connect(lambda x : self.plainTextEdit.setFont(x))
        self.plainTextEdit.keyPressEvent = self._plainTextEdit_keyPressEvent            
        self.plainTextEdit.wheelEvent = self._plainTextEdit_wheelEvent            

        # private variable
        self.__currentpath = ""
        
    def _new_script(self):    
        reply = QMessageBox.question(self, 'Text clear', 
                 'Text will be cleared.\n\nNever restore it.\n\nIs really clear?', QMessageBox.Yes, QMessageBox.No)    
        if reply == QMessageBox.Yes:
            self.plainTextEdit.clear()
        else:
            pass
            
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
        try:
            exec(self.plainTextEdit.toPlainText(), globals())        
        except:  # (OverflowError, ValueError, SyntaxError, NameError):
            import sys, traceback
            info = sys.exc_info()
            backtrace = traceback.format_exception(*info)
            for line in backtrace:
                sys.stderr.write(line)

    