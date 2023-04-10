from __future__ import annotations
import sys
import os
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,QMenu,QMessageBox,
    QLabel, QToolBar, QAction, QStatusBar, QWidget, QHBoxLayout, QVBoxLayout, QTreeWidget, QTreeWidgetItem
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QVariant
sys.path.append('QT/QtProperty')
sys.path.append('QT/libqt5')

from pyqtcore import QList
from qtvariantproperty import QtVariantEditorFactory, QtVariantPropertyManager
from qttreepropertybrowser import QtTreePropertyBrowser

from bloxlib.Exploit import roblox
from bloxlib.instance import Instance
from bloxlib.Memory import GetDataModel
sys.path.append("icons")
#e
def addToClipBoard(text):
    command = 'echo | set /p nul=' + text.strip() + '| clip'
    os.system(command)

class ExplorerToolBar(QToolBar):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupButtons()
        
    def setupButtons(self):
        self.save_button = QAction(QIcon("icons/ui/Save.png"),"Save", self)
        self.save_button.setStatusTip("Save current hierarchy to a file")
        self.save_button.triggered.connect(self.save_button_action)
        self.addAction(self.save_button)

        self.settings_btn = QAction(QIcon("icons/ui/settings2.png"), "Settings", self)
        self.settings_btn.setStatusTip("Program Settings")
        self.settings_btn.triggered.connect(self.settings_btn_action)
        self.addAction(self.settings_btn)

    def save_button_action(self, s):
        print("Save Button Clicked ! ")
    
    def settings_btn_action(self, s):
        print("Settings clicked")


class IndexedSignals(QObject):
    childAdded = pyqtSignal(object)
    childRemoved = pyqtSignal(object)


class IndexedTreeWidgetItem(QTreeWidgetItem):
    
    def __init__(self, index=0, parent=None):
        self.index = index # instance address
        self.signals = IndexedSignals() 
        self.signals.childAdded.connect(self.childNew)
        super().__init__(parent)
    
    def addChild(self, child):
        super(IndexedTreeWidgetItem, self).addChild(child)
        child.setIcon(0, QIcon("icons/instance/" + Instance(child.index).GetClassName()))
        self.signals.childAdded.emit(child)
    def removeChild(self, child: 'QTreeWidgetItem'):
        super().removeChild(child)
        self.signals.childRemoved.emit(child)

    def childNew(self, child : IndexedTreeWidgetItem):
        local_instance = Instance(child.index)
        child_list = roblox.Program.read_int(local_instance.getAddress() + 0x2C) # 0x30 don't work anymore, roblox edited offset?
        if child_list == 0:
            child.setChildIndicatorPolicy(IndexedTreeWidgetItem.ChildIndicatorPolicy.DontShowIndicator)
        else:
            child.setChildIndicatorPolicy(IndexedTreeWidgetItem.ChildIndicatorPolicy.ShowIndicator)





class ExplorerTree(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.itemExpanded.connect(self.expand_item)
        self.itemCollapsed.connect(self.collapse_item)
        

    def expand_item(self, item : IndexedTreeWidgetItem):
        if item.childCount() == 0:
            local_instance = Instance(item.index)
            for child in local_instance.GetChildren():
                item.addChild(IndexedTreeWidgetItem(child.getAddress(), [child.GetName()]))
                
    def collapse_item(self, item : IndexedTreeWidgetItem):
        for i in reversed(range(item.childCount())): # https://stackoverflow.com/questions/38098811/how-to-remove-children-of-qtreewidgetitem
            item.removeChild(item.child(i))
    
    
class FormWidget(QWidget):

    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
        self.datamodel()
        self.__controls()
        self.__layout()

    def datamodel(self):
        self.DataModel = Instance(GetDataModel())

    def menuContextTree(self, point):
        # Infos about the node selected.
        index = self.tree_widget.indexAt(point)

        if not index.isValid():
            return

        item = self.tree_widget.itemAt(point)
        name = item.text(0)  # The text of the node.
        self.contextItem = item
        # We build the menu.
        menu = QMenu()
        action = menu.addAction("Selected : " + name)
        menu.addSeparator()
        copy_path_action = menu.addAction("Copy Path")
        clone_action = menu.addAction("Clone")
        destroy_action = menu.addAction("Destroy")
        copy_path_action.triggered.connect(self.copy_path)
        destroy_action.triggered.connect(self.destroy_action)

        menu.exec_(self.tree_widget.mapToGlobal(point))
        
    def copy_path(self, s):
        texts = []
        current_item = self.contextItem
        while current_item is not None:
            texts.append(current_item.text(0))
            current_item = current_item.parent()
        texts.reverse()
        path = ""
        path += "Game"
        texts.pop()
        for elem in texts:
            path += f'.FindFirstChild("{elem}")'
        addToClipBoard(path)
    def destroy_action(self, s):
        local_instance = Instance(self.contextItem.index)
        local_instance.Destroy()
        self.contextItem.parent().removeChild(self.contextItem)


    def item_clicked(self, item : IndexedTreeWidgetItem):
        self.current_item = item
        self.selected_parent = 0
        if item.index != 0:
            local_instance = Instance(item.index)
            self.NameView.setValue(local_instance.GetName())
            self.ClassView.setValue(local_instance.GetClassName())
            self.AddressView.setValue(roblox.d2h(local_instance.getAddress()))
        else:
            self.NameView.setValue("None")
            self.ClassView.setValue("None")
            self.AddressView.setValue("None")

    def __controls(self):
        self.toolbar = ExplorerToolBar("MainToolbar")

        self.tree_widget = ExplorerTree()
        self.tree_widget.setHeaderLabels(['Instances'])
        self.tree_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self.menuContextTree)

        root_icon = QIcon('icons/instance/WorldModel.png')
        root_game = IndexedTreeWidgetItem(self.DataModel.getAddress(),['Game'])
        root_game.setChildIndicatorPolicy(IndexedTreeWidgetItem.ChildIndicatorPolicy.ShowIndicator) # to allow us to expand it
        root_game.setIcon(0, root_icon)
        self.tree_widget.addTopLevelItem(root_game)
        self.tree_widget.itemClicked.connect(self.item_clicked)

        ### Property Editor part
        self.variantManager = QtVariantPropertyManager()
        self.topItem = self.variantManager.addProperty(QtVariantPropertyManager.groupTypeId(), "Property Edit")
        self.NameView = self.variantManager.addProperty(QVariant.String, "Name")
        self.NameView.setAttribute("readOnly", True)
        self.ClassView = self.variantManager.addProperty(QVariant.String, "Class")
        self.ClassView.setAttribute("readOnly", True)
        self.AddressView = self.variantManager.addProperty(QVariant.String, "Address")
        self.AddressView.setAttribute("readOnly", True)

        self.topItem.addSubProperty(self.NameView)
        self.topItem.addSubProperty(self.ClassView)
        self.topItem.addSubProperty(self.AddressView)

        self.variantFactory = QtVariantEditorFactory()

        self.variantEditor = QtTreePropertyBrowser()
        self.variantEditor.setFactoryForManager(self.variantManager, self.variantFactory)
        self.variantEditor.addProperty(self.topItem)
        self.variantEditor.setPropertiesWithoutValueMarked(True)
        self.variantEditor.setRootIsDecorated(False)
        self.variantEditor.showMaximized()

    def __layout(self):
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.tree_widget)
        self.vbox.addWidget(self.variantEditor)
        self.setLayout(self.vbox)


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("External Explorer")
        self.setWindowIcon(QIcon("icons/instance/Model.png"))
        self.form_widget = FormWidget(self)
        _widget = QWidget()
        _layout = QVBoxLayout(_widget)
        _layout.addWidget(self.form_widget)
        self.setCentralWidget(_widget)
        self.addToolBar(self.form_widget.toolbar)

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
