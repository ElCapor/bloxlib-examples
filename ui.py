from Instance import Instance
from Exploit import roblox

def GetDescendants(apple_item, instance):
    # Add the current instance to the tree widget
    instance_item = QTreeWidgetItem([instance.GetName()])
    apple_item.addChild(instance_item)
    
    # Recursively add the descendants of the current instance to the tree widget
    for child_instance in instance.GetChildren():
        GetDescendants(instance_item, child_instance)

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem

app = QApplication([])
tree_widget = QTreeWidget()
tree_widget.setHeaderLabels(['Fruits'])

# Create an instance of QIcon class and specify the path to the icon file
apple_icon = QIcon('icon.png')


# Create an instance of QTreeWidgetItem class and specify the text for the item
apple_item = QTreeWidgetItem(['Game'])
GetDescendants(apple_item, DModel)

# Set the icon for the item using setIcon() method
apple_item.setIcon(0, apple_icon)


# Add the item to the QTreeWidget using addChild() method
tree_widget.addTopLevelItem(apple_item)


tree_widget.show()
app.exec_()