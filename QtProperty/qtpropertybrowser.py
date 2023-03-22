# -*- coding: utf-8 -*-
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
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES LOSS OF USE,
## DATA, OR PROFITS OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
##
## $QT_END_LICENSE$
##
#############################################################################

import copy
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QLineEdit, QWidget
from PyQt5.QtGui import QIcon, QColor

from pyqtcore import QList, QMap, QMapList, QMapMapList

g_viewToManagerToFactory = None
def m_viewToManagerToFactory():
    global g_viewToManagerToFactory
    if not g_viewToManagerToFactory:
        g_viewToManagerToFactory = QMapMapList()
    return g_viewToManagerToFactory

g_managerToFactoryToViews = None
def m_managerToFactoryToViews():
    global g_managerToFactoryToViews
    if not g_managerToFactoryToViews:
        g_managerToFactoryToViews = QMapMapList()
    return g_managerToFactoryToViews

class QtPropertyPrivate():
    def __init__(self, manager):
        self.q_ptr = None
        self.m_enabled = True
        self.m_modified = False
        self.m_manager = manager

        self.m_parentItems = set()
        self.m_subItems = QList()
        self.m_toolTip = ''
        self.m_statusTip = ''
        self.m_whatsThis = ''
        self.m_name = ''
        self.m_nameColor = QColor()
        self.m_valueColor = QColor()
        
###
#    \class QtProperty
#
#    \brief The QtProperty class encapsulates an instance of a property.
#
#    Properties are created by objects of QtAbstractPropertyManager
#    subclasses a manager can create properties of a given type, and
#    is used in conjunction with the QtAbstractPropertyBrowser class. A
#    property is always owned by the manager that created it, which can
#    be retrieved using the propertyManager() function.
#
#    QtProperty contains the most common property attributes, and
#    provides functions for retrieving as well as setting their values:
#
#    \table
#    \header \o Getter \o Setter
#    \row
#    \o propertyName() \o setPropertyName()
#    \row
#    \o statusTip() \o setStatusTip()
#    \row
#    \o toolTip() \o setToolTip()
#    \row
#    \o whatsThis() \o setWhatsThis()
#    \row
#    \o isEnabled() \o setEnabled()
#    \row
#    \o isModified() \o setModified()
#    \row
#    \o valueText() \o Nop
#    \row
#    \o valueIcon() \o Nop
#    \endtable
#
#    It is also possible to nest properties: QtProperty provides the
#    addSubProperty(), insertSubProperty() and removeSubProperty() functions to
#    manipulate the set of subproperties. Use the subProperties()
#    function to retrieve a property's current set of subproperties.
#    Note that nested properties are not owned by the parent property,
#    i.e. each subproperty is owned by the manager that created it.
#
#    \sa QtAbstractPropertyManager, QtBrowserItem
###
class QtProperty():
    ###
    #    Creates a property with the given \a manager.
    #
    #    This constructor is only useful when creating a custom QtProperty
    #    subclass (e.g. QtVariantProperty). To create a regular QtProperty
    #    object, use the QtAbstractPropertyManager::addProperty()
    #    function instead.
    #
    #    \sa QtAbstractPropertyManager::addProperty()
    ###
    def __init__(self, manager=None):
        self.d__ptr = QtPropertyPrivate(manager)
        self.d__ptr.q_ptr = self
        
    ###
    #    Destroys this property.
    #
    #    Note that subproperties are detached but not destroyed, i.e. they
    #    can still be used in another context.
    #
    #    \sa QtAbstractPropertyManager::clear()
    #
    ###
    def __del__(self):
        self.destroy()

    # As python can't force free memory after use del, so we have to destroy it manual
    def destroy(self):
        for property in self.d__ptr.m_parentItems:
            property.d__ptr.m_manager.d__ptr.propertyRemoved(self, property)

        if self.d__ptr.m_manager and self.d__ptr.m_manager!=-1:
            self.d__ptr.m_manager.d__ptr.propertyDestroyed(self)

        for property in self.d__ptr.m_subItems:
            parentItems = property.d__ptr.m_parentItems
            if parentItems.__contains__(self):
                parentItems.remove(self)

        for property in self.d__ptr.m_parentItems:
            property.d__ptr.m_subItems.removeAll(self)
            
    ###
    #    Returns the set of subproperties.
    #
    #    Note that subproperties are not owned by \e this property, but by
    #    the manager that created them.
    #
    #    \sa insertSubProperty(), removeSubProperty()
    ###
    def subProperties(self):
        return self.d__ptr.m_subItems

    ###
    #    Returns a pointer to the manager that owns this property.
    ###
    def propertyManager(self):
        return self.d__ptr.m_manager

    ###
    #    Returns the property's  tool tip.
    #
    #    \sa setToolTip()
    ###
    def toolTip(self):
        return self.d__ptr.m_toolTip

    ###
    #    Returns the property's status tip.
    #
    #    \sa setStatusTip()
    ###
    def statusTip(self):
        return self.d__ptr.m_statusTip

    ###
    #    Returns the property's "What's This" help text.
    #
    #    \sa setWhatsThis()
    ###
    def whatsThis(self):
        return self.d__ptr.m_whatsThis

    ###
    #    Returns the property's name.
    #
    #    \sa setPropertyName()
    ###
    def propertyName(self):
        return self.d__ptr.m_name

    ###
    #    Returns whether the property is enabled.
    #
    #    \sa setEnabled()
    ###
    def isEnabled(self):
        return self.d__ptr.m_enabled

    ###
    #    Returns whether the property is modified.
    #
    #    \sa setModified()
    ###
    def isModified(self):
        return self.d__ptr.m_modified

    ###
    #    Returns whether the property has a value.
    #
    #    \sa QtAbstractPropertyManager::hasValue()
    ###
    def hasValue(self):
        return self.d__ptr.m_manager.hasValue(self)

    ###
    #    Returns an icon representing the current state of this property.
    #
    #    If the given property type can not generate such an icon, this:
    #    function returns an invalid icon.
    #
    #    \sa QtAbstractPropertyManager::valueIcon()
    ###
    def valueIcon(self):
        ico = self.d__ptr.m_manager.valueIcon(self)
        if not ico:
            return QIcon()
        return ico

    ###
    #    Returns a string representing the current state of this property.
    #
    #    If the given property type can not generate such a string, this:
    #    function returns an empty string.
    #
    #    \sa QtAbstractPropertyManager::valueText()
    ###
    def valueText(self):
        return self.d__ptr.m_manager.valueText(self)

    ###
    #    Returns the display text according to the echo-mode set on the editor.
    #
    #    When the editor is a QLineEdit, this will return a string equal to what
    #    is displayed.
    #
    #    \sa QtAbstractPropertyManager::valueText()
    ###
    def displayText(self):
        return self.d__ptr.m_manager.displayText(self)

    ###
    #    Sets the property's tool tip to the given \a text.
    #
    #    \sa toolTip()
    ###
    def setToolTip(self, text):
        if (self.d__ptr.m_toolTip == text):
            return

        self.d__ptr.m_toolTip = text
        self.propertyChanged()

    ###
    #    Sets the property's status tip to the given \a text.
    #
    #    \sa statusTip()
    ###
    def setStatusTip(self, text):
        if (self.d__ptr.m_statusTip == text):
            return

        self.d__ptr.m_statusTip = text
        self.propertyChanged()

    ###
    #    Sets the property's "What's This" help text to the given \a text.
    #
    #    \sa whatsThis()
    ###
    def setWhatsThis(self, text):
        if (self.d__ptr.m_whatsThis == text):
            return

        self.d__ptr.m_whatsThis = text
        self.propertyChanged()

    ###
    #    \fn void QtProperty::setPropertyName(const name)
    #
    #    Sets the property's  name to the given \a name.
    #
    #    \sa propertyName()
    ###
    def setPropertyName(self, text):
        if (self.d__ptr.m_name == text):
            return

        self.d__ptr.m_name = text
        self.propertyChanged()

    ###
    #    \fn void QtProperty::setNameColor(const QColor &color)
    #
    #    Sets the property's name color to the given \a color.
    #
    #    \sa nameColor()
    ###
    def setNameColor(self, color):
        if (self.d__ptr.m_nameColor == color):
            return

        self.d__ptr.m_nameColor = color
        self.propertyChanged()

    ###
    #    \fn void QtProperty::setValueColor(const QColor &color)
    #
    #    Sets the property's value color to the given \a color.
    #
    #    \sa valueColor()
    ###
    def setValueColor(self, color):
        if (self.d__ptr.m_valueColor == color):
            return

        self.d__ptr.m_valueColor = color
        self.propertyChanged()

    ###
    #    Enables or disables the property according to the passed \a enable value.
    #
    #    \sa isEnabled()
    ###
    def setEnabled(self, enable):
        if (self.d__ptr.m_enabled == enable):
            return

        self.d__ptr.m_enabled = enable
        self.propertyChanged()

    ###
    #    Sets the property's modified state according to the passed \a modified value.
    #
    #    \sa isModified()
    ###
    def setModified(self, modified):
        if (self.d__ptr.m_modified == modified):
            return

        self.d__ptr.m_modified = modified
        self.propertyChanged()

    ###
    #    Appends the given \a property to this property's subproperties.
    #
    #    If the given \a property already is added, this function does:
    #    nothing.
    #
    #    \sa insertSubProperty(), removeSubProperty()
    ###
    def addSubProperty(self, property):
        after = None
        if (len(self.d__ptr.m_subItems) > 0):
            after = self.d__ptr.m_subItems[-1]
        self.insertSubProperty(property, after)

    ###
    #    \fn void QtProperty::insertSubProperty(property, precedingProperty)
    #
    #    Inserts the given \a property after the specified \a
    #    precedingProperty into this property's list of subproperties.  If
    #    \a precedingProperty is 0, the specified \a property is inserted
    #    at the beginning of the list.
    #
    #    If the given \a property already is inserted, this function does:
    #    nothing.
    #
    #    \sa addSubProperty(), removeSubProperty()
    ###
    def insertSubProperty(self, property, afterProperty):
        if (not property):
            return

        if (property == self):
            return

        # traverse all children of item. if this item is a child of item then cannot add.
        pendingList = copy.copy(property.subProperties())
        visited = QMap()
        while len(pendingList) > 0:
            i = pendingList[0]
            if (i == self):
                return
            pendingList.removeFirst()
            if (visited.get(i)):
                continue
            visited[i] = True
            pendingList += i.subProperties()

        pendingList = self.subProperties()
        pos = 0
        newPos = 0
        properAfterProperty = None
        while (pos < len(pendingList)):
            i = pendingList[pos]
            if (i == property):
                return # if item is already inserted in this item then cannot add.
            if (i == afterProperty):
                newPos = pos + 1
                properAfterProperty = afterProperty

            pos += 1

        self.d__ptr.m_subItems.insert(newPos, property)
        property.d__ptr.m_parentItems.add(self)

        self.d__ptr.m_manager.d__ptr.propertyInserted(property, self, properAfterProperty)

    ###
    #    Removes the given \a property from the list of subproperties
    #    without deleting it.
    #
    #    \sa addSubProperty(), insertSubProperty()
    ###
    def removeSubProperty(self, property):
        if (not property):
            return

        self.d__ptr.m_manager.d__ptr.propertyRemoved(property, self)

        pendingList = self.subProperties()
        pos = 0
        while (pos < len(pendingList)):
            if (pendingList[pos] == property):
                self.d__ptr.m_subItems.removeAt(pos)
                property.d__ptr.m_parentItems.remove(self)
                return

            pos += 1

    ###
    #    \internal
    ###
    def propertyChanged(self):
        self.d__ptr.m_manager.d__ptr.propertyChanged(self)

    def propertyDestroyed(self, property):
        if property in self.d__ptr.m_properties:
            self.propertyDestroyedSignal.emit(property)
            self.uninitializeProperty(property)
            self.d__ptr.m_properties.remove(property)

class QtAbstractPropertyManagerPrivate():
    def __init__(self):
        self.m_properties = set()

    def propertyDestroyed(self, property):
        if property in self.m_properties:
            self.q_ptr.propertyDestroyedSignal.emit(property)
            self.q_ptr.uninitializeProperty(property)
            self.m_properties.remove(property)

    def propertyChanged(self, property):
        self.q_ptr.propertyChangedSignal.emit(property)

    def propertyRemoved(self, property, parentProperty):
        self.q_ptr.propertyRemovedSignal.emit(property, parentProperty)

    def propertyInserted(self, property, parentProperty, afterProperty=None):
        self.q_ptr.propertyInsertedSignal.emit(property, parentProperty, [afterProperty])

###
#    \class QtAbstractPropertyManager
#
#    \brief The QtAbstractPropertyManager provides an interface for
#    property managers.
#
#    A manager can create and manage properties of a given type, and is
#    used in conjunction with the QtAbstractPropertyBrowser class.
#
#    When using a property browser widget, the properties are created
#    and managed by implementations of the QtAbstractPropertyManager
#    class. To ensure that the properties' values will be displayed
#    using suitable editing widgets, the managers are associated with
#    objects of QtAbstractEditorFactory subclasses. The property browser
#    will use these associations to determine which factories it should
#    use to create the preferred editing widgets.
#
#    The QtAbstractPropertyManager class provides common functionality
#    like creating a property using the addProperty() function, and
#    retrieving the properties created by the manager using the
#    properties() function. The class also provides signals that are
#    emitted when the manager's properties change: propertyInserted(),
#    propertyRemoved(), propertyChanged() and propertyDestroyed().
#
#    QtAbstractPropertyManager subclasses are supposed to provide their
#    own type specific API. Note that several ready-made
#    implementations are available:
#
#    \list
#    \o QtBoolPropertyManager
#    \o QtColorPropertyManager
#    \o QtDatePropertyManager
#    \o QtDateTimePropertyManager
#    \o QtDoublePropertyManager
#    \o QtEnumPropertyManager
#    \o QtFlagPropertyManager
#    \o QtFontPropertyManager
#    \o QtGroupPropertyManager
#    \o QtIntPropertyManager
#    \o QtPointPropertyManager
#    \o QtRectPropertyManager
#    \o QtSizePropertyManager
#    \o QtSizePolicyPropertyManager
#    \o QtStringPropertyManager
#    \o QtTimePropertyManager
#    \o QtVariantPropertyManager
#    \endlist
#
#    \sa QtAbstractEditorFactoryBase, QtAbstractPropertyBrowser, QtProperty
###

###
#    \fn void QtAbstractPropertyManager::propertyInserted(newProperty,
#                parentProperty, precedingProperty)
#
#    This signal is emitted when a new subproperty is inserted into an
#    existing property, passing pointers to the \a newProperty, \a
#    parentProperty and \a precedingProperty as parameters.
#
#    If \a precedingProperty is 0, the \a newProperty was inserted at:
#    the beginning of the \a parentProperty's subproperties list.
#
#    Note that signal is emitted only if the \a parentProperty is created
#    by this manager.
#
#    \sa QtAbstractPropertyBrowser::itemInserted()
###

###
#    \fn void QtAbstractPropertyManager::propertyChanged(property)
#
#    This signal is emitted whenever a property's data changes, passing
#    a pointer to the \a property as parameter.
#
#    Note that signal is only emitted for properties that are created by
#    this manager.
#
#    \sa QtAbstractPropertyBrowser::itemChanged()
###

###
#    \fn void QtAbstractPropertyManager::propertyRemoved(property, parent)
#
#    This signal is emitted when a subproperty is removed, passing
#    pointers to the removed \a property and the \a parent property as
#    parameters.
#
#    Note that signal is emitted only when the \a parent property is
#    created by this manager.
#
#    \sa QtAbstractPropertyBrowser::itemRemoved()
###

###
#    \fn void QtAbstractPropertyManager::propertyDestroyed(property)
#
#    This signal is emitted when the specified \a property is about to
#    be destroyed.
#
#    Note that signal is only emitted for properties that are created
#    by this manager.
#
#    \sa clear(), uninitializeProperty()
###

###
#    \fn void QtAbstractPropertyBrowser::currentItemChanged(current)
#
#    This signal is emitted when the current item changes. The current item is specified by \a current.
#
#    \sa QtAbstractPropertyBrowser::setCurrentItem()
###
class QtAbstractPropertyManager(QObject):
    propertyInsertedSignal = pyqtSignal(QtProperty, QtProperty, list)
    propertyChangedSignal = pyqtSignal(QtProperty)
    propertyRemovedSignal = pyqtSignal(QtProperty, QtProperty)
    propertyDestroyedSignal = pyqtSignal(QtProperty)
    ###
    #    Creates an abstract property manager with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtAbstractPropertyManager, self).__init__(parent)

        self.d__ptr = QtAbstractPropertyManagerPrivate()
        self.d__ptr.q_ptr = self

    ###
    #    Destroys the manager. All properties created by the manager are
    #    destroyed.
    ###
    def __del__(self):
        self.clear()

    #    Destroys all the properties that this manager has created.
    #
    #    \sa propertyDestroyed(), uninitializeProperty()
    ###
    def clear(self):
        properties = list(self.properties())
        for i in range(len(properties)):
            prop = properties[i]
            prop.destroy()

    ###
    #    Returns the set of properties created by this manager.
    #
    #    \sa addProperty()
    ###
    def properties(self):
        return self.d__ptr.m_properties

    ###
    #    Returns whether the given \a property has a value.
    #
    #    The default implementation of this function returns True.
    #
    #    \sa QtProperty::hasValue()
    ###
    def hasValue(self, property):
        return True

    ###
    #    Returns an icon representing the current state of the given \a
    #    property.
    #
    #    The default implementation of this function returns an invalid
    #    icon.
    #
    #    \sa QtProperty::valueIcon()
    ###
    def valueIcon(self, property):
        return QIcon()

    ###
    #    Returns a string representing the current state of the given \a
    #    property.
    #
    #    The default implementation of this function returns an empty
    #    string.
    #
    #    \sa QtProperty::valueText()
    ###
    def valueText(self, property):
        return ''

    ###
    #    Returns a string representing the current state of the given \a
    #    property.
    #
    #    The default implementation of this function returns an empty
    #    string.
    #
    #    \sa QtProperty::valueText()
    ###
    def displayText(self, property):
        return ''

    ###
    #    Returns the echo mode representing the current state of the given \a
    #    property.
    #
    #    The default implementation of this function returns QLineEdit.Normal.
    #
    #    \sa QtProperty::valueText()
    ###
    def echoMode(self, property):
        return QLineEdit.Normal

    ###
    #    Creates a property with the given \a name which then is owned by this manager.
    #
    #    Internally, this function calls the createProperty() and
    #    initializeProperty() functions.
    #
    #    \sa initializeProperty(), properties()
    ###
    def addProperty(self, name=''):
        property = self.createProperty()
        if (property):
            property.setPropertyName(name)
            self.d__ptr.m_properties.add(property)
            self.initializeProperty(property)

        return property

    ###
    #    Creates a property.
    #
    #    The base implementation produce QtProperty instances Reimplement
    #    this function to make this manager produce objects of a QtProperty
    #    subclass.
    #
    #    \sa addProperty(), initializeProperty()
    ###
    def createProperty(self):
        return QtProperty(self)

    ###
    #    \fn void QtAbstractPropertyManager::initializeProperty(property) = 0
    #
    #    This function is called whenever a new valid property pointer has
    #    been created, passing the pointer as parameter.
    #
    #    The purpose is to let the manager know that the \a property has
    #    been created so that it can provide additional attributes for the
    #    new property, e.g. QtIntPropertyManager adds \l
    #    QtIntPropertyManager::value()value, \l
    #    QtIntPropertyManager::minimum()minimumand \l
    #    QtIntPropertyManager::maximum()maximumattributes. Since each manager
    #    subclass adds type specific attributes, this function is pure
    #    virtual and must be reimplemented when deriving from the
    #    QtAbstractPropertyManager class.
    #
    #    \sa addProperty(), createProperty()
    ###

    ###
    #    This function is called just before the specified \a property is destroyed.
    #
    #    The purpose is to let the property manager know that the \a
    #    property is being destroyed so that it can remove the property's
    #    additional attributes.
    #
    #    \sa clear(), propertyDestroyed()
    ###
    def uninitializeProperty(self, property):
        pass

###
#    \class QtAbstractEditorFactoryBase
#
#    \brief The QtAbstractEditorFactoryBase provides an interface for
#    editor factories.
#
#    An editor factory is a class that is able to create an editing
#    widget of a specified type (e.g. line edits or comboboxes) for a
#    given QtProperty object, and it is used in conjunction with the
#    QtAbstractPropertyManager and QtAbstractPropertyBrowser classes.
#
#    When using a property browser widget, the properties are created
#    and managed by implementations of the QtAbstractPropertyManager
#    class. To ensure that the properties' values will be displayed
#    using suitable editing widgets, the managers are associated with
#    objects of QtAbstractEditorFactory subclasses. The property browser
#    will use these associations to determine which factories it should
#    use to create the preferred editing widgets.
#
#    Typically, an editor factory is created by subclassing the
#    QtAbstractEditorFactory template class which inherits
#    QtAbstractEditorFactoryBase. But note that several ready-made
#    implementations are available:
#
#    \list
#    \o QtCheckBoxFactory
#    \o QtDateEditFactory
#    \o QtDateTimeEditFactory
#    \o QtDoubleSpinBoxFactory
#    \o QtEnumEditorFactory
#    \o QtLineEditFactory
#    \o QtScrollBarFactory
#    \o QtSliderFactory
#    \o QtSpinBoxFactory
#    \o QtTimeEditFactory
#    \o QtVariantEditorFactory
#    \endlist
#
#    \sa QtAbstractPropertyManager, QtAbstractPropertyBrowser
###

###
#    \fn virtualQtAbstractEditorFactoryBase::createEditor(property,
#        parent) = 0
#
#    Creates an editing widget (with the given \a parent) for the given
#    \a property.
#
#    This function is reimplemented in QtAbstractEditorFactory template class
#    which also provides a pure virtual convenience overload of this
#    function enabling access to the property's manager.
#
#    \sa QtAbstractEditorFactory::createEditor()
###

###
#    \fn QtAbstractEditorFactoryBase::QtAbstractEditorFactoryBase(parent = None)
#
#    Creates an abstract editor factory with the given \a parent.
###

###
#    \fn virtual void QtAbstractEditorFactoryBase::breakConnection(manager) = 0
#
#    \internal
#
#    Detaches property manager from factory.
#    This method is reimplemented in QtAbstractEditorFactory template subclass.
#    You don't need to reimplement it in your subclasses. Instead implement more convenient
#    QtAbstractEditorFactory::disconnectPropertyManager() which gives you access to particular manager subclass.
###

###
#    \fn virtual void QtAbstractEditorFactoryBase::managerDestroyed(manager) = 0
#
#    \internal
#
#    This method is called when property manager is being destroyed.
#    Basically it notifies factory not to produce editors for properties owned by \a manager.
#    You don't need to reimplement it in your subclass. This method is implemented in
#    QtAbstractEditorFactory template subclass.
###

###
#    \class QtAbstractEditorFactory
#
#    \brief The QtAbstractEditorFactory is the base template class for editor
#    factories.
#
#    An editor factory is a class that is able to create an editing
#    widget of a specified type (e.g. line edits or comboboxes) for a
#    given QtProperty object, and it is used in conjunction with the
#    QtAbstractPropertyManager and QtAbstractPropertyBrowser classes.
#
#    Note that the QtAbstractEditorFactory functions are using the
#    PropertyManager template argument class which can be any
#    QtAbstractPropertyManager subclass. For example:
#
#    \code
#        QtSpinBoxFactory *factory
#        managers = factory.propertyManagers()
#    \endcode
#
#    Note that QtSpinBoxFactory by definition creates editing widgets
#    \e only for properties created by QtIntPropertyManager.
#
#    When using a property browser widget, the properties are created
#    and managed by implementations of the QtAbstractPropertyManager
#    class. To ensure that the properties' values will be displayed
#    using suitable editing widgets, the managers are associated with
#    objects of QtAbstractEditorFactory subclasses. The property browser will
#    use these associations to determine which factories it should use
#    to create the preferred editing widgets.
#
#    A QtAbstractEditorFactory object is capable of producing editors for
#    several property managers at the same time. To create an
#    association between this factory and a given manager, use the
#    addPropertyManager() function. Use the removePropertyManager() function to make
#    this factory stop producing editors for a given property
#    manager. Use the propertyManagers() function to retrieve the set of
#    managers currently associated with this factory.
#
#    Several ready-made implementations of the QtAbstractEditorFactory class
#    are available:
#
#    \list
#    \o QtCheckBoxFactory
#    \o QtDateEditFactory
#    \o QtDateTimeEditFactory
#    \o QtDoubleSpinBoxFactory
#    \o QtEnumEditorFactory
#    \o QtLineEditFactory
#    \o QtScrollBarFactory
#    \o QtSliderFactory
#    \o QtSpinBoxFactory
#    \o QtTimeEditFactory
#    \o QtVariantEditorFactory
#    \endlist
#
#    When deriving from the QtAbstractEditorFactory class, several pure virtual
#    functions must be implemented: the connectPropertyManager() function is
#    used by the factory to connect to the given manager's signals, the
#    createEditor() function is supposed to create an editor for the
#    given property controlled by the given manager, and finally the
#    disconnectPropertyManager() function is used by the factory to disconnect
#    from the specified manager's signals.
#
#    \sa QtAbstractEditorFactoryBase, QtAbstractPropertyManager
###

###
#    \fn QtAbstractEditorFactory::QtAbstractEditorFactory(parent = None)
#
#    Creates an editor factory with the given \a parent.
#
#    \sa addPropertyManager()
###

###
#    \fnQtAbstractEditorFactory::createEditor(property,parent)
#
#    Creates an editing widget (with the given \a parent) for the given
#    \a property.
###

###
#    \fn void QtAbstractEditorFactory::addPropertyManager(manager)
#
#    Adds the given \a manager to this factory's set of managers,
#    making this factory produce editing widgets for properties created
#    by the given manager.
#
#    The PropertyManager type is a template argument class, and represents the chosen
#    QtAbstractPropertyManager subclass.
#
#    \sa propertyManagers(), removePropertyManager()
###

###
#    \fn void QtAbstractEditorFactory::removePropertyManager(manager)
#
#    Removes the given \a manager from this factory's set of
#    managers. The PropertyManager type is a template argument class, and may be
#    any QtAbstractPropertyManager subclass.
#
#    \sa propertyManagers(), addPropertyManager()
###

###
#    \fn virtual void QtAbstractEditorFactory::connectPropertyManager(manager) = 0
#
#    Connects this factory to the given \a manager's signals.  The
#    PropertyManager type is a template argument class, and represents
#    the chosen QtAbstractPropertyManager subclass.
#
#    This function is used internally by the addPropertyManager() function, and
#    makes it possible to update an editing widget when the associated
#    property's data changes. This is typically done in custom slots
#    responding to the signals emitted by the property's manager,
#    e.g. QtIntPropertyManager::valueChanged() and
#    QtIntPropertyManager::rangeChanged().
#
#    \sa propertyManagers(), disconnectPropertyManager()
###

###
#    \fn virtualQtAbstractEditorFactory::createEditor(manager, property,
#                parent) = 0
#
#    Creates an editing widget with the given \a parent for the
#    specified \a property created by the given \a manager. The
#    PropertyManager type is a template argument class, and represents
#    the chosen QtAbstractPropertyManager subclass.
#
#    This function must be implemented in derived classes: It is
#    recommended to store a pointer to the widget and map it to the
#    given \a property, since the widget must be updated whenever the
#    associated property's data changes. This is typically done in
#    custom slots responding to the signals emitted by the property's
#    manager, e.g. QtIntPropertyManager::valueChanged() and
#    QtIntPropertyManager::rangeChanged().
#
#    \sa connectPropertyManager()
###

###
#    \fn virtual void QtAbstractEditorFactory::disconnectPropertyManager(manager) = 0
#
#    Disconnects this factory from the given \a manager's signals. The
#    PropertyManager type is a template argument class, and represents
#    the chosen QtAbstractPropertyManager subclass.
#
#    This function is used internally by the removePropertyManager() function.
#
#    \sa propertyManagers(), connectPropertyManager()
###

###
#    \fn QtAbstractEditorFactory::propertyManagers():
#
#    Returns the factory's set of associated managers.  The
#    PropertyManager type is a template argument class, and represents
#    the chosen QtAbstractPropertyManager subclass.
#
#    \sa addPropertyManager(), removePropertyManager()
###

###
#    \fn QtAbstractEditorFactory::propertyManager(property):
#
#    Returns the property manager for the given \a property, or 0 if
#    the given \a property doesn't belong to any of this factory's
#    registered managers.
#
#    The PropertyManager type is a template argument class, and represents the chosen
#    QtAbstractPropertyManager subclass.
#
#    \sa propertyManagers()
###

###
#    \fn virtual void QtAbstractEditorFactory::managerDestroyed(manager)
#
#    \internal
#    \reimp
###
class QtBrowserItemPrivate():
    def __init__(self, browser, property, parent):
        self.q_ptr = None
        self.m_browser = browser
        self.m_property = property
        self.m_parent = parent
        self.m_children = QList()

    def __del__(self):
        pass

    def addChild(self, index, after):
        if index in self.m_children:
            return
        idx = self.m_children.indexOf(after) + 1 # we insert after returned idx, if it was -1 then we set idx to 0
        self.m_children.insert(idx, index)

    def removeChild(self, index):
        self.m_children.removeAll(index)

###
#    \class QtBrowserItem
#
#    \brief The QtBrowserItem class represents a property in
#    a property browser instance.
#
#    Browser items are created whenever a QtProperty is inserted to the
#    property browser. A QtBrowserItem uniquely identifies a
#    browser's item. Thus, if the same QtProperty is inserted multiple
#    times, each occurrence gets its own unique QtBrowserItem. The
#    items are owned by QtAbstractPropertyBrowser and automatically
#    deleted when they are removed from the browser.
#
#    You can traverse a browser's properties by calling parent() and
#    children(). The property and the browser associated with an item
#    are available as property() and browser().
#
#    \sa QtAbstractPropertyBrowser, QtProperty
###
class QtBrowserItem():
    def __init__(self, browser=None, property=None, parent=None):
        self.d__ptr = QtBrowserItemPrivate(browser, property, parent)
        self.d__ptr.q_ptr = self

    def __del__(self):
        del self.d__ptr

    ###
    #    Returns the property which is accosiated with this item. Note that
    #    several items can be associated with the same property instance in
    #    the same property browser.
    #
    #    \sa QtAbstractPropertyBrowser::items()
    ###

    def property(self):
        return self.d__ptr.m_property

    ###
    #    Returns the parent item of \e this item. Returns 0 if \e this item
    #    is associated with top-level property in item's property browser.
    #
    #    \sa children()
    ###

    def parent(self):
        return self.d__ptr.m_parent

    ###
    #    Returns the children items of \e this item. The properties
    #    reproduced from children items are always the same as
    #    reproduced from associated property' children, for example:
    #
    #    \code
    #        item
    #        childrenItems = item.children()
    #
    #        childrenProperties = item.property().subProperties()
    #    \endcode
    #
    #    The \e childrenItems list represents the same list as \e childrenProperties.
    ###

    def children(self):
        return self.d__ptr.m_children

    ###
    #    Returns the property browser which owns \e this item.
    ###

    def browser(self):
        return self.d__ptr.m_browser

class QtAbstractPropertyBrowserPrivate():
    def __init__(self):
        self.q_ptr = None
        self.m_subItems = QList()
        self.m_managerToProperties = QMapList()
        self.m_propertyToParents = QMapList()
        self.m_topLevelPropertyToIndex = QMap()
        self.m_topLevelIndexes = QList()
        self.m_propertyToIndexes = QMapList()
        self.m_currentItem = None

    def insertSubTree(self, property, parentProperty):
        if (self.m_propertyToParents.get(property)):
            # property was already inserted, so its manager is connected
            # and all its children are inserted and theirs managers are connected
            # we just register new parent (parent has to be new).
            self.m_propertyToParents[property].append(parentProperty)
            # don't need to update m_managerToProperties map since
            # m_managerToProperties[manager] already contains property.
            return

        manager = property.propertyManager()
        if not self.m_managerToProperties[manager]:
            # connect manager's signals
            manager.propertyInsertedSignal.connect(self.slotPropertyInserted)
            manager.propertyRemovedSignal.connect(self.slotPropertyRemoved)
            manager.propertyDestroyedSignal.connect(self.slotPropertyDestroyed)
            manager.propertyChangedSignal.connect(self.slotPropertyDataChanged)

        self.m_managerToProperties[manager].append(property)
        self.m_propertyToParents[property].append(parentProperty)

        for subProperty in property.subProperties():
            self.insertSubTree(subProperty, property)

    def removeSubTree(self, property, parentProperty):
        if (not self.m_propertyToParents.get(property)):
            # ASSERT
            return

        self.m_propertyToParents[property].removeAll(parentProperty)
        if len(self.m_propertyToParents[property]) > 0:
            return

        self.m_propertyToParents.remove(property)
        manager = property.propertyManager()
        self.m_managerToProperties[manager].removeAll(property)
        if not self.m_managerToProperties[manager]:
            # disconnect manager's signals
            manager.propertyInsertedSignal.disconnect(self.slotPropertyInserted)
            manager.propertyRemovedSignal.disconnect(self.slotPropertyRemoved)
            manager.propertyDestroyedSignal.disconnect(self.slotPropertyDestroyed)
            manager.propertyChangedSignal.disconnect(self.slotPropertyDataChanged)
            self.m_managerToProperties.remove(manager)

        for subProperty in property.subProperties():
            self.removeSubTree(subProperty, property)

    def createBrowserIndexes(self, property, parentProperty, afterProperty):
        parentToAfter = QMap()
        if (afterProperty):
            if not afterProperty in self.m_propertyToIndexes.keys():
                return

            indexes = self.m_propertyToIndexes[afterProperty]
            for idx in indexes:
                parentIdx = idx.parent()
                if ((parentProperty and parentIdx and parentIdx.property() == parentProperty) or (not parentProperty and not parentIdx)):
                    parentToAfter[idx.parent()] = idx
        elif (parentProperty):
            if not parentProperty in self.m_propertyToIndexes.keys():
                return

            for idx in indexes:
                parentToAfter[idx] = 0

        else:
            parentToAfter[0] = 0

        for it in parentToAfter.keys():
            self.createBrowserIndex(property, it, parentToAfter[it])

    def createBrowserIndex(self, property, parentIndex, afterIndex):
        newIndex = QtBrowserItem(self.q_ptr, property, parentIndex)
        if (parentIndex):
            parentIndex.d__ptr.addChild(newIndex, afterIndex)
        else:
            self.m_topLevelPropertyToIndex[property] = newIndex
            self.m_topLevelIndexes.insert(self.m_topLevelIndexes.indexOf(afterIndex) + 1, newIndex)

        if not self.m_propertyToIndexes.get(property):
            self.m_propertyToIndexes[property] = QList()
        self.m_propertyToIndexes[property].append(newIndex)
        self.itemInserted(newIndex, afterIndex)
        subItems = property.subProperties()
        afterChild = 0
        for child in subItems:
            afterChild = self.createBrowserIndex(child, newIndex, afterChild)

        return newIndex

    def removeBrowserIndexes(self, property, parentProperty):
        toRemove = QList()
        if not property in self.m_propertyToIndexes.keys():
            return

        indexes = self.m_propertyToIndexes[property]
        for idx in indexes:
            parentIdx = idx.parent()
            if ((parentProperty and parentIdx and parentIdx.property() == parentProperty) or (not parentProperty and not parentIdx)):
                toRemove.append(idx)

        for index in toRemove:
            self.removeBrowserIndex(index)

    def removeBrowserIndex(self, index):
        children = index.children()
        for i in range(len(children)-1, -1, -1):
            self.removeBrowserIndex(children[i])

        self.itemRemoved(index)
        if (index.parent()):
            index.parent().d__ptr.removeChild(index)
        else:
            self.m_topLevelPropertyToIndex.remove(index.property())
            self.m_topLevelIndexes.removeAll(index)

        property = index.property()
        self.m_propertyToIndexes[property].removeAll(index)
        if len(self.m_propertyToIndexes[property])<=0:
            self.m_propertyToIndexes.remove(property)
        del index

    def clearIndex(self, index):
        children = index.children()
        for c in children:
            self.clearIndex(c)

        del index

    def slotPropertyInserted(self, property, parentProperty, afterProperty):
        if (not self.m_propertyToParents.get(parentProperty)):
            return
        if type(afterProperty)==list:
            afterProperty = afterProperty[0]
        self.createBrowserIndexes(property, parentProperty, afterProperty)
        self.insertSubTree(property, parentProperty)
        #self.propertyInserted(property, parentProperty, afterProperty)

    def slotPropertyRemoved(self, property, parentProperty):
        if (not self.m_propertyToParents.get(parentProperty)):
            return
        self.removeSubTree(property, parentProperty) # this line should be probably moved down after propertyRemoved call
        #self.propertyRemoved(property, parentProperty)
        self.removeBrowserIndexes(property, parentProperty)

    def slotPropertyDestroyed(self, property):
        if not property in self.m_subItems:
            return
        self.removeProperty(property)

    def slotPropertyDataChanged(self, property):
        if not property in self.m_propertyToIndexes.keys():
            return

        indexes = self.m_propertyToIndexes[property]
        for idx in indexes:
            self.itemChanged(idx)

###
#    \class QtAbstractPropertyBrowser
#
#    \brief QtAbstractPropertyBrowser provides a base class for
#    implementing property browsers.
#
#    A property browser is a widget that enables the user to edit a
#    given set of properties.  Each property is represented by a label
#    specifying the property's name, and an editing widget (e.g. a line
#    edit or a combobox) holding its value. A property can have zero or
#    more subproperties.
#
#    \image qtpropertybrowser.png
#
#    The top level properties can be retrieved using the
#    properties() function. To traverse each property's
#    subproperties, use the QtProperty::subProperties() function. In
#    addition, the set of top level properties can be manipulated using
#    the addProperty(), insertProperty() and removeProperty()
#    functions. Note that the QtProperty class provides a corresponding
#    set of functions making it possible to manipulate the set of
#    subproperties as well.
#
#    To remove all the properties from the property browser widget, use
#    the clear() function. This function will clear the editor, but it
#    will not delete the properties since they can still be used in
#    other editors.
#
#    The properties themselves are created and managed by
#    implementations of the QtAbstractPropertyManager class. A manager
#    can handle (i.e. create and manage) properties of a given type. In
#    the property browser the managers are associated with
#    implementations of the QtAbstractEditorFactory: A factory is a
#    class able to create an editing widget of a specified type.
#
#    When using a property browser widget, managers must be created for
#    each of the required property types before the properties
#    themselves can be created. To ensure that the properties' values
#    will be displayed using suitable editing widgets, the managers
#    must be associated with objects of the preferred factory
#    implementations using the setFactoryForManager() function. The
#    property browser will use these associations to determine which
#    factory it should use to create the preferred editing widget.
#
#    Note that a factory can be associated with many managers, but a
#    manager can only be associated with one single factory within the
#    context of a single property browser.  The associations between
#    managers and factories can at any time be removed using the
#    unsetFactoryForManager() function.
#
#    Whenever the property data changes or a property is inserted or
#    removed, the itemChanged(), itemInserted() or
#    itemRemoved() functions are called, respectively. These
#    functions must be reimplemented in derived classes in order to
#    update the property browser widget. Be aware that some property
#    instances can appear several times in an abstract tree
#    structure. For example:
#
#    \table 100%
#    \row
#    \o
#    \code
#        property1, *property2, *property3
#
#        property2.addSubProperty(property1)
#        property3.addSubProperty(property2)
#
#        QtAbstractPropertyBrowser *editor
#
#        editor.addProperty(property1)
#        editor.addProperty(property2)
#        editor.addProperty(property3)
#    \endcode
#    \o  \image qtpropertybrowser-duplicate.png
#    \endtable
#
#    The addProperty() function returns a QtBrowserItem that uniquely
#    identifies the created item.
#
#    To make a property editable in the property browser, the
#    createEditor() function must be called to provide the
#    property with a suitable editing widget.
#
#    Note that there are two ready-made property browser
#    implementations:
#
#    \list
#        \o QtGroupBoxPropertyBrowser
#        \o QtTreePropertyBrowser
#    \endlist
#
#    \sa QtAbstractPropertyManager, QtAbstractEditorFactoryBase
###

###
#    \fn void QtAbstractPropertyBrowser::setFactoryForManager(manager,
#                    *factory)
#
#    Connects the given \a manager to the given \a factory, ensuring
#    that properties of the \a manager's type will be displayed with an
#    editing widget suitable for their value.
#
#    For example:
#
#    \code
#        QtIntintManager
#        QtDoubledoubleManager
#
#        myInteger = intManager.addProperty()
#        myDouble = doubleManager.addProperty()
#
#        QtSpinBoxFactory  *spinBoxFactory
#        QtDoubleSpinBoxFactory *doubleSpinBoxFactory
#
#        QtAbstractPropertyBrowser *editor
#        editor.setFactoryForManager(intManager, spinBoxFactory)
#        editor.setFactoryForManager(doubleManager, doubleSpinBoxFactory)
#
#        editor.addProperty(myInteger)
#        editor.addProperty(myDouble)
#    \endcode
#
#    In this example the \c myInteger property's value is displayed
#    with a QSpinBox widget, while the \c myDouble property's value is
#    displayed with a QDoubleSpinBox widget.
#
#    Note that a factory can be associated with many managers, but a
#    manager can only be associated with one single factory.  If the
#    given \a manager already is associated with another factory, the
#    old association is broken before the new one established.
#
#    This function ensures that the given \a manager and the given \a
#    factory are compatible, and it automatically calls the
#    QtAbstractEditorFactory::addPropertyManager() function if necessary.
#
#    \sa unsetFactoryForManager()
###

###
#    \fn virtual void QtAbstractPropertyBrowser::itemInserted(insertedItem,
#        precedingItem) = 0
#
#    This function is called to update the widget whenever a property
#    is inserted or added to the property browser, passing pointers to
#    the \a insertedItem of property and the specified
#    \a precedingItem as parameters.
#
#    If \a precedingItem is 0, the \a insertedItem was put at:
#    the beginning of its parent item's list of subproperties. If
#    the parent of \a insertedItem is 0, the \a insertedItem was added as a top
#    level property of \e this property browser.
#
#    This function must be reimplemented in derived classes. Note that
#    if the \a insertedItem's property has subproperties, this:
#    method will be called for those properties as soon as the current call is finished.
#
#    \sa insertProperty(), addProperty()
###

###
#    \fn virtual void QtAbstractPropertyBrowser::itemRemoved(item) = 0
#
#    This function is called to update the widget whenever a property
#    is removed from the property browser, passing the pointer to the
#    \a item of the property as parameters. The passed \a item is
#    deleted just after this call is finished.
#
#    If the the parent of \a item is 0, the removed \a item was a:
#    top level property in this editor.
#
#    This function must be reimplemented in derived classes. Note that
#    if the removed \a item's property has subproperties, this:
#    method will be called for those properties just before the current call is started.
#
#    \sa removeProperty()
###

###
#    \fn virtual void QtAbstractPropertyBrowser::itemChanged(item) = 0
#
#    This function is called whenever a property's data changes,
#    passing a pointer to the \a item of property as parameter.
#
#    This function must be reimplemented in derived classes in order to
#    update the property browser widget whenever a property's name,
#    tool tip, status tip, "what's this" text, value text or value icon
#    changes.
#
#    Note that if the property browser contains several occurrences of
#    the same property, this method will be called once for each
#    occurrence (with a different item each time).
#
#    \sa QtProperty, items()
###
class QtAbstractPropertyBrowser(QWidget):
    currentItemChangedSignal = pyqtSignal(QtBrowserItem)
    ###
    #    Creates an abstract property browser with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtAbstractPropertyBrowser, self).__init__(parent)

        self.d__ptr = QtAbstractPropertyBrowserPrivate()
        self.d__ptr.q_ptr = self

        self.d__ptr.m_subItems = QList()
        self.d__ptr.m_managerToProperties = QMapList()
        self.d__ptr.m_propertyToParents = QMapList()
        self.d__ptr.m_topLevelPropertyToIndex = QMap()
        self.d__ptr.m_topLevelIndexes = QList()
        self.d__ptr.m_propertyToIndexes = QMapList()
        self.d__ptr.m_currentItem = None

    def insertSubTree(self, property, parentProperty):
        if (self.d__ptr.m_propertyToParents.get(property)):
            # property was already inserted, so its manager is connected
            # and all its children are inserted and theirs managers are connected
            # we just register new parent (parent has to be new).
            self.d__ptr.m_propertyToParents[property].append(parentProperty)
            # don't need to update d__ptr.m_managerToProperties map since
            # d__ptr.m_managerToProperties[manager] already contains property.
            return

        manager = property.propertyManager()
        if not self.d__ptr.m_managerToProperties[manager]:
            # connect manager's signals
            manager.propertyInsertedSignal.connect(self.slotPropertyInserted)
            manager.propertyRemovedSignal.connect(self.slotPropertyRemoved)
            manager.propertyDestroyedSignal.connect(self.slotPropertyDestroyed)
            manager.propertyChangedSignal.connect(self.slotPropertyDataChanged)

        self.d__ptr.m_managerToProperties[manager].append(property)
        self.d__ptr.m_propertyToParents[property].append(parentProperty)

        for subProperty in property.subProperties():
            self.insertSubTree(subProperty, property)

    def removeSubTree(self, property, parentProperty):
        if (not self.d__ptr.m_propertyToParents.get(property)):
            # ASSERT
            return

        self.d__ptr.m_propertyToParents[property].removeAll(parentProperty)
        if len(self.d__ptr.m_propertyToParents[property]) > 0:
            return

        self.d__ptr.m_propertyToParents.remove(property)
        manager = property.propertyManager()
        self.d__ptr.m_managerToProperties[manager].removeAll(property)
        if not self.d__ptr.m_managerToProperties[manager]:
            # disconnect manager's signals
            manager.propertyInsertedSignal.disconnect(self.slotPropertyInserted)
            manager.propertyRemovedSignal.disconnect(self.slotPropertyRemoved)
            manager.propertyDestroyedSignal.disconnect(self.slotPropertyDestroyed)
            manager.propertyChangedSignal.disconnect(self.slotPropertyDataChanged)
            self.d__ptr.m_managerToProperties.remove(manager)

        for subProperty in property.subProperties():
            self.removeSubTree(subProperty, property)

    def createBrowserIndexes(self, property, parentProperty, afterProperty):
        parentToAfter = QMap()
        if afterProperty:
            indexes = self.d__ptr.m_propertyToIndexes.get(afterProperty)
            if not indexes:
                return

            for idx in indexes:
                parentIdx = idx.parent()
                if ((parentProperty and parentIdx and parentIdx.property() == parentProperty) or (not parentProperty and not parentIdx)):
                    parentToAfter[idx.parent()] = idx
        elif parentProperty:
            indexes = self.d__ptr.m_propertyToIndexes.get(parentProperty)
            if not indexes:
                return
                
            for idx in indexes:
                parentToAfter[idx] = 0
        else:
            parentToAfter[0] = 0

        for it in parentToAfter.keys():
            self.createBrowserIndex(property, it, parentToAfter[it])

    def createBrowserIndex(self, property, parentIndex, afterIndex):
        newIndex = QtBrowserItem(self, property, parentIndex)
        if (parentIndex):
            parentIndex.d__ptr.addChild(newIndex, afterIndex)
        else:
            self.d__ptr.m_topLevelPropertyToIndex[property] = newIndex
            self.d__ptr.m_topLevelIndexes.insert(self.d__ptr.m_topLevelIndexes.indexOf(afterIndex) + 1, newIndex)

        if not self.d__ptr.m_propertyToIndexes.get(property):
            self.d__ptr.m_propertyToIndexes[property] = QList()
        self.d__ptr.m_propertyToIndexes[property].append(newIndex)
        self.itemInserted(newIndex, afterIndex)
        subItems = property.subProperties()
        afterChild = 0
        for child in subItems:
            afterChild = self.createBrowserIndex(child, newIndex, afterChild)

        return newIndex

    def removeBrowserIndexes(self, property, parentProperty):
        toRemove = QList()
        if not property in self.d__ptr.m_propertyToIndexes.keys():
            return

        indexes = self.d__ptr.m_propertyToIndexes[property]
        for idx in indexes:
            parentIdx = idx.parent()
            if ((parentProperty and parentIdx and parentIdx.property() == parentProperty) or (not parentProperty and not parentIdx)):
                toRemove.append(idx)

        for index in toRemove:
            self.removeBrowserIndex(index)

    def removeBrowserIndex(self, index):
        children = index.children()
        for i in range(len(children)-1, -1, -1):
            self.removeBrowserIndex(children[i])

        self.itemRemoved(index)
        if (index.parent()):
            index.parent().d__ptr.removeChild(index)
        else:
            self.d__ptr.m_topLevelPropertyToIndex.remove(index.property())
            self.d__ptr.m_topLevelIndexes.removeAll(index)

        property = index.property()
        self.d__ptr.m_propertyToIndexes[property].removeAll(index)
        if len(self.d__ptr.m_propertyToIndexes[property])<=0:
            self.d__ptr.m_propertyToIndexes.remove(property)
        del index

    def clearIndex(self, index):
        children = index.children()
        for c in children:
            self.clearIndex(c)

        del index

    def slotPropertyInserted(self, property, parentProperty, afterProperty):
        if (not self.d__ptr.m_propertyToParents.get(parentProperty)):
            return
        if type(afterProperty)==list:
            afterProperty = afterProperty[0]
        self.createBrowserIndexes(property, parentProperty, afterProperty)
        self.insertSubTree(property, parentProperty)
        #self.propertyInserted(property, parentProperty, afterProperty)

    def slotPropertyRemoved(self, property, parentProperty):
        if (not self.d__ptr.m_propertyToParents.get(parentProperty)):
            return
        self.removeSubTree(property, parentProperty) # this line should be probably moved down after propertyRemoved call
        #self.propertyRemoved(property, parentProperty)
        self.removeBrowserIndexes(property, parentProperty)

    def slotPropertyDestroyed(self, property):
        if not property in self.d__ptr.m_subItems:
            return
        self.removeProperty(property)

    def slotPropertyDataChanged(self, property):
        if not property in self.d__ptr.m_propertyToIndexes.keys():
            return

        indexes = self.d__ptr.m_propertyToIndexes[property]
        for idx in indexes:
            self.itemChanged(idx)

        #self.propertyChanged(property)

    ###
    #    Destroys the property browser, and destroys all the items that were
    #    created by this property browser.
    #
    #    Note that the properties that were displayed in the editor are not
    #    deleted since they still can be used in other editors. Neither
    #    does the destructor delete the property managers and editor
    #    factories that were used by this property browser widget unless
    #    this widget was their parent.
    #
    #    \sa QtAbstractPropertyManager::~QtAbstractPropertyManager()
    ###
    def __del__(self):
        indexes = self.topLevelItems()
        for itItem in indexes:
            self.clearIndex(itItem)

    ###
    #    Returns the property browser's list of top level properties.
    #
    #    To traverse the subproperties, use the QtProperty::subProperties()
    #    function.
    #
    #    \sa addProperty(), insertProperty(), removeProperty()
    ###
    def properties(self):
        return self.d__ptr.m_subItems

    ###
    #    Returns the property browser's list of all items associated
    #    with the given \a property.
    #
    #    There is one item per instance of the property in the browser.
    #
    #    \sa topLevelItem()
    ###

    def items(self, property):
        return self.d__ptr.m_propertyToIndexes[property]

    ###
    #    Returns the top-level items associated with the given \a property.
    #
    #    Returns 0 if \a property wasn't inserted into this property
    #    browser or isn't a top-level one.
    #
    #    \sa topLevelItems(), items()
    ###

    def topLevelItem(self, property):
        return self.d__ptr.m_topLevelPropertyToIndex[property]

    ###
    #    Returns the list of top-level items.
    #
    #    \sa topLevelItem()
    ###

    def topLevelItems(self):
        return self.d__ptr.m_topLevelIndexes

    ###
    #    Removes all the properties from the editor, but does not delete
    #    them since they can still be used in other editors.
    #
    #    \sa removeProperty(), QtAbstractPropertyManager::clear()
    ###
    def clear(self):
        subList = self.properties()
        for x in range(len(subList)-1, -1, -1):
            self.removeProperty(subList[-1])

    ###
    #    Appends the given \a property (and its subproperties) to the
    #    property browser's list of top level properties. Returns the item
    #    created by property browser which is associated with the \a property.
    #    In order to get all children items created by the property
    #    browser in this call, the returned item should be traversed.
    #
    #    If the specified \a property is already added, this function does:
    #    nothing and returns 0.
    #
    #    \sa insertProperty(), QtProperty::addSubProperty(), properties()
    ###
    def addProperty(self, property):
        afterProperty = 0
        if len(self.d__ptr.m_subItems) > 0:
            afterProperty = self.d__ptr.m_subItems[-1]
        return self.insertProperty(property, afterProperty)

    ###
    #    \fn QtAbstractPropertyBrowser::insertProperty(property,
    #            afterProperty)
    #
    #    Inserts the given \a property (and its subproperties) after
    #    the specified \a afterProperty in the browser's list of top
    #    level properties. Returns item created by property browser which
    #    is associated with the \a property. In order to get all children items
    #    created by the property browser in this call returned item should be traversed.
    #
    #    If the specified \a afterProperty is 0, the given \a property is:
    #    inserted at the beginning of the list.  If \a property is
    #    already inserted, this function does nothing and returns 0.
    #
    #    \sa addProperty(), QtProperty::insertSubProperty(), properties()
    ###
    def insertProperty(self, property, afterProperty):
        if (not property):
            return 0

        # if item is already inserted in this item then cannot add.
        pendingList = self.properties()
        pos = 0
        newPos = 0
        while (pos < len(pendingList)):
            prop = pendingList[pos]
            if (prop == property):
                return 0
            if (prop == afterProperty):
                newPos = pos + 1

            pos += 1

        self.createBrowserIndexes(property, 0, afterProperty)

        # traverse inserted subtree and connect to manager's signals
        self.insertSubTree(property, 0)

        self.d__ptr.m_subItems.insert(newPos, property)
        #propertyInserted(property, 0, properAfterProperty)
        return self.topLevelItem(property)

    ###
    #    Removes the specified \a property (and its subproperties) from the
    #    property browser's list of top level properties. All items
    #    that were associated with the given \a property and its children
    #    are deleted.
    #
    #    Note that the properties are \e not deleted since they can still
    #    be used in other editors.
    #
    #    \sa clear(), QtProperty::removeSubProperty(), properties()
    ###
    def removeProperty(self, property):
        if (not property):
            return

        pendingList = self.properties()
        pos = 0
        while (pos < len(pendingList)):
            if (pendingList[pos] == property):
                self.d__ptr.m_subItems.removeAt(pos) #perhaps this two lines
                self.removeSubTree(property, 0) #should be moved down after propertyRemoved call.
                #propertyRemoved(property, 0)

                self.removeBrowserIndexes(property, 0)

                # when item is deleted, item will call removeItem for top level items,
                # and itemRemoved for nested items.

                return

            pos += 1

    ###
    #    Creates an editing widget (with the given \a parent) for the given
    #    \a property according to the previously established associations
    #    between property managers and editor factories.
    #
    #    If the property is created by a property manager which was not:
    #    associated with any of the existing factories in \e this property
    #    editor, the function returns 0.
    #
    #    To make a property editable in the property browser, the
    #    createEditor() function must be called to provide the
    #    property with a suitable editing widget.
    #
    #    Reimplement this function to provide additional decoration for the
    #    editing widgets created by the installed factories.
    #
    #    \sa setFactoryForManager()
    ###
    def createEditor(self, property, parent):
        factory = 0
        manager = property.propertyManager()

        pb = m_viewToManagerToFactory().get(self)
        if pb:
            factory = pb.get(manager)

        if (not factory):
            return 0
        return factory.findEditor(property, parent)

    def addFactory(self, abstractManager, abstractFactory):
        connectNeeded = False
        if (not abstractManager in m_managerToFactoryToViews().keys()) or (not abstractFactory in m_managerToFactoryToViews()[abstractManager]):
            connectNeeded = True
        elif self in m_managerToFactoryToViews()[abstractManager][abstractFactory]:
            return connectNeeded

        if (self in m_viewToManagerToFactory().keys()) and (abstractManager in m_viewToManagerToFactory()[self]):
            self.unsetFactoryForManager(abstractManager)

        m_managerToFactoryToViews()[abstractManager][abstractFactory].append(self)
        m_viewToManagerToFactory()[self][abstractManager] = abstractFactory

        return connectNeeded

    ###
    #    Removes the association between the given \a manager and the
    #    factory bound to it, automatically calling the
    #    QtAbstractEditorFactory::removePropertyManager() function if necessary.
    #
    #    \sa setFactoryForManager()
    ###
    def unsetFactoryForManager(self, manager):
        if (not self in m_viewToManagerToFactory().keys()) or (not manager in m_viewToManagerToFactory()[self]):
            return

        abstractFactory = m_viewToManagerToFactory()[self][manager]
        m_viewToManagerToFactory()[self].pop(manager)
        if not m_viewToManagerToFactory()[self]:
            m_viewToManagerToFactory().remove(self)

        m_managerToFactoryToViews()[manager][abstractFactory][self].clear()
        if len(m_managerToFactoryToViews()[manager][abstractFactory])<=0:
            m_managerToFactoryToViews().remove(manager)[abstractFactory]
            abstractFactory.breakConnection(manager)
            if not m_managerToFactoryToViews()[manager]:
                m_managerToFactoryToViews().remove(manager)

    ###
    #    Returns the current item in the property browser.
    #
    #    \sa setCurrentItem()
    ###
    def currentItem(self):
        return self.d__ptr.m_currentItem

    ###
    #    Sets the current item in the property browser to \a item.
    #
    #    \sa currentItem(), currentItemChanged()
    ###
    def setCurrentItem(self, item):
        oldItem = self.d__ptr.m_currentItem
        self.d__ptr.m_currentItem = item
        if (oldItem != item):
            if item==0 or item==None:
                item = QtBrowserItem()
            self.currentItemChangedSignal.emit(item)

    def setFactoryForManager(self, manager, factory):
        if self.addFactory(manager, factory):
            factory.addPropertyManager(manager)

class QtAbstractEditorFactoryBase(QObject):
    def __init__(self, parent=None):
        super(QtAbstractEditorFactoryBase, self).__init__(parent)

    def createEditor(self, property, parent):
        pass

    def breakConnection(self, manager):
        pass

class QtAbstractEditorFactory(QObject):
    def __init__(self,parent=None):
        super(QtAbstractEditorFactory,self).__init__(parent)
        self.m_managers = set()

    def findEditor(self, property, parent):
        for manager in self.m_managers:
            if (manager == property.propertyManager()):
                return self.createEditor(manager, property, parent)

        return 0

    def addPropertyManager(self, manager):
        if manager in self.m_managers:
            return
        self.m_managers.add(manager)
        self.connectPropertyManager(manager)
        manager.destroyed.connect(self.managerDestroyed)

    def removePropertyManager(self, manager):
        if not manager in self.m_managers:
            return
        manager.destroyed.disconnect(self.managerDestroyed)
        self.disconnectPropertyManager(manager)
        self.m_managers.remove(manager)

    def propertyManagers(self):
        return self.m_managers

    def propertyManager(self, property):
        manager = property.propertyManager()
        for m in self.m_managers:
            if (m == manager):
                return m
        return 0

    def managerDestroyed(self, manager):
        for m in self.m_managers:
            if (m == manager):
                self.m_managers.remove(m)
                return

    def breakConnection(self, manager):
        for m in self.m_managers:
            if (m == manager):
                self.removePropertyManager(m)
                return

