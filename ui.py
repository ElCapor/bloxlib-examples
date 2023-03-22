from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem

app = QApplication([])
tree_widget = QTreeWidget()
tree_widget.setHeaderLabels(['Fruits'])

# Create an instance of QIcon class and specify the path to the icon file
apple_icon = QIcon('icon.png')
orange_icon = QIcon('folder.png')

# Create an instance of QTreeWidgetItem class and specify the text for the item
apple_item = QTreeWidgetItem(['Apple'])
orange_item = QTreeWidgetItem(['Orange'])

# Set the icon for the item using setIcon() method
apple_item.setIcon(0, apple_icon)
orange_item.setIcon(0, orange_icon)

# Add the item to the QTreeWidget using addChild() method
tree_widget.addTopLevelItem(apple_item)
tree_widget.addTopLevelItem(orange_item)

tree_widget.show()
app.exec_()
