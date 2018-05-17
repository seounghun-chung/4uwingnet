from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import uic
from feature import consolemanager
from feature.command import Command

import os
import traceback

qtDesignerPath = os.path.dirname(__file__)
form_class = uic.loadUiType(os.path.join(qtDesignerPath, "MainWindows.ui"))[0]


class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.graphicsView.dragEnterEvent = self._lineEdit_dragEnterEvent
        self.graphicsView.dragMoveEvent = self._lineEdit_dropEvent

        self.lineEdit.returnPressed.connect(self._lineEdit_returnPressed)
        self.lineEdit.dragEnterEvent = self._lineEdit_dragEnterEvent
        self.lineEdit.dropEvent = self._lineEdit_dropEvent

        # default dock is closed
        self.dockWidget.visibilityChanged.connect(self._dockWidget_visible_changed)
        self.dockWidget.hide()
        self.dockWidgetContents.stdout_redirect(False)

        self.actionRun_script.triggered.connect(self._actionOpen_triggered_connect)

        # set command class instance to other windows
        self.ClassCommand = Command()
        self.widget_2.getCommandInstance(self.ClassCommand) # connect command windows
        consolemanager.connect(self.ClassCommand)   # connect console consolemanager
        consolemanager.connect(self.dockWidgetContents) # connect console windows to consolemanager

#        self.tabWidget.removeTab(2)

    def _actionOpen_triggered_connect(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if (os.path.isfile(fileName) == True):
            consolemanager.cexec(fileName)
        else:
            pass

    def _dockWidget_visible_changed(self, e):
        if (e is True):
            self.dockWidgetContents.stdout_redirect(True)
        else:
            self.dockWidgetContents.stdout_redirect(False)

    def _lineEdit_returnPressed(self):
        text = self.lineEdit.displayText()
        try:
            self.graphicsView.setPhoto(QtGui.QPixmap(text))
        except:
            traceback.print_exc()

    def _lineEdit_dragEnterEvent(self, e):
        if (e.mimeData().hasUrls()):
            e.acceptProposedAction()

    def _lineEdit_dropEvent(self, e):
        self.lineEdit.setText(e.mimeData().urls()[0].toLocalFile())
        self.graphicsView.setPhoto(QtGui.QPixmap(e.mimeData().urls()[0].toLocalFile()))
