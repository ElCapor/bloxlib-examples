from __future__ import annotations
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QToolBar, QAction, QStatusBar, QWidget, QHBoxLayout, QVBoxLayout, QTreeWidget, QTreeWidgetItem
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QObject
sys.path.append("Instance")
from bloxlib.Exploit import roblox
from bloxlib.instance import Instance, shared_instances
from bloxlib.Memory import GetDataModel
sys.path.append("icons")


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
        child.setIcon(0, QIcon("icons/instance/" + Instance.GetClassName(Instance(child.index))))
        self.signals.childAdded.emit(child)
    def removeChild(self, child: 'QTreeWidgetItem'):
        super().removeChild(child)
        self.signals.childRemoved.emit(child)

    def childNew(self, child : IndexedTreeWidgetItem):
        local_instance = Instance(child.index)
        child_list = roblox.Program.read_int(local_instance.getAddress() + 0x30)
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
    def __controls(self):
        self.toolbar = ExplorerToolBar("MainToolbar")

        self.tree_widget = ExplorerTree()
        self.tree_widget.setHeaderLabels(['Instances'])

        root_icon = QIcon('icons/instance/WorldModel.png')
        root_game = IndexedTreeWidgetItem(self.DataModel.getAddress(),['Game'])
        root_game.setChildIndicatorPolicy(IndexedTreeWidgetItem.ChildIndicatorPolicy.ShowIndicator) # to allow us to expand it
        root_game.setIcon(0, root_icon)
        self.tree_widget.addTopLevelItem(root_game)
        
    def __layout(self):
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.tree_widget)
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
