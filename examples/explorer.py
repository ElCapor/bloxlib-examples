import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QToolBar, QAction, QStatusBar, QWidget, QHBoxLayout, QVBoxLayout, QTreeWidget, QTreeWidgetItem
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
sys.path.append("Instance")
from Exploit import roblox
from Instance import Instance
from Memory import GetDataModel
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



class IndexedTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, index=0, parent=None):
        self.index = index # instance address
        super().__init__(parent)
    

class ExplorerTree(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.itemDoubleClicked.connect(self.double_click)
    
    def double_click(self, item, column):
        print("Item double click at " + item.index)
        local_instance = Instance(item.index)
    
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

        # Create an instance of QIcon class and specify the path to the icon file
        root_icon = QIcon('icons/instance/WorldModel.png')


        # Create an instance of QTreeWidgetItem class and specify the text for the item
        root_game = IndexedTreeWidgetItem(self.DataModel.getAddress(),['Game'])
        #GetDescendants(apple_item, DModel)

        # Set the icon for the item using setIcon() method
        root_game.setIcon(0, root_icon)

        # Add the item to the QTreeWidget using addChild() method
        self.tree_widget.addTopLevelItem(root_game)
        
    def __layout(self):
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.tree_widget)
        self.setLayout(self.vbox)


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("My Awesome App")
        self.form_widget = FormWidget(self)
        _widget = QWidget()
        _layout = QVBoxLayout(_widget)
        _layout.addWidget(self.form_widget)
        self.setCentralWidget(_widget)
        self.addToolBar(self.form_widget.toolbar)
        
        

    def onMyToolBarButtonClick(self, s):
        print("click", s)

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()