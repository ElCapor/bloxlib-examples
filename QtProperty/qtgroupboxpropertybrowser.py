#############################################################################
##
## Copyright (C) 2013 Digia Plc and/or its subsidiary(-ies).
## Contact: http:##www.qt-project.org/legal
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

from qtpropertybrowser import QtAbstractPropertyBrowser
from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtWidgets import (
    QGridLayout, QLabel, QGroupBox, QSizePolicy, QSpacerItem,
    QFrame
    )
from pyqtcore import (
    QList,
    QMap
    )
class WidgetItem():
    def __init__(self):
        self.widget = 0# can be null
        self.label = 0
        self.widgetLabel = 0
        self.groupBox = 0
        self.layout = 0
        self.line = 0
        self.parent = None
        self.children = QList()

class QtGroupBoxPropertyBrowserPrivate():
    def __init__(self):
        self.q_ptr = None
        self.m_indexToItem = QMap()
        self.m_itemToIndex = QMap()
        self.m_widgetToItem = QMap()
        self.m_mainLayout = 0
        self.m_children = QList()
        self.m_recreateQueue = QList()

    def createEditor(self, property, parent):
        return self.q_ptr.createEditor(property, parent)

    def init(self, parent):
        self.m_mainLayout = QGridLayout()
        parent.setLayout(self.m_mainLayout)
        item = QSpacerItem(0, 0, QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.m_mainLayout.addItem(item, 0, 0)

    def slotEditorDestroyed(self):
        editor = self.q_ptr.sender()
        if (not editor):
            return
        if (not editor in self.m_widgetToItem.keys()):
            return
        self.m_widgetToItem[editor].widget = 0
        self.m_widgetToItem.remove(editor)

    def slotUpdate(self):
        for item in self.m_recreateQueue:
            par = item.parent
            w = 0
            l = 0
            oldRow = -1
            if (not par):
                w = self.q_ptr
                l = self.m_mainLayout
                oldRow = self.m_children.indexOf(item)
            else:
                w = par.groupBox
                l = par.layout
                oldRow = par.children.indexOf(item)
                if (self.hasHeader(par)):
                    oldRow += 2

            if (item.widget):
                item.widget.setParent(w)
            elif (item.widgetLabel):
                item.widgetLabel.setParent(w)
            else:
                item.widgetLabel = QLabel(w)
                item.widgetLabel.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed))
                item.widgetLabel.setTextFormat(Qt.PlainText)

            span = 1
            if (item.widget):
                l.addWidget(item.widget, oldRow, 1, 1, 1)
            elif (item.widgetLabel):
                l.addWidget(item.widgetLabel, oldRow, 1, 1, 1)
            else:
                span = 2
            item.label = QLabel(w)
            item.label.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
            l.addWidget(item.label, oldRow, 0, 1, span)

            self.updateItem(item)

        self.m_recreateQueue.clear()

    def updateLater(self):
        QTimer.singleShot(0, self.q_ptr, self.slotUpdate())

    def propertyInserted(self, index, afterIndex):
        afterItem = self.m_indexToItem[afterIndex]
        parentItem = self.m_indexToItem.value(index.parent())

        newItem = WidgetItem()
        newItem.parent = parentItem

        layout = 0
        parentWidget = 0
        row = -1
        if (not afterItem):
            row = 0
            if (parentItem):
                parentItem.children.insert(0, newItem)
            else:
                self.m_children.insert(0, newItem)
        else:
            if (parentItem):
                row = parentItem.children.indexOf(afterItem) + 1
                parentItem.children.insert(row, newItem)
            else:
                row = self.m_children.indexOf(afterItem) + 1
                self.m_children.insert(row, newItem)

        if (parentItem and self.hasHeader(parentItem)):
            row += 2

        if (not parentItem):
            layout = self.m_mainLayout
            parentWidget = self.q_ptr
        else:
            if not parentItem.groupBox:
                self.m_recreateQueue.removeAll(parentItem)
                par = parentItem.parent
                w = 0
                l = 0
                oldRow = -1
                if (not par):
                    w = self.q_ptr
                    l = self.m_mainLayout
                    oldRow = self.m_children.indexOf(parentItem)
                else:
                    w = par.groupBox
                    l = par.layout
                    oldRow = par.children.indexOf(parentItem)
                    if (self.hasHeader(par)):
                        oldRow += 2

                parentItem.groupBox = QGroupBox(w)
                parentItem.layout = QGridLayout()
                parentItem.groupBox.setLayout(parentItem.layout)
                if (parentItem.label):
                    l.removeWidget(parentItem.label)
                    parentItem.label.close()
                    parentItem.label = 0

                if (parentItem.widget):
                    l.removeWidget(parentItem.widget)
                    parentItem.widget.setParent(parentItem.groupBox)
                    parentItem.layout.addWidget(parentItem.widget, 0, 0, 1, 2)
                    parentItem.line = QFrame(parentItem.groupBox)
                elif (parentItem.widgetLabel):
                    l.removeWidget(parentItem.widgetLabel)
                    parentItem.widgetLabel.close()
                    parentItem.widgetLabel = 0

                if (parentItem.line):
                    parentItem.line.setFrameShape(QFrame.HLine)
                    parentItem.line.setFrameShadow(QFrame.Sunken)
                    parentItem.layout.addWidget(parentItem.line, 1, 0, 1, 2)

                l.addWidget(parentItem.groupBox, oldRow, 0, 1, 2)
                self.updateItem(parentItem)

            layout = parentItem.layout
            parentWidget = parentItem.groupBox

        newItem.label = QLabel(parentWidget)
        newItem.label.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        newItem.widget = self.createEditor(index.property(), parentWidget)
        if (not newItem.widget):
            newItem.widgetLabel = QLabel(parentWidget)
            newItem.widgetLabel.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed))
            newItem.widgetLabel.setTextFormat(Qt.PlainText)
        else:
            newItem.widget.destroyed.connect(self.slotEditorDestroyed)
            self.m_widgetToItem[newItem.widget] = newItem

        self.insertRow(layout, row)
        span = 1
        if (newItem.widget):
            layout.addWidget(newItem.widget, row, 1)
        elif (newItem.widgetLabel):
            layout.addWidget(newItem.widgetLabel, row, 1)
        else:
            span = 2
        layout.addWidget(newItem.label, row, 0, 1, span)

        self.m_itemToIndex[newItem] = index
        self.m_indexToItem[index] = newItem

        self.updateItem(newItem)

    def propertyRemoved(self, index):
        item = self.m_indexToItem[index]

        self.m_indexToItem.remove(index)
        self.m_itemToIndex.remove(item)

        parentItem = item.parent

        row = -1

        if (parentItem):
            row = parentItem.children.indexOf(item)
            parentItem.children.removeAt(row)
            if (self.hasHeader(parentItem)):
                row += 2
        else:
            row = self.m_children.indexOf(item)
            self.m_children.removeAt(row)

        if (item.widget):
            item.widget.close()
            del item.widget
        if (item.label):
            item.label.close()
            del item.label
        if (item.widgetLabel):
            item.widgetLabel.close()
            del item.widgetLabel
        if (item.groupBox):
            item.groupBox.close()
            del item.groupBox

        if (not parentItem):
            self.removeRow(self.m_mainLayout, row)
        elif len(parentItem.children) > 0:
            self.removeRow(parentItem.layout, row)
        else:
            par = parentItem.parent
            l = 0
            oldRow = -1
            if (not par):
                l = self.m_mainLayout
                oldRow = self.m_children.indexOf(parentItem)
            else:
                l = par.layout
                oldRow = par.children.indexOf(parentItem)
                if (self.hasHeader(par)):
                    oldRow += 2

            if (parentItem.widget):
                parentItem.widget.hide()
                parentItem.widget.setParent(0)
            elif (parentItem.widgetLabel):
                parentItem.widgetLabel.hide()
                parentItem.widgetLabel.setParent(0)
            else:
                #parentItem.widgetLabel = QLabel(w)
                pass

            l.removeWidget(parentItem.groupBox)
            parentItem.groupBox.close()
            parentItem.groupBox = 0
            parentItem.line = 0
            parentItem.layout = 0
            if (not parentItem in self.m_recreateQueue):
                 self.m_recreateQueue.append(parentItem)
            self.updateLater()

        self.m_recreateQueue.removeAll(item)

        del item

    def insertRow(self, layout, row):
        itemToPos = QMap()
        idx = 0
        while (idx < layout.count()):
            r, c, rs, cs = layout.getItemPosition(idx)
            if (r >= row):
                itemToPos[layout.takeAt(idx)] = QRect(r + 1, c, rs, cs)
            else:
                idx += 1

        for it in itemToPos.keys():
            r = itemToPos[it]
            layout.addItem(it, r.x(), r.y(), r.width(), r.height())

    def removeRow(self, layout, row):
        itemToPos = QMap()
        idx = 0
        while (idx < layout.count()):
            r, c, rs, cs = layout.getItemPosition(idx)
            if (r > row):
                itemToPos[layout.takeAt(idx)] = QRect(r - 1, c, rs, cs)
            else:
                idx += 1

        for it in itemToPos.keys():
            r = itemToPos[it]
            layout.addItem(it, r.x(), r.y(), r.width(), r.height())

    def hasHeader(self, item):
        if (item.widget):
            return True
        return False

    def propertyChanged(self, index):
        item = self.m_indexToItem[index]

        self.updateItem(item)

    def updateItem(self, item):
        property = self.m_itemToIndex[item].property()
        if (item.groupBox):
            font = item.groupBox.font()
            font.setUnderline(property.isModified())
            item.groupBox.setFont(font)
            item.groupBox.setTitle(property.propertyName())
            item.groupBox.setToolTip(property.toolTip())
            item.groupBox.setStatusTip(property.statusTip())
            item.groupBox.setWhatsThis(property.whatsThis())
            item.groupBox.setEnabled(property.isEnabled())

        if (item.label):
            font = item.label.font()
            font.setUnderline(property.isModified())
            item.label.setFont(font)
            item.label.setText(property.propertyName())
            item.label.setToolTip(property.toolTip())
            item.label.setStatusTip(property.statusTip())
            item.label.setWhatsThis(property.whatsThis())
            item.label.setEnabled(property.isEnabled())

        if (item.widgetLabel):
            font = item.widgetLabel.font()
            font.setUnderline(False)
            item.widgetLabel.setFont(font)
            item.widgetLabel.setText(property.valueText())
            item.widgetLabel.setToolTip(property.valueText())
            item.widgetLabel.setEnabled(property.isEnabled())

        if (item.widget):
            font = item.widget.font()
            font.setUnderline(False)
            item.widget.setFont(font)
            item.widget.setEnabled(property.isEnabled())
            item.widget.setToolTip(property.valueText())

        #item.setIcon(1, property.valueIcon())

###
#    \class QtGroupBoxPropertyBrowser
#
#    \brief The QtGroupBoxPropertyBrowser class provides a QGroupBox
#    based property browser.
#
#    A property browser is a widget that enables the user to edit a
#    given set of properties. Each property is represented by a label
#    specifying the property's name, and an editing widget (e.g. a line
#    edit or a combobox) holding its value. A property can have zero or
#    more subproperties.
#
#    QtGroupBoxPropertyBrowser provides group boxes for all nested
#    properties, i.e. subproperties are enclosed by a group box with
#    the parent property's name as its title. For example:
#
#    \image qtgroupboxpropertybrowser.png
#
#    Use the QtAbstractPropertyBrowser API to add, insert and remove
#    properties from an instance of the QtGroupBoxPropertyBrowser
#    class. The properties themselves are created and managed by
#    implementations of the QtAbstractPropertyManager class.
#
#    \sa QtTreePropertyBrowser, QtAbstractPropertyBrowser
###

###
#    Creates a property browser with the given \a parent.
###
class QtGroupBoxPropertyBrowser(QtAbstractPropertyBrowser):
    def __init__(self, parent=None):
        super(QtGroupBoxPropertyBrowser, self).__init__(parent)

        self.d_ptr = QtGroupBoxPropertyBrowserPrivate()
        self.d_ptr.q_ptr = self
        self.d_ptr.init(self)

    ###
    #    Destroys this property browser.
    #
    #    Note that the properties that were inserted into this browser are
    #    \e not destroyed since they may still be used in other
    #    browsers. The properties are owned by the manager that created
    #    them.
    #
    #    \sa QtProperty, QtAbstractPropertyManager
    ###
    def __del__(self):
        for it in self.d_ptr.m_itemToIndex.keys():
           del it
        del self.d_ptr

    ###
    #    \reimp
    ###
    def itemInserted(self, item, afterItem):
        self.d_ptr.propertyInserted(item, afterItem)

    ###
    #    \reimp
    ###
    def itemRemoved(self, item):
        self.d_ptr.propertyRemoved(item)

    ###
    #    \reimp
    ###
    def itemChanged(self, item):
        self.d_ptr.propertyChanged(item)

    ###
    #   Return the position of scroll bar
    ###
    def scrollPosition(self):
        return 0, 0
    
    ###
    #   Set scroll bars position
    ###
    def setScrollPosition(self, dx, dy):
        pass