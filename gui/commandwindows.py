from feature import consolemanager

from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
import os
import xml.etree.ElementTree
import xmltodict

#logging.basicConfig(level = logging.DEBUG)

qtDesignerPath = os.path.dirname(__file__)
xmlconfigPath = os.path.join(os.path.dirname(__file__),"../config/")

form_class = uic.loadUiType(os.path.join(qtDesignerPath, "CommandWindows.ui"))[0]

styleSheet = """
QTreeView {
    alternate-background-color: #f6fafb;
    background: #e8f4fc;
}
"""
class Model(QStandardItemModel):
    def __init__(self, data):
        QStandardItemModel.__init__(self)
        with open(os.path.join(xmlconfigPath, 'load.xml')) as fd:
            doc = xmltodict.parse(fd.read())
        
        for mainattr in doc["main"]:    # find command type (routine, readidentifier, ...)
            parentitem = QStandardItem(mainattr)

            for subattr in doc["main"][mainattr]:   # select one of attr in routine / session ..
                for eachofitem in doc["main"][mainattr][subattr]:   # find all data in attr
                    childitem = QStandardItem(eachofitem["name"])
                    childitem.setToolTip(eachofitem["desc"])
                    childitem.setData(eachofitem)
                    parentitem.appendRow(childitem)
            self.appendRow(parentitem)

        d = data[0]  # Fruit
        item = QStandardItem(d["type"])
        child = QStandardItem(d["objects"][0])  # Apple
        child.setToolTip("hello python")
        child.setData(3)
        item.appendRow(child)
        child = QStandardItem(d["objects"][1])  # Banana
        item.appendRow(child)
#        self.setItem(0, 0, item)
        self.appendRow(item)
        d = data[1]  # Vegetable
        item = QStandardItem(d["type"])
        child = QStandardItem(d["objects"][0])  # Carrot
        item.appendRow(child)
        child = QStandardItem(d["objects"][1])  # Tomato
        item.appendRow(child)
        self.appendRow(item)

    def _add_standard_item(self, s, f):
        for i in f.findall(s):
            item = QStandardItem(i.get('name'))
            for j in i.findall('attr'):
                child = QStandardItem(j.find('type').get('name'))
                child.setToolTip(j.find('desc').text)
                data = [j.find('type').get('command'), j.find('type').get('length')]
                child.setData(data)
#                child.setData(bytes.fromhex(j.find('type').get('command')))
                item.appendRow(child)
            self.appendRow(item)


class CommandWindows(QWidget, form_class):
    def __init__(self, parent = None):
        super(CommandWindows, self).__init__(parent)
        self.setupUi(self)

        self.data = [
            {"type": "Fruit", "objects": ["Apple", "Banana"]},
            {"type": "Vegetable", "objects": ["Carrot", "Tomato"]},
        ]
        self.model = Model(self.data)
        self.treeView.reset()
        self.treeView.setModel(self.model)
        self.treeView.expandAll()
        self.treeView.setAlternatingRowColors(True)
        self.treeView.setStyleSheet(styleSheet)

        self.treeView.activated.connect(self.dummy) # activated -> pressed @fixme pyqt bug fix
#        self.treeView.pressed.connect(self.treeView_itemSelectionChanged_connect)
        self.treeView.selectionModel().currentChanged.connect(self.treeView_itemSelectionChanged_connect)  # self.selectionChanged

#        self.treeView.itemSelectionChanged.connect()
#        self.treeView.returnPressed.connect(self.dummy)

    def treeView_itemSelectionChanged_connect(self, e):
        item = self.model.itemFromIndex(e)
        try:    # parents node don't display information
            self.label.setText("Command Name : " + item.text())
            self.label_2.setText("Command Info : " + (item.data()["command"]))
            self.label_3.setText("Command Length : " + (item.data()["length"]))
            self.label_4.setText("Command Desc : " + str(item.toolTip()))
        except TypeError as e:
            self.label.setText("Command Name : ")
            self.label_2.setText("Command Info : ")
            self.label_3.setText("Command Length : ")
            self.label_4.setText("Command Desc : ")

#    def keyPressEvent(self, event):
#        if event.key() == (QtCore.Qt.Key_Return):
#            self.dummy(self.treeView.currentIndex())

    def dummy(self,e):
        item = self.model.itemFromIndex(e)
        if item.hasChildren() is False:
            print("%s : " % item.text(), end="")
            print(item.data())
