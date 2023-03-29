# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2013 Digia Plc and/or its subsidiary(-ies).
## Contact: http://www.qt-project.org/legal
##
## This file is part of the Qt Solutions component.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Digia Plc and its Subsidiary(-ies) nor the names
##     of its contributors may be used to endorse or promote products derived
##     from this software without specific prior written permission.
##
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
##
## $QT_END_LICENSE$
##
#############################################################################

import sys

sys.path.append('QtProperty')
sys.path.append('libqt5')

from PyQt5.QtWidgets import QApplication, QLineEdit
from PyQt5.QtCore import (
    QTranslator, 
    QVariant, 
    QDate, 
    QTime, 
    QDateTime, 
    Qt, 
    QLocale, 
    QPoint, 
    QPointF, 
    QSize, 
    QSizeF, 
    QRect, 
    QRectF
    )

from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QMenu, QApplication, QTreeWidget, QTreeWidgetItem, QMainWindow, QWidget, QVBoxLayout,QLabel, QLineEdit, QHBoxLayout, QComboBox

from pyqtcore import QList
from qtvariantproperty import QtVariantEditorFactory, QtVariantPropertyManager
from qttreepropertybrowser import QtTreePropertyBrowser
from Instance import Instance, GetClassName
from Exploit import roblox
from Memory import GetDataModel
from PyQt5.QtCore import pyqtSlot, Qt
class IndexedTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, index=0, parent=None):
        super().__init__(parent)
        self.index = index


class RightClickTreeWidget(QTreeWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

    def mousePressEvent (self, event):
        if event.button() == Qt.RightButton:
            print("right click !")
        QTreeWidget.mousePressEvent(self, event)

def GetDescendants(apple_item, instance):
    # Add the current instance to the tree widget
    instance_item = IndexedTreeWidgetItem(instance.getAddress(),[instance.GetName()])
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
        self.viewData = {
            "Name":"None",
            "Address":"None"
        }


    def datamodel(self):
        self.DataModel = Instance(GetDataModel())
    def menuContextTree(self, point):
        # Infos about the node selected.
        index = self.tree_widget.indexAt(point)

        if not index.isValid():
            return

        item = self.tree_widget.itemAt(point)
        name = item.text(0)  # The text of the node.

        # We build the menu.
        menu = QMenu()
        action = menu.addAction("Souris au-dessus de")
        action = menu.addAction(name)
        menu.addSeparator()
        action_1 = menu.addAction("Choix 1")
        action_2 = menu.addAction("Choix 2")
        action_3 = menu.addAction("Choix 3")


        menu.exec_(self.tree_widget.mapToGlobal(point))

    @pyqtSlot(QTreeWidgetItem, int)
    def on_item_clicked(self, item, column):
        print(item.index)
        if item.index != 0:
            for added in self.addedPropList:
                self.topItem.removeSubProperty(added)
                self.addedPropList.remove(added)
            local_instance = Instance(item.index)
            self.NameView.setValue(local_instance.GetName())
            self.ClassView.setValue(GetClassName(local_instance))
            self.AddressView.setValue(roblox.d2h(local_instance.getAddress()))
            self.propDescriptorEnumList.clear()
            for prop in local_instance.GetPropertyDescriptors():
                self.propDescriptorEnumList.append(prop.GetName())
                new_item = self.variantManager.addProperty(QVariant.String, prop.GetName())
                new_item.setAttribute("readOnly", True)
                new_item.setValue("Not Implemented Yet")
                self.addedPropList.append(new_item)
            for added in self.addedPropList:
                self.topItem.addSubProperty(added)
                
            self.propDescriptorEnum.setValue(1)
            self.propDescriptorEnum.setAttribute("enumNames", self.propDescriptorEnumList)
        else:
            self.NameView.setValue("None")
            self.ClassView.setValue("None")
            self.AddressView.setValue("None")

            self.propDescriptorEnumList.clear()
            self.propDescriptorEnum.setAttribute("enumNames", self.propDescriptorEnumList)
            for added in self.addedPropList:
                self.topItem.removeSubProperty(added)
                self.addedPropList.remove(added)
    def __controls(self):
        self.tree_widget = RightClickTreeWidget()
        self.tree_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self.menuContextTree)
        self.tree_widget.itemClicked.connect(self.on_item_clicked)
        self.tree_widget.setHeaderLabels(['Fruits'])
        #apple_icon = QIcon('icon.png')
        apple_item = IndexedTreeWidgetItem(0,['Game'])
        #apple_item.setIcon(0, apple_icon)
        GetDescendants(apple_item,self.DataModel)
        self.tree_widget.addTopLevelItem(apple_item)
        self.variantManager = QtVariantPropertyManager()
        self.topItem = self.variantManager.addProperty(QtVariantPropertyManager.groupTypeId(), "Property Edit")
        self.NameView = self.variantManager.addProperty(QVariant.String, "Name")
        self.NameView.setAttribute("readOnly", True)
        self.ClassView = self.variantManager.addProperty(QVariant.String, "Class")
        self.ClassView.setAttribute("readOnly", True)
        self.AddressView = self.variantManager.addProperty(QVariant.String, "Address")
        self.AddressView.setAttribute("readOnly", True)
        self.propDescriptorEnum = self.variantManager.addProperty(QtVariantPropertyManager.enumTypeId(), "Property Descriptors : ")
        self.propDescriptorEnumList = QList()
        self.propDescriptorEnumList.append("Enum0")
        self.propDescriptorEnumList.append("Enum1")
        self.propDescriptorEnum.setAttribute("enumNames", self.propDescriptorEnumList)
        self.addedPropList = []
        self.topItem.addSubProperty(self.NameView)
        self.topItem.addSubProperty(self.ClassView)
        self.topItem.addSubProperty(self.AddressView)

        self.topItem.addSubProperty(self.propDescriptorEnum)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()