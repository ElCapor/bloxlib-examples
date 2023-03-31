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

from qteditorfactory import (
    QtAbstractEditorFactory,
    QtSpinBoxFactory,
    QtCheckBoxFactory,
    QtDoubleSpinBoxFactory,
    QtLineEditFactory,
    QtDateEditFactory,
    QtTimeEditFactory,
    QtDateTimeEditFactory,
    QtKeySequenceEditorFactory,
    QtCharEditorFactory,
    QtEnumEditorFactory,
    QtCursorEditorFactory,
    QtColorEditorFactory,
    QtFontEditorFactory
    )
from qtpropertybrowser import QtProperty
from qtpropertymanager import (
    QtAbstractPropertyManager,
    QtIntPropertyManager,
    QtBoolPropertyManager,
    QtDoublePropertyManager,
    QtStringPropertyManager,
    QtDatePropertyManager,
    QtTimePropertyManager,
    QtDateTimePropertyManager,
    QtKeySequencePropertyManager,
    QtCharPropertyManager,
    QtLocalePropertyManager,
    QtPointPropertyManager,
    QtPointFPropertyManager,
    QtSizePropertyManager,
    QtSizeFPropertyManager,
    QtRectPropertyManager,
    QtRectFPropertyManager,
    QtEnumPropertyManager,
    QtFlagPropertyManager,
    QtSizePolicyPropertyManager,
    QtFontPropertyManager,
    QtColorPropertyManager,
    QtCursorPropertyManager,
    QtGroupPropertyManager
    )
from pyqtcore import QMap, QMapMap, qMetaTypeId
from PyQt5.QtCore import QVariant, pyqtSignal, QUrl
from PyQt5.QtGui import QIcon, QKeySequence

class QtEnumPropertyType():
    def __init__(self):
        pass

class QtFlagPropertyType():
    def __init__(self):
        pass

class QtGroupPropertyType():
    def __init__(self):
        pass

class QtIconMap():
    def __init__(self):
        pass
        
g_propertyToWrappedProperty = None
def propertyToWrappedProperty():
    global g_propertyToWrappedProperty
    if not g_propertyToWrappedProperty:
        g_propertyToWrappedProperty = QMap()
    return g_propertyToWrappedProperty

def wrappedProperty(property):
    return propertyToWrappedProperty().get(property, 0)

class QtVariantPropertyPrivate():
    ###
    #   Creates a variant property using the given \a manager.
    #
    #   Do not use this constructor to create variant property instances
    #   use the QtVariantPropertyManager.addProperty() function
    #   instead.  This constructor is used internally by the
    #   QtVariantPropertyManager.createProperty() function.
    #
    #   \sa QtVariantPropertyManager
    ###
    def __init__(self, manager):
        self.q_ptr = None
        self.manager = manager

###
#   \class QtVariantProperty
#
#   \brief The QtVariantProperty class is a convenience class handling
#   QVariant based properties.
#
#   QtVariantProperty provides additional API: A property's type,
#   value type, attribute values and current value can easily be
#   retrieved using the propertyType(), valueType(), attributeValue()
#   and value() functions respectively. In addition, the attribute
#   values and the current value can be set using the corresponding
#   setValue() and setAttribute() functions.
#
#   For example, instead of writing:
#
#   \code
#   QtVariantPropertyManager *variantPropertyManager
#   property
#
#   variantPropertyManager.setValue(property, 10)
#   \endcode
#
#   you can write:
#
#   \code
#   QtVariantPropertyManager *variantPropertyManager
#   QtVariantProperty *property
#
#   property.setValue(10)
#   \endcode
#
#   QtVariantProperty instances can only be created by the
#   QtVariantPropertyManager class.
#
#   \sa QtProperty, QtVariantPropertyManager, QtVariantEditorFactory
###
class QtVariantProperty(QtProperty):
    ###
    #   Creates a variant property using the given \a manager.
    #
    #   Do not use this constructor to create variant property instances
    #   use the QtVariantPropertyManager.addProperty() function
    #   instead.  This constructor is used internally by the
    #   QtVariantPropertyManager.createProperty() function.
    #
    #   \sa QtVariantPropertyManager
    ###
    def __init__(self, manager):
        super(QtVariantProperty, self).__init__(manager)

        self.d_ptr = QtVariantPropertyPrivate(manager)
        self.d_ptr.q_ptr = self

    ###
    #   Destroys this property.

    #   \sa QtProperty::~QtProperty()
    ###
    def __del__(self):
        del self.d_ptr

    ###
    #   Returns the property's current value.
    #
    #   \sa valueType(), setValue()
    ###
    def value(self):
        return self.d_ptr.manager.value(self)

    ###
    #   Returns this property's value for the specified \a attribute.
    #
    #   QtVariantPropertyManager provides a couple of related functions:
    #   \l{QtVariantPropertyManager.attributes()}{attributes()and
    #   \l{QtVariantPropertyManager.attributeType()}{attributeType()}.
    #
    #   \sa setAttribute()
    ###
    def attributeValue(self, attribute):
        return self.d_ptr.manager.attributeValue(self, attribute)

    ###
    #   Returns the type of this property's value.
    #
    #   \sa propertyType()
    ###
    def valueType(self):
        return self.d_ptr.manager.valueType(self)

    ###
    #   Returns this property's type.
    #
    #   QtVariantPropertyManager provides several related functions:
    #   \l{QtVariantPropertyManager.enumTypeId()}{enumTypeId()},
    #   \l{QtVariantPropertyManager.flagTypeId()}{flagTypeId()and
    #   \l{QtVariantPropertyManager.groupTypeId()}{groupTypeId()}.
    #
    #   \sa valueType()
    ###
    def propertyType(self):
        return self.d_ptr.manager.propertyType(self)

    ###
    #   Sets the value of this property to \a value.
    #
    #   The specified \a value must be of the type returned by
    #   valueType(), or of a type that can be converted to valueType()
    #   using the QVariant.canConvert() function; otherwise this function
    #   does nothing.
    #
    #   \sa value()
    ###
    def setValue(self, value):
        self.d_ptr.manager.setValue(self, value)

    ###
    #   Sets the \a attribute of property to \a value.
    #
    #   QtVariantPropertyManager provides the related
    #   \l{QtVariantPropertyManager.setAttribute()}{setAttribute()}
    #   function.
    #
    #   \sa attributeValue()
    ###
    def setAttribute(self, attribute, value):
        self.d_ptr.manager.setAttribute(self, attribute, value)

class QtVariantPropertyManagerPrivate():
    def __init__(self):
        self.q_ptr = None
        self.m_creatingProperty = False
        self.m_creatingSubProperties = False
        self.m_destroyingSubProperties = False
        self.m_propertyType = 0
        self.m_constraintAttribute = "constraint"
        self.m_singleStepAttribute = "singleStep"
        self.m_decimalsAttribute = "decimals"
        self.m_enumIconsAttribute = "enumIcons"
        self.m_enumNamesAttribute = "enumNames"
        self.m_flagNamesAttribute = "flagNames"
        self.m_maximumAttribute = "maximum"
        self.m_minimumAttribute = "minimum"
        self.m_regExpAttribute = "regExp"
        self.m_echoModeAttribute = "echoMode"
        self.m_readOnlyAttribute = "readOnly"
        self.m_textVisibleAttribute = "textVisible"
        self.m_typeToPropertyManager = QMap()
        self.m_typeToAttributeToAttributeType = QMapMap()
        self.m_propertyToType = QMap()
        self.m_typeToValueType = QMap()
        self.m_internalToProperty = QMap()

    def internalPropertyToType(self, property):
        t = 0
        internPropertyManager = property.propertyManager()
        tp = type(internPropertyManager)
        if tp == QtIntPropertyManager:
            t = QVariant.Int
        elif tp == QtEnumPropertyManager:
            t = QtVariantPropertyManager.enumTypeId()
        elif tp == QtBoolPropertyManager:
            t = QVariant.Bool
        elif tp == QtDoublePropertyManager:
            t = QVariant.Double
        return t

    def createSubProperty(self, parent, after, internal):
        type = self.internalPropertyToType(internal)
        if not type:
            return 0

        wasCreatingSubProperties = self.m_creatingSubProperties
        self.m_creatingSubProperties = True

        varChild = self.q_ptr.addProperty(type, internal.propertyName())

        self.m_creatingSubProperties = wasCreatingSubProperties

        varChild.setPropertyName(internal.propertyName())
        varChild.setToolTip(internal.toolTip())
        varChild.setStatusTip(internal.statusTip())
        varChild.setWhatsThis(internal.whatsThis())

        parent.insertSubProperty(varChild, after)

        self.m_internalToProperty[internal] = varChild
        propertyToWrappedProperty()[varChild] = internal
        return varChild

    def removeSubProperty(self, property):
        internChild = self.wrappedProperty(property)
        wasDestroyingSubProperties = self.m_destroyingSubProperties
        self.m_destroyingSubProperties = True
        self.m_destroyingSubProperties = wasDestroyingSubProperties
        self.m_internalToProperty.remove(internChild)
        propertyToWrappedProperty().pop(property)

    def slotPropertyInserted(self, property, parent, after):
        if (self.m_creatingProperty):
            return
        if type(after)==list:
            after = after[0]
        varParent = self.m_internalToProperty.get(parent, 0)
        if (not varParent):
            return

        varAfter = 0
        if after and after.propertyManager()!=-1:
            varAfter = self.m_internalToProperty.get(after, 0)
            if (not varAfter):
                return

        self.createSubProperty(varParent, varAfter, property)

    def slotPropertyRemoved(self, property, parent):
        varProperty = self.m_internalToProperty.get(property, 0)
        if (not varProperty):
            return

        self.removeSubProperty(varProperty)

    def valueChanged(self, property, val):
        varProp = self.m_internalToProperty.get(property, 0)
        if (not varProp):
            return
        self.q_ptr.valueChangedSignal.emit(varProp, val)
        self.q_ptr.propertyChangedSignal.emit(varProp)

    def slotValueChanged(self, property, val):
        self.valueChanged(property, val)

    def slotRangeChanged(self, property, min, max):
        varProp = self.m_internalToProperty.get(property, 0)
        if varProp:
            self.q_ptr.attributeChangedSignal.emit(varProp, self.m_minimumAttribute, min)
            self.q_ptr.attributeChangedSignal.emit(varProp, self.m_maximumAttribute, max)

    def slotSingleStepChanged(self, property, step):
        varProp = self.m_internalToProperty.get(property, 0)
        if varProp:
            self.q_ptr.attributeChangedSignal.emit(varProp, self.m_singleStepAttribute, step)

    def slotDecimalsChanged(self, property, prec):
        varProp = self.m_internalToProperty.get(property, 0)
        if varProp:
            self.q_ptr.attributeChangedSignal.emit(varProp,  self.m_decimalsAttribute, prec)

    def slotRegExpChanged(self, property, regExp):
        varProp = self.m_internalToProperty.get(property, 0)
        if varProp:
            self.q_ptr.attributeChangedSignal.emit(varProp,  self.m_regExpAttribute, regExp)

    def slotEchoModeChanged(self, property, mode):
        varProp = self.m_internalToProperty.get(property, 0)
        if varProp:
            self.q_ptr.attributeChangedSignal.emit(varProp,  self.m_echoModeAttribute, mode)

    def slotReadOnlyChanged(self, property, readOnly):
        varProp = self.m_internalToProperty.get(property, 0)
        if varProp:
            self.q_ptr.attributeChangedSignal.emit(varProp,  self.m_readOnlyAttribute, readOnly)

    def slotTextVisibleChanged(self, property, textVisible):
        varProp = self.m_internalToProperty.get(property, 0)
        if varProp:
            self.q_ptr.attributeChangedSignal.emit(varProp,  self.m_textVisibleAttribute, textVisible)

    def _slotValueChanged(self, property, val):
        if type(val)==QKeySequence:
            raise NotImplementedError
        self._valueChanged(property, QVariant(val))

    def slotConstraintChanged(self, property, constraint):
        varProp = self.m_internalToProperty.get(property, 0)
        if varProp:
            self.q_ptr.attributeChangedSignal.emit(varProp,  self.m_constraintAttribute, constraint)

    def slotEnumNamesChanged(self, property, enumNames):
        varProp = self.m_internalToProperty.get(property, 0)
        if varProp:
            self.q_ptr.attributeChangedSignal.emit(varProp,  self.m_enumNamesAttribute, enumNames)

    def slotEnumIconsChanged(self, property, enumIcons):
        varProp = self.m_internalToProperty.get(property, 0)
        if varProp:
            v = QVariant(enumIcons)
            self.q_ptr.attributeChangedSignal.emit(varProp, self.m_enumIconsAttribute, v)

    def slotFlagNamesChanged(self, property, flagNames):
        varProp = self.m_internalToProperty.get(property, 0)
        if varProp:
            self.q_ptr.attributeChangedSignal.emit(varProp,  self.m_flagNamesAttribute, flagNames)

###
#    \class QtVariantPropertyManager
#
#    \brief The QtVariantPropertyManager class provides and manages QVariant based properties.
#
#    QtVariantPropertyManager provides the addProperty() function which
#    creates QtVariantProperty objects. The QtVariantProperty class is
#    a convenience class handling QVariant based properties inheriting
#    QtProperty. A QtProperty object created by a
#    QtVariantPropertyManager instance can be converted into a
#    QtVariantProperty object using the variantProperty() function.
#
#    The property's value can be retrieved using the value(), and set
#    using the setValue() slot. In addition the property's type, and
#    the type of its value, can be retrieved using the propertyType()
#    and valueType() functions respectively.
#
#    A property's type is a QVariant.Type enumerator value, and
#    usually a property's type is the same as its value type. But for
#    some properties the types differ, for example for enums, flags and
#    group types in which case QtVariantPropertyManager provides the
#    enumTypeId(), flagTypeId() and groupTypeId() functions,
#    respectively, to identify their property type (the value types are
#    QVariant.Int for the enum and flag types, and QVariant.Invalid
#    for the group type).
#
#    Use the isPropertyTypeSupported() function to check if a particular
#    property type is supported. The currently supported property types
#    are:
#
#    \table
#    \header
#        \o Property Type
#        \o Property Type Id
#    \row
#        \o int
#        \o QVariant.Int
#    \row
#        \o double
#        \o QVariant.Double
#    \row
#        \o bool
#        \o QVariant.Bool
#    \row
#        \o QString
#        \o QVariant.String
#    \row
#        \o QDate
#        \o QVariant.date
#    \row
#        \o QTime
#        \o QVariant.time
#    \row
#        \o QDateTime
#        \o QVariant.datetime
#    \row
#        \o QKeySequence
#        \o QVariant.KeySequence
#    \row
#        \o QChar
#        \o QVariant.Char
#    \row
#        \o QLocale
#        \o QVariant.Locale
#    \row
#        \o QPoint
#        \o QVariant.Point
#    \row
#        \o QPointF
#        \o QVariant.PointF
#    \row
#        \o QSize
#        \o QVariant.Size
#    \row
#        \o QSizeF
#        \o QVariant.SizeF
#    \row
#        \o QRect
#        \o QVariant.Rect
#    \row
#        \o QRectF
#        \o QVariant.RectF
#    \row
#        \o QColor
#        \o QVariant.Color
#    \row
#        \o QSizePolicy
#        \o QVariant.SizePolicy
#    \row
#        \o QFont
#        \o QVariant.Font
#    \row
#        \o QCursor
#        \o QVariant.Cursor
#    \row
#        \o enum
#        \o enumTypeId()
#    \row
#        \o flag
#        \o flagTypeId()
#    \row
#        \o group
#        \o groupTypeId()
#    \endtable
#
#    Each property type can provide additional attributes,
#    e.g. QVariant.Int and QVariant.Double provides minimum and
#    maximum values. The currently supported attributes are:
#
#    \table
#    \header
#        \o Property Type
#        \o Attribute Name
#        \o Attribute Type
#    \row
#        \o \c int
#        \o minimum
#        \o QVariant.Int
#    \row
#        \o
#        \o maximum
#        \o QVariant.Int
#    \row
#        \o
#        \o singleStep
#        \o QVariant.Int
#    \row
#        \o \c double
#        \o minimum
#        \o QVariant.Double
#    \row
#        \o
#        \o maximum
#        \o QVariant.Double
#    \row
#        \o
#        \o singleStep
#        \o QVariant.Double
#    \row
#        \o
#        \o decimals
#        \o QVariant.Int
#    \row
#        \o \c bool
#        \o textVisible
#        \o QVariant.Bool
#    \row
#        \o QString
#        \o regExp
#        \o QVariant.RegExp
#    \row
#        \o
#        \o echoMode
#        \o QVariant.Int
#    \row
#        \o QDate
#        \o minimum
#        \o date
#    \row
#        \o
#        \o maximum
#        \o date
#    \row
#        \o QPointF
#        \o decimals
#        \o QVariant.Int
#    \row
#        \o QSize
#        \o minimum
#        \o QVariant.Size
#    \row
#        \o
#        \o maximum
#        \o QVariant.Size
#    \row
#        \o QSizeF
#        \o minimum
#        \o QVariant.SizeF
#    \row
#        \o
#        \o maximum
#        \o QVariant.SizeF
#    \row
#        \o
#        \o decimals
#        \o QVariant.Int
#    \row
#        \o QRect
#        \o constraint
#        \o QVariant.Rect
#    \row
#        \o QRectF
#        \o constraint
#        \o QVariant.RectF
#    \row
#        \o
#        \o decimals
#        \o QVariant.Int
#    \row
#        \o \c enum
#        \o enumNames
#        \o QVariant.StringList
#    \row
#        \o
#        \o enumIcons
#        \o iconMapTypeId()
#    \row
#        \o \c flag
#        \o flagNames
#        \o QVariant.StringList
#    \endtable
#
#    The attributes for a given property type can be retrieved using
#    the attributes() function. Each attribute has a value type which
#    can be retrieved using the attributeType() function, and a value
#    accessible through the attributeValue() function. In addition, the
#    value can be set using the setAttribute() slot.
#
#    QtVariantManager also provides the valueChanged() signal which is
#    emitted whenever a property created by this manager change, and
#    the attributeChanged() signal which is emitted whenever an
#    attribute of such a property changes.
#
#    \sa QtVariantProperty, QtVariantEditorFactory
###

###
#    \fn void QtVariantPropertyManager.valueChanged(property, value)
#
#    This signal is emitted whenever a property created by this manager
#    changes its value, passing a pointer to the \a property and the
#    new \a value as parameters.
#
#    \sa setValue()
###

###
#    \fn void QtVariantPropertyManager.attributeChanged(property,
#               attribute, value)
#
#    This signal is emitted whenever an attribute of a property created
#    by this manager changes its value, passing a pointer to the \a
#    property, the \a attribute and the new \a value as parameters.
#
#    \sa setAttribute()
###
class QtVariantPropertyManager(QtAbstractPropertyManager):
    valueChangedSignal = pyqtSignal(QtProperty, QVariant)
    attributeChangedSignal = pyqtSignal(QtProperty, str ,QVariant)
    ###
    #    Creates a manager with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtVariantPropertyManager, self).__init__(parent)

        self.d_ptr = QtVariantPropertyManagerPrivate()
        self.d_ptr.q_ptr = self

        intPropertyManager = QtIntPropertyManager(self)
        self.d_ptr.m_typeToPropertyManager[QVariant.Int] = intPropertyManager
        self.d_ptr.m_typeToAttributeToAttributeType[QVariant.Int][self.d_ptr.m_minimumAttribute] = QVariant.Int
        self.d_ptr.m_typeToAttributeToAttributeType[QVariant.Int][self.d_ptr.m_maximumAttribute] = QVariant.Int
        self.d_ptr.m_typeToAttributeToAttributeType[QVariant.Int][self.d_ptr.m_singleStepAttribute] = QVariant.Int
        self.d_ptr.m_typeToAttributeToAttributeType[QVariant.Int][self.d_ptr.m_readOnlyAttribute] = QVariant.Bool
        self.d_ptr.m_typeToValueType[QVariant.Int] = QVariant.Int
        intPropertyManager.valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        intPropertyManager.rangeChangedSignal.connect(self.d_ptr.slotRangeChanged)
        intPropertyManager.singleStepChangedSignal.connect(self.d_ptr.slotSingleStepChanged)
        doublePropertyManager = QtDoublePropertyManager(self)
        self.d_ptr.m_typeToPropertyManager[QVariant.Double] = doublePropertyManager
        self.d_ptr.m_typeToAttributeToAttributeType[QVariant.Double][self.d_ptr.m_minimumAttribute] = QVariant.Double
        self.d_ptr.m_typeToAttributeToAttributeType[QVariant.Double][self.d_ptr.m_maximumAttribute] = QVariant.Double
        self.d_ptr.m_typeToAttributeToAttributeType[QVariant.Double][self.d_ptr.m_singleStepAttribute] = QVariant.Double
        self.d_ptr.m_typeToAttributeToAttributeType[QVariant.Double][self.d_ptr.m_decimalsAttribute] = QVariant.Int
        self.d_ptr.m_typeToAttributeToAttributeType[QVariant.Double][self.d_ptr.m_readOnlyAttribute] = QVariant.Bool
        self.d_ptr.m_typeToValueType[QVariant.Double] = QVariant.Double
        doublePropertyManager.valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        doublePropertyManager.rangeChangedSignal.connect(self.d_ptr.slotRangeChanged)
        doublePropertyManager.singleStepChangedSignal.connect(self.d_ptr.slotSingleStepChanged)
        doublePropertyManager.decimalsChangedSignal.connect(self.d_ptr.slotDecimalsChanged)
        boolPropertyManager = QtBoolPropertyManager(self)
        self.d_ptr.m_typeToPropertyManager[QVariant.Bool] = boolPropertyManager
        self.d_ptr.m_typeToAttributeToAttributeType[QVariant.Bool][self.d_ptr.m_textVisibleAttribute] = QVariant.Bool
        self.d_ptr.m_typeToValueType[QVariant.Bool] = QVariant.Bool
        boolPropertyManager.valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        boolPropertyManager.textVisibleChangedSignal.connect(self.d_ptr.slotTextVisibleChanged)
        stringPropertyManager = QtStringPropertyManager(self)
        self.d_ptr.m_typeToPropertyManager[QVariant.String] = stringPropertyManager
        self.d_ptr.m_typeToValueType[QVariant.String] = QVariant.String
        self.d_ptr.m_typeToAttributeToAttributeType[QVariant.String][self.d_ptr.m_regExpAttribute] = QVariant.RegExp
        self.d_ptr.m_typeToAttributeToAttributeType[QVariant.String][self.d_ptr.m_echoModeAttribute] = QVariant.Int
        self.d_ptr.m_typeToAttributeToAttributeType[QVariant.String][self.d_ptr.m_readOnlyAttribute] = QVariant.Bool

        stringPropertyManager.valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        stringPropertyManager.regExpChangedSignal.connect(self.d_ptr.slotRegExpChanged)
        stringPropertyManager.echoModeChangedSignal.connect(self.d_ptr.slotEchoModeChanged)
        stringPropertyManager.readOnlyChangedSignal.connect(self.d_ptr.slotReadOnlyChanged)

        datePropertyManager = QtDatePropertyManager(self)
        self.d_ptr.m_typeToPropertyManager[QVariant.Date] = datePropertyManager
        self.d_ptr.m_typeToValueType[QVariant.Date] = QVariant.Date
        self.d_ptr.m_typeToAttributeToAttributeType[QVariant.Date][self.d_ptr.m_minimumAttribute] = QVariant.Date
        self.d_ptr.m_typeToAttributeToAttributeType[QVariant.Date][self.d_ptr.m_maximumAttribute] = QVariant.Date
        datePropertyManager.valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        datePropertyManager.rangeChangedSignal.connect(self.d_ptr.slotRangeChanged)
        timePropertyManager = QtTimePropertyManager(self)
        self.d_ptr.m_typeToPropertyManager[QVariant.Time] = timePropertyManager
        self.d_ptr.m_typeToValueType[QVariant.Time] = QVariant.Time
        timePropertyManager.valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        dateTimePropertyManager = QtDateTimePropertyManager(self)
        self.d_ptr.m_typeToPropertyManager[QVariant.DateTime] = dateTimePropertyManager
        self.d_ptr.m_typeToValueType[QVariant.DateTime] = QVariant.DateTime
        dateTimePropertyManager.valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        keySequencePropertyManager = QtKeySequencePropertyManager(self)
        self.d_ptr.m_typeToPropertyManager[QVariant.KeySequence] = keySequencePropertyManager
        self.d_ptr.m_typeToValueType[QVariant.KeySequence] = QVariant.KeySequence
        keySequencePropertyManager.valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        charPropertyManager = QtCharPropertyManager(self)
        self.d_ptr.m_typeToPropertyManager[QVariant.Char] = charPropertyManager
        self.d_ptr.m_typeToValueType[QVariant.Char] = QVariant.String
        charPropertyManager.valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        localePropertyManager = QtLocalePropertyManager(self)
        self.d_ptr.m_typeToPropertyManager[QVariant.Locale] = localePropertyManager
        self.d_ptr.m_typeToValueType[QVariant.Locale] = QVariant.Locale
        localePropertyManager.valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        localePropertyManager.subEnumPropertyManager().valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        localePropertyManager.propertyInsertedSignal.connect(self.d_ptr.slotPropertyInserted)
        localePropertyManager.propertyRemovedSignal.connect(self.d_ptr.slotPropertyRemoved)
        pointPropertyManager = QtPointPropertyManager(self)
        self.d_ptr.m_typeToPropertyManager[QVariant.Point] = pointPropertyManager
        self.d_ptr.m_typeToValueType[QVariant.Point] = QVariant.Point
        pointPropertyManager.valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        pointPropertyManager.subIntPropertyManager().valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        pointPropertyManager.propertyInsertedSignal.connect(self.d_ptr.slotPropertyInserted)
        pointPropertyManager.propertyRemovedSignal.connect(self.d_ptr.slotPropertyRemoved)
        pointFPropertyManager = QtPointFPropertyManager(self)
        self.d_ptr.m_typeToPropertyManager[QVariant.PointF] = pointFPropertyManager
        self.d_ptr.m_typeToValueType[QVariant.PointF] = QVariant.PointF
        self.d_ptr.m_typeToAttributeToAttributeType[QVariant.PointF][self.d_ptr.m_decimalsAttribute] = QVariant.Int
        pointFPropertyManager.valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        pointFPropertyManager.decimalsChangedSignal.connect(self.d_ptr.slotDecimalsChanged)
        pointFPropertyManager.subDoublePropertyManager().valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        pointFPropertyManager.propertyInsertedSignal.connect(self.d_ptr.slotPropertyInserted)
        pointFPropertyManager.propertyRemovedSignal.connect(self.d_ptr.slotPropertyRemoved)
        sizePropertyManager = QtSizePropertyManager(self)
        self.d_ptr.m_typeToPropertyManager[QVariant.Size] = sizePropertyManager
        self.d_ptr.m_typeToValueType[QVariant.Size] = QVariant.Size
        self.d_ptr.m_typeToAttributeToAttributeType[QVariant.Size][self.d_ptr.m_minimumAttribute] = QVariant.Size
        self.d_ptr.m_typeToAttributeToAttributeType[QVariant.Size][self.d_ptr.m_maximumAttribute] = QVariant.Size
        sizePropertyManager.valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        sizePropertyManager.rangeChangedSignal.connect(self.d_ptr.slotRangeChanged)
        sizePropertyManager.subIntPropertyManager().valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        sizePropertyManager.subIntPropertyManager().rangeChangedSignal.connect(self.d_ptr.slotRangeChanged)
        sizePropertyManager.propertyInsertedSignal.connect(self.d_ptr.slotPropertyInserted)
        sizePropertyManager.propertyRemovedSignal.connect(self.d_ptr.slotPropertyRemoved)
        sizeFPropertyManager = QtSizeFPropertyManager(self)
        self.d_ptr.m_typeToPropertyManager[QVariant.SizeF] = sizeFPropertyManager
        self.d_ptr.m_typeToValueType[QVariant.SizeF] = QVariant.SizeF
        self.d_ptr.m_typeToAttributeToAttributeType[QVariant.SizeF][self.d_ptr.m_minimumAttribute] = QVariant.SizeF
        self.d_ptr.m_typeToAttributeToAttributeType[QVariant.SizeF][self.d_ptr.m_maximumAttribute] = QVariant.SizeF
        self.d_ptr.m_typeToAttributeToAttributeType[QVariant.SizeF][self.d_ptr.m_decimalsAttribute] = QVariant.Int
        sizeFPropertyManager.valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        sizeFPropertyManager.rangeChangedSignal.connect(self.d_ptr.slotRangeChanged)
        sizeFPropertyManager.decimalsChangedSignal.connect(self.d_ptr.slotDecimalsChanged)
        sizeFPropertyManager.subDoublePropertyManager().valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        sizeFPropertyManager.subDoublePropertyManager().rangeChangedSignal.connect(self.d_ptr.slotRangeChanged)
        sizeFPropertyManager.propertyInsertedSignal.connect(self.d_ptr.slotPropertyInserted)
        sizeFPropertyManager.propertyRemovedSignal.connect(self.d_ptr.slotPropertyRemoved)
        rectPropertyManager = QtRectPropertyManager(self)
        self.d_ptr.m_typeToPropertyManager[QVariant.Rect] = rectPropertyManager
        self.d_ptr.m_typeToValueType[QVariant.Rect] = QVariant.Rect
        self.d_ptr.m_typeToAttributeToAttributeType[QVariant.Rect][self.d_ptr.m_constraintAttribute] = QVariant.Rect
        rectPropertyManager.valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        rectPropertyManager.constraintChangedSignal.connect(self.d_ptr.slotConstraintChanged)
        rectPropertyManager.subIntPropertyManager().valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        rectPropertyManager.subIntPropertyManager().rangeChangedSignal.connect(self.d_ptr.slotRangeChanged)
        rectPropertyManager.propertyInsertedSignal.connect(self.d_ptr.slotPropertyInserted)
        rectPropertyManager.propertyRemovedSignal.connect(self.d_ptr.slotPropertyRemoved)
        rectFPropertyManager = QtRectFPropertyManager(self)
        self.d_ptr.m_typeToPropertyManager[QVariant.RectF] = rectFPropertyManager
        self.d_ptr.m_typeToValueType[QVariant.RectF] = QVariant.RectF
        self.d_ptr.m_typeToAttributeToAttributeType[QVariant.RectF][self.d_ptr.m_constraintAttribute] = QVariant.RectF
        self.d_ptr.m_typeToAttributeToAttributeType[QVariant.RectF][self.d_ptr.m_decimalsAttribute] = QVariant.Int
        rectFPropertyManager.valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        rectFPropertyManager.constraintChangedSignal.connect(self.d_ptr.slotConstraintChanged)
        rectFPropertyManager.decimalsChangedSignal.connect(self.d_ptr.slotDecimalsChanged)
        rectFPropertyManager.subDoublePropertyManager().valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        rectFPropertyManager.subDoublePropertyManager().rangeChangedSignal.connect(self.d_ptr.slotRangeChanged)
        rectFPropertyManager.propertyInsertedSignal.connect(self.d_ptr.slotPropertyInserted)
        rectFPropertyManager.propertyRemovedSignal.connect(self.d_ptr.slotPropertyRemoved)
        colorPropertyManager = QtColorPropertyManager(self)
        self.d_ptr.m_typeToPropertyManager[QVariant.Color] = colorPropertyManager
        self.d_ptr.m_typeToValueType[QVariant.Color] = QVariant.Color
        colorPropertyManager.valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        colorPropertyManager.subIntPropertyManager().valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        colorPropertyManager.propertyInsertedSignal.connect(self.d_ptr.slotPropertyInserted)
        colorPropertyManager.propertyRemovedSignal.connect(self.d_ptr.slotPropertyRemoved)
        enumId = QtVariantPropertyManager.enumTypeId()
        enumPropertyManager = QtEnumPropertyManager(self)
        self.d_ptr.m_typeToPropertyManager[enumId] = enumPropertyManager
        self.d_ptr.m_typeToValueType[enumId] = QVariant.Int
        self.d_ptr.m_typeToAttributeToAttributeType[enumId][self.d_ptr.m_enumNamesAttribute] = QVariant.StringList
        self.d_ptr.m_typeToAttributeToAttributeType[enumId][self.d_ptr.m_enumIconsAttribute] = QtVariantPropertyManager.iconMapTypeId()
        enumPropertyManager.valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        enumPropertyManager.enumNamesChangedSignal.connect(self.d_ptr.slotEnumNamesChanged)
        enumPropertyManager.enumIconsChangedSignal.connect(self.d_ptr.slotEnumIconsChanged)
        sizePolicyPropertyManager = QtSizePolicyPropertyManager(self)
        self.d_ptr.m_typeToPropertyManager[QVariant.SizePolicy] = sizePolicyPropertyManager
        self.d_ptr.m_typeToValueType[QVariant.SizePolicy] = QVariant.SizePolicy
        sizePolicyPropertyManager.valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        sizePolicyPropertyManager.subIntPropertyManager().valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        sizePolicyPropertyManager.subIntPropertyManager().rangeChangedSignal.connect(self.d_ptr.slotRangeChanged)
        sizePolicyPropertyManager.subEnumPropertyManager().valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        sizePolicyPropertyManager.subEnumPropertyManager().enumNamesChangedSignal.connect(self.d_ptr.slotEnumNamesChanged)
        sizePolicyPropertyManager.propertyInsertedSignal.connect(self.d_ptr.slotPropertyInserted)
        sizePolicyPropertyManager.propertyRemovedSignal.connect(self.d_ptr.slotPropertyRemoved)
        fontPropertyManager = QtFontPropertyManager(self)
        self.d_ptr.m_typeToPropertyManager[QVariant.Font] = fontPropertyManager
        self.d_ptr.m_typeToValueType[QVariant.Font] = QVariant.Font
        fontPropertyManager.valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        fontPropertyManager.subIntPropertyManager().valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        fontPropertyManager.subIntPropertyManager().rangeChangedSignal.connect(self.d_ptr.slotRangeChanged)
        fontPropertyManager.subEnumPropertyManager().valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        fontPropertyManager.subEnumPropertyManager().enumNamesChangedSignal.connect(self.d_ptr.slotEnumNamesChanged)
        fontPropertyManager.subBoolPropertyManager().valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        fontPropertyManager.propertyInsertedSignal.connect(self.d_ptr.slotPropertyInserted)
        fontPropertyManager.propertyRemovedSignal.connect(self.d_ptr.slotPropertyRemoved)
        cursorPropertyManager = QtCursorPropertyManager(self)
        self.d_ptr.m_typeToPropertyManager[QVariant.Cursor] = cursorPropertyManager
        self.d_ptr.m_typeToValueType[QVariant.Cursor] = QVariant.Cursor
        cursorPropertyManager.valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        flagId = QtVariantPropertyManager.flagTypeId()
        flagPropertyManager = QtFlagPropertyManager(self)
        self.d_ptr.m_typeToPropertyManager[flagId] = flagPropertyManager
        self.d_ptr.m_typeToValueType[flagId] = QVariant.Int
        self.d_ptr.m_typeToAttributeToAttributeType[flagId][self.d_ptr.m_flagNamesAttribute] = QVariant.StringList
        flagPropertyManager.valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        flagPropertyManager.flagNamesChangedSignal.connect(self.d_ptr.slotFlagNamesChanged)
        flagPropertyManager.subBoolPropertyManager().valueChangedSignal.connect(self.d_ptr.slotValueChanged)
        flagPropertyManager.propertyInsertedSignal.connect(self.d_ptr.slotPropertyInserted)
        flagPropertyManager.propertyRemovedSignal.connect(self.d_ptr.slotPropertyRemoved)
        groupId = QtVariantPropertyManager.groupTypeId()
        groupPropertyManager = QtGroupPropertyManager(self)
        self.d_ptr.m_typeToPropertyManager[groupId] = groupPropertyManager
        self.d_ptr.m_typeToValueType[groupId] = QVariant.Invalid

    ###
    #   Destroys this manager, and all the properties it has created.
    ###
    def __del__(self):
        self.clear()
        del self.d_ptr

    ###
    #   Returns the type id for an enum property.
    #
    #   Note that the property's value type can be retrieved using the
    #   valueType() function (which is QVariant.Int for the enum property
    #   type).
    #
    #   \sa propertyType(), valueType()
    ###
    def enumTypeId():
        return qMetaTypeId(QtEnumPropertyType)

    ###
    #   Returns the type id for a flag property.
    #
    #   Note that the property's value type can be retrieved using the
    #   valueType() function (which is QVariant.Int for the flag property
    #   type).
    #
    #   \sa propertyType(), valueType()
    ###
    def flagTypeId():
        return qMetaTypeId(QtFlagPropertyType)

    ###
    #   Returns the type id for a group property.
    #
    #   Note that the property's value type can be retrieved using the
    #   valueType() function (which is QVariant.Invalid for the group
    #   property type, since it doesn't provide any value).
    #
    #   \sa propertyType(), valueType()
    ###
    def groupTypeId():
        return qMetaTypeId(QtGroupPropertyType)

    ###
    #   Returns the type id for a icon map attribute.
    #
    #   Note that the property's attribute type can be retrieved using the
    #   attributeType() function.
    #
    #   \sa attributeType(), QtEnumPropertyManager.enumIcons()
    ###
    def iconMapTypeId():
        return qMetaTypeId(QtIconMap)

    ###
    #    Returns the given \a property converted into a QtVariantProperty.
    #
    #    If the \a property was not created by this variant manager, the:
    #    function returns 0.
    #
    #    \sa createProperty()
    ###
    def variantProperty(self, property):
        it = self.d_ptr.m_propertyToType.get(property)
        if not it:
            return 0
        return it[0]

    ###
    #    Returns True if the given \a propertyType is supported by this
    #    variant manager; otherwise False.
    #
    #    \sa propertyType()
    ###
    def isPropertyTypeSupported(self, propertyType):
        if (propertyType in self.d_ptr.m_typeToValueType.keys()):
            return True
        return False

    ###
    #   Creates and returns a variant property of the given \a propertyType
    #   with the given \a name.
    #
    #   If the specified \a propertyType is not supported by this variant
    #   manager, this function returns 0.
    #
    #   Do not use the inherited
    #   QtAbstractPropertyManager.addProperty() function to create a
    #   variant property (that function will always return 0 since it will
    #   not be clear what type the property should have).
    #
    #    \sa isPropertyTypeSupported()
    ###
    def addProperty(self, propertyType, name=''):
        if (not self.isPropertyTypeSupported(propertyType)):
            return 0

        wasCreating = self.d_ptr.m_creatingProperty
        self.d_ptr.m_creatingProperty = True
        self.d_ptr.m_propertyType = propertyType
        property = super(QtVariantPropertyManager, self).addProperty(name)
        self.d_ptr.m_creatingProperty = wasCreating
        self.d_ptr.m_propertyType = 0

        if (not property):
            return 0

        return self.variantProperty(property)

    ###
    #    Returns the given \a property's value.
    #
    #    If the given \a property is not managed by this manager, this:
    #    function returns an invalid variant.
    #
    #    \sa setValue()
    ###
    def value(self, property):
        internProp = propertyToWrappedProperty().get(property, 0)
        if (internProp == 0):
            return None

        manager = internProp.propertyManager()
        tm = type(manager)
        if tm == QtKeySequencePropertyManager:
            return QVariant(manager.value(internProp))
        else:
            return manager.value(internProp)

        return None

    ###
    #    Returns the given \a property's value type.
    #
    #    \sa propertyType()
    ###
    def valueType(self, property):
        propType = self.propertyType(property)
        return self._valueType(propType)

    ###
    #    \overload
    #
    #    Returns the value type associated with the given \a propertyType.
    ###
    def _valueType(self, propertyType):
        return self.d_ptr.m_typeToValueType.get(propertyType, 0)

    ###
    #    Returns the given \a property's type.
    #
    #    \sa valueType()
    ###
    def propertyType(self, property):
        it = self.d_ptr.m_propertyToType.get(property)
        if not it:
            return 0
        return it[1]

    ###
    #    Returns the given \a property's value for the specified \a
    #    attribute
    #
    #    If the given \a property was not created by \e this manager, or if:
    #    the specified \a attribute does not exist, this function returns
    #    an invalid variant.
    #
    #    \sa attributes(), attributeType(), setAttribute()
    ###
    def attributeValue(self, property, attribute):
        propType = self.propertyType(property)
        if (not propType):
            return None

        attributes = self.d_ptr.m_typeToAttributeToAttributeType.get(propType)
        if not attributes:
            return None

        attr = attributes.get(attribute)
        if not attr:
            return None

        internProp = propertyToWrappedProperty().get(property, 0)
        if (internProp == 0):
            return None

        manager = internProp.propertyManager()
        tm = type(manager)
        if tm == QtIntPropertyManager:
            if (attribute == self.d_ptr.m_maximumAttribute):
                return manager.maximum(internProp)
            if (attribute == self.d_ptr.m_minimumAttribute):
                return manager.minimum(internProp)
            if (attribute == self.d_ptr.m_singleStepAttribute):
                return manager.singleStep(internProp)
            if (attribute == self.d_ptr.m_readOnlyAttribute):
                return manager.isReadOnly(internProp)
            return None
        elif tm == QtDoublePropertyManager:
            if (attribute == self.d_ptr.m_maximumAttribute):
                return manager.maximum(internProp)
            if (attribute == self.d_ptr.m_minimumAttribute):
                return manager.minimum(internProp)
            if (attribute == self.d_ptr.m_singleStepAttribute):
                return manager.singleStep(internProp)
            if (attribute == self.d_ptr.m_decimalsAttribute):
                return manager.decimals(internProp)
            if (attribute == self.d_ptr.m_readOnlyAttribute):
                return manager.isReadOnly(internProp)
            return None
        elif tm == QtBoolPropertyManager:
            if (attribute == self.d_ptr.m_textVisibleAttribute):
                return manager.textVisible(internProp)
            return None
        elif tm == QtStringPropertyManager:
            if (attribute == self.d_ptr.m_regExpAttribute):
                return manager.regExp(internProp)
            if (attribute == self.d_ptr.m_echoModeAttribute):
                return manager.echoMode(internProp)
            if (attribute == self.d_ptr.m_readOnlyAttribute):
                return manager.isReadOnly(internProp)
            return None
        elif tm == QtDatePropertyManager:
            if (attribute == self.d_ptr.m_maximumAttribute):
                return manager.maximum(internProp)
            if (attribute == self.d_ptr.m_minimumAttribute):
                return manager.minimum(internProp)
            return None
        elif tm == QtPointFPropertyManager:
            if (attribute == self.d_ptr.m_decimalsAttribute):
                return manager.decimals(internProp)
            return None
        elif tm == QtSizePropertyManager:
            if (attribute == self.d_ptr.m_maximumAttribute):
                return manager.maximum(internProp)
            if (attribute == self.d_ptr.m_minimumAttribute):
                return manager.minimum(internProp)
            return None
        elif tm == QtSizeFPropertyManager:
            if (attribute == self.d_ptr.m_maximumAttribute):
                return manager.maximum(internProp)
            if (attribute == self.d_ptr.m_minimumAttribute):
                return manager.minimum(internProp)
            if (attribute == self.d_ptr.m_decimalsAttribute):
                return manager.decimals(internProp)
            return None
        elif tm == QtRectPropertyManager:
            if (attribute == self.d_ptr.m_constraintAttribute):
                return manager.constraint(internProp)
            return None
        elif tm == QtRectFPropertyManager:
            if (attribute == self.d_ptr.m_constraintAttribute):
                return manager.constraint(internProp)
            if (attribute == self.d_ptr.m_decimalsAttribute):
                return manager.decimals(internProp)
            return None
        elif tm == QtEnumPropertyManager:
            if (attribute == self.d_ptr.m_enumNamesAttribute):
                return manager.enumNames(internProp)
            if (attribute == self.d_ptr.m_enumIconsAttribute):
                v = QVariant(self.enumManager.enumIcons(internProp))
                return v
            return None
        elif tm == QtFlagPropertyManager:
            if (attribute == self.d_ptr.m_flagNamesAttribute):
                return manager.flagNames(internProp)
            return None
        return None

    ###
    #    Returns a list of the given \a propertyType 's attributes.
    #
    #    \sa attributeValue(), attributeType()
    ###
    def attributes(self, propertyType):
        it = self.d_ptr.m_typeToAttributeToAttributeType.get(propertyType)
        if not it:
            return []
        return it.keys()

    ###
    #    Returns the type of the specified \a attribute of the given \a
    #    propertyType.
    #
    #    If the given \a propertyType is not supported by \e this manager,:
    #    or if the given \a propertyType does not possess the specified \a
    #    attribute, this function returns QVariant.Invalid.
    #
    #    \sa attributes(), valueType()
    ###
    def attributeType(self, propertyType, attribute):
        it = self.d_ptr.m_typeToAttributeToAttributeType.get(propertyType)
        if not it:
            return 0

        attributes = it
        itAttr = attributes.get(attribute)
        if not itAttr:
            return 0
        return itAttr

    ###
    #    \fn void QtVariantPropertyManager.setValue(property, value)
    #
    #    Sets the value of the given \a property to \a value.
    #
    #    The specified \a value must be of a type returned by valueType(),
    #    or of type that can be converted to valueType() using the
    #    QVariant.canConvert() function, otherwise this function does
    #    nothing.
    #
    #    \sa value(), QtVariantProperty.setValue(), valueChanged()
    ###
    def setValue(self, property, val):
        propType = QVariant(val).userType()
        if (not propType):
            return

        valType = self.valueType(property)

        if (propType != valType and not QVariant(val).canConvert(valType)):
            return

        internProp = propertyToWrappedProperty().get(property, 0)
        if (internProp == 0):
            return

        manager = internProp.propertyManager()
        tm = type(manager)
        if tm==QtStringPropertyManager:
            tv = type(val)
            if tv==QUrl:
                val = val.toString()
            elif tv != str:
                val = str(val)
        manager.setValue(internProp, val)

    ###
    #    Sets the value of the specified \a attribute of the given \a
    #    property, to \a value.
    #
    #    The new \a value's type must be of the type returned by
    #    attributeType(), or of a type that can be converted to
    #    attributeType() using the QVariant.canConvert() function,
    #    otherwise this function does nothing.
    #
    #    \sa attributeValue(), QtVariantProperty.setAttribute(), attributeChanged()
    ###
    def setAttribute(self, property, attribute, value):
        if type(value)!=QVariant:
            value = QVariant(value)
        oldAttr = QVariant(self.attributeValue(property, attribute))
        if (not oldAttr.isValid()):
            return
        attrType = value.userType()
        if (not attrType):
            return

        if (attrType != self.attributeType(self.propertyType(property), attribute) and not value.canConvert(attrType)):
            return

        internProp = propertyToWrappedProperty().get(property, 0)
        if (internProp == 0):
            return

        manager = internProp.propertyManager()
        tm = type(manager)
        value = value.value()
        if tm == QtIntPropertyManager:
            if (attribute == self.d_ptr.m_maximumAttribute):
                manager.setMaximum(internProp, value)
            elif (attribute == self.d_ptr.m_minimumAttribute):
                manager.setMinimum(internProp, value)
            elif (attribute == self.d_ptr.m_singleStepAttribute):
                manager.setSingleStep(internProp, value)
            elif (attribute == self.d_ptr.m_readOnlyAttribute):
                manager.setReadOnly(internProp, value)
            return
        elif tm == QtDoublePropertyManager:
            if (attribute == self.d_ptr.m_maximumAttribute):
                manager.setMaximum(internProp, value)
            if (attribute == self.d_ptr.m_minimumAttribute):
                manager.setMinimum(internProp, value)
            if (attribute == self.d_ptr.m_singleStepAttribute):
                manager.setSingleStep(internProp, value)
            if (attribute == self.d_ptr.m_decimalsAttribute):
                manager.setDecimals(internProp, value)
            if (attribute == self.d_ptr.m_readOnlyAttribute):
                manager.setReadOnly(internProp, value)
            return
        elif tm == QtBoolPropertyManager:
            if (attribute == self.d_ptr.m_textVisibleAttribute):
                manager.setTextVisible(internProp, value)
            return
        elif tm == QtStringPropertyManager:
            if (attribute == self.d_ptr.m_regExpAttribute):
                manager.setRegExp(internProp, value)
            if (attribute == self.d_ptr.m_echoModeAttribute):
                manager.setEchoMode(internProp, value)
            if (attribute == self.d_ptr.m_readOnlyAttribute):
                manager.setReadOnly(internProp, value)
            return
        elif tm == QtDatePropertyManager:
            if (attribute == self.d_ptr.m_maximumAttribute):
                manager.setMaximum(internProp, value)
            if (attribute == self.d_ptr.m_minimumAttribute):
                manager.setMinimum(internProp, value)
            return
        elif tm == QtPointFPropertyManager:
            if (attribute == self.d_ptr.m_decimalsAttribute):
                manager.setDecimals(internProp, value)
            return
        elif tm == QtSizePropertyManager:
            if (attribute == self.d_ptr.m_maximumAttribute):
                manager.setMaximum(internProp, value)
            if (attribute == self.d_ptr.m_minimumAttribute):
                manager.setMinimum(internProp, value)
            return
        elif tm == QtSizeFPropertyManager:
            if (attribute == self.d_ptr.m_maximumAttribute):
                manager.setMaximum(internProp, value)
            if (attribute == self.d_ptr.m_minimumAttribute):
                manager.setMinimum(internProp, value)
            if (attribute == self.d_ptr.m_decimalsAttribute):
                manager.setDecimals(internProp, value)
            return
        elif tm == QtRectPropertyManager:
            if (attribute == self.d_ptr.m_constraintAttribute):
                manager.setConstraint(internProp, value)
            return
        elif tm == QtRectFPropertyManager:
            if (attribute == self.d_ptr.m_constraintAttribute):
                manager.setConstraint(internProp, value)
            if (attribute == self.d_ptr.m_decimalsAttribute):
                manager.setDecimals(internProp, value)
            return
        elif tm == QtEnumPropertyManager:
            if (attribute == self.d_ptr.m_enumNamesAttribute):
                manager.setEnumNames(internProp, value)
            if (attribute == self.d_ptr.m_enumIconsAttribute):
                manager.setEnumIcons(internProp, value)
            return
        elif tm == QtFlagPropertyManager:
            if (attribute == self.d_ptr.m_flagNamesAttribute):
                manager.setFlagNames(internProp, value)
            return

    ###
    #    \reimp
    ###
    def hasValue(self, property):
        if (self.propertyType(property) == QtVariantPropertyManager.groupTypeId()):
            return False
        return True

    ###
    #    \reimp
    ###
    def valueText(self, property):
        internProp = propertyToWrappedProperty().get(property, 0)
        if internProp:
            if len(internProp.displayText())>0:
                return internProp.displayText()
            else:
                return internProp.valueText()
        else:
            return ''

    ###
    #    \reimp
    ###
    def valueIcon(self, property):
        internProp = propertyToWrappedProperty().get(property, 0)
        if internProp:
            return internProp.valueIcon()
        else:
            return QIcon()

    ###
    #    \reimp
    ###
    def initializeProperty(self, property):
        varProp = self.variantProperty(property)
        if (not varProp):
            return

        it = self.d_ptr.m_typeToPropertyManager.get(self.d_ptr.m_propertyType)
        if it:
            internProp = 0
            if (not self.d_ptr.m_creatingSubProperties):
                manager = it
                internProp = manager.addProperty()
                self.d_ptr.m_internalToProperty[internProp] = varProp

            propertyToWrappedProperty()[varProp] = internProp
            if (internProp):
                children = internProp.subProperties()
                lastProperty = 0
                for itChild in children:
                    prop = self.d_ptr.createSubProperty(varProp, lastProperty, itChild)
                    if prop:
                        lastProperty = prop

    ###
    #    \reimp
    ###
    def uninitializeProperty(self, property):
        type_it = self.d_ptr.m_propertyToType.get(property)
        if not type_it:
            return

        x = propertyToWrappedProperty()
        it = x.get(property)
        if it:
            internProp = it
            if (internProp):
                self.d_ptr.m_internalToProperty.remove(internProp)
                if (not self.d_ptr.m_destroyingSubProperties):
                    del internProp

            x.erase(property)

        self.d_ptr.m_propertyToType.erase(property)

    ###
    #    \reimp
    ###
    def createProperty(self):
        if (not self.d_ptr.m_creatingProperty):
            return 0

        property = QtVariantProperty(self)
        self.d_ptr.m_propertyToType[property] = (property, self.d_ptr.m_propertyType)
        return property

class QtVariantEditorFactoryPrivate():
    def __init__(self):
        self.q_ptr = None
        self.m_spinBoxFactory = None
        self.m_doubleSpinBoxFactory = None
        self.m_checkBoxFactory = None
        self.m_lineEditFactory = None
        self.m_dateEditFactory = None
        self.m_timeEditFactory = None
        self.m_dateTimeEditFactory = None
        self.m_keySequenceEditorFactory = None
        self.m_charEditorFactory = None
        self.m_comboBoxFactory = None
        self.m_cursorEditorFactory = None
        self.m_colorEditorFactory = None
        self.m_fontEditorFactory = None
        self.m_factoryToType = QMap()
        self.m_typeToFactory = QMap()

###
#    \class QtVariantEditorFactory
#
#    \brief The QtVariantEditorFactory class provides widgets for properties
#    created by QtVariantPropertyManager objects.
#
#    The variant factory provides the following widgets for the
#    specified property types:
#
#    \table
#    \header
#        \o Property Type
#        \o Widget
#    \row
#        \o \c int
#        \o QSpinBox
#    \row
#        \o \c double
#        \o QDoubleSpinBox
#    \row
#        \o \c bool
#        \o QCheckBox
#    \row
#        \o QString
#        \o QLineEdit
#    \row
#        \o QDate
#        \o QDateEdit
#    \row
#        \o QTime
#        \o QTimeEdit
#    \row
#        \o QDateTime
#        \o QDateTimeEdit
#    \row
#        \o QKeySequence
#        \o customized editor
#    \row
#        \o QChar
#        \o customized editor
#    \row
#        \o \c enum
#        \o QComboBox
#    \row
#        \o QCursor
#        \o QComboBox
#    \endtable
#
#    Note that QtVariantPropertyManager supports several additional property
#    types for which the QtVariantEditorFactory class does not provide
#    editing widgets, e.g. QPoint and QSize. To provide widgets for other
#    types using the variant approach, derive from the QtVariantEditorFactory
#    class.
#
#    \sa QtAbstractEditorFactory, QtVariantPropertyManager
###
class QtVariantEditorFactory(QtAbstractEditorFactory):
    ###
    #    Creates a factory with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtVariantEditorFactory, self).__init__(parent)

        self.d_ptr = QtVariantEditorFactoryPrivate()
        self.d_ptr.q_ptr = self

        self.d_ptr.m_spinBoxFactory = QtSpinBoxFactory(self)
        self.d_ptr.m_factoryToType[self.d_ptr.m_spinBoxFactory] = QVariant.Int
        self.d_ptr.m_typeToFactory[QVariant.Int] = self.d_ptr.m_spinBoxFactory

        self.d_ptr.m_doubleSpinBoxFactory = QtDoubleSpinBoxFactory(self)
        self.d_ptr.m_factoryToType[self.d_ptr.m_doubleSpinBoxFactory] = QVariant.Double
        self.d_ptr.m_typeToFactory[QVariant.Double] = self.d_ptr.m_doubleSpinBoxFactory

        self.d_ptr.m_checkBoxFactory = QtCheckBoxFactory(self)
        self.d_ptr.m_factoryToType[self.d_ptr.m_checkBoxFactory] = QVariant.Bool
        self.d_ptr.m_typeToFactory[QVariant.Bool] = self.d_ptr.m_checkBoxFactory

        self.d_ptr.m_lineEditFactory = QtLineEditFactory(self)
        self.d_ptr.m_factoryToType[self.d_ptr.m_lineEditFactory] = QVariant.String
        self.d_ptr.m_typeToFactory[QVariant.String] = self.d_ptr.m_lineEditFactory

        self.d_ptr.m_dateEditFactory = QtDateEditFactory(self)
        self.d_ptr.m_factoryToType[self.d_ptr.m_dateEditFactory] = QVariant.Date
        self.d_ptr.m_typeToFactory[QVariant.Date] = self.d_ptr.m_dateEditFactory

        self.d_ptr.m_timeEditFactory = QtTimeEditFactory(self)
        self.d_ptr.m_factoryToType[self.d_ptr.m_timeEditFactory] = QVariant.Time
        self.d_ptr.m_typeToFactory[QVariant.Time] = self.d_ptr.m_timeEditFactory

        self.d_ptr.m_dateTimeEditFactory = QtDateTimeEditFactory(self)
        self.d_ptr.m_factoryToType[self.d_ptr.m_dateTimeEditFactory] = QVariant.DateTime
        self.d_ptr.m_typeToFactory[QVariant.DateTime] = self.d_ptr.m_dateTimeEditFactory

        self.d_ptr.m_keySequenceEditorFactory = QtKeySequenceEditorFactory(self)
        self.d_ptr.m_factoryToType[self.d_ptr.m_keySequenceEditorFactory] = QVariant.KeySequence
        self.d_ptr.m_typeToFactory[QVariant.KeySequence] = self.d_ptr.m_keySequenceEditorFactory

        self.d_ptr.m_charEditorFactory = QtCharEditorFactory(self)
        self.d_ptr.m_factoryToType[self.d_ptr.m_charEditorFactory] = QVariant.Char
        self.d_ptr.m_typeToFactory[QVariant.Char] = self.d_ptr.m_charEditorFactory

        self.d_ptr.m_cursorEditorFactory = QtCursorEditorFactory(self)
        self.d_ptr.m_factoryToType[self.d_ptr.m_cursorEditorFactory] = QVariant.Cursor
        self.d_ptr.m_typeToFactory[QVariant.Cursor] = self.d_ptr.m_cursorEditorFactory

        self.d_ptr.m_colorEditorFactory = QtColorEditorFactory(self)
        self.d_ptr.m_factoryToType[self.d_ptr.m_colorEditorFactory] = QVariant.Color
        self.d_ptr.m_typeToFactory[QVariant.Color] = self.d_ptr.m_colorEditorFactory

        self.d_ptr.m_fontEditorFactory = QtFontEditorFactory(self)
        self.d_ptr.m_factoryToType[self.d_ptr.m_fontEditorFactory] = QVariant.Font
        self.d_ptr.m_typeToFactory[QVariant.Font] = self.d_ptr.m_fontEditorFactory

        self.d_ptr.m_comboBoxFactory = QtEnumEditorFactory(self)
        enumId = QtVariantPropertyManager.enumTypeId()
        self.d_ptr.m_factoryToType[self.d_ptr.m_comboBoxFactory] = enumId
        self.d_ptr.m_typeToFactory[enumId] = self.d_ptr.m_comboBoxFactory

    ###
    #   Destroys this factory, and all the widgets it has created.
    ###
    def __del__(self):
        del self.d_ptr

    ###
    #    \internal
    #
    #    Reimplemented from the QtAbstractEditorFactory class.
    ###
    def connectPropertyManager(self, manager):
        intPropertyManagers = manager.findChildren(QtIntPropertyManager)
        for itInt in intPropertyManagers:
            self.d_ptr.m_spinBoxFactory.addPropertyManager(itInt)

        doublePropertyManagers = manager.findChildren(QtDoublePropertyManager)
        for itDouble in doublePropertyManagers:
            self.d_ptr.m_doubleSpinBoxFactory.addPropertyManager(itDouble)

        boolPropertyManagers = manager.findChildren(QtBoolPropertyManager)
        for itBool in boolPropertyManagers:
            self.d_ptr.m_checkBoxFactory.addPropertyManager(itBool)

        stringPropertyManagers = manager.findChildren(QtStringPropertyManager)
        for itString in stringPropertyManagers:
            self.d_ptr.m_lineEditFactory.addPropertyManager(itString)

        datePropertyManagers = manager.findChildren(QtDatePropertyManager)
        for itDate in datePropertyManagers:
            self.d_ptr.m_dateEditFactory.addPropertyManager(itDate)

        timePropertyManagers = manager.findChildren(QtTimePropertyManager)
        for itTime in timePropertyManagers:
            self.d_ptr.m_timeEditFactory.addPropertyManager(itTime)

        dateTimePropertyManagers = manager.findChildren(QtDateTimePropertyManager)
        for itDateTime in dateTimePropertyManagers:
            self.d_ptr.m_dateTimeEditFactory.addPropertyManager(itDateTime)

        keySequencePropertyManagers = manager.findChildren(QtKeySequencePropertyManager)
        for itKeySequence in keySequencePropertyManagers:
            self.d_ptr.m_keySequenceEditorFactory.addPropertyManager(itKeySequence)

        charPropertyManagers = manager.findChildren(QtCharPropertyManager)
        for itChar in charPropertyManagers:
            self.d_ptr.m_charEditorFactory.addPropertyManager(itChar)

        localePropertyManagers = manager.findChildren(QtLocalePropertyManager)
        for itLocale in localePropertyManagers:
            self.d_ptr.m_comboBoxFactory.addPropertyManager(itLocale.subEnumPropertyManager())

        pointPropertyManagers = manager.findChildren(QtPointPropertyManager)
        for itPoint in pointPropertyManagers:
            self.d_ptr.m_spinBoxFactory.addPropertyManager(itPoint.subIntPropertyManager())

        pointFPropertyManagers = manager.findChildren(QtPointFPropertyManager)
        for itPointF in pointFPropertyManagers:
            self.d_ptr.m_doubleSpinBoxFactory.addPropertyManager(itPointF.subDoublePropertyManager())

        sizePropertyManagers = manager.findChildren(QtSizePropertyManager)
        for itSize in sizePropertyManagers:
            self.d_ptr.m_spinBoxFactory.addPropertyManager(itSize.subIntPropertyManager())

        sizeFPropertyManagers = manager.findChildren(QtSizeFPropertyManager)
        for itSizeF in sizeFPropertyManagers:
            self.d_ptr.m_doubleSpinBoxFactory.addPropertyManager(itSizeF.subDoublePropertyManager())

        rectPropertyManagers = manager.findChildren(QtRectPropertyManager)
        for itRect in rectPropertyManagers:
            self.d_ptr.m_spinBoxFactory.addPropertyManager(itRect.subIntPropertyManager())

        rectFPropertyManagers = manager.findChildren(QtRectFPropertyManager)
        for itRectF in rectFPropertyManagers:
            self.d_ptr.m_doubleSpinBoxFactory.addPropertyManager(itRectF.subDoublePropertyManager())

        colorPropertyManagers = manager.findChildren(QtColorPropertyManager)
        for itColor in colorPropertyManagers:
            self.d_ptr.m_colorEditorFactory.addPropertyManager(itColor)
            self.d_ptr.m_spinBoxFactory.addPropertyManager(itColor.subIntPropertyManager())

        enumPropertyManagers = manager.findChildren(QtEnumPropertyManager)
        for itEnum in enumPropertyManagers:
            self.d_ptr.m_comboBoxFactory.addPropertyManager(itEnum)

        sizePolicyPropertyManagers = manager.findChildren(QtSizePolicyPropertyManager)
        for itSizePolicy in sizePolicyPropertyManagers:
            self.d_ptr.m_spinBoxFactory.addPropertyManager(itSizePolicy.subIntPropertyManager())
            self.d_ptr.m_comboBoxFactory.addPropertyManager(itSizePolicy.subEnumPropertyManager())

        fontPropertyManagers = manager.findChildren(QtFontPropertyManager)
        for itFont in fontPropertyManagers:
            self.d_ptr.m_fontEditorFactory.addPropertyManager(itFont)
            self.d_ptr.m_spinBoxFactory.addPropertyManager(itFont.subIntPropertyManager())
            self.d_ptr.m_comboBoxFactory.addPropertyManager(itFont.subEnumPropertyManager())
            self.d_ptr.m_checkBoxFactory.addPropertyManager(itFont.subBoolPropertyManager())

        cursorPropertyManagers = manager.findChildren(QtCursorPropertyManager)
        for itCursor in cursorPropertyManagers:
            self.d_ptr.m_cursorEditorFactory.addPropertyManager(itCursor)

        flagPropertyManagers = manager.findChildren(QtFlagPropertyManager)
        for itFlag in flagPropertyManagers:
            self.d_ptr.m_checkBoxFactory.addPropertyManager(itFlag.subBoolPropertyManager())

    ###
    #    \internal
    #
    #    Reimplemented from the QtAbstractEditorFactory class.
    ###
    def createEditor(self, manager, property, parent):
        propType = manager.propertyType(property)
        factory = self.d_ptr.m_typeToFactory.get(propType, 0)
        if (not factory):
            return 0
        return factory.findEditor(wrappedProperty(property), parent)

    ###
    #    \internal
    #
    #    Reimplemented from the QtAbstractEditorFactory class.
    ###
    def disconnectPropertyManager(self, manager):
        intPropertyManagers = self.findChildren(manager)
        for itInt in intPropertyManagers:
            self.d_ptr.m_spinBoxFactory.removePropertyManager(itInt)

        doublePropertyManagers = self.findChildren(manager)
        for itDouble in doublePropertyManagers:
            self.d_ptr.m_doubleSpinBoxFactory.removePropertyManager(itDouble)

        boolPropertyManagers = self.findChildren(manager)
        for itBool in boolPropertyManagers:
            self.d_ptr.m_checkBoxFactory.removePropertyManager(itBool)

        stringPropertyManagers = self.findChildren(manager)
        for itString in stringPropertyManagers:
            self.d_ptr.m_lineEditFactory.removePropertyManager(itString)

        datePropertyManagers = self.findChildren(manager)
        for itDate in datePropertyManagers:
            self.d_ptr.m_dateEditFactory.removePropertyManager(itDate)

        timePropertyManagers = self.findChildren(manager)
        for itTime in timePropertyManagers:
            self.d_ptr.m_timeEditFactory.removePropertyManager(itTime)

        dateTimePropertyManagers = self.findChildren(manager)
        for itDateTime in dateTimePropertyManagers:
            self.d_ptr.m_dateTimeEditFactory.removePropertyManager(itDateTime)

        keySequencePropertyManagers = self.findChildren(manager)
        for itKeySequence in keySequencePropertyManagers:
            self.d_ptr.m_keySequenceEditorFactory.removePropertyManager(itKeySequence)

        charPropertyManagers = self.findChildren(manager)
        for itChar in charPropertyManagers:
            self.d_ptr.m_charEditorFactory.removePropertyManager(itChar)

        localePropertyManagers = self.findChildren(manager)
        for itLocale in localePropertyManagers:
            self.d_ptr.m_comboBoxFactory.removePropertyManager(itLocale.subEnumPropertyManager())

        pointPropertyManagers = self.findChildren(manager)
        for itPoint in pointPropertyManagers:
            self.d_ptr.m_spinBoxFactory.removePropertyManager(itPoint.subIntPropertyManager())

        pointFPropertyManagers = self.findChildren(manager)
        for itPointF in pointFPropertyManagers:
            self.d_ptr.m_doubleSpinBoxFactory.removePropertyManager(itPointF.subDoublePropertyManager())

        sizePropertyManagers = self.findChildren(manager)
        for itSize in sizePropertyManagers:
            self.d_ptr.m_spinBoxFactory.removePropertyManager(itSize.subIntPropertyManager())

        sizeFPropertyManagers = self.findChildren(manager)
        for itSizeF in sizeFPropertyManagers:
            self.d_ptr.m_doubleSpinBoxFactory.removePropertyManager(itSizeF.subDoublePropertyManager())

        rectPropertyManagers = self.findChildren(manager)
        for itRect in rectPropertyManagers:
            self.d_ptr.m_spinBoxFactory.removePropertyManager(itRect.subIntPropertyManager())

        rectFPropertyManagers = self.findChildren(manager)
        for itRectF in rectFPropertyManagers:
            self.d_ptr.m_doubleSpinBoxFactory.removePropertyManager(itRectF.subDoublePropertyManager())

        colorPropertyManagers = self.findChildren(manager)
        for itColor in colorPropertyManagers:
            self.d_ptr.m_colorEditorFactory.removePropertyManager(itColor)
            self.d_ptr.m_spinBoxFactory.removePropertyManager(itColor.subIntPropertyManager())

        enumPropertyManagers = self.findChildren(manager)
        for itEnum in enumPropertyManagers:
            self.d_ptr.m_comboBoxFactory.removePropertyManager(itEnum)

        sizePolicyPropertyManagers = self.findChildren(manager)
        for itSizePolicy in sizePolicyPropertyManagers:
            self.d_ptr.m_spinBoxFactory.removePropertyManager(itSizePolicy.subIntPropertyManager())
            self.d_ptr.m_comboBoxFactory.removePropertyManager(itSizePolicy.subEnumPropertyManager())

        fontPropertyManagers = self.findChildren(manager)
        for itFont in fontPropertyManagers:
            self.d_ptr.m_fontEditorFactory.removePropertyManager(itFont)
            self.d_ptr.m_spinBoxFactory.removePropertyManager(itFont.subIntPropertyManager())
            self.d_ptr.m_comboBoxFactory.removePropertyManager(itFont.subEnumPropertyManager())
            self.d_ptr.m_checkBoxFactory.removePropertyManager(itFont.subBoolPropertyManager())

        cursorPropertyManagers = self.findChildren(manager)
        for itCursor in cursorPropertyManagers:
            self.d_ptr.m_cursorEditorFactory.removePropertyManager(itCursor)

        flagPropertyManagers = self.findChildren(manager)
        for itFlag in flagPropertyManagers:
            self.d_ptr.m_checkBoxFactory.removePropertyManager(itFlag.subBoolPropertyManager())
