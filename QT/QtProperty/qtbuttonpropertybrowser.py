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

from qtpropertybrowser import QtAbstractPropertyBrowser, QtBrowserItem
from PyQt5.QtCore import QTimer, Qt, QSize, QRect, pyqtSignal
from PyQt5.QtWidgets import (
    QGridLayout,
    QToolButton,
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QFrame

    )
from pyqtcore import QList, QMap

###
#    \class QtButtonPropertyBrowser
#
#    \brief The QtButtonPropertyBrowser class provides a drop down QToolButton
#    based property browser.
#
#    A property browser is a widget that enables the user to edit a
#    given set of properties. Each property is represented by a label
#    specifying the property's name, and an editing widget (e.g. a line
#    edit or a combobox) holding its value. A property can have zero or
#    more subproperties.
#
#    QtButtonPropertyBrowser provides drop down button for all nested
#    properties, i.e. subproperties are enclosed by a container associated with
#    the drop down button. The parent property's name is displayed as button text. For example:
#
#    \image qtbuttonpropertybrowser.png
#
#    Use the QtAbstractPropertyBrowser API to add, insert and remove
#    properties from an instance of the QtButtonPropertyBrowser
#    class. The properties themselves are created and managed by
#    implementations of the QtAbstractPropertyManager class.
#
#    \sa QtTreePropertyBrowser, QtAbstractPropertyBrowser
###

###
#    \fn void QtButtonPropertyBrowser::collapsed(item)
#
#    This signal is emitted when the \a item is collapsed.
#
#    \sa expanded(), setExpanded()
###

###
#    \fn void QtButtonPropertyBrowser::expanded(item)
#
#    This signal is emitted when the \a item is expanded.
#
#    \sa collapsed(), setExpanded()
###

###
#    Creates a property browser with the given \a parent.
###

class WidgetItem():
    def __init__(self):
        self.label = 0
        self.widgetLabel = 0
        self.button = 0
        self.container = 0
        self.layout = 0
        self.parent = None
        self.children = QList()
        self.expanded = False
        self.widget = 0# can be null

class QtButtonPropertyBrowserPrivate():
    def __init__(self):
        self.q_ptr = None
        self.WidgetItem = WidgetItem()
        self.m_indexToItem = QMap()
        self.m_itemToIndex = QMap()
        self.m_widgetToItem = QMap()
        self.m_buttonToItem = QMap()
        self.m_mainLayout = None
        self.m_children = QList()
        self.m_recreateQueue = QList()

    def createEditor(self, property, parent):
        return self.q_ptr.createEditor(property, parent)

    def createButton(self, parent=None):
        button = QToolButton(parent)
        button.setCheckable(True)
        button.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))
        button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        button.setArrowType(Qt.DownArrow)
        button.setIconSize(QSize(3, 16))
        ###
        #QIcon icon
        #icon.addPixmap(self.style().standardPixmap(QStyle.SP_ArrowDown), QIcon.Normal, QIcon.Off)
        #icon.addPixmap(self.style().standardPixmap(QStyle.SP_ArrowUp), QIcon.Normal, QIcon.On)
        #button.setIcon(icon)
        ###
        return button

    def gridRow(self, item):
        siblings = QList()
        if (item.parent):
            siblings = item.parent.children
        else:
            siblings = self.m_children

        row = 0
        for sibling in siblings:
            if (sibling == item):
                return row
            row += self.gridSpan(sibling)

        return -1

    def gridSpan(self, item):
        if (item.container and item.expanded):
            return 2
        return 1

    def init(self, parent):
        self.m_mainLayout = QGridLayout()
        parent.setLayout(self.m_mainLayout)
        item = QSpacerItem(0, 0, QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.m_mainLayout.addItem(item, 0, 0)

    def slotEditorDestroyed(self):
        editor = self.q_ptr.sender()
        if (not editor):
            return
        if not self.m_widgetToItem.get(editor):
            return
        self.m_widgetToItem[editor].widget = 0
        self.m_widgetToItem.remove(editor)

    def slotUpdate(self):
        for item in self.m_recreateQueue:
            parent = item.parent
            w = 0
            l = 0
            oldRow = self.gridRow(item)
            if (parent):
                w = parent.container
                l = parent.layout
            else:
                w = self.q_ptr
                l = self.m_mainLayout

            span = 1
            if (not item.widget and not item.widgetLabel):
                span = 2
            item.label = QLabel(w)
            item.label.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
            l.addWidget(item.label, oldRow, 0, 1, span)

            self.updateItem(item)

        self.m_recreateQueue.clear()

    def setExpanded(self, item, expanded):
        if (item.expanded == expanded):
            return

        if (not item.container):
            return

        item.expanded = expanded
        row = self.gridRow(item)
        parent = item.parent
        l = 0
        if (parent):
            l = parent.layout
        else:
            l = self.m_mainLayout

        if (expanded):
            self.insertRow(l, row + 1)
            l.addWidget(item.container, row + 1, 0, 1, 2)
            item.container.show()
        else:
            l.removeWidget(item.container)
            item.container.hide()
            self.removeRow(l, row + 1)

        item.button.setChecked(expanded)
        if expanded:
            item.button.setArrowType(Qt.UpArrow)
        else:
            item.button.setArrowType(Qt.DownArrow)

    def slotToggled(self, checked):
        item = self.m_buttonToItem[self.q_ptr.sender()]
        if (not item):
            return

        self.setExpanded(item, checked)

        if (checked):
            self.q_ptr.expandedSignal.emit(self.m_itemToIndex[item])
        else:
            self.q_ptr.collapsedSignal.emit(self.m_itemToIndex[item])

    def updateLater(self):
        QTimer.singleShot(0, self.slotUpdate)

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
            row = self.gridRow(afterItem) + self.gridSpan(afterItem)
            if (parentItem):
                parentItem.children.insert(parentItem.children.indexOf(afterItem) + 1, newItem)
            else:
                self.m_children.insert(self.m_children.indexOf(afterItem) + 1, newItem)

        if (not parentItem):
            layout = self.m_mainLayout
            parentWidget = self.q_ptr
        else:
            if (not parentItem.container):
                self.m_recreateQueue.removeAll(parentItem)
                grandParent = parentItem.parent
                l = 0
                oldRow = self.gridRow(parentItem)
                if (grandParent):
                    l = grandParent.layout
                else:
                    l = self.m_mainLayout

                container = QFrame()
                container.setFrameShape(QFrame.Panel)
                container.setFrameShadow(QFrame.Raised)
                parentItem.container = container
                parentItem.button = self.createButton()
                self.m_buttonToItem[parentItem.button] = parentItem
                parentItem.button.toggled.connect(self.slotToggled)
                parentItem.layout = QGridLayout()
                container.setLayout(parentItem.layout)
                if (parentItem.label):
                    l.removeWidget(parentItem.label)
                    parentItem.label.close()
                    parentItem.label = 0

                span = 1
                if (not parentItem.widget and not parentItem.widgetLabel):
                    span = 2
                l.addWidget(parentItem.button, oldRow, 0, 1, span)
                self.updateItem(parentItem)

            layout = parentItem.layout
            parentWidget = parentItem.container

        newItem.label = QLabel(parentWidget)
        newItem.label.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        newItem.widget = self.createEditor(index.property(), parentWidget)
        if (newItem.widget):
            newItem.widget.destroyed.connect(self.slotEditorDestroyed)
            self.m_widgetToItem[newItem.widget] = newItem
        elif (index.property().hasValue()):
            newItem.widgetLabel = QLabel(parentWidget)
            newItem.widgetLabel.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed))

        self.insertRow(layout, row)
        span = 1
        if (newItem.widget):
            layout.addWidget(newItem.widget, row, 1)
        elif (newItem.widgetLabel):
            layout.addWidget(newItem.widgetLabel, row, 1)
        else:
            span = 2
        layout.addWidget(newItem.label, row, 0, span, 1)

        self.m_itemToIndex[newItem] = index
        self.m_indexToItem[index] = newItem

        self.updateItem(newItem)

    def propertyRemoved(self, index):
        item = self.m_indexToItem[index]

        self.m_indexToItem.remove(index)
        self.m_itemToIndex.remove(item)

        parentItem = item.parent

        row = self.gridRow(item)

        if (parentItem):
            parentItem.children.removeAt(parentItem.children.indexOf(item))
        else:
            self.m_children.removeAt(self.m_children.indexOf(item))

        colSpan = self.gridSpan(item)

        self.m_buttonToItem.remove(item.button)

        if (item.widget):
            item.widget.close()
            del item.widget
        if (item.label):
            item.label.close()
            del item.label
        if (item.widgetLabel):
            item.widgetLabel.close()
            del item.widgetLabel
        if (item.button):
            item.button.close()
            del item.button
        if (item.container):
            item.container.close()
            del item.container

        if (not parentItem):
            self.removeRow(self.m_mainLayout, row)
            if (colSpan > 1):
                self.removeRow(self.m_mainLayout, row)
        elif (len(parentItem.children) != 0):
            self.removeRow(parentItem.layout, row)
            if (colSpan > 1):
                self.removeRow(parentItem.layout, row)
        else:
            grandParent = parentItem.parent
            l = 0
            if (grandParent):
                l = grandParent.layout
            else:
                l = self.m_mainLayout

            parentRow = self.gridRow(parentItem)
            parentSpan = self.gridSpan(parentItem)

            l.removeWidget(parentItem.button)
            l.removeWidget(parentItem.container)
            parentItem.button.close()
            del parentItem.button
            parentItem.container.close()
            del parentItem.container
            parentItem.button = 0
            parentItem.container = 0
            parentItem.layout = 0
            if (not parentItem in self.m_recreateQueue):
                 self.m_recreateQueue.append(parentItem)
            if (parentSpan > 1):
                self.removeRow(l, parentRow + 1)

            self.updateLater()

        self.m_recreateQueue.removeAll(item)

        del item

    def insertRow(self, layout, row):
        itemToPos = QMap()
        idx = 0
        while (idx < len(layout)):
            r, c, rs, cs = layout.getItemPosition(idx)
            if (r >= row):
                itemToPos[layout.takeAt(idx)] = QRect(r + 1, c, rs, cs)
            else:
                idx += 1

        for k in itemToPos.keys():
            r = itemToPos[k]
            layout.addItem(k, r.x(), r.y(), r.width(), r.height())

    def removeRow(self, layout, row):
        itemToPos = QMap()
        idx = 0
        while (idx < len(layout)):
            r, c, rs, cs = layout.getItemPosition(idx)
            if (r > row):
                itemToPos[layout.takeAt(idx)] = QRect(r - 1, c, rs, cs)
            else:
                idx += 1

        for k in itemToPos.keys():
            r = itemToPos[k]
            layout.addItem(k, r.x(), r.y(), r.width(), r.height())

    def propertyChanged(self, index):
        item = self.m_indexToItem[index]

        self.updateItem(item)

    def updateItem(self, item):
        property = self.m_itemToIndex[item].property()
        if (item.button):
            font = item.button.font()
            font.setUnderline(property.isModified())
            item.button.setFont(font)
            item.button.setText(property.propertyName())
            item.button.setToolTip(property.toolTip())
            item.button.setStatusTip(property.statusTip())
            item.button.setWhatsThis(property.whatsThis())
            item.button.setEnabled(property.isEnabled())

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

class QtButtonPropertyBrowser(QtAbstractPropertyBrowser):
    collapsedSignal = pyqtSignal(QtBrowserItem)
    expandedSignal = pyqtSignal(QtBrowserItem)
    def __init__(self, parent=None):
        super(QtButtonPropertyBrowser, self).__init__(parent)

        self.d_ptr = QtButtonPropertyBrowserPrivate()
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
        for item in self.d_ptr.m_itemToIndex.keys():
            del item
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
    #    Sets the \a item to either collapse or expanded, depending on the value of \a expanded.
    #
    #    \sa isExpanded(), expanded(), collapsed()
    ###
    def setExpanded(self, item, expanded):
        itm = self.d_ptr.m_indexToItem[item]
        if (itm):
            self.d_ptr.setExpanded(itm, expanded)

    ###
    #    Returns True if the \a item is expanded; otherwise returns False.
    #
    #    \sa setExpanded()
    ###
    def isExpanded(self, item):
        itm = self.d_ptr.m_indexToItem[item]
        if (itm):
            return itm.expanded
        return False

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
    
