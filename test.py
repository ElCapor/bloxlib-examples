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
from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QMainWindow, QWidget, QVBoxLayout,QLabel, QLineEdit, QHBoxLayout, QComboBox

from pyqtcore import QList
from qtvariantproperty import QtVariantEditorFactory, QtVariantPropertyManager
from qttreepropertybrowser import QtTreePropertyBrowser
from Instance import Instance, GetClassName
from Exploit import roblox
from Memory import GetDataModel
from PyQt5.QtCore import pyqtSlot
class IndexedTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, index=0, parent=None):
        super().__init__(parent)
        self.index = index


def GetDescendants(apple_item, instance):
    # Add the current instance to the tree widget
    instance_item = IndexedTreeWidgetItem(instance.getAddress(),[instance.GetNameOld()])
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

    @pyqtSlot(QTreeWidgetItem, int)
    def on_item_clicked(self, item, column):
        print(item.index)
        if item.index != 0:
            local_instance = Instance(item.index)
            self.NameView.setValue(local_instance.GetNameOld())
            self.ClassView.setValue(GetClassName(local_instance))
        else:
            self.NameView.setValue("None")
            self.ClassView.setValue("None")
    def __controls(self):
        self.tree_widget = QTreeWidget()
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
        self.topItem.addSubProperty(self.NameView)
        self.topItem.addSubProperty(self.ClassView)


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