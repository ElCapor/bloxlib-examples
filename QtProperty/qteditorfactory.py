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
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
##
## $QT_END_LICENSE$
##
#############################################################################

from qtpropertybrowserutils import (
    QtKeySequenceEdit, 
    QtBoolEdit,
    QtPropertyBrowserUtils
    )
from pyqtcore import QMapList, QList, QMap
from qtpropertybrowser import QtAbstractEditorFactory
from qtpropertymanager import QtEnumPropertyManager, cursorDatabase
from PyQt5.QtCore import Qt, QEvent, pyqtSignal
from PyQt5.QtWidgets import (
    QStyle,
    QWidget,
    QSpinBox,
    QAction,
    QScrollBar,
    QComboBox,
    QLineEdit,
    QDateTimeEdit,
    QHBoxLayout,
    QApplication,
    QSizePolicy,
    QColorDialog,
    QFontDialog,
    QSpacerItem,
    QStyleOption,
    QSlider,
    QDoubleSpinBox,
    QDateEdit,
    QTimeEdit,
    QToolButton,
    QLabel

    )
from PyQt5.QtGui import (
    QPainter,
    QRegExpValidator,
    QKeySequence,
    QCursor,
    QBrush,
    QIcon,
    QFont,
    QColor)

# Set a hard coded left margin to account for the indentation
# of the tree view icon when switching to an editor
def setupTreeViewEditorMargin(lt):
    DecorationMargin = 4
    if (QApplication.layoutDirection() == Qt.LeftToRight):
        lt.setContentsMargins(DecorationMargin, 0, 0, 0)
    else:
        lt.setContentsMargins(0, 0, DecorationMargin, 0)

g_editorFactoryWidget = None

def registerEditorFactory(classType, widgetType):
    global g_editorFactoryWidget
    if not g_editorFactoryWidget:
        g_editorFactoryWidget = QMap()
    g_editorFactoryWidget[classType] = widgetType

# ---------- EditorFactoryPrivate:
# Base class for editor factory private classes. Manages mapping of properties to editors and vice versa.
class EditorFactoryPrivate():
    def __init__(self):
        self.q_ptr = None

    m_createdEditors = QMap()
    m_editorToProperty = QMap()

    def createEditor(self, property, parent):
        editorClass = g_editorFactoryWidget.get(type(self))
        if editorClass:
            editor = editorClass(parent)
        self.initializeEditor(property, editor)
        self.lastEditor = editor
        return editor

    def initializeEditor(self, property, editor):
        if not self.m_createdEditors.get(property):
            self.m_createdEditors[property] = QList()
        self.m_createdEditors[property].append(editor)
        self.m_editorToProperty[editor] = property

    def slotEditorDestroyed(self, obj):
        if obj in self.m_editorToProperty.keys():
            property = self.m_editorToProperty[obj]
            pit = self.m_createdEditors.get(property)
            if pit:
                pit.removeAll(obj)

                if len(pit)==0:
                    self.m_createdEditors.erase(property)

            self.m_editorToProperty.erase(obj)
            return

class QtSpinBoxFactoryPrivate(EditorFactoryPrivate):
    def __init__(self):
        self.q_ptr = None

    def slotPropertyChanged(self, property, value):
        editors = self.m_createdEditors.get(property)
        if not editors:
            return
        for editor in editors:
            if (editor != value):
                editor.blockSignals(True)
                editor.setValue(value)
                editor.blockSignals(False)

    def slotRangeChanged(self, property, min, max):
        editors = self.m_createdEditors.get(property)
        if editors is None:
            return

        manager = self.q_ptr.propertyManager(property)
        if not manager:
            return

        for editor in editors:
            editor.blockSignals(True)
            editor.setRange(min, max)
            editor.setValue(manager.value(property))
            editor.blockSignals(False)

    def slotSingleStepChanged(self, property, step):
        editors = self.m_createdEditors.get(property)
        if editors is None:
            return
        for editor in editors:
            editor.blockSignals(True)
            editor.setSingleStep(step)
            editor.blockSignals(False)

    def slotReadOnlyChanged(self,  property, readOnly):
        editors = self.m_createdEditors.get(property)
        if editors is None:
            return

        manager = self.q_ptr.propertyManager(property)
        if not manager:
            return

        for editor in editors:
            editor.blockSignals(True)
            editor.setReadOnly(readOnly)
            editor.blockSignals(False)

    def slotSetValue(self, value):
        object = self.q_ptr.sender()
        for itEditor in self.m_editorToProperty.keys():
            if itEditor == object:
                property = self.m_editorToProperty[itEditor]
                manager = self.q_ptr.propertyManager(property)
                if (not manager):
                    return
                manager.setValue(property, value)
                return

registerEditorFactory(QtSpinBoxFactoryPrivate, QSpinBox)

###
#    \class QtSpinBoxFactory
#
#    \brief The QtSpinBoxFactory class provides QSpinBox widgets for
#    properties created by QtIntPropertyManager objects.
#
#    \sa QtAbstractEditorFactory, QtIntPropertyManager
###
class QtSpinBoxFactory(QtAbstractEditorFactory):
    ###
    #    Creates a factory with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtSpinBoxFactory, self).__init__(parent)

        self.d_ptr = QtSpinBoxFactoryPrivate()
        self.d_ptr.q_ptr = self

    ###
    #    Destroys this factory, and all the widgets it has created.
    ###
    def __del__(self):
        self.d_ptr.m_editorToProperty.clear()
        del self.d_ptr

    ###
    #    \internal
    #
    #    Reimplemented from the QtAbstractEditorFactory class.
    ###
    def connectPropertyManager(self, manager):
        manager.valueChangedSignal.connect(self.d_ptr.slotPropertyChanged)
        manager.rangeChangedSignal.connect(self.d_ptr.slotRangeChanged)
        manager.singleStepChangedSignal.connect(self.d_ptr.slotSingleStepChanged)
        manager.readOnlyChangedSignal.connect(self.d_ptr.slotReadOnlyChanged)

    ###
    #    \internal
    #
    #    Reimplemented from the QtAbstractEditorFactory class.
    ###
    def createEditor(self, manager, property, parent):
        editor = self.d_ptr.createEditor(property, parent)
        editor.setSingleStep(manager.singleStep(property))
        editor.setRange(manager.minimum(property), manager.maximum(property))
        editor.setValue(manager.value(property))
        editor.setKeyboardTracking(False)
        editor.setReadOnly(manager.isReadOnly(property))

        editor.valueChanged.connect(self.d_ptr.slotSetValue)
        editor.destroyed.connect(self.d_ptr.slotEditorDestroyed)
        return editor

    ###
    #    \internal
    #
    #    Reimplemented from the QtAbstractEditorFactory class.
    ###
    def disconnectPropertyManager(self, manager):
        manager.valueChangedSignal.disconnect(self.d_ptr.slotPropertyChanged)
        manager.rangeChangedSignal.disconnect(self.d_ptr.slotRangeChanged)
        manager.singleStepChangedSignal.disconnect(self.d_ptr.slotSingleStepChanged)
        manager.readOnlyChangedSignal.disconnect(self.d_ptr.slotReadOnlyChanged)

class QtSliderFactoryPrivate(EditorFactoryPrivate):
    def __init__(self):
        self.q_ptr = None

    def slotPropertyChanged(self, property, value):
        editors = self.m_createdEditors.get(property)
        if not editors:
            return

        for editor in editors:
            editor.blockSignals(True)
            editor.setValue(value)
            editor.blockSignals(False)

    def slotRangeChanged(self, property, min, max):
        editors = self.m_createdEditors.get(property)
        if not editors:
            return

        manager = self.q_ptr.propertyManager(property)
        if (not manager):
            return

        for editor in editors:
            editor.blockSignals(True)
            editor.setRange(min, max)
            editor.setValue(manager.value(property))
            editor.blockSignals(False)

    def slotSingleStepChanged(self, property, step):
        editors = self.m_createdEditors.get(property)
        if not editors:
            return

        for editor in editors:
            editor.blockSignals(True)
            editor.setSingleStep(step)
            editor.blockSignals(False)

    def slotSetValue(self, value):
        object = self.q_ptr.sender()
        for itEditor in self.m_editorToProperty.keys():
            if (itEditor == object):
                property = self.m_editorToProperty[itEditor]
                manager = self.q_ptr.propertyManager(property)
                if (not manager):
                    return
                manager.setValue(property, value)
                return

registerEditorFactory(QtSliderFactoryPrivate, QSlider)

###
#    \class QtSliderFactory
#
#    \brief The QtSliderFactory class provides QSlider widgets for
#    properties created by QtIntPropertyManager objects.
#
#    \sa QtAbstractEditorFactory, QtIntPropertyManager
###
class QtSliderFactory(QtAbstractEditorFactory):
    ###
    #    Creates a factory with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtSliderFactory, self).__init__(parent)

        self.d_ptr = QtSliderFactoryPrivate()
        self.d_ptr.q_ptr = self

    ###
    #    Destroys this factory, and all the widgets it has created.
    ###
    def __del__(self):
        self.d_ptr.m_editorToProperty.clear()
        del self.d_ptr

    ###
    #    \internal
    #
    #    Reimplemented from the QtAbstractEditorFactory class.
    ###
    def connectPropertyManager(self, manager):
        manager.valueChangedSignal.connect(self.d_ptr.slotPropertyChanged)
        manager.rangeChangedSignal.connect(self.d_ptr.slotRangeChanged)
        manager.singleStepChangedSignal.connect(self.d_ptr.slotSingleStepChanged)

    ###
    #    \internal
    #
    #    Reimplemented from the QtAbstractEditorFactory class.
    ###
    def createEditor(self, manager, property, parent):
        editor = QSlider(Qt.Horizontal, parent)
        self.d_ptr.initializeEditor(property, editor)
        editor.setSingleStep(manager.singleStep(property))
        editor.setRange(manager.minimum(property), manager.maximum(property))
        editor.setValue(manager.value(property))

        editor.valueChanged.connect(self.d_ptr.slotSetValue)
        editor.destroyed.connect(self.d_ptr.slotEditorDestroyed)
        return editor

    ###
    #    \internal
    #
    #    Reimplemented from the QtAbstractEditorFactory class.
    ###
    def disconnectPropertyManager(self, manager):
        manager.valueChangedSignal.disconnect(self.d_ptr.slotPropertyChanged)
        manager.rangeChangedSignal.disconnect(self.d_ptr.slotRangeChanged)
        manager.singleStepChangedSignal.disconnect(self.d_ptr.slotSingleStepChanged)

class QtScrollBarFactoryPrivate(EditorFactoryPrivate):
    def __init__(self):
        self.q_ptr = None

    def slotPropertyChanged(self, property, value):
        editors = self.m_createdEditors.get(property)
        if not editors:
            return

        for editor in editors:
            editor.blockSignals(True)
            editor.setValue(value)
            editor.blockSignals(False)

    def slotRangeChanged(self, property, min, max):
        editors = self.m_createdEditors.get(property)
        if not editors:
            return

        manager = self.q_ptr.propertyManager(property)
        if (not manager):
            return

        for editor in editors:
            editor.blockSignals(True)
            editor.setRange(min, max)
            editor.setValue(manager.value(property))
            editor.blockSignals(False)

    def slotSingleStepChanged(self, property, step):
        editors = self.m_createdEditors.get(property)
        if not editors:
            return

        for editor in editors:
            editor.blockSignals(True)
            editor.setSingleStep(step)
            editor.blockSignals(False)

    def slotSetValue(self, value):
        object = self.q_ptr.sender()
        for itEditor in self.m_editorToProperty.keys():
            if (itEditor == object):
                property = self.m_editorToProperty[itEditor]
                manager = self.q_ptr.propertyManager(property)
                if (not manager):
                    return
                manager.setValue(property, value)
                return

registerEditorFactory(QtScrollBarFactoryPrivate, QScrollBar)

###
#    \class QtScrollBarFactory
#
#    \brief The QtScrollBarFactory class provides QScrollBar widgets for
#    properties created by QtIntPropertyManager objects.
#
#    \sa QtAbstractEditorFactory, QtIntPropertyManager
###
class QtScrollBarFactory(QtAbstractEditorFactory):
    ###
    #    Creates a factory with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtScrollBarFactory, self).__init__(parent)

        self.d_ptr = QtScrollBarFactoryPrivate()
        self.d_ptr.q_ptr = self

    ###
    #    Destroys this factory, and all the widgets it has created.
    ###
    def __del__(self):
        self.d_ptr.m_editorToProperty.clear()
        del self.d_ptr

    ###
    #    \internal
    #
    #    Reimplemented from the QtAbstractEditorFactory class.
    ###
    def connectPropertyManager(self, manager):
        manager.valueChangedSignal.connect(self.d_ptr.slotPropertyChanged)
        manager.rangeChangedSignal.connect(self.d_ptr.slotRangeChanged)
        manager.singleStepChangedSignal.connect(self.d_ptr.slotSingleStepChanged)

    ###
    #    \internal
    #
    #    Reimplemented from the QtAbstractEditorFactory class.
    ###
    def createEditor(self, manager, property, parent):
        editor = QScrollBar(Qt.Horizontal, parent)
        self.d_ptr.initializeEditor(property, editor)
        editor.setSingleStep(manager.singleStep(property))
        editor.setRange(manager.minimum(property), manager.maximum(property))
        editor.setValue(manager.value(property))
        editor.valueChanged.connect(self.d_ptr.slotSetValue)
        editor.destroyed.connect(self.d_ptr.slotEditorDestroyed)
        return editor

    ###
    #    \internal
    #
    #    Reimplemented from the QtAbstractEditorFactory class.
    ###
    def disconnectPropertyManager(self, manager):
        manager.valueChangedSignal.disconnect(self.d_ptr.slotPropertyChanged)
        manager.rangeChangedSignal.disconnect(self.d_ptr.slotRangeChanged)
        manager.singleStepChangedSignal.disconnect(self.d_ptr.slotSingleStepChanged)

class QtCheckBoxFactoryPrivate(EditorFactoryPrivate):
    def __init__(self):
        self.q_ptr = None

    def slotPropertyChanged(self, property, value):
        editors = self.m_createdEditors.get(property)
        if not editors:
            return

        for editor in editors:
            editor.blockCheckBoxSignals(True)
            editor.setChecked(value)
            editor.blockCheckBoxSignals(False)

    def slotTextVisibleChanged(self, property, textVisible):
        editors = self.m_createdEditors.get(property)
        if not editors:
            return

        manager = self.q_ptr.propertyManager(property)
        if (not manager):
            return

        for editor in editors:
            editor.setTextVisible(textVisible)

    def slotSetValue(self, value):
        object = self.q_ptr.sender()
        property = self.m_editorToProperty.get(object)
        if property:
            manager = self.q_ptr.propertyManager(property)
            if (not manager):
                return
            manager.setValue(property, value)
            return

registerEditorFactory(QtCheckBoxFactoryPrivate, QtBoolEdit)

###
#    \class QtCheckBoxFactory
#
#    \brief The QtCheckBoxFactory class provides QCheckBox widgets for
#    properties created by QtBoolPropertyManager objects.
#
#    \sa QtAbstractEditorFactory, QtBoolPropertyManager
###
class QtCheckBoxFactory(QtAbstractEditorFactory):
    ###
    #    Creates a factory with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtCheckBoxFactory, self).__init__(parent)

        self.d_ptr = QtCheckBoxFactoryPrivate()
        self.d_ptr.q_ptr = self

    ###
    #    Destroys this factory, and all the widgets it has created.
    ###
    def __del__(self):
        self.d_ptr.m_editorToProperty.clear()
        del self.d_ptr

    ###
    #    \internal
    #
    #    Reimplemented from the QtAbstractEditorFactory class.
    ###
    def connectPropertyManager(self, manager):
        manager.valueChangedSignal.connect(self.d_ptr.slotPropertyChanged)
        manager.textVisibleChangedSignal.connect(self.d_ptr.slotTextVisibleChanged)

    ###
    #    \internal
    #
    #    Reimplemented from the QtAbstractEditorFactory class.
    ###
    def createEditor(self, manager, property, parent):
        editor = self.d_ptr.createEditor(property, parent)
        editor.setChecked(manager.value(property))
        editor.setTextVisible(manager.textVisible(property))

        editor.toggledSignal.connect(self.d_ptr.slotSetValue)
        editor.destroyed.connect(self.d_ptr.slotEditorDestroyed)
        return editor

    ###
    #    \internal
    #
    #    Reimplemented from the QtAbstractEditorFactory class.
    ###
    def disconnectPropertyManager(self, manager):
        manager.valueChangedSignal.disconnect(self.d_ptr.slotPropertyChanged)
        manager.textVisibleChangedSignal.disconnect(self.d_ptr.slotTextVisibleChanged)

class QtDoubleSpinBoxFactoryPrivate(EditorFactoryPrivate):
    def __init__(self):
        self.q_ptr = None

    def slotPropertyChanged(self, property, value):
        editors = self.m_createdEditors[property]
        if editors is None:
            return
        for editor in editors:
            if (editor.value() != value):
                editor.blockSignals(True)
                editor.setValue(value)
                editor.blockSignals(False)

    def slotRangeChanged(self, property, min, max):
        editors = self.m_createdEditors.get(property)
        if not editors:
            return

        manager = self.q_ptr.propertyManager(property)
        if (not manager):
            return

        editors = self.m_createdEditors[property]
        for editor in editors:
            editor.blockSignals(True)
            editor.setRange(min, max)
            editor.setValue(manager.value(property))
            editor.blockSignals(False)

    def slotSingleStepChanged(self, property, step):
        editors = self.m_createdEditors.get(property)
        if not editors:
            return

        manager = self.q_ptr.propertyManager(property)
        if (not manager):
            return

        editors = self.m_createdEditors[property]

        for editor in editors:
            editor.blockSignals(True)
            editor.setSingleStep(step)
            editor.blockSignals(False)

    def slotReadOnlyChanged(self,  property, readOnly):
        editors = self.m_createdEditors.get(property)
        if not editors:
            return

        manager = self.q_ptr.propertyManager(property)
        if (not manager):
            return

        for editor in editors:
            editor.blockSignals(True)
            editor.setReadOnly(readOnly)
            editor.blockSignals(False)

    def slotDecimalsChanged(self, property, prec):
        editors = self.m_createdEditors.get(property)
        if not editors:
            return

        manager = self.q_ptr.propertyManager(property)
        if (not manager):
            return

        editors = self.m_createdEditors[property]

        for editor in editors:
            editor.blockSignals(True)
            editor.setDecimals(prec)
            editor.setValue(manager.value(property))
            editor.blockSignals(False)

    def slotSetValue(self, value):
        object = self.q_ptr.sender()
        for itEditor in self.m_editorToProperty.keys():
            if (itEditor == object):
                property = self.m_editorToProperty[itEditor]
                manager = self.q_ptr.propertyManager(property)
                if (not manager):
                    return
                manager.setValue(property, value)
                return

registerEditorFactory(QtDoubleSpinBoxFactoryPrivate, QDoubleSpinBox)

### \class QtDoubleSpinBoxFactory

#   \brief The QtDoubleSpinBoxFactory class provides QDoubleSpinBox
#   widgets for properties created by QtDoublePropertyManager objects.

#   \sa QtAbstractEditorFactory, QtDoublePropertyManager
###
class QtDoubleSpinBoxFactory(QtAbstractEditorFactory):
    ###
    #   Creates a factory with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtDoubleSpinBoxFactory, self).__init__(parent)

        self.d_ptr = QtDoubleSpinBoxFactoryPrivate()
        self.d_ptr.q_ptr = self

    ###
    #   Destroys this factory, and all the widgets it has created.
    ###
    def __del__(self):
        self.d_ptr.m_editorToProperty.clear()
        del self.d_ptr

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def connectPropertyManager(self, manager):
        manager.valueChangedSignal.connect(self.d_ptr.slotPropertyChanged)
        manager.rangeChangedSignal.connect(self.d_ptr.slotRangeChanged)
        manager.singleStepChangedSignal.connect(self.d_ptr.slotSingleStepChanged)
        manager.decimalsChangedSignal.connect(self.d_ptr.slotDecimalsChanged)
        manager.readOnlyChangedSignal.connect(self.d_ptr.slotReadOnlyChanged)

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def createEditor(self, manager, property, parent):
        editor = self.d_ptr.createEditor(property, parent)
        editor.setSingleStep(manager.singleStep(property))
        editor.setDecimals(manager.decimals(property))
        editor.setRange(manager.minimum(property), manager.maximum(property))
        editor.setValue(manager.value(property))
        editor.setKeyboardTracking(False)
        editor.setReadOnly(manager.isReadOnly(property))

        editor.valueChanged.connect(self.d_ptr.slotSetValue)
        editor.destroyed.connect(self.d_ptr.slotEditorDestroyed)
        return editor

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def disconnectPropertyManager(self, manager):
        manager.valueChangedSignal.disconnect(self.d_ptr.slotPropertyChanged)
        manager.rangeChangedSignal.disconnect(self.d_ptr.slotRangeChanged)
        manager.singleStepChangedSignal.disconnect(self.d_ptr.slotSingleStepChanged)
        manager.decimalsChangedSignal.disconnect(self.d_ptr.slotDecimalsChanged)
        manager.readOnlyChangedSignal.disconnect(self.d_ptr.slotReadOnlyChanged)

class QtLineEditFactoryPrivate(EditorFactoryPrivate):
    def __init__(self):
        self.q_ptr = None

    def slotPropertyChanged(self, property, value):
        editors = self.m_createdEditors.get(property)
        if not editors:
            return

        for editor in editors:
            if (editor.text() != value):
                editor.blockSignals(True)
                editor.setText(value)
                editor.blockSignals(False)

    def slotRegExpChanged(self, property, regExp):
        editors = self.m_createdEditors.get(property)
        if not editors:
            return

        manager = self.q_ptr.propertyManager(property)
        if (not manager):
            return

        for editor in editors:
            editor.blockSignals(True)
            oldValidator = editor.validator()
            newValidator = 0
            if (regExp.isValid()):
                newValidator = QRegExpValidator(regExp, editor)

            editor.setValidator(newValidator)
            if (oldValidator):
                del oldValidator
            editor.blockSignals(False)

    def slotEchoModeChanged(self, property, echoMode):
        editors = self.m_createdEditors.get(property)
        if not editors:
            return

        manager = self.q_ptr.propertyManager(property)
        if (not manager):
            return

        for editor in editors:
            editor.blockSignals(True)
            editor.setEchoMode(echoMode)
            editor.blockSignals(False)

    def slotReadOnlyChanged(self,  property, readOnly):
        editors = self.m_createdEditors.get(property)
        if not editors:
            return

        manager = self.q_ptr.propertyManager(property)
        if (not manager):
            return

        for editor in editors:
            editor.blockSignals(True)
            editor.setReadOnly(readOnly)
            editor.blockSignals(False)

    def slotSetValue(self, value):
        object = self.q_ptr.sender()
        for itEditor in self.m_editorToProperty.keys():
            if (itEditor == object):
                property = self.m_editorToProperty[itEditor]
                manager = self.q_ptr.propertyManager(property)
                if (not manager):
                    return
                manager.setValue(property, value)
                return

registerEditorFactory(QtLineEditFactoryPrivate, QLineEdit)

###
#    \class QtLineEditFactory

#    \brief The QtLineEditFactory class provides QLineEdit widgets for
#    properties created by QtStringPropertyManager objects.

#    \sa QtAbstractEditorFactory, QtStringPropertyManager
###
class QtLineEditFactory(QtAbstractEditorFactory):
    ###
    #    Creates a factory with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtLineEditFactory, self).__init__(parent)

        self.d_ptr = QtLineEditFactoryPrivate()
        self.d_ptr.q_ptr = self

    ###
    #   Destroys this factory, and all the widgets it has created.
    ###
    def __del__(self):
        self.d_ptr.m_editorToProperty.clear()
        del self.d_ptr

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def connectPropertyManager(self, manager):
        manager.valueChangedSignal.connect(self.d_ptr.slotPropertyChanged)
        manager.regExpChangedSignal.connect(self.d_ptr.slotRegExpChanged)
        manager.echoModeChangedSignal.connect(self.d_ptr.slotEchoModeChanged)
        manager.readOnlyChangedSignal.connect(self.d_ptr.slotReadOnlyChanged)

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def createEditor(self, manager, property, parent):
        editor = self.d_ptr.createEditor(property, parent)
        editor.setEchoMode(manager.echoMode(property))
        editor.setReadOnly(manager.isReadOnly(property))
        regExp = manager.regExp(property)
        if (regExp.isValid()):
            validator = QRegExpValidator(regExp, editor)
            editor.setValidator(validator)

        editor.setText(manager.value(property))

        editor.textChanged.connect(self.d_ptr.slotSetValue)
        editor.destroyed.connect(self.d_ptr.slotEditorDestroyed)
        return editor

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def disconnectPropertyManager(self, manager):
        manager.valueChangedSignal.disconnect(self.d_ptr.slotPropertyChanged)
        manager.regExpChangedSignal.disconnect(self.d_ptr.slotRegExpChanged)
        manager.echoModeChangedSignal.disconnect(self.d_ptr.slotEchoModeChanged)
        manager.readOnlyChangedSignal.disconnect(self.d_ptr.slotReadOnlyChanged)

class QtDateEditFactoryPrivate(EditorFactoryPrivate):
    def __init__(self):
        self.q_ptr = None

    def slotPropertyChanged(self, property, value):
        editors = self.m_createdEditors.get(property)
        if not editors:
            return

        for editor in editors:
            editor.blockSignals(True)
            editor.setDate(value)
            editor.blockSignals(False)

    def slotRangeChanged(self, property, min, max):
        editors = self.m_createdEditors.get(property)
        if not editors:
            return

        manager = self.q_ptr.propertyManager(property)
        if (not manager):
            return

        for editor in editors:
            editor.blockSignals(True)
            editor.setDateRange(min, max)
            editor.setDate(manager.value(property))
            editor.blockSignals(False)

    def slotSetValue(self, value):
        object = self.q_ptr.sender()
        for itEditor in self.m_editorToProperty.keys():
            if (itEditor == object):
                property = self.m_editorToProperty[itEditor]
                manager = self.q_ptr.propertyManager(property)
                if (not manager):
                    return
                manager.setValue(property, value)
                return

registerEditorFactory(QtDateEditFactoryPrivate, QDateEdit)
###
#   \class QtDateEditFactory

#   \brief The QtDateEditFactory class provides QDateEdit widgets for
#   properties created by QtDatePropertyManager objects.

#   \sa QtAbstractEditorFactory, QtDatePropertyManager
###
class QtDateEditFactory(QtAbstractEditorFactory):
    ###
    #   Creates a factory with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtDateEditFactory, self).__init__(parent)

        self.d_ptr = QtDateEditFactoryPrivate()
        self.d_ptr.q_ptr = self

    ###
    #   Destroys this factory, and all the widgets it has created.
    ###
    def __del__(self):
        self.d_ptr.m_editorToProperty.clear()
        del self.d_ptr

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def connectPropertyManager(self, manager):
        manager.valueChangedSignal.connect(self.d_ptr.slotPropertyChanged)
        manager.rangeChangedSignal.connect(self.d_ptr.slotRangeChanged)

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def createEditor(self, manager, property, parent):
        editor = self.d_ptr.createEditor(property, parent)
        editor.setCalendarPopup(True)
        editor.setDateRange(manager.minimum(property), manager.maximum(property))
        editor.setDate(manager.value(property))

        editor.dateChanged.connect(self.d_ptr.slotSetValue)
        editor.destroyed.connect(self.d_ptr.slotEditorDestroyed)
        return editor

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def disconnectPropertyManager(self, manager):
        manager.valueChangedSignal.disconnect(self.d_ptr.slotPropertyChanged)
        manager.rangeChangedSignal.disconnect(self.d_ptr.slotRangeChanged)

class QtTimeEditFactoryPrivate(EditorFactoryPrivate):
    def __init__(self):
        self.q_ptr = None

    def slotPropertyChanged(self, property, value):
        editors = self.m_createdEditors.get(property)
        if not editors:
            return

        for editor in editors:
            editor.blockSignals(True)
            editor.setTime(value)
            editor.blockSignals(False)

    def slotSetValue(self, value):
        object = self.q_ptr.sender()
        for itEditor in self.m_editorToProperty.keys():
            if (itEditor == object):
                property = self.m_editorToProperty[itEditor]
                manager = self.q_ptr.propertyManager(property)
                if (not manager):
                    return
                manager.setValue(property, value)
                return

registerEditorFactory(QtTimeEditFactoryPrivate, QTimeEdit)

###
#   \class QtTimeEditFactory

#   \brief The QtTimeEditFactory class provides QTimeEdit widgets for
#   properties created by QtTimePropertyManager objects.

#   \sa QtAbstractEditorFactory, QtTimePropertyManager
###
class QtTimeEditFactory(QtAbstractEditorFactory):
    ###
    #   Creates a factory with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtTimeEditFactory, self).__init__(parent)

        self.d_ptr = QtTimeEditFactoryPrivate()
        self.d_ptr.q_ptr = self

    ###
    #   Destroys this factory, and all the widgets it has created.
    ###
    def __del__(self):
        self.d_ptr.m_editorToProperty.clear()
        del self.d_ptr

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def connectPropertyManager(self, manager):
        manager.valueChangedSignal.connect(self.d_ptr.slotPropertyChanged)

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def createEditor(self, manager, property, parent):
        editor = self.d_ptr.createEditor(property, parent)
        editor.setTime(manager.value(property))

        editor.timeChanged.connect(self.d_ptr.slotSetValue)
        editor.destroyed.connect(self.d_ptr.slotEditorDestroyed)
        return editor

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def disconnectPropertyManager(self, manager):
        manager.valueChangedSignal.disconnect(self.d_ptr.slotPropertyChanged)

class QtDateTimeEditFactoryPrivate(EditorFactoryPrivate):
    def __init__(self):
        self.q_ptr = None

    def slotPropertyChanged(self, property, value):
        editors = self.m_createdEditors.get(property)
        if not editors:
            return

        for editor in editors:
            editor.blockSignals(True)
            editor.setDateTime(value)
            editor.blockSignals(False)

    def slotSetValue(self, value):
        object = self.q_ptr.sender()
        for itEditor in self.m_editorToProperty.keys():
            if (itEditor == object):
                property = self.m_editorToProperty[itEditor]
                manager = self.q_ptr.propertyManager(property)
                if (not manager):
                    return
                manager.setValue(property, value)
                return

registerEditorFactory(QtDateTimeEditFactoryPrivate, QDateTimeEdit)
###
#   \class QtDateTimeEditFactory

#   \brief The QtDateTimeEditFactory class provides QDateTimeEdit
#   widgets for properties created by QtDateTimePropertyManager objects.

#   \sa QtAbstractEditorFactory, QtDateTimePropertyManager
###
class QtDateTimeEditFactory(QtAbstractEditorFactory):
    ###
    #   Creates a factory with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtDateTimeEditFactory, self).__init__(parent)

        self.d_ptr = QtDateTimeEditFactoryPrivate()
        self.d_ptr.q_ptr = self

    ###
    #   Destroys this factory, and all the widgets it has created.
    ###
    def __del__(self):
        self.d_ptr.m_editorToProperty.clear()
        del self.d_ptr

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def connectPropertyManager(self, manager):
        manager.valueChangedSignal.connect(self.d_ptr.slotPropertyChanged)

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def createEditor(self, manager, property, parent):
        editor = self.d_ptr.createEditor(property, parent)
        editor.setDateTime(manager.value(property))

        editor.dateTimeChanged.connect(self.d_ptr.slotSetValue)
        editor.destroyed.connect(self.d_ptr.slotEditorDestroyed)
        return editor

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def disconnectPropertyManager(self, manager):
        manager.valueChangedSignal.disconnect(self.d_ptr.slotPropertyChanged)

class QtKeySequenceEditorFactoryPrivate(EditorFactoryPrivate):
    def __init__(self):
        self.q_ptr = None

    def slotPropertyChanged(self, property, value):
        editors = self.m_createdEditors.get(property)
        if not editors:
            return

        for editor in editors:
            editor.blockSignals(True)
            editor.setKeySequence(value)
            editor.blockSignals(False)

    def slotSetValue(self, value):
        object = self.q_ptr.sender()
        for itEditor in self.m_editorToProperty.keys():
            if (itEditor == object):
                property = self.m_editorToProperty[itEditor]
                manager = self.q_ptr.propertyManager(property)
                if (not manager):
                    return
                manager.setValue(property, value)
                return

registerEditorFactory(QtKeySequenceEditorFactoryPrivate, QtKeySequenceEdit)
###
#   \class QtKeySequenceEditorFactory

#   \brief The QtKeySequenceEditorFactory class provides editor
#   widgets for properties created by QtKeySequencePropertyManager objects.

#   \sa QtAbstractEditorFactory
###
class QtKeySequenceEditorFactory(QtAbstractEditorFactory):
    ###
    #   Creates a factory with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtKeySequenceEditorFactory, self).__init__(parent)

        self.d_ptr = QtKeySequenceEditorFactoryPrivate()
        self.d_ptr.q_ptr = self

    ###
    #   Destroys this factory, and all the widgets it has created.
    ###
    def __del__(self):
        self.d_ptr.m_editorToProperty.clear()
        del self.d_ptr

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def connectPropertyManager(self, manager):
        manager.valueChangedSignal.connect(self.d_ptr.slotPropertyChanged)

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def createEditor(self, manager, property, parent):
        editor = self.d_ptr.createEditor(property, parent)
        editor.setKeySequence(manager.value(property))

        editor.keySequenceChangedSignal.connect(self.d_ptr.slotSetValue)
        editor.destroyed.connect(self.d_ptr.slotEditorDestroyed)
        return editor

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def disconnectPropertyManager(self, manager):
        manager.valueChangedSignal.disconnect(self.d_ptr.slotPropertyChanged)

class QtCharEdit(QWidget):
    valueChangedSignal = pyqtSignal(str)
    def __init__(self, parent=None):
        super(QtCharEdit, self).__init__(parent)

        self.m_lineEdit = QLineEdit(self)
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.m_lineEdit)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.m_lineEdit.installEventFilter(self)
        self.m_lineEdit.setReadOnly(True)
        self.m_lineEdit.setFocusProxy(self)
        self.setFocusPolicy(self.m_lineEdit.focusPolicy())
        self.setAttribute(Qt.WA_InputMethodEnabled)
        self.m_value = ''

    def eventFilter(self, o, e):
        if (o == self.m_lineEdit and e.type() == QEvent.ContextMenu):
            c = (e)
            menu = self.m_lineEdit.createStandardContextMenu()
            actions = menu.actions()
            for action in actions:
                action.setShortcut(QKeySequence())
                actionString = action.text()
                pos = actionString.lastIndexOf('\t')
                if (pos > 0):
                    actionString = actionString.remove(pos, actionString.length() - pos)
                action.setText(actionString)

            actionBefore = 0
            if (len(actions) > 0):
                actionBefore = actions[0]
            clearAction = QAction(self.tr("Clear Char"), menu)
            menu.insertAction(actionBefore, clearAction)
            menu.insertSeparator(actionBefore)
            clearAction.setEnabled(not self.m_value=='')
            clearAction.triggeredSignal.connect(self.d_ptr.slotClearChar)
            menu.exec(c.globalPos())
            del menu
            e.accept()
            return True

        return super(QtCharEdit, self).eventFilter(o, e)

    def slotClearChar(self):
        if (self.m_value == ''):
            return
        self.setValue('')
        self.valueChangedSignal.emit(self.m_value)

    def handleKeyEvent(self, e):
        key = e.key()
        if key in [Qt.Key_Control, Qt.Key_Shift, Qt.Key_Meta, Qt.Key_Alt, Qt.Key_Super_L, Qt.Key_Return]:
            return

        text = e.text()
        if (len(text) != 1):
            return

        c = text[0]
        if (not c.isprintable()):
            return

        if (self.m_value == c):
            return

        self.m_value = c
        if self.m_value=='':
            s = ''
        else:
            s = str(self.m_value)
        self.m_lineEdit.setText(s)
        e.accept()
        self.valueChangedSignal.emit(self.m_value)

    def setValue(self, value):
        if (value == self.m_value):
            return

        self.m_value = value
        if value=='':
            s = ''
        else:
            s = str(value)
        self.m_lineEdit.setText(s)

    def value(self):
        return  self.m_value

    def focusInEvent(self, e):
        self.m_lineEdit.event(e)
        self.m_lineEdit.selectAll()
        super(QtCharEdit, self).focusInEvent(e)

    def focusOutEvent(self, e):
        self.m_lineEdit.event(e)
        super(QtCharEdit, self).focusOutEvent(e)

    def keyPressEvent(self, e):
        self.handleKeyEvent(e)
        e.accept()

    def keyReleaseEvent(self, e):
        self.m_lineEdit.event(e)

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

    def event(self, e):
        x = e.type()
        if x in [QEvent.Shortcut, QEvent.ShortcutOverride, QEvent.KeyRelease]:
            e.accept()
            return True

        return super(QtCharEdit, self).event(e)

class QtCharEditorFactoryPrivate(EditorFactoryPrivate):
    def __init__(self):
        self.q_ptr = None

    def slotPropertyChanged(self, property, value):
        editors = self.m_createdEditors.get(property)
        if not editors:
            return

        for editor in editors:
            editor.blockSignals(True)
            editor.setValue(value)
            editor.blockSignals(False)

    def slotSetValue(self, value):
        object = self.q_ptr.sender()
        for itEditor in self.m_editorToProperty.keys():
            if (itEditor == object):
                property = self.m_editorToProperty[itEditor]
                manager = self.q_ptr.propertyManager(property)
                if (not manager):
                    return
                manager.setValue(property, value)
                return

registerEditorFactory(QtCharEditorFactoryPrivate, QtCharEdit)
###
#   \class QtCharEditorFactory

#   \brief The QtCharEditorFactory class provides editor
#   widgets for properties created by QtCharPropertyManager objects.

#   \sa QtAbstractEditorFactory
###
class QtCharEditorFactory(QtAbstractEditorFactory):
    ###
    #   Creates a factory with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtCharEditorFactory, self).__init__(parent)

        self.d_ptr = QtCharEditorFactoryPrivate()
        self.d_ptr.q_ptr = self

    ###
    #   Destroys this factory, and all the widgets it has created.
    ###
    def __del__(self):
        self.d_ptr.m_editorToProperty.clear()
        del self.d_ptr

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def connectPropertyManager(self, manager):
        manager.valueChangedSignal.connect(self.d_ptr.slotPropertyChanged)

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def createEditor(self, manager, property, parent):
        editor = self.d_ptr.createEditor(property, parent)
        editor.setValue(manager.value(property))

        editor.valueChangedSignal.connect(self.d_ptr.slotSetValue)
        editor.destroyed.connect(self.d_ptr.slotEditorDestroyed)
        return editor

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def disconnectPropertyManager(self, manager):
        manager.valueChangedSignal.disconnect(self.d_ptr.slotPropertyChanged)

class QtEnumEditorFactoryPrivate(EditorFactoryPrivate):
    def __init__(self):
        self.q_ptr = None

    def slotPropertyChanged(self, property, value):
        editors = self.m_createdEditors.get(property)
        if not editors:
            return

        for editor in editors:
            editor.blockSignals(True)
            editor.setCurrentIndex(value)
            editor.blockSignals(False)

    def slotEnumNamesChanged(self, property, enumNames):
        editors = self.m_createdEditors.get(property)
        if not editors:
            return

        manager = self.q_ptr.propertyManager(property)
        if (not manager):
            return

        enumIcons = manager.enumIcons(property)

        for editor in editors:
            editor.blockSignals(True)
            editor.clear()
            editor.addItems(enumNames)
            nameCount = len(enumNames)
            for i in range(nameCount):
                editor.setItemIcon(i, enumIcons.get(i, QIcon()))
            editor.setCurrentIndex(manager.value(property))
            editor.blockSignals(False)

    def slotEnumIconsChanged(self, property, enumIcons):
        editors = self.m_createdEditors.get(property)
        if not editors:
            return

        manager = self.q_ptr.propertyManager(property)
        if (not manager):
            return

        enumNames = manager.enumNames(property)

        for editor in editors:
            editor.blockSignals(True)
            nameCount = len(enumNames)
            for i in range(nameCount):
                editor.setItemIcon(i, enumIcons.value(i))
            editor.setCurrentIndex(manager.value(property))
            editor.blockSignals(False)

    def slotSetValue(self, value):
        object = self.q_ptr.sender()
        for itEditor in self.m_editorToProperty.keys():
            if (itEditor == object):
                property = self.m_editorToProperty[itEditor]
                manager = self.q_ptr.propertyManager(property)
                if (not manager):
                    return
                manager.setValue(property, value)
                return

registerEditorFactory(QtEnumEditorFactoryPrivate, QComboBox)
###
#   \class QtEnumEditorFactory

#   \brief The QtEnumEditorFactory class provides QComboBox widgets for
#   properties created by QtEnumPropertyManager objects.

#   \sa QtAbstractEditorFactory, QtEnumPropertyManager
###
class QtEnumEditorFactory(QtAbstractEditorFactory):
    ###
    #   Creates a factory with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtEnumEditorFactory, self).__init__(parent)

        self.d_ptr = QtEnumEditorFactoryPrivate()
        self.d_ptr.q_ptr = self

    ###
    #   Destroys this factory, and all the widgets it has created.
    ###
    def __del__(self):
        self.d_ptr.m_editorToProperty.clear()
        del self.d_ptr

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def connectPropertyManager(self, manager):
        manager.valueChangedSignal.connect(self.d_ptr.slotPropertyChanged)
        manager.enumNamesChangedSignal.connect(self.d_ptr.slotEnumNamesChanged)

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def createEditor(self, manager, property, parent):
        editor = self.d_ptr.createEditor(property, parent)
        editor.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
        editor.setMinimumContentsLength(1)
        editor.view().setTextElideMode(Qt.ElideRight)
        enumNames = manager.enumNames(property)
        editor.addItems(enumNames)
        enumIcons = manager.enumIcons(property)
        enumNamesCount = len(enumNames)
        for i in range(enumNamesCount):
            icon = enumIcons[i]
            if type(icon) is not QIcon:
                icon = QIcon()
            editor.setItemIcon(i, icon)
        editor.setCurrentIndex(manager.value(property))

        editor.currentIndexChanged.connect(self.d_ptr.slotSetValue)
        editor.destroyed.connect(self.d_ptr.slotEditorDestroyed)
        return editor

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def disconnectPropertyManager(self, manager):
        manager.valueChangedSignal.disconnect(self.d_ptr.slotPropertyChanged)
        manager.enumNamesChangedSignal.disconnect(self.d_ptr.slotEnumNamesChanged)

class QtCursorEditorFactoryPrivate(EditorFactoryPrivate):
    def __init__(self):
        self.q_ptr = None
        self.m_enumEditorFactory = None
        self.m_enumPropertyManager = None
        self.m_updatingEnum = False
        self.m_propertyToEnum = QMap()
        self.m_enumToProperty = QMap()
        self.m_enumToEditors = QMapList()
        self.m_editorToEnum = QMap()

    def slotPropertyChanged(self, property, cursor):
        # update enum property
        enumProp = self.m_propertyToEnum[property]
        if (not enumProp):
            return

        self.m_updatingEnum = True
        self.m_enumPropertyManager.setValue(enumProp, cursorDatabase().cursorToValue(cursor))
        self.m_updatingEnum = False

    def slotEnumChanged(self, property, value):
        if (self.m_updatingEnum):
            return
        # update cursor property
        prop = self.m_enumToProperty[property]
        if (not prop):
            return
        cursorManager = self.q_ptr.propertyManager(prop)
        if (not cursorManager):
            return
        cursorManager.setValue(prop, QCursor(cursorDatabase().valueToCursor(value)))

    def slotEditorDestroyed(self, object):
        # remove from  m_editorToEnum map
        # remove from  m_enumToEditors map
        # if m_enumToEditors doesn't contains more editors delete enum property
        for editor in self.m_editorToEnum.keys():
            if (editor == object):
                enumProp = self.m_editorToEnum[editor]
                self.m_editorToEnum.remove(editor)
                self.m_enumToEditors[enumProp].removeAll(editor)
                if len(self.m_enumToEditors[enumProp])<=0:
                    self.m_enumToEditors.remove(enumProp)
                    property = self.m_enumToProperty[enumProp]
                    self.m_enumToProperty.remove(enumProp)
                    self.m_propertyToEnum.remove(property)
                    del enumProp

                return

###
#   \class QtCursorEditorFactory

#   \brief The QtCursorEditorFactory class provides QComboBox widgets for
#   properties created by QtCursorPropertyManager objects.

#   \sa QtAbstractEditorFactory, QtCursorPropertyManager
###
class QtCursorEditorFactory(QtAbstractEditorFactory):
    ###
    #   Creates a factory with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtCursorEditorFactory, self).__init__(parent)

        self.d_ptr = QtCursorEditorFactoryPrivate()
        self.d_ptr.q_ptr = self

        self.d_ptr.m_enumEditorFactory = QtEnumEditorFactory(self)
        self.d_ptr.m_enumPropertyManager = QtEnumPropertyManager(self)
        self.d_ptr.m_enumPropertyManager.valueChangedSignal.connect(self.d_ptr.slotEnumChanged)
        self.d_ptr.m_enumEditorFactory.addPropertyManager(self.d_ptr.m_enumPropertyManager)

    ###
    #   Destroys this factory, and all the widgets it has created.
    ###
    def __del__(self):
        pass
    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def connectPropertyManager(self, manager):
        manager.valueChangedSignal.connect(self.d_ptr.slotPropertyChanged)

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def createEditor(self, manager, property, parent):
        enumProp = 0
        if (property in self.d_ptr.m_propertyToEnum):
            enumProp = self.d_ptr.m_propertyToEnum[property]
        else:
            enumProp = self.d_ptr.m_enumPropertyManager.addProperty(property.propertyName())
            self.d_ptr.m_enumPropertyManager.setEnumNames(enumProp, cursorDatabase().cursorShapeNames())
            self.d_ptr.m_enumPropertyManager.setEnumIcons(enumProp, cursorDatabase().cursorShapeIcons())
            self.d_ptr.m_enumPropertyManager.setValue(enumProp, cursorDatabase().cursorToValue(manager.value(property)))
            self.d_ptr.m_propertyToEnum[property] = enumProp
            self.d_ptr.m_enumToProperty[enumProp] = property

        af = self.d_ptr.m_enumEditorFactory
        editor = af.findEditor(enumProp, parent)
        self.d_ptr.m_enumToEditors[enumProp].append(editor)
        self.d_ptr.m_editorToEnum[editor] = enumProp
        editor.destroyed.connect(self.d_ptr.slotEditorDestroyed)
        return editor

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def disconnectPropertyManager(self, manager):
        manager.valueChangedSignal.disconnect(self.d_ptr.slotPropertyChanged)

    # QtColorEditWidget

class QtColorEditWidget(QWidget):
    valueChangedSignal = pyqtSignal(QColor)
    def __init__(self, parent=None):
        super(QtColorEditWidget, self).__init__(parent)

        self.m_color = QColor()
        self.m_pixmapLabel = QLabel()
        self.m_label = QLabel()
        self.m_button = QToolButton()
        self.lt = QHBoxLayout(self)
        setupTreeViewEditorMargin(self.lt)
        self.lt.setSpacing(0)
        self.lt.addWidget(self.m_pixmapLabel)
        self.lt.addWidget(self.m_label)
        self.lt.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Ignored))

        self.m_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Ignored)
        self.m_button.setFixedWidth(20)
        self.setFocusProxy(self.m_button)
        self.setFocusPolicy(self.m_button.focusPolicy())
        self.m_button.setText(self.tr("..."))
        self.m_button.installEventFilter(self)
        self.m_button.clicked.connect(self.buttonClicked)
        self.lt.addWidget(self.m_button)
        self.m_pixmapLabel.setPixmap(QtPropertyBrowserUtils.brushValuePixmap(QBrush(self.m_color)))
        self.m_label.setText(QtPropertyBrowserUtils.colorValueText(self.m_color))

    def setValue(self, c):
        if (self.m_color != c):
            self.m_color = c
            self.m_pixmapLabel.setPixmap(QtPropertyBrowserUtils.brushValuePixmap(QBrush(c)))
            self.m_label.setText(QtPropertyBrowserUtils.colorValueText(c))

    def buttonClicked(self):
        ok = ''
        oldRgba = self.m_color
        newRgba = QColorDialog.getColor(oldRgba, self, ok, QColorDialog.ShowAlphaChannel)
        if newRgba != oldRgba:
            self.setValue(newRgba)
            self.valueChangedSignal.emit(self.m_color)

    def eventFilter(self, obj, ev):
        if (obj == self.m_button):
            k = ev.type()
            if k in [QEvent.KeyPress, QEvent.KeyRelease]:# Prevent the QToolButton from handling Enter/Escape meant control the delegate
                x = ev.key()
                if x in [Qt.Key_Escape, Qt.Key_Enter, Qt.Key_Return]:
                    ev.ignore()
                    return True

        return super(QtColorEditWidget, self).eventFilter(obj, ev)

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

class QtColorEditorFactoryPrivate(EditorFactoryPrivate):
    def __init__(self):
        self.q_ptr = None

    def slotPropertyChanged(self, property, value):
        editors = self.m_createdEditors.get(property)
        if not editors:
            return

        for editor in editors:
            editor.setValue(value)

    def slotSetValue(self, value):
        object = self.q_ptr.sender()
        for itEditor in self.m_editorToProperty.keys():
            if (itEditor == object):
                property = self.m_editorToProperty[itEditor]
                manager = self.q_ptr.propertyManager(property)
                if (not manager):
                    return
                manager.setValue(property, value)
                return

registerEditorFactory(QtColorEditorFactoryPrivate, QtColorEditWidget)
###
#   \class QtColorEditorFactory

#   \brief The QtColorEditorFactory class provides color editing  for
#   properties created by QtColorPropertyManager objects.

#   \sa QtAbstractEditorFactory, QtColorPropertyManager
###
class QtColorEditorFactory(QtAbstractEditorFactory):
    ###
    #   Creates a factory with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtColorEditorFactory, self).__init__(parent)

        self.d_ptr = QtColorEditorFactoryPrivate()
        self.d_ptr.q_ptr = self

    ###
    #   Destroys this factory, and all the widgets it has created.
    ###
    def __del__(self):
        self.d_ptr.m_editorToProperty.clear()
        del self.d_ptr

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def connectPropertyManager(self, manager):
        manager.valueChangedSignal.connect(self.d_ptr.slotPropertyChanged)

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def createEditor(self, manager, property, parent):
        editor = self.d_ptr.createEditor(property, parent)
        editor.setValue(manager.value(property))
        editor.valueChangedSignal.connect(self.d_ptr.slotSetValue)
        editor.destroyed.connect(self.d_ptr.slotEditorDestroyed)
        return editor

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def disconnectPropertyManager(self, manager):
        manager.valueChangedSignal.disconnect(self.d_ptr.slotPropertyChanged)

    # QtFontEditWidget

class QtFontEditWidget(QWidget):
    valueChanged = pyqtSignal(QFont)

    def __init__(self, parent=None):
        super(QtFontEditWidget, self).__init__(parent)

        self.m_font = QFont()
        self.m_pixmapLabel = QLabel()
        self.m_label = QLabel()
        self.m_button = QToolButton()
        self.lt = QHBoxLayout(self)
        setupTreeViewEditorMargin(self.lt)
        self.lt.setSpacing(0)
        self.lt.addWidget(self.m_pixmapLabel)
        self.lt.addWidget(self.m_label)
        self.lt.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Ignored))

        self.m_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Ignored)
        self.m_button.setFixedWidth(20)
        self.setFocusProxy(self.m_button)
        self.setFocusPolicy(self.m_button.focusPolicy())
        self.m_button.setText(self.tr("..."))
        self.m_button.installEventFilter(self)
        self.m_button.clicked.connect(self.buttonClicked)
        self.lt.addWidget(self.m_button)
        self.m_pixmapLabel.setPixmap(QtPropertyBrowserUtils.fontValuePixmap(self.m_font))
        self.m_label.setText(QtPropertyBrowserUtils.fontValueText(self.m_font))

    def setValue(self, f):
        if (self.m_font != f):
            self.m_font = f
            self.m_pixmapLabel.setPixmap(QtPropertyBrowserUtils.fontValuePixmap(f))
            self.m_label.setText(QtPropertyBrowserUtils.fontValueText(f))

    def buttonClicked(self):
        ok = False
        newFont,ok = QFontDialog.getFont(self.m_font, self, self.tr("Select Font"))
        if (ok and newFont != self.m_font):
            f = QFont(self.m_font)
            # prevent mask for unchanged attributes, don't change other attributes (like kerning, etc...)
            if (self.m_font.family() != newFont.family()):
                f.setFamily(newFont.family())
            if (self.m_font.pointSize() != newFont.pointSize()):
                f.setPointSize(newFont.pointSize())
            if (self.m_font.bold() != newFont.bold()):
                f.setBold(newFont.bold())
            if (self.m_font.italic() != newFont.italic()):
                f.setItalic(newFont.italic())
            if (self.m_font.underline() != newFont.underline()):
                f.setUnderline(newFont.underline())
            if (self.m_font.strikeOut() != newFont.strikeOut()):
                f.setStrikeOut(newFont.strikeOut())
            self.setValue(f)
            self.valueChanged.emit(self.m_font)

    def eventFilter(self, obj, ev):
        if (obj == self.m_button):
            k = ev.type()
            if k in [QEvent.KeyPress, QEvent.KeyRelease]:# Prevent the QToolButton from handling Enter/Escape meant control the delegate
                x = ev.key()
                if x in [Qt.Key_Escape, Qt.Key_Enter, Qt.Key_Return]:
                    ev.ignore()
                    return True

        return super(QtFontEditWidget, self).eventFilter(obj, ev)

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

class QtFontEditorFactoryPrivate(EditorFactoryPrivate):
    def __init__(self):
        self.q_ptr = None

    def slotPropertyChanged(self, property, value):
        editors = self.m_createdEditors.get(property)
        if not editors:
            return

        for editor in editors:
            editor.setValue(value)

    def slotSetValue(self, value):
        object = self.q_ptr.sender()
        property = self.m_editorToProperty.get(object)
        if property:
            manager = self.q_ptr.propertyManager(property)
            if (not manager):
                return
            manager.setValue(property, value)
            return

registerEditorFactory(QtFontEditorFactoryPrivate, QtFontEditWidget)
###
#   \class QtFontEditorFactory

#   \brief The QtFontEditorFactory class provides font editing for
#   properties created by QtFontPropertyManager objects.

#   \sa QtAbstractEditorFactory, QtFontPropertyManager
###
class QtFontEditorFactory(QtAbstractEditorFactory):
    ###
    #   Creates a factory with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtFontEditorFactory, self).__init__(parent)

        self.d_ptr = QtFontEditorFactoryPrivate()
        self.d_ptr.q_ptr = self

    ###
    #   Destroys this factory, and all the widgets it has created.
    ###
    def __del__(self):
        self.d_ptr.m_editorToProperty.clear()
        del self.d_ptr

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def connectPropertyManager(self, manager):
        manager.valueChangedSignal.connect(self.d_ptr.slotPropertyChanged)

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def createEditor(self, manager, property, parent):
        editor = self.d_ptr.createEditor(property, parent)
        editor.setValue(manager.value(property))
        editor.valueChanged.connect(self.d_ptr.slotSetValue)
        editor.destroyed.connect(self.d_ptr.slotEditorDestroyed)
        return editor

    ###
    #   \internal

    #   Reimplemented from the QtAbstractEditorFactory class.
    ###
    def disconnectPropertyManager(self, manager):
        manager.valueChangedSignal.disconnect(self.d_ptr.slotPropertyChanged)

