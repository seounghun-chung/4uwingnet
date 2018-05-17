from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from feature.testmanager import TestManager
import os
from PyQt5 import uic

qtDesignerPath = os.path.dirname(__file__)
form_class = uic.loadUiType(os.path.join(qtDesignerPath, "TestView.ui"))[0]

class unittestRunThread(QThread):
    def __init__(self, target):
        QThread.__init__(self)
        self.cond = QWaitCondition()
        self.mutex = QMutex()
        self.target = target

    def run(self):
        self.target()


class TestView(QWidget, form_class):
    def __init__(self, parent = None):
        super(TestView, self).__init__(parent)
        self.setupUi(self)

        self.completeCount = 0
        self.failCount = 0
        self.t1 = None

        # qt interface connect
        self.utmanager = TestManager(self)  # for connecting callback

        self.listWidget.setAcceptDrops(True)
        self.listWidget.setDragEnabled(True)
        self.listWidget.keyPressEvent = self.listWidget_keyPressEvent
        self.listWidget.dragEnterEvent = self._listWidget_dragEnterEvent
        self.listWidget.dropEvent = self._listWidget_dropEvent
        self.listWidget_2.clicked.connect(self.listWidget_2_clicked)


        self.pushButton.clicked.connect(self.pushButton_click)  # Run button
        self.pushButton.setShortcut("Alt+r")
        self.pushButton_2.clicked.connect(self.pushButton_2_click)  # Load button
        self.pushButton_2.setShortcut("Alt+l")

    def _listWidget_dragEnterEvent(self, e):
        if (e.mimeData().hasUrls()):
            e.acceptProposedAction()

    def _listWidget_dropEvent(self, e):
        for ii in e.mimeData().urls()[0].toLocalFile():
            print(ii)


    def pushButton_click(self):  # run button click
        selectListItems = self.listWidget.selectedItems()
        if len(selectListItems) == 0:  # all item will be executed
            for index in range(0, self.listWidget.count()):
                item = self.listWidget.item(index)
                self.listWidget_item_preexecuted(item)
            self.listWidget.clear()
        else:  # selected item will be executed
            for item in selectListItems:
                self.listWidget.takeItem(self.listWidget.row(item))
                self.listWidget_item_preexecuted(item)
        self.listWidget_item_executed()

    def pushButton_2_click(self):  # load button click
        filter = "python script (*.py);;xml script (*.xml)"
        file_name = QFileDialog()
        file_name.setFileMode(QFileDialog.ExistingFiles)
        names = file_name.getOpenFileNames(self, "Load files", "./", filter)

        # load script and parse unittest in here
        for script in names[0]:
            self.unittest_parse(script)

    def unittest_parse(self, path):
        # parse unittest list for running
        ret = self.listWidget_append(path)  # check which duplicated items is existed
        if ret is True:
            self.utmanager.addTests(path)
        else:
            pass

    def listWidget_item_preexecuted(self, item):
        # will be executed in multiprocess?
        if type(item) is str:
            self.utmanager.prepareTests(item)
        else:
            self.utmanager.prepareTests(item.text())

    def listWidget_item_executed(self):
        self.t1 = unittestRunThread(self.utmanager.run)
        self.t1.start()

    def listWidget_item_delete(self, item):
        self.utmanager.delTests(item.text())

    def listWidget_append(self, label):
        s = self.listWidget.findItems(label, Qt.MatchContains)
        if len(s) > 0:
            return False
        else:
            self.listWidget.addItem(label)
            return True

    def listWidget_keyPressEvent(self, event):
        QListWidget.keyPressEvent(self.listWidget, event)

        # user new event
        if event.key() in (Qt.Key_Backspace, Qt.Key_Delete):  # delete tests
            selectListItems = self.listWidget.selectedItems()
            for item in selectListItems:
                t = self.listWidget.takeItem(self.listWidget.row(item))
                self.listWidget_item_delete(t)
        elif event.key() in (Qt.Key_Return, Qt.Key_P):  # execute tests
            selectListItems = self.listWidget.selectedItems()
            for item in selectListItems:
                t = self.listWidget.takeItem(self.listWidget.row(item))
                self.listWidget_item_preexecuted(t)
            self.listWidget_item_executed()
        else:
            pass

    def dummy(self):
        print("test")

    def listWidget_2_clicked(self):
        s = self.listWidget_2.currentItem()
        if (len(s.toolTip())) > 0:  # fail / error case
            msgBox = QMessageBox()
            msgBox.setWindowTitle(s.text())
            msgBox.setText(s.toolTip())
            msgBox.exec_()
            pass
        else:
            pass

    def label_2_countup(self):
        self.completeCount += 1;
        self.label_2.setText("Completed Test : %d" % (self.completeCount))

    def label_3_countup(self):
        self.failCount += 1;
        self.label_3.setText("Fail Test : %d" % (self.failCount))

    # GUI unittest report callback functions
    def notifyTestFailed(self, test, err):
        "Override to indicate that a test has just failed"
        self.listWidget_2.addItem(str(test))

        # set colot at last item index from total item count
        currentItem = self.listWidget_2.item(self.listWidget_2.count() - 1)
        currentItem.setForeground(QColor("red"))
        currentItem.setToolTip(err)
        self.label_3_countup()

    def notifyTestErrored(self, test, err):
        "Override to indicate that a test has just errored"
        pass

    def notifyTestSkipped(self, test, reason):
        "Override to indicate that test was skipped"
        pass

    def notifyTestFailedExpectedly(self, test, err):
        "Override to indicate that test has just failed expectedly"
        pass

    def notifyTestStarted(self, test):
        "Override to indicate that a test is about to run"
        pass

    def notifyTestFinished(self, test):
        """Override to indicate that a test has finished (it may already have
           failed or errored)"""
        self.listWidget_2.item(self.listWidget_2.count() - 1).setText(test)
        self.label_2_countup()

        pass

    def notifyTestSuccessed(self, test):
        self.listWidget_2.addItem(str(test))
        self.listWidget_2.item(self.listWidget_2.count() - 1).setForeground(QColor("green"))