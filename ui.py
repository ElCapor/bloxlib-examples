from Instance import Instance
from Exploit import roblox
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QMainWindow, QWidget, QVBoxLayout,QLabel, QLineEdit, QHBoxLayout, QComboBox
from Memory import GetDataModel
def GetDescendants(apple_item, instance):
    # Add the current instance to the tree widget
    instance_item = QTreeWidgetItem([instance.GetName()])
    apple_item.addChild(instance_item)
    
    # Recursively add the descendants of the current instance to the tree widget
    for child_instance in instance.GetChildren():
        GetDescendants(instance_item, child_instance)



class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.form_widget = FormWidget(self)
        _widget = QWidget()
        _layout = QVBoxLayout(_widget)
        _layout.addWidget(self.form_widget)
        self.setCentralWidget(_widget)



class FormWidget(QWidget):

    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
        self.datamodel()
        self.__controls()
        self.__layout()

    def datamodel(self):
        self.DataModel = Instance(GetDataModel())
    def __controls(self):
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(['Fruits'])

        # Create an instance of QIcon class and specify the path to the icon file
        apple_icon = QIcon('icon.png')


        # Create an instance of QTreeWidgetItem class and specify the text for the item
        apple_item = QTreeWidgetItem(['Game'])
        #GetDescendants(apple_item, DModel)

        # Set the icon for the item using setIcon() method
        apple_item.setIcon(0, apple_icon)
        GetDescendants(apple_item,self.DataModel)

        # Add the item to the QTreeWidget using addChild() method
        self.tree_widget.addTopLevelItem(apple_item)
        
    def __layout(self):
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.tree_widget)
        self.setLayout(self.vbox)

app = QApplication([])


win = MainWindow()
win.show()
app.exec_()