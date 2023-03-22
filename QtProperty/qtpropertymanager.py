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

import copy
from PyQt5.QtCore import (
    QObject,
    QLocale,
    QSize,
    QPoint,
    QRect,
    QRectF,
    QRegExp,
    Qt,
    QDate,
    QTime,
    QDateTime,
    QSizeF,
    QTimer,
    qAddPostRoutine,
    QCoreApplication,
    pyqtSignal,
    QPointF,
    pyqtProperty
)

from PyQt5.QtWidgets import (
    QStyle,
    QApplication,
    QSizePolicy,
    QLineEdit,
    QStyleOptionButton
    )
from PyQt5.QtGui import (
    QIcon,
    QPainter,
    QPixmap,
    QKeySequence,
    QCursor,
    QFontDatabase,
    QFont,
    QColor,
    QBrush
    )

from qtpropertybrowser import QtProperty, QtAbstractPropertyManager
from qtpropertybrowserutils import QtPropertyBrowserUtils, QtCursorDatabase
from pyqtcore import QList, QMap, QMapList, QMapMap, INT_MAX, INT_MIN

DATA_VAL            = 1
DATA_MINVAL         = 2
DATA_MAXVAL         = 3
DATA_SINGLESTEP     = 4
DATA_READONLY       = 5
DATA_DECIMALS       = 6
DATA_TEXTVISIBLE    = 7
DATA_ENUMNAMES      = 8
DATA_FLAGNAMES      = 9
DATA_REGEXP         = 10
DATA_ECHOMODE       = 11
DATA_CONSTRAINT     = 12
DATA_ENUMICONS      = 13
DATA_GETMINVAL      = 20
DATA_GETMAXVAL      = 21
DATA_SETMINVAL      = 22
DATA_SETMAXVAL      = 23

def setSimpleMinimumData(data, minVal):
    data.minVal = minVal
    if (data.maxVal < data.minVal):
        data.maxVal = data.minVal

    if (data.val < data.minVal):
        data.val = data.minVal

def setSimpleMaximumData(data, maxVal):
    data.maxVal = maxVal
    if (data.minVal > data.maxVal):
        data.minVal = data.maxVal

    if (data.val > data.maxVal):
        data.val = data.maxVal

def setSizeMinimumData(data, newMinVal):
    data.minVal = newMinVal
    if (data.maxVal.width() < data.minVal.width()):
        data.maxVal.setWidth(data.minVal.width())
    if (data.maxVal.height() < data.minVal.height()):
        data.maxVal.setHeight(data.minVal.height())

    if (data.val.width() < data.minVal.width()):
        data.val.setWidth(data.minVal.width())
    if (data.val.height() < data.minVal.height()):
        data.val.setHeight(data.minVal.height())

def setSizeMaximumData(data, newMaxVal):
    data.maxVal = newMaxVal
    if (data.minVal.width() > data.maxVal.width()):
        data.minVal.setWidth(data.maxVal.width())
    if (data.minVal.height() > data.maxVal.height()):
        data.minVal.setHeight(data.maxVal.height())

    if (data.val.width() > data.maxVal.width()):
        data.val.setWidth(data.maxVal.width())
    if (data.val.height() > data.maxVal.height()):
        data.val.setHeight(data.maxVal.height())

def qBoundSize(minVal, val, maxVal):
    t1 = type(minVal)
    t2 = type(val)
    t3 = type(maxVal)
    croppedVal = val
    if t1==t2==t3:
        if t1 in [QSize, QSizeF]:
            if (minVal.width() > val.width()):
                croppedVal.setWidth(minVal.width())
            elif (maxVal.width() < val.width()):
                croppedVal.setWidth(maxVal.width())

            if (minVal.height() > val.height()):
                croppedVal.setHeight(minVal.height())
            elif (maxVal.height() < val.height()):
                croppedVal.setHeight(maxVal.height())
        else:
            croppedVal = max(min(maxVal, croppedVal), minVal)

    return croppedVal

# Match the exact signature of qBound for VS 6.
def qBound(minVal, val, maxVal):
    t1 = type(minVal)
    t2 = type(val)
    t3 = type(maxVal)
    if t1 in [QSize, QSizeF] and t2 in [QSize, QSizeF] and t3 in [QSize, QSizeF]:
        return qBoundSize(minVal, val, maxVal)
    else:
        return max(min(maxVal, val), minVal)

def orderSizeBorders(minVal, maxVal):
    fromSize = minVal
    toSize = maxVal
    if (fromSize.width() > toSize.width()):
        fromSize.setWidth(maxVal.width())
        toSize.setWidth(minVal.width())

    if (fromSize.height() > toSize.height()):
        fromSize.setHeight(maxVal.height())
        toSize.setHeight(minVal.height())

    return (fromSize,toSize)

def orderBorders(minVal, maxVal):
    t1 = type(minVal)
    t2 = type(maxVal)

    if t1 in [QSize, QSizeF] and t2 in [QSize, QSizeF]:
        orderSizeBorders(minVal, maxVal)
    else:
        if (minVal > maxVal):
            minVal, maxVal = maxVal, minVal

def getData(propertyMap, data, property, defaultValue = None):
    it = propertyMap.get(property)
    if not it:
        return defaultValue
    if data == DATA_MINVAL:
        return it.minVal
    elif data == DATA_MAXVAL:
        return it.maxVal
    elif data == DATA_SINGLESTEP:
        return it.singleStep
    elif data == DATA_READONLY:
        return it.readOnly
    elif data == DATA_DECIMALS:
        return it.decimals
    elif data == DATA_TEXTVISIBLE:
        return it.textVisible
    elif data == DATA_ENUMNAMES:
        return it.enumNames
    elif data == DATA_ENUMICONS:
        return it.enumIcons
    elif data == DATA_FLAGNAMES:
        return it.flagNames
    elif data == DATA_REGEXP:
        return it.regExp
    elif data == DATA_ECHOMODE:
        return it.echoMode
    else:
        return it.val

def getValue(propertyMap, property, defaultValue = None):
    return getData(propertyMap, DATA_VAL, property, defaultValue)

def getMinimum(propertyMap, property, defaultValue = None):
    return getData(propertyMap, DATA_MINVAL, property, defaultValue)

def getMaximum(propertyMap, property, defaultValue = None):
    return getData(propertyMap, DATA_MAXVAL, property, defaultValue)

def setSimpleValue(propertyMap, manager,propertyChangedSignal,valueChangedSignal, property, val):
    if not property in propertyMap.keys():
        return

    if (propertyMap[property] == val):
        return

    propertyMap[property] = val

    propertyChangedSignal.emit(property)
    valueChangedSignal.emit(property, val)

def setValueInRange(manager, managerPrivate, propertyChangedSignal, valueChangedSignal, property, val, setSubPropertyValue=None):
    if not property in managerPrivate.m_values.keys():
        return

    data = managerPrivate.m_values[property]

    if (data.val == val):
        return

    oldVal = data.val

    data.val = qBound(data.minVal, val, data.maxVal)

    if data.val == oldVal:
        return

    if setSubPropertyValue:
        setSubPropertyValue(property, data.val)

    propertyChangedSignal.emit(property)
    valueChangedSignal.emit(property, data.val)

def setBorderValues(manager, managerPrivate, propertyChangedSignal, valueChangedSignal, rangeChangedSignal, property, minVal, maxVal,setSubPropertyRange):
    if not property in managerPrivate.m_values.keys():
        return

    fromVal = minVal
    toVal = maxVal
    t1 = type(minVal)
    t2 = type(maxVal)

    if t1 in [QSize, QSizeF] and t2 in [QSize, QSizeF]:
        t = orderSizeBorders(minVal, maxVal)
        fromVal, toVal = t[0], t[1]
    else:
        if (fromVal > toVal):
            fromVal, toVal = toVal, fromVal

    data = managerPrivate.m_values[property]

    if (data.minVal == fromVal and data.maxVal == toVal):
        return

    oldVal = data.val

    data.setMinimumValue(fromVal)
    data.setMaximumValue(toVal)

    rangeChangedSignal.emit(property, data.minVal, data.maxVal)

    if (setSubPropertyRange):
        setSubPropertyRange(property, data.minVal, data.maxVal, data.val)

    if (data.val == oldVal):
        return

    propertyChangedSignal.emit(property)
    valueChangedSignal.emit(property, data.val)

def setBorderValue(manager, managerPrivate, propertyChangedSignal, valueChangedSignal,rangeChangedSignal, property,getRangeVal,setRangeVal,borderVal, setSubPropertyRange):
    if not property in managerPrivate.m_values.keys():
        return

    data = managerPrivate.m_values[property]

    if getRangeVal == DATA_GETMINVAL:
        bval = data.minimumValue()
    elif getRangeVal == DATA_GETMAXVAL:
        bval = data.maximumValue()
    else:
        bval = data.val
    if (bval == borderVal):
        return

    oldVal = data.val
    if setRangeVal == DATA_SETMINVAL:
        data.setMinimumValue(borderVal)
    elif setRangeVal == DATA_SETMAXVAL:
        data.setMaximumValue(borderVal)
    else:
        pass

    rangeChangedSignal.emit(property, data.minVal, data.maxVal)

    if (setSubPropertyRange):
        setSubPropertyRange(property, data.minVal, data.maxVal, data.val)

    if (data.val == oldVal):
        return

    propertyChangedSignal.emit(property)
    valueChangedSignal.emit(property, data.val)

def setMinimumValue(manager, managerPrivate, propertyChangedSignal, valueChangedSignal, rangeChangedSignal, property, minVal):
    setSubPropertyRange = 0
    setBorderValue(manager, managerPrivate,
            propertyChangedSignal, valueChangedSignal, rangeChangedSignal,
            property, DATA_GETMINVAL, DATA_SETMINVAL, minVal, setSubPropertyRange)

def setMaximumValue(manager, managerPrivate, propertyChangedSignal, valueChangedSignal, rangeChangedSignal, property, maxVal):
    setSubPropertyRange = 0
    setBorderValue(manager, managerPrivate, propertyChangedSignal, valueChangedSignal, rangeChangedSignal, property, DATA_GETMAXVAL, DATA_SETMAXVAL, maxVal, setSubPropertyRange)

class QtMetaEnumWrapper(QObject):
    def __init__(self, parent):
        super(QtMetaEnumWrapper,self).__init__(parent)

        self.policy()

    def policy(self):
        return QSizePolicy.Ignored
    policy = pyqtProperty(QSizePolicy.Policy, fget=policy)

class QtMetaEnumProvider():
    def __init__(self):
        self.m_languageEnumNames = QList()
        self.m_countryEnumNames = QMap()
        self.m_indexToLanguage = QMap()
        self.m_languageToIndex = QMap()
        self.m_indexToCountry = QMapMap()
        self.m_countryToIndex = QMapMap()
        self.m_policyEnumNames = {0:'Fixed', 1:'Minimum', 4:'Maximum', 5:'Preferred', 7:'Expanding', 3:'MinimumExpanding', 13:'Ignored'}
        self.initLocale()

    def policyEnumValueNames(self):
        return self.m_policyEnumNames

    def policyEnumNames(self):
        return QList(self.m_policyEnumNames.values())

    def languageEnumNames(self):
        return self.m_languageEnumNames

    def countryEnumNames(self, language):
        return  self.m_countryEnumNames[language]

    def sortCountries(self, countries):
        countriesMap = QMap()
        for country in countries:
            c = country.country()
            countriesMap[c] = QLocale.countryToString(c)
        sorted(countriesMap)
        return countriesMap.keys()

    def initLocale(self):
        nameToLanguage={}
        language = QLocale.C
        while (language <= QLocale.LastLanguage):
            locale = QLocale(language)
            if (locale.language() == language):
                nameToLanguage[language] = QLocale.languageToString(language)
            language = language + 1

        system = QLocale.system()
        sysLang = system.language()
        if not QLocale.languageToString(system.language()) in nameToLanguage.values():
            nameToLanguage[QLocale.languageToString(sysLang)] = sysLang

        languages = nameToLanguage.keys()
        for language in languages:
            countries = QLocale.matchingLocales(language, QLocale.AnyScript, QLocale.AnyCountry)
            if len(countries)>0 and language == sysLang:
                countries.append(QLocale(sysLang, system.country()))

            if (len(countries)>0 and not self.m_languageToIndex.get(language)):
                countries = self.sortCountries(countries)
                langIdx = len(self.m_languageEnumNames)
                self.m_indexToLanguage[langIdx] = language
                self.m_languageToIndex[language] = langIdx
                countryNames = QList()
                countryIdx = 0
                for c in countries:
                    country = c
                    countryNames.append(QLocale.countryToString(country))
                    self.m_indexToCountry[langIdx][countryIdx] = country
                    self.m_countryToIndex[language][country] = countryIdx
                    countryIdx += 1

                self.m_languageEnumNames.append(QLocale.languageToString(language))
                self.m_countryEnumNames[language] = countryNames

    def indexToSizePolicy(self, index):
        keys = list(self.m_policyEnumNames.keys())
        l = len(keys)
        if index<0 or index>=l:
            return -1

        return keys[index]

    def sizePolicyToIndex(self, policy):
        i = 0
        keys = list(self.m_policyEnumNames.keys())
        for k in keys:
            if policy==k:
                return i
            i += 1

        return -1

    def indexToLocale(self, languageIndex, countryIndex):
        l = QLocale.C
        c = QLocale.AnyCountry
        if (self.m_indexToLanguage.get(languageIndex)):
            l = self.m_indexToLanguage[languageIndex]
            if (self.m_indexToCountry.get(languageIndex) and  self.m_indexToCountry[languageIndex].get(countryIndex)):
                c = self.m_indexToCountry[languageIndex][countryIndex]

        return [l, c]

    def localeToIndex(self, language, country):
        l = 0
        c = 0
        if (self.m_languageToIndex.get(language)):
            l = self.m_languageToIndex[language]
            if (self.m_countryToIndex.get(language) and  self.m_countryToIndex[language].get(country)):
                c = self.m_countryToIndex[language][country]

        return [l, c]

g_metaEnumProvider = None
def metaEnumProvider():
    global g_metaEnumProvider
    if not g_metaEnumProvider:
        g_metaEnumProvider = QtMetaEnumProvider()
    return g_metaEnumProvider

# QtGroupPropertyManager

###
#    \class QtGroupPropertyManager
#
#    \brief The QtGroupPropertyManager provides and manages group properties.
#
#    This class is intended to provide a grouping element without any value.
#
#    \sa QtAbstractPropertyManager
###
class QtGroupPropertyManager(QtAbstractPropertyManager):
    ###
    #    Creates a manager with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtGroupPropertyManager, self).__init__(parent)

    ###
    #    \reimp
    ###
    def hasValue(self, property):
        return False

    ###
    #    \reimp
    ###
    def initializeProperty(self, property):
        pass

    ###
    #    \reimp
    ###
    def uninitializeProperty(self, property):
        pass

class QtIntPropertyManagerPrivate():
    class Data():
        def __init__(self):
            self.val = 0
            self.minVal = -INT_MAX
            self.maxVal = INT_MAX
            self.singleStep = 1
            self.readOnly = False

        def minimumValue(self):
            return self.minVal

        def maximumValue(self):
            return self.maxVal

        def setMinimumValue(self, newMinVal):
            setSimpleMinimumData(self, newMinVal)

        def setMaximumValue(self, newMaxVal):
            setSimpleMaximumData(self, newMaxVal)

    def __init__(self):
        self.q_ptr = None
        self.m_values = QMap()
        self.Data = QtIntPropertyManagerPrivate.Data()

###
#    \class QtIntPropertyManager
#
#    \brief The QtIntPropertyManager provides and manages int properties.
#
#    An int property has a current value, and a range specifying the
#    valid values. The range is defined by a minimum and a maximum
#    value.
#
#    The property's value and range can be retrieved using the value(),
#    minimum() and maximum() functions, and can be set using the
#    setValue(), setMinimum() and setMaximum() slots. Alternatively,
#    the range can be defined in one go using the setRange() slot.
#
#    In addition, QtIntPropertyManager provides the valueChanged() signal which
#    is emitted whenever a property created by this manager changes,
#    and the rangeChanged() signal which is emitted whenever such a
#    property changes its range of valid values.
#
#    \sa QtAbstractPropertyManager, QtSpinBoxFactory, QtSliderFactory, QtScrollBarFactory
###

###
#    \fn void QtIntPropertyManager.valueChanged(property, value)
#
#    This signal is emitted whenever a property created by this manager
#    changes its value, passing a pointer to the \a property and the new
#    \a value as parameters.
#
#    \sa setValue()
###

###
#    \fn void QtIntPropertyManager.rangeChanged(property, minimum, maximum)
#
#    This signal is emitted whenever a property created by this manager
#    changes its range of valid values, passing a pointer to the
#    \a property and the new \a minimum and \a maximum values.
#
#    \sa setRange()
###

###
#    \fn void QtIntPropertyManager.singleStepChanged(property, step)
#
#    This signal is emitted whenever a property created by this manager
#    changes its single step property, passing a pointer to the
#    \a property and the new \a step value
#
#    \sa setSingleStep()
###
class QtIntPropertyManager(QtAbstractPropertyManager):
    valueChangedSignal = pyqtSignal(QtProperty, int)
    rangeChangedSignal = pyqtSignal(QtProperty, int, int)
    singleStepChangedSignal = pyqtSignal(QtProperty, int)
    readOnlyChangedSignal = pyqtSignal(QtProperty, bool)

    ###
    #    Creates a manager with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtIntPropertyManager, self).__init__(parent)

        self.d_ptr = QtIntPropertyManagerPrivate()
        self.d_ptr.q_ptr = self

    ###
    #    Destroys this manager, and all the properties it has created.
    ###
    def __del__(self):
        self.clear()
        del self.d_ptr

    ###
    #    Returns the given \a property's value.
    #
    #    If the given property is not managed by this manager, this:
    #    function returns 0.
    #
    #    \sa setValue()
    ###
    def value(self, property):
        return getValue(self.d_ptr.m_values, property, 0)

    ###
    #    Returns the given \a property's minimum value.
    #
    #    \sa setMinimum(), maximum(), setRange()
    ###
    def minimum(self, property):
        return getMinimum(self.d_ptr.m_values, property, 0)

    ###
    #    Returns the given \a property's maximum value.
    #
    #    \sa setMaximum(), minimum(), setRange()
    ###
    def maximum(self, property):
        return getMaximum(self.d_ptr.m_values, property, 0)

    ###
    #    Returns the given \a property's step value.
    #
    #    The step is typically used to increment or decrement a property value while pressing an arrow key.
    #
    #    \sa setSingleStep()
    ###
    def singleStep(self, property):
        return getData(self.d_ptr.m_values, DATA_SINGLESTEP, property, 0)

    ###
    #    Returns read-only status of the property.
    #
    #    When property is read-only it's value can be selected and copied from editor but not modified.
    #
    #    \sa QtIntPropertyManager.setReadOnly
    ###
    def isReadOnly(self, property):
        return getData(self.d_ptr.m_values, DATA_READONLY, property, 0)

    ###
    #    \reimp
    ###
    def valueText(self, property):
        d = self.d_ptr.m_values.get(property)
        if not d:
            return ''
        return str(d.val)

    ###
    #    \fn void QtIntPropertyManager.setValue(property, value)
    #
    #    Sets the value of the given \a property to \a value.
    #
    #    If the specified \a value is not valid according to the given \a:
    #    property's range, the \a value is adjusted to the nearest valid
    #    value within the range.
    #
    #    \sa value(), setRange(), valueChanged()
    ###
    def setValue(self, property, val):
        setSubPropertyValue = None
        setValueInRange(self, self.d_ptr, self.propertyChangedSignal,self.valueChangedSignal,
                    property, val, setSubPropertyValue)

    ###
    #    Sets the minimum value for the given \a property to \a minVal.
    #
    #    When setting the minimum value, the maximum and current values are
    #    adjusted if necessary (ensuring that the range remains valid and
    #    that the current value is within the range).
    #
    #    \sa minimum(), setRange(), rangeChanged()
    ###
    def setMinimum(self, property, minVal):
        setMinimumValue(self, self.d_ptr,
                    self.propertyChangedSignal,
                    self.valueChangedSignal,
                    self.rangeChangedSignal,
                    property, minVal)

    ###
    #    Sets the maximum value for the given \a property to \a maxVal.
    #
    #    When setting maximum value, the minimum and current values are
    #    adjusted if necessary (ensuring that the range remains valid and
    #    that the current value is within the range).
    #
    #    \sa maximum(), setRange(), rangeChanged()
    ###
    def setMaximum(self, property, maxVal):
        setMaximumValue(self, self.d_ptr,
                    self.propertyChangedSignal,
                    self.valueChangedSignal,
                    self.rangeChangedSignal,
                    property, maxVal)

    ###
    #    \fn void QtIntPropertyManager.setRange(property, minimum, maximum)
    #
    #    Sets the range of valid values.
    #
    #    This is a convenience function defining the range of valid values
    #    in one go; setting the \a minimum and \a maximum values for the
    #    given \a property with a single function call.
    #
    #    When setting a new range, the current value is adjusted if
    #    necessary (ensuring that the value remains within range).
    #
    #    \sa setMinimum(), setMaximum(), rangeChanged()
    ###
    def setRange(self, property, minVal, maxVal):
        setSubPropertyRange = 0
        setBorderValues(self, self.d_ptr,
                    self.propertyChangedSignal,
                    self.valueChangedSignal,
                    self.rangeChangedSignal,
                    property, minVal, maxVal, setSubPropertyRange)

    ###
    #    Sets the step value for the given \a property to \a step.
    #
    #    The step is typically used to increment or decrement a property value while pressing an arrow key.
    #
    #    \sa singleStep()
    ###
    def setSingleStep(self, property, step):
        if not property in self.d_ptr.m_values.keys():
            return

        data = self.d_ptr.m_values[property]

        if (step < 0):
            step = 0

        if (data.singleStep == step):
            return

        data.singleStep = step

        self.d_ptr.m_values[property] = data

        self.singleStepChangedSignal.emit(property, data.singleStep)

    ###
    #    Sets read-only status of the property.
    #
    #    \sa QtIntPropertyManager.setReadOnly
    ###
    def setReadOnly(self, property, readOnly):
        if not property in self.d_ptr.m_values.keys():
            return

        data = self.d_ptr.m_values[property]

        if (data.readOnly == readOnly):
            return

        data.readOnly = readOnly
        self.d_ptr.m_values[property] = data

        self.propertyChangedSignal.emit(property)
        self.readOnlyChangedSignal.emit(property, data.readOnly)

    ###
    #    \reimp
    ###
    def initializeProperty(self, property):
        self.d_ptr.m_values[property] = QtIntPropertyManagerPrivate.Data()

    ###
    #    \reimp
    ###
    def uninitializeProperty(self, property):
        self.d_ptr.m_values.remove(property)

class QtDoublePropertyManagerPrivate():
    class Data():
        val = 0.0
        minVal = -INT_MAX
        maxVal = INT_MAX
        singleStep = 1
        decimals = 2
        readOnly = False

        def minimumValue(self):
            return self.minVal

        def maximumValue(self):
            return self.maxVal

        def setMinimumValue(self, newMinVal):
            setSimpleMinimumData(self, newMinVal)

        def setMaximumValue(self, newMaxVal):
            setSimpleMaximumData(self, newMaxVal)

    def __init__(self):
        self.q_ptr = None
        self.m_values = QMap()
        self.Data = QtDoublePropertyManagerPrivate.Data()

###
#    \class QtDoublePropertyManager
#
#    \brief The QtDoublePropertyManager provides and manages double properties.
#
#    A double property has a current value, and a range specifying the
#    valid values. The range is defined by a minimum and a maximum
#    value.
#
#    The property's value and range can be retrieved using the value(),
#    minimum() and maximum() functions, and can be set using the
#    setValue(), setMinimum() and setMaximum() slots.
#    Alternatively, the range can be defined in one go using the
#    setRange() slot.
#
#    In addition, QtDoublePropertyManager provides the valueChanged() signal
#    which is emitted whenever a property created by this manager
#    changes, and the rangeChanged() signal which is emitted whenever
#    such a property changes its range of valid values.
#
#    \sa QtAbstractPropertyManager, QtDoubleSpinBoxFactory
###

###
#    \fn void QtDoublePropertyManager.valueChanged(property, value)
#
#    This signal is emitted whenever a property created by this manager
#    changes its value, passing a pointer to the \a property and the new
#    \a value as parameters.
#
#    \sa setValue()
###

###
#    \fn void QtDoublePropertyManager.rangeChanged(property, minimum, maximum)
#
#    This signal is emitted whenever a property created by this manager
#    changes its range of valid values, passing a pointer to the
#    \a property and the new \a minimum and \a maximum values
#
#    \sa setRange()
###

###
#    \fn void QtDoublePropertyManager.decimalsChanged(property, prec)
#
#    This signal is emitted whenever a property created by this manager
#    changes its precision of value, passing a pointer to the
#    \a property and the new \a prec value
#
#    \sa setDecimals()
###

###
#    \fn void QtDoublePropertyManager.singleStepChanged(property, step)
#
#    This signal is emitted whenever a property created by this manager
#    changes its single step property, passing a pointer to the
#    \a property and the new \a step value
#
#    \sa setSingleStep()
###
class QtDoublePropertyManager(QtAbstractPropertyManager):
    valueChangedSignal = pyqtSignal(QtProperty, float)
    rangeChangedSignal = pyqtSignal(QtProperty, float, float)
    singleStepChangedSignal = pyqtSignal(QtProperty, float)
    decimalsChangedSignal = pyqtSignal(QtProperty, int)
    readOnlyChangedSignal = pyqtSignal(QtProperty, bool)

    ###
    #    Creates a manager with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtDoublePropertyManager, self).__init__(parent)

        self.d_ptr = QtDoublePropertyManagerPrivate()
        self.d_ptr.q_ptr = self

    ###
    #    Destroys  this manager, and all the properties it has created.
    ###
    def __del__(self):
        self.clear()
        del self.d_ptr

    ###
    #    Returns the given \a property's value.
    #
    #    If the given property is not managed by this manager, this:
    #    function returns 0.
    #
    #    \sa setValue()
    ###
    def value(self, property):
        return getValue(self.d_ptr.m_values, property, 0.0)

    ###
    #    Returns the given \a property's minimum value.
    #
    #    \sa maximum(), setRange()
    ###
    def minimum(self, property):
        return getMinimum(self.d_ptr.m_values, property, 0.0)

    ###
    #    Returns the given \a property's maximum value.
    #
    #    \sa minimum(), setRange()
    ###
    def maximum(self, property):
        return getMaximum(self.d_ptr.m_values, property, 0.0)

    ###
    #    Returns the given \a property's step value.
    #
    #    The step is typically used to increment or decrement a property value while pressing an arrow key.
    #
    #    \sa setSingleStep()
    ###
    def singleStep(self, property):
        return getData(self.d_ptr.m_values, DATA_SINGLESTEP, property, 0)

    ###
    #    Returns the given \a property's precision, in decimals.
    #
    #    \sa setDecimals()
    ###
    def decimals(self, property):
        return getData(self.d_ptr.m_values, DATA_DECIMALS, property, 0)

    ###
    #    Returns read-only status of the property.
    #
    #    When property is read-only it's value can be selected and copied from editor but not modified.
    #
    #    \sa QtDoublePropertyManager.setReadOnly
    ###
    def isReadOnly(self, property):
        return getData(self.d_ptr.m_values, DATA_READONLY, property, False)

    ###
    #    \reimp
    ###
    def valueText(self, property):
        if not property in self.d_ptr.m_values.keys():
            return ''
        return QLocale.system().toString(float(self.d_ptr.m_values[property].val), 'f', self.d_ptr.m_values[property].decimals)

    ###
    #    \fn void QtDoublePropertyManager.setValue(property, value)
    #
    #    Sets the value of the given \a property to \a value.
    #
    #    If the specified \a value is not valid according to the given:
    #    \a property's range, the \a value is adjusted to the nearest valid value
    #    within the range.
    #
    #    \sa value(), setRange(), valueChanged()
    ###
    def setValue(self, property, val):
        setSubPropertyValue = 0
        setValueInRange(self,
                    self.d_ptr,
                    self.propertyChangedSignal,
                    self.valueChangedSignal,
                    property, val, setSubPropertyValue)

    ###
    #    Sets the step value for the given \a property to \a step.
    #
    #    The step is typically used to increment or decrement a property value while pressing an arrow key.
    #
    #    \sa singleStep()
    ###
    def setSingleStep(self, property, step):
        if not property in self.d_ptr.m_values.keys():
            return

        data = self.d_ptr.m_values[property]

        if (step < 0):
            step = 0

        if (data.singleStep == step):
            return

        data.singleStep = step

        self.d_ptr.m_values[property] = data

        self.singleStepChangedSignal.emit(property, data.singleStep)

    ###
    #    Sets read-only status of the property.
    #
    #    \sa QtDoublePropertyManager.setReadOnly
    ###
    def setReadOnly(self, property, readOnly):

        if not property in self.d_ptr.m_values.keys():
            return

        data = self.d_ptr.m_values[property]

        if (data.readOnly == readOnly):
            return

        data.readOnly = readOnly
        self.d_ptr.m_values[property] = data

        self.propertyChangedSignal.emit(property)
        self.readOnlyChangedSignal.emit(property, data.readOnly)

    ###
    #    \fn void QtDoublePropertyManager.setDecimals(property, prec)
    #
    #    Sets the precision of the given \a property to \a prec.
    #
    #    The valid decimal range is 0-13. The default is 2.
    #
    #    \sa decimals()
    ###
    def setDecimals(self, property, prec):

        if not property in self.d_ptr.m_values.keys():
            return

        data = self.d_ptr.m_values[property]

        if (prec > 13):
            prec = 13
        elif (prec < 0):
            prec = 0

        if (data.decimals == prec):
            return

        data.decimals = prec

        self.d_ptr.m_values[property] = data

        self.decimalsChangedSignal.emit(property, data.decimals)

    ###
    #    Sets the minimum value for the given \a property to \a minVal.
    #
    #    When setting the minimum value, the maximum and current values are
    #    adjusted if necessary (ensuring that the range remains valid and
    #    that the current value is within in the range).
    #
    #    \sa minimum(), setRange(), rangeChanged()
    ###
    def setMinimum(self, property, minVal):
        setMinimumValue(self, self.d_ptr,
                    self.propertyChangedSignal,
                    self.valueChangedSignal,
                    self.rangeChangedSignal,
                    property, minVal)

    ###
    #    Sets the maximum value for the given \a property to \a maxVal.
    #
    #    When setting the maximum value, the minimum and current values are
    #    adjusted if necessary (ensuring that the range remains valid and
    #    that the current value is within in the range).
    #
    #    \sa maximum(), setRange(), rangeChanged()
    ###
    def setMaximum(self, property, maxVal):
        setMaximumValue(self, self.d_ptr,
                    self.propertyChangedSignal,
                    self.valueChangedSignal,
                    self.rangeChangedSignal,
                    property, maxVal)

    ###
    #    \fn void QtDoublePropertyManager.setRange(property, minimum, maximum)
    #
    #    Sets the range of valid values.
    #
    #    This is a convenience function defining the range of valid values
    #    in one go; setting the \a minimum and \a maximum values for the
    #    given \a property with a single function call.
    #
    #    When setting a new range, the current value is adjusted if
    #    necessary (ensuring that the value remains within range).
    #
    #    \sa setMinimum(), setMaximum(), rangeChanged()
    ###
    def setRange(self, property, minVal, maxVal):
        setSubPropertyRange = 0
        setBorderValues(self, self.d_ptr,
                    self.propertyChangedSignal,
                    self.valueChangedSignal,
                    self.rangeChangedSignal,
                    property, minVal, maxVal, setSubPropertyRange)

    ###
    #    \reimp
    ###
    def initializeProperty(self, property):
        self.d_ptr.m_values[property] = QtDoublePropertyManagerPrivate.Data()

    ###
    #    \reimp
    ###
    def uninitializeProperty(self, property):
        self.d_ptr.m_values.remove(property)

class QtStringPropertyManagerPrivate():
    class Data():
        val = ''
        regExp = QRegExp('*',  Qt.CaseSensitive, QRegExp.Wildcard)
        echoMode = QLineEdit.Normal
        readOnly = False

    def __init__(self):
        self.q_ptr = None
        self.Data = QtStringPropertyManagerPrivate.Data()
        self.m_values = QMap()

###
#    \class QtStringPropertyManager
#
#    \brief The QtStringPropertyManager provides and manages QString properties.
#
#    A string property's value can be retrieved using the value()
#    function, and set using the setValue() slot.
#
#    The current value can be checked against a regular expression. To
#    set the regular expression use the setRegExp() slot, use the
#    regExp() function to retrieve the currently set expression.
#
#    In addition, QtStringPropertyManager provides the valueChanged() signal
#    which is emitted whenever a property created by this manager
#    changes, and the regExpChanged() signal which is emitted whenever
#    such a property changes its currently set regular expression.
#
#    \sa QtAbstractPropertyManager, QtLineEditFactory
###

###
#    \fn void QtStringPropertyManager.valueChanged(property, value)
#
#    This signal is emitted whenever a property created by this manager
#    changes its value, passing a pointer to the \a property and the
#    new \a value as parameters.
#
#    \sa setValue()
###

###
#    \fn void QtStringPropertyManager.regExpChanged(property, regExp)
#
#    This signal is emitted whenever a property created by this manager
#    changes its currenlty set regular expression, passing a pointer to
#    the \a property and the new \a regExp as parameters.
#
#    \sa setRegExp()
###

###
#    Creates a manager with the given \a parent.
###
class QtStringPropertyManager(QtAbstractPropertyManager):
    valueChangedSignal = pyqtSignal(QtProperty, str)
    regExpChangedSignal = pyqtSignal(QtProperty, QRegExp)
    echoModeChangedSignal = pyqtSignal(QtProperty, int)
    readOnlyChangedSignal = pyqtSignal(QtProperty, bool)

    ###
    #    Creates a manager with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtStringPropertyManager, self).__init__(parent)

        self.d_ptr = QtStringPropertyManagerPrivate()
        self.d_ptr.q_ptr = self

    ###
    #    Destroys this manager, and all the properties it has created.
    ###
    def __del__(self):
        self.clear()
        del self.d_ptr

    ###
    #    Returns the given \a property's value.
    #
    #    If the given property is not managed by this manager, this:
    #    function returns an empty string.
    #
    #    \sa setValue()
    ###
    def value(self, property):
        return getValue(self.d_ptr.m_values, property, '')

    ###
    #    Returns the given \a property's currently set regular expression.
    #
    #    If the given \a property is not managed by this manager, this:
    #    function returns an empty expression.
    #
    #    \sa setRegExp()
    ###
    def regExp(self, property):
        return getData(self.d_ptr.m_values, DATA_REGEXP, property, QRegExp())

    ###
    #    \reimp
    ###
    def echoMode(self, property):
        return getData(self.d_ptr.m_values, DATA_ECHOMODE, property, 0)

    ###
    #    Returns read-only status of the property.
    #
    #    When property is read-only it's value can be selected and copied from editor but not modified.
    #
    #    \sa QtStringPropertyManager.setReadOnly
    ###
    def isReadOnly(self, property):
        return getData(self.d_ptr.m_values, DATA_READONLY, property, False)

    ###
    #    \reimp
    ###
    def valueText(self, property):
        if not property in self.d_ptr.m_values.keys():
            return ''

        return self.d_ptr.m_values[property].val

    ###
    #    \reimp
    ###
    def displayText(self, property):
        if not property in self.d_ptr.m_values.keys():
            return ''

        edit = QLineEdit()
        edit.setEchoMode(self.d_ptr.m_values[property].echoMode)
        edit.setText(self.d_ptr.m_values[property].val)
        return edit.displayText()

    ###
    #    \fn void QtStringPropertyManager.setValue(property, value)
    #
    #    Sets the value of the given \a property to \a value.
    #
    #    If the specified \a value doesn't match the given \a property's:
    #    regular expression, this function does nothing.
    #
    #    \sa value(), setRegExp(), valueChanged()
    ###
    def setValue(self, property, val):
        if not property in self.d_ptr.m_values.keys():
            return

        data = self.d_ptr.m_values[property]

        if (data.val == val):
            return

        if (data.regExp.isValid() and not data.regExp.exactMatch(val)):
            return

        data.val = val

        self.d_ptr.m_values[property] = data

        self.propertyChangedSignal.emit(property)
        self.valueChangedSignal.emit(property, data.val)

    ###
    #    Sets the regular expression of the given \a property to \a regExp.
    #
    #    \sa regExp(), setValue(), regExpChanged()
    ###
    def setRegExp(self, property, regExp):

        if not property in self.d_ptr.m_values.keys():
            return

        data = self.d_ptr.m_values[property]

        if (data.regExp == regExp):
            return

        data.regExp = regExp

        self.d_ptr.m_values[property] = data

        self.regExpChangedSignal.emit(property, data.regExp)

    def setEchoMode(self, property, echoMode):
        if not property in self.d_ptr.m_values.keys():
            return

        data = self.d_ptr.m_values[property]

        if (data.echoMode == echoMode):
            return

        data.echoMode = echoMode
        self.d_ptr.m_values[property] = data

        self.propertyChangedSignal.emit(property)
        self.echoModeChangedSignal.emit(property, data.echoMode)

    ###
    #    Sets read-only status of the property.
    #
    #    \sa QtStringPropertyManager.setReadOnly
    ###
    def setReadOnly(self, property, readOnly):

        if not property in self.d_ptr.m_values.keys():
            return

        data = self.d_ptr.m_values[property]

        if (data.readOnly == readOnly):
            return

        data.readOnly = readOnly
        self.d_ptr.m_values[property] = data

        self.propertyChangedSignal.emit(property)
        self.echoModeChangedSignal.emit(property, data.echoMode)

    ###
    #    \reimp
    ###
    def initializeProperty(self, property):
        self.d_ptr.m_values[property] = QtStringPropertyManagerPrivate.Data()

    ###
    #    \reimp
    ###
    def uninitializeProperty(self, property):
        self.d_ptr.m_values.remove(property)

    # QtBoolPropertyManager
    #     Return an icon containing a check box indicator
def drawCheckBox(value):
    opt = QStyleOptionButton()
    if value:
        opt.state |= QStyle.State_On
    else:
        opt.state |= QStyle.State_Off
    opt.state |= QStyle.State_Enabled
    style = QApplication.style()
    # Figure out size of an indicator and make sure it is not scaled down in a list view item
    # by making the pixmap as big as a list view icon and centering the indicator in it.
    # (if it is smaller, it can't be helped)
    indicatorWidth = style.pixelMetric(QStyle.PM_IndicatorWidth, opt)
    indicatorHeight = style.pixelMetric(QStyle.PM_IndicatorHeight, opt)
    listViewIconSize = indicatorWidth
    pixmapWidth = indicatorWidth
    pixmapHeight = max(indicatorHeight, listViewIconSize)

    opt.rect = QRect(0, 0, indicatorWidth, indicatorHeight)
    pixmap = QPixmap(pixmapWidth, pixmapHeight)
    pixmap.fill(Qt.transparent)
    # Center?
    if pixmapWidth > indicatorWidth:
        xoff = (pixmapWidth  - indicatorWidth)  / 2
    else:
        xoff = 0
    if pixmapHeight > indicatorHeight:
        yoff = (pixmapHeight - indicatorHeight) / 2
    else:
        yoff = 0
    painter = QPainter(pixmap)
    painter.translate(xoff, yoff)
    style.drawPrimitive(QStyle.PE_IndicatorCheckBox, opt, painter)
    painter.end()
    return QIcon(pixmap)

class QtBoolPropertyManagerPrivate():
    class Data():
        val = False
        val2 = False
        textVisible = True

    def __init__(self, parent=None):
        self.q_ptr = None
        self.m_values = QMap()
        self.Data = QtBoolPropertyManagerPrivate.Data()
        self.m_checkedIcon = drawCheckBox(True)
        self.m_uncheckedIcon = drawCheckBox(False)

###
#    \class QtBoolPropertyManager
#
#    \brief The QtBoolPropertyManager class provides and manages boolean properties.
#
#    The property's value can be retrieved using the value() function,
#    and set using the setValue() slot.
#
#    In addition, QtBoolPropertyManager provides the valueChanged() signal
#    which is emitted whenever a property created by this manager
#    changes.
#
#    \sa QtAbstractPropertyManager, QtCheckBoxFactory
###

###
#    \fn void QtBoolPropertyManager.valueChanged(property, value)
#
#    This signal is emitted whenever a property created by this manager
#    changes its value, passing a pointer to the \a property and the
#    new \a value as parameters.
###
class QtBoolPropertyManager(QtAbstractPropertyManager):
    valueChangedSignal = pyqtSignal(QtProperty, bool)
    textVisibleChangedSignal = pyqtSignal(QtProperty, bool)

    ###
    #    Creates a manager with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtBoolPropertyManager, self).__init__(parent)

        self.d_ptr = QtBoolPropertyManagerPrivate()
        self.d_ptr.q_ptr = self

    ###
    #    Destroys this manager, and all the properties it has created.
    ###
    def __del__(self):
        self.clear()
        del self.d_ptr

    ###
    #    Returns the given \a property's value.
    #
    #    If the given \a property is not managed by \e this manager, this:
    #    function returns False.
    #
    #    \sa setValue()
    ###
    def value(self, property):
        return getValue(self.d_ptr.m_values, property, False)

    def textVisible(self, property):
        return getData(self.d_ptr.m_values, DATA_TEXTVISIBLE, property, False)

    ###
    #    \reimp
    ###
    def valueText(self, property):
        if not property in self.d_ptr.m_values.keys():
            return ''

        data = self.d_ptr.m_values[property]
        if (not data.textVisible):
            return ''

        trueText = self.tr("True")
        falseText = self.tr("False")
        if data.val:
            return trueText
        else:
            return falseText

    ###
    #    \reimp
    ###
    def valueIcon(self, property):
        if not property in self.d_ptr.m_values.keys():
            return QIcon()
        if self.d_ptr.m_values[property].val:
            return self.d_ptr.m_checkedIcon
        else:
            return self.d_ptr.m_uncheckedIcon

    ###
    #    \fn void QtBoolPropertyManager.setValue(property, value)
    #
    #    Sets the value of the given \a property to \a value.
    #
    #    \sa value()
    ###
    def setValue(self, property, val):
        if not property in self.d_ptr.m_values.keys():
            return

        data = self.d_ptr.m_values[property]
        if (data.val == val):
            return

        data.val = val
        self.d_ptr.m_values[property] = data

        self.propertyChangedSignal.emit(property)
        self.valueChangedSignal.emit(property, data.val)

    def setTextVisible(self, property, textVisible):
        if not property in self.d_ptr.m_values.keys():
            return

        data = self.d_ptr.m_values[property]

        if (data.textVisible == textVisible):
            return

        data.textVisible = textVisible
        self.d_ptr.m_values[property] = data

        self.propertyChangedSignal.emit(property)
        self.textVisibleChangedSignal.emit(property, data.textVisible)

    ###
    #    \reimp
    ###
    def initializeProperty(self, property):
        self.d_ptr.m_values[property] = QtBoolPropertyManagerPrivate.Data()

    ###
    #    \reimp
    ###
    def uninitializeProperty(self, property):
        self.d_ptr.m_values.remove(property)

class QtDatePropertyManagerPrivate():
    class Data():
        val = QDate.currentDate()
        minVal = QDate(1752, 9, 14)
        maxVal = QDate(7999, 12, 31)
        def minimumValue(self):
            return self.minVal

        def maximumValue(self):
            return self.maxVal

        def setMinimumValue(self, newMinVal):
            setSimpleMinimumData(self, newMinVal)

        def setMaximumValue(self, newMaxVal):
            setSimpleMaximumData(self, newMaxVal)

    def __init__(self):
        self.q_ptr = None
        self.m_values = QMap()
        self.Data = QtDatePropertyManagerPrivate.Data()
        self.m_format = ''

###
#    \class QtDatePropertyManager
#
#    \brief The QtDatePropertyManager provides and manages QDate properties.
#
#    A date property has a current value, and a range specifying the
#    valid dates. The range is defined by a minimum and a maximum
#    value.
#
#    The property's values can be retrieved using the minimum(),
#    maximum() and value() functions, and can be set using the
#    setMinimum(), setMaximum() and setValue() slots. Alternatively,
#    the range can be defined in one go using the setRange() slot.
#
#    In addition, QtDatePropertyManager provides the valueChanged() signal
#    which is emitted whenever a property created by this manager
#    changes, and the rangeChanged() signal which is emitted whenever
#    such a property changes its range of valid dates.
#
#    \sa QtAbstractPropertyManager, QtDateEditFactory, QtDateTimePropertyManager
###

###
#    \fn void QtDatePropertyManager.valueChanged(property, value)
#
#    This signal is emitted whenever a property created by this manager
#    changes its value, passing a pointer to the \a property and the new
#    \a value as parameters.
#
#    \sa setValue()
###

###
#    \fn void QtDatePropertyManager.rangeChanged(property, minimum, maximum)
#
#    This signal is emitted whenever a property created by this manager
#    changes its range of valid dates, passing a pointer to the \a
#    property and the new \a minimum and \a maximum dates.
#
#    \sa setRange()
###
class QtDatePropertyManager(QtAbstractPropertyManager):
    valueChangedSignal = pyqtSignal(QtProperty , QDate)
    rangeChangedSignal = pyqtSignal(QtProperty , QDate, QDate)

    ###
    #    Creates a manager with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtDatePropertyManager, self).__init__(parent)

        self.d_ptr = QtDatePropertyManagerPrivate()
        self.d_ptr.q_ptr = self
        loc = QLocale()
        self.d_ptr.m_format = loc.dateFormat(QLocale.ShortFormat)

    ###
    #    Destroys this manager, and all the properties it has created.
    ###
    def __del__(self):
        self.clear()
        del self.d_ptr

    ###
    #    Returns the given \a property's value.
    #
    #    If the given \a property is not managed by \e this manager, this:
    #    function returns an invalid date.
    #
    #    \sa setValue()
    ###
    def value(self, property):
        return getValue(self.d_ptr.m_values, property, QDate())

    ###
    #    Returns the given \a  property's  minimum date.
    #
    #    \sa maximum(), setRange()
    ###
    def minimum(self, property):
        return getMinimum(self.d_ptr.m_values, property, QDate())

    ###
    #    Returns the given \a property's maximum date.
    #
    #    \sa minimum(), setRange()
    ###
    def maximum(self, property):
        return getMaximum(self.d_ptr.m_values, property, QDate())

    ###
    #    \reimp
    ###
    def valueText(self, property):
        if not property in self.d_ptr.m_values.keys():
            return ''
        return self.d_ptr.m_values[property].val.toString(self.d_ptr.m_format)

    ###
    #    \fn void QtDatePropertyManager.setValue(property, value)
    #
    #    Sets the value of the given \a property to \a value.
    #
    #    If the specified \a value is not a valid date according to the:
    #    given \a property's range, the value is adjusted to the nearest
    #    valid value within the range.
    #
    #    \sa value(), setRange(), valueChanged()
    ###
    def setValue(self, property, val):
        setSubPropertyValue = 0
        setValueInRange(self,
                    self.d_ptr,
                    self.propertyChangedSignal,
                    self.valueChangedSignal,
                    property, val, setSubPropertyValue)

    ###
    #    Sets the minimum value for the given \a property to \a minVal.
    #
    #    When setting the minimum value, the maximum and current values are
    #    adjusted if necessary (ensuring that the range remains valid and
    #    that the current value is within in the range).
    #
    #    \sa minimum(), setRange()
    ###
    def setMinimum(self, property, minVal):
        setMinimumValue(self, self.d_ptr,
                    self.propertyChangedSignal,
                    self.valueChangedSignal,
                    self.rangeChangedSignal,
                    property, minVal)

    ###
    #    Sets the maximum value for the given \a property to \a maxVal.
    #
    #    When setting the maximum value, the minimum and current
    #    values are adjusted if necessary (ensuring that the range remains
    #    valid and that the current value is within in the range).
    #
    #    \sa maximum(), setRange()
    ###
    def setMaximum(self, property, maxVal):
        setMaximumValue(self, self.d_ptr,
                    self.propertyChangedSignal,
                    self.valueChangedSignal,
                    self.rangeChangedSignal,
                    property, maxVal)

    ###
    #    \fn void QtDatePropertyManager.setRange(property, minimum, maximum)
    #
    #    Sets the range of valid dates.
    #
    #    This is a convenience function defining the range of valid dates
    #    in one go; setting the \a minimum and \a maximum values for the
    #    given \a property with a single function call.
    #
    #    When setting a new date range, the current value is adjusted if
    #    necessary (ensuring that the value remains in date range).
    #
    #    \sa setMinimum(), setMaximum(), rangeChanged()
    ###
    def setRange(self, property, minVal, maxVal):
        setSubPropertyRange = 0
        setBorderValues(self, self.d_ptr,
                    self.propertyChangedSignal,
                    self.valueChangedSignal,
                    self.rangeChangedSignal,
                    property, minVal, maxVal, setSubPropertyRange)

    ###
    #    \reimp
    ###
    def initializeProperty(self, property):
        self.d_ptr.m_values[property] = QtDatePropertyManagerPrivate.Data()

    ###
    #    \reimp
    ###
    def uninitializeProperty(self, property):
        self.d_ptr.m_values.remove(property)

class QtTimePropertyManagerPrivate():
    def __init__(self):
        self.q_ptr = None
        self.m_values = QMap()
        self.m_format = ''

# QtTimePropertyManager
###
#    \class QtTimePropertyManager
#
#    \brief The QtTimePropertyManager provides and manages QTime properties.
#
#    A time property's value can be retrieved using the value()
#    function, and set using the setValue() slot.
#
#    In addition, QtTimePropertyManager provides the valueChanged() signal
#    which is emitted whenever a property created by this manager
#    changes.
#
#    \sa QtAbstractPropertyManager, QtTimeEditFactory
###

###
#    \fn void QtTimePropertyManager.valueChanged(property, value)
#
#    This signal is emitted whenever a property created by this manager
#    changes its value, passing a pointer to the \a property and the
#    new \a value as parameters.
#
#    \sa setValue()
###
class QtTimePropertyManager(QtAbstractPropertyManager):
    valueChangedSignal = pyqtSignal(QtProperty, QTime)

    ###
    #    Creates a manager with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtTimePropertyManager, self).__init__(parent)

        self.d_ptr = QtTimePropertyManagerPrivate()
        self.d_ptr.q_ptr = self

        loc = QLocale()
        self.d_ptr.m_format = loc.timeFormat(QLocale.ShortFormat)

    ###
    #    Destroys this manager, and all the properties it has created.
    ###
    def __del__(self):
        self.clear()
        del self.d_ptr

    ###
    #    Returns the given \a property's value.
    #
    #    If the given property is not managed by this manager, this:
    #    function returns an invalid time object.
    #
    #    \sa setValue()
    ###
    def value(self, property):
        return self.d_ptr.m_values.get(property, QTime())

    ###
    #    \reimp
    ###
    def valueText(self, property):
        if not property in self.d_ptr.m_values.keys():
            return ''
        return self.d_ptr.m_values[property].toString(self.d_ptr.m_format)

    ###
    #    \fn void QtTimePropertyManager.setValue(property, value)
    #
    #    Sets the value of the given \a property to \a value.
    #
    #    \sa value(), valueChanged()
    ###
    def setValue(self, property, val):
        setSimpleValue(self.d_ptr.m_values, self,
                    self.propertyChangedSignal,
                    self.valueChangedSignal,
                    property, val)

    ###
    #    \reimp
    ###
    def initializeProperty(self, property):
        self.d_ptr.m_values[property] = QTime.currentTime()

    ###
    #    \reimp
    ###
    def uninitializeProperty(self, property):
        self.d_ptr.m_values.remove(property)

class QtDateTimePropertyManagerPrivate():
    def __init__(self):
        self.q_ptr = None

        self.m_values = QMap()
        self.m_format = ''

###  \class QtDateTimePropertyManager

#    \brief The QtDateTimePropertyManager provides and manages QDateTime properties.
#
#    A date and time property has a current value which can be
#    retrieved using the value() function, and set using the setValue()
#    slot. In addition, QtDateTimePropertyManager provides the
#    valueChanged() signal which is emitted whenever a property created
#    by this manager changes.
#
#    \sa QtAbstractPropertyManager, QtDateTimeEditFactory, QtDatePropertyManager
###
#
###
#    \fn void QtDateTimePropertyManager.valueChanged(property, value)
#
#    This signal is emitted whenever a property created by this manager
#    changes its value, passing a pointer to the \a property and the new
#    \a value as parameters.
###
#
class QtDateTimePropertyManager(QtAbstractPropertyManager):
    valueChangedSignal = pyqtSignal(QtProperty, QDateTime)

    ###
    #    Creates a manager with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtDateTimePropertyManager, self).__init__(parent)

        self.d_ptr = QtDateTimePropertyManagerPrivate()
        self.d_ptr.q_ptr = self

        loc = QLocale()
        self.d_ptr.m_format = loc.dateFormat(QLocale.ShortFormat)
        self.d_ptr.m_format += ' '
        self.d_ptr.m_format += loc.timeFormat(QLocale.ShortFormat)

    #
    ###
    #    Destroys this manager, and all the properties it has created.
    ###
    def __del__(self):
        self.clear()
        del self.d_ptr

    #
    ###
    #    Returns the given \a property's value.
    #
    #    If the given \a property is not managed by this manager, this:
    #    function returns an invalid QDateTime object.
    #
    #    \sa setValue()
    ###
    def value(self, property):
        return self.d_ptr.m_values.get(property, QDateTime())
    #
    ###
    #    \reimp
    ###
    def valueText(self, property):
        return self.d_ptr.m_values[property].toString(self.d_ptr.m_format)

    #
    ###
    #    \fn void QtDateTimePropertyManager.setValue(property, value)
    #
    #    Sets the value of the given \a property to \a value.
    #
    #    \sa value(), valueChanged()
    ###
    def setValue(self, property, val):
        setSimpleValue(self.d_ptr.m_values, self,
                    self.propertyChangedSignal,
                    self.valueChangedSignal,
                    property, val)

    #
    ###
    #    \reimp
    ###
    def initializeProperty(self, property):
        self.d_ptr.m_values[property] = QDateTime.currentDateTime()

    #
    ###
    #    \reimp
    ###
    def uninitializeProperty(self, property):
        self.d_ptr.m_values.remove(property)

class QtKeySequencePropertyManagerPrivate():
    def __init__(self):
        self.q_ptr = None
        self.m_format = ''
        self.m_values = QMap()

###  \class QtKeySequencePropertyManager
#
#    \brief The QtKeySequencePropertyManager provides and manages QKeySequence properties.
#
#    A key sequence's value can be retrieved using the value()
#    function, and set using the setValue() slot.
#
#    In addition, QtKeySequencePropertyManager provides the valueChanged() signal
#    which is emitted whenever a property created by this manager
#    changes.
#
#    \sa QtAbstractPropertyManager
###

###
#    \fn void QtKeySequencePropertyManager.valueChanged(property, value)
#
#    This signal is emitted whenever a property created by this manager
#    changes its value, passing a pointer to the \a property and the new
#    \a value as parameters.
###
class QtKeySequencePropertyManager(QtAbstractPropertyManager):
    valueChangedSignal = pyqtSignal(QtProperty, QKeySequence)

    ###
    #    Creates a manager with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtKeySequencePropertyManager, self).__init__(parent)

        self.d_ptr = QtKeySequencePropertyManagerPrivate()
        self.d_ptr.q_ptr = self

    ###
    #    Destroys this manager, and all the properties it has created.
    ###
    def __del__(self):
        self.clear()
        del self.d_ptr

    ###
    #    Returns the given \a property's value.
    #
    #    If the given \a property is not managed by this manager, this:
    #    function returns an empty QKeySequence object.
    #
    #    \sa setValue()
    ###
    def value(self, property):
        return self.d_ptr.m_values.get(property, QKeySequence())

    ###
    #    \reimp
    ###
    def valueText(self, property):
        if not property in self.d_ptr.m_values.keys():
            return ''
        return self.d_ptr.m_values[property].toString(QKeySequence.NativeText)

    ###
    #    \fn void QtKeySequencePropertyManager.setValue(property, value)
    #
    #    Sets the value of the given \a property to \a value.
    #
    #    \sa value(), valueChanged()
    ###
    def setValue(self, property, val):
        setSimpleValue(self.d_ptr.m_values, self,
                    self.propertyChangedSignal,
                    self.valueChangedSignal,
                    property, val)

    ###
    #    \reimp
    ###
    def initializeProperty(self, property):
        self.d_ptr.m_values[property] = QKeySequence()

    ###
    #    \reimp
    ###
    def uninitializeProperty(self, property):
        self.d_ptr.m_values.remove(property)

class QtCharPropertyManagerPrivate():
    def __init__(self):
        self.q_ptr = None
        self.m_values = QMap()

###  \class QtCharPropertyManager

#    \brief The QtCharPropertyManager provides and manages QChar properties.
#
#    A char's value can be retrieved using the value()
#    function, and set using the setValue() slot.
#
#    In addition, QtCharPropertyManager provides the valueChanged() signal
#    which is emitted whenever a property created by this manager
#    changes.
#
#    \sa QtAbstractPropertyManager
###
#
###
#    \fn void QtCharPropertyManager.valueChanged(property, value)
#
#    This signal is emitted whenever a property created by this manager
#    changes its value, passing a pointer to the \a property and the new
#    \a value as parameters.
###
#
class QtCharPropertyManager(QtAbstractPropertyManager):
    valueChangedSignal = pyqtSignal(QtProperty, str)
    ###
    #    Creates a manager with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtCharPropertyManager, self).__init__(parent)

        self.d_ptr = QtCharPropertyManagerPrivate()
        self.d_ptr.q_ptr = self

    ###
    #    Destroys this manager, and all the properties it has created.
    ###
    def __del__(self):
        self.clear()
        del self.d_ptr

    #
    ###
    #    Returns the given \a property's value.
    #
    #    If the given \a property is not managed by this manager, this:
    #    function returns an null QChar object.
    #
    #    \sa setValue()
    ###
    def value(self, property):
        return self.d_ptr.m_values.get(property, '')

    #
    ###
    #    \reimp
    ###
    def valueText(self, property):
        if not property in self.d_ptr.m_values.keys():
            return ''
        c = self.d_ptr.m_values[property]
        if c=='':
            return ''
        else:
            return str(c)

    #
    ###
    #    \fn void QtCharPropertyManager.setValue(property, value)
    #
    #    Sets the value of the given \a property to \a value.
    #
    #    \sa value(), valueChanged()
    ###
    def setValue(self, property, val):
        setSimpleValue(self.d_ptr.m_values, self,
                    self.propertyChangedSignal,
                    self.valueChangedSignal,
                    property, val)

    #
    ###
    #    \reimp
    ###
    def initializeProperty(self, property):
        self.d_ptr.m_values[property] = ''

    #
    ###
    #    \reimp
    ###
    def uninitializeProperty(self, property):
        self.d_ptr.m_values.remove(property)

class QtLocalePropertyManagerPrivate():
    def __init__(self):
        self.q_ptr = None
        self.m_values = QMap()
        self.m_propertyToLanguage = QMap()
        self.m_propertyToCountry = QMap()
        self.m_languageToProperty = QMap()
        self.m_countryToProperty = QMap()
        self.m_enumPropertyManager = None

    def slotEnumChanged(self, property, value):
        prop = self.m_languageToProperty.get(property, 0)
        if prop:
            loc = self.m_values[prop]
            newLanguage = loc.language()
            newCountry = loc.country()
            newLanguage, c = metaEnumProvider().indexToLocale(value, 0)
            newLoc = QLocale(newLanguage, newCountry)
            self.q_ptr.setValue(prop, newLoc)
        else:
            prop = self.m_countryToProperty.get(property, 0)
            if prop:
                loc = self.m_values[prop]
                newLanguage = loc.language()
                newCountry = loc.country()
                newLanguage, newCountry = metaEnumProvider().indexToLocale(self.m_enumPropertyManager.value(self.m_propertyToLanguage[prop]), value)
                newLoc = QLocale(newLanguage, newCountry)
                self.q_ptr.setValue(prop, newLoc)

    def slotPropertyDestroyed(self, property):
        subProp = self.m_languageToProperty.get(property, 0)
        if subProp:
            self.m_propertyToLanguage[subProp] = 0
            self.m_languageToProperty.remove(property)
        else:
            subProp = self.m_countryToProperty.get(property, 0)
            if subProp:
                self.m_propertyToCountry[subProp] = 0
                self.m_countryToProperty.remove(property)

        self.m_enumPropertyManager = QtEnumPropertyManager(self)
        self.m_enumPropertyManager.valueChangedSignal.connect(self.slotEnumChanged)
        self.m_enumPropertyManager.propertyDestroyedSignal.connect(self.slotPropertyDestroyed)

###
#    \class QtLocalePropertyManager
#
#    \brief The QtLocalePropertyManager provides and manages properties.
#
#    A locale property has nested \e language and \e country
#    subproperties. The top-level property's value can be retrieved
#    using the value() function, and set using the setValue() slot.
#
#    The subproperties are created by QtEnumPropertyManager object.
#    These submanager can be retrieved using the subEnumPropertyManager()
#    function. In order to provide editing widgets for the subproperties
#    in a property browser widget, this manager must be associated with editor factory.
#
#    In addition, QtLocalePropertyManager provides the valueChanged()
#    signal which is emitted whenever a property created by this
#    manager changes.
#
#    \sa QtAbstractPropertyManager, QtEnumPropertyManager
###
#
###
#    \fn void QtLocalePropertyManager.valueChanged(property, value)
#
#    This signal is emitted whenever a property created by this manager
#    changes its value, passing a pointer to the \a property and the
#    new \a value as parameters.
#
#    \sa setValue()
###
#
class QtLocalePropertyManager(QtAbstractPropertyManager):
    valueChangedSignal = pyqtSignal(QtProperty, QLocale)
    ###
    #    Creates a manager with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtLocalePropertyManager, self).__init__(parent)

        self.d_ptr = QtLocalePropertyManagerPrivate()
        self.d_ptr.q_ptr = self

        self.d_ptr.m_enumPropertyManager = QtEnumPropertyManager(self)
        self.d_ptr.m_enumPropertyManager.valueChangedSignal.connect(self.d_ptr.slotEnumChanged)
        self.d_ptr.m_enumPropertyManager.propertyDestroyedSignal.connect(self.d_ptr.slotPropertyDestroyed)

    #
    ###
    #    Destroys this manager, and all the properties it has created.
    ###
    def __del__(self):
        self.clear()
        del self.d_ptr

    #
    ###
    #    Returns the manager that creates the nested \e language
    #    and \e country subproperties.
    #
    #    In order to provide editing widgets for the mentioned subproperties
    #    in a property browser widget, this manager must be associated with
    #    an editor factory.
    #
    #    \sa QtAbstractPropertyBrowser.setFactoryForManager()
    ###
    def subEnumPropertyManager(self):
        return self.d_ptr.m_enumPropertyManager

    #
    ###
    #    Returns the given \a property's value.
    #
    #    If the given property is not managed by this manager, this:
    #    function returns the default locale.
    #
    #    \sa setValue()
    ###
    def value(self, property):
        return self.d_ptr.m_values.get(property, QLocale())

    #
    ###
    #    \reimp
    ###
    def valueText(self, property):
        if not property in self.d_ptr.m_values.keys():
            return ''
        loc = self.d_ptr.m_values[property]
        langIdx = 0
        countryIdx = 0
        langIdx, countryIdx = metaEnumProvider().localeToIndex(loc.language(), loc.country())
        s = self.tr("%s, %s"%(metaEnumProvider().languageEnumNames()[langIdx],
                metaEnumProvider().countryEnumNames(loc.language()).at(countryIdx)))
        return s

    #
    ###
    #    \fn void QtLocalePropertyManager.setValue(property, value)
    #
    #    Sets the value of the given \a property to \a value. Nested
    #    properties are updated automatically.
    #
    #    \sa value(), valueChanged()
    ###
    def setValue(self, property, val):
        if not property in self.d_ptr.m_values.keys():
            return

        loc = self.d_ptr.m_values[property]
        if (loc == val):
            return

        self.d_ptr.m_values[property] = val

        langIdx = 0
        countryIdx = 0
        langIdx, countryIdx = metaEnumProvider().localeToIndex(val.language(), val.country())
        if (loc.language() != val.language()):
            self.d_ptr.m_enumPropertyManager.setValue(self.d_ptr.m_propertyToLanguage[property], langIdx)
            self.d_ptr.m_enumPropertyManager.setEnumNames(self.d_ptr.m_propertyToCountry[property],
                        metaEnumProvider().countryEnumNames(val.language()))

        self.d_ptr.m_enumPropertyManager.setValue(self.d_ptr.m_propertyToCountry[property], countryIdx)

        self.propertyChangedSignal.emit(property)
        self.valueChangedSignal.emit(property, val)

    #
    ###
    #    \reimp
    ###
    def initializeProperty(self, property):
        val = QLocale()
        self.d_ptr.m_values[property] = val

        langIdx = 0
        countryIdx = 0
        langIdx, countryIdx = metaEnumProvider().localeToIndex(val.language(), val.country())

        languageProp = self.d_ptr.m_enumPropertyManager.addProperty()
        languageProp.setPropertyName(self.tr("Language"))
        self.d_ptr.m_enumPropertyManager.setEnumNames(languageProp, metaEnumProvider().languageEnumNames())
        self.d_ptr.m_enumPropertyManager.setValue(languageProp, langIdx)
        self.d_ptr.m_propertyToLanguage[property] = languageProp
        self.d_ptr.m_languageToProperty[languageProp] = property
        property.addSubProperty(languageProp)

        countryProp = self.d_ptr.m_enumPropertyManager.addProperty()
        countryProp.setPropertyName(self.tr("Country"))
        self.d_ptr.m_enumPropertyManager.setEnumNames(countryProp, metaEnumProvider().countryEnumNames(val.language()))
        self.d_ptr.m_enumPropertyManager.setValue(countryProp, countryIdx)
        self.d_ptr.m_propertyToCountry[property] = countryProp
        self.d_ptr.m_countryToProperty[countryProp] = property
        property.addSubProperty(countryProp)

    #
    ###
    #    \reimp
    ###
    def uninitializeProperty(self, property):
        languageProp = self.d_ptr.m_propertyToLanguage[property]
        if (languageProp):
            self.d_ptr.m_languageToProperty.remove(languageProp)
            del languageProp

        self.d_ptr.m_propertyToLanguage.remove(property)

        countryProp = self.d_ptr.m_propertyToCountry[property]
        if (countryProp):
            self.d_ptr.m_countryToProperty.remove(countryProp)
            del countryProp

        self.d_ptr.m_propertyToCountry.remove(property)

        self.d_ptr.m_values.remove(property)

class QtPointPropertyManagerPrivate():
    def __init__(self):
        self.q_ptr = None

        self.m_values = QMap()
        self.m_propertyToX = QMap()
        self.m_propertyToY = QMap()
        self.m_xToProperty = QMap()
        self.m_yToProperty = QMap()

    def slotIntChanged(self, property, value):
        xprop = self.m_xToProperty.get(property, 0)
        if xprop:
            p = copy.copy(self.m_values[xprop])
            p.setX(value)
            self.q_ptr.setValue(xprop, p)
        else:
            yprop = self.m_yToProperty.get(property, 0)
            if yprop:
                p = copy.copy(self.m_values[yprop])
                p.setY(value)
                self.q_ptr.setValue(yprop, p)

    def slotPropertyDestroyed(self, property):
        pointProp = self.m_xToProperty.get(property, 0)
        if pointProp:
            self.m_propertyToX[pointProp] = 0
            self.m_xToProperty.remove(property)
        else:
            pointProp = self.m_yToProperty.get(property, 0)
            if pointProp:
                self.m_propertyToY[pointProp] = 0
                self.m_yToProperty.remove(property)

###  \class QtPointPropertyManager
#
#    \brief The QtPointPropertyManager provides and manages properties.
#
#    A point property has nested \e x and \e y subproperties. The
#    top-level property's value can be retrieved using the value()
#    function, and set using the setValue() slot.
#
#    The subproperties are created by a QtIntPropertyManager object. This
#    manager can be retrieved using the subIntPropertyManager() function. In
#    order to provide editing widgets for the subproperties in a
#    property browser widget, this manager must be associated with an
#    editor factory.
#
#    In addition, QtPointPropertyManager provides the valueChanged() signal which
#    is emitted whenever a property created by this manager changes.
#
#    \sa QtAbstractPropertyManager, QtIntPropertyManager, QtPointFPropertyManager
###

###
#    \fn void QtPointPropertyManager.valueChanged(property, value)
#
#    This signal is emitted whenever a property created by this manager
#    changes its value, passing a pointer to the \a property and the
#    new \a value as parameters.
#
#    \sa setValue()
###
class QtPointPropertyManager(QtAbstractPropertyManager):
    valueChangedSignal = pyqtSignal(QtProperty, QPoint)
    ###
    #    Creates a manager with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtPointPropertyManager, self).__init__(parent)

        self.d_ptr = QtPointPropertyManagerPrivate()
        self.d_ptr.q_ptr = self

        self.d_ptr.m_intPropertyManager = QtIntPropertyManager(self)
        self.d_ptr.m_intPropertyManager.valueChangedSignal.connect(self.d_ptr.slotIntChanged)
        self.d_ptr.m_intPropertyManager.propertyDestroyedSignal.connect(self.d_ptr.slotPropertyDestroyed)

    ###
    #    Destroys this manager, and all the properties it has created.
    ###
    def __del__(self):
        self.clear()
        del self.d_ptr

    ###
    #    Returns the manager that creates the nested \e x and \e y
    #    subproperties.
    #
    #    In order to provide editing widgets for the subproperties in a
    #    property browser widget, this manager must be associated with an
    #    editor factory.
    #
    #    \sa QtAbstractPropertyBrowser.setFactoryForManager()
    ###
    def subIntPropertyManager(self):
        return self.d_ptr.m_intPropertyManager

    ###
    #    Returns the given \a property's value.
    #
    #    If the given \a property is not managed by this manager, this:
    #    function returns a point with coordinates (0, 0).
    #
    #    \sa setValue()
    ###
    def value(self, property):
        return self.d_ptr.m_values.get(property, QPoint())

    ###
    #    \reimp
    ###
    def valueText(self, property):
        if not property in self.d_ptr.m_values.keys():
            return ''
        v = self.d_ptr.m_values[property]
        return self.tr("(%d, %d)"%(v.x(), v.y()))

    ###
    #    \fn void QtPointPropertyManager.setValue(property, value)
    #
    #    Sets the value of the given \a property to \a value. Nested
    #    properties are updated automatically.
    #
    #    \sa value(), valueChanged()
    ###
    def setValue(self, property, val):
        if not property in self.d_ptr.m_values.keys():
            return

        if (self.d_ptr.m_values[property] == val):
            return

        self.d_ptr.m_values[property] = val
        self.d_ptr.m_intPropertyManager.setValue(self.d_ptr.m_propertyToX[property], val.x())
        self.d_ptr.m_intPropertyManager.setValue(self.d_ptr.m_propertyToY[property], val.y())

        self.propertyChangedSignal.emit(property)
        self.valueChangedSignal.emit(property, val)

    ###
    #    \reimp
    ###
    def initializeProperty(self, property):
        self.d_ptr.m_values[property] = QPoint(0, 0)

        xProp = self.d_ptr.m_intPropertyManager.addProperty()
        xProp.setPropertyName(self.tr("X"))
        self.d_ptr.m_intPropertyManager.setValue(xProp, 0)
        self.d_ptr.m_propertyToX[property] = xProp
        self.d_ptr.m_xToProperty[xProp] = property
        property.addSubProperty(xProp)

        yProp = self.d_ptr.m_intPropertyManager.addProperty()
        yProp.setPropertyName(self.tr("Y"))
        self.d_ptr.m_intPropertyManager.setValue(yProp, 0)
        self.d_ptr.m_propertyToY[property] = yProp
        self.d_ptr.m_yToProperty[yProp] = property
        property.addSubProperty(yProp)

    ###
    #    \reimp
    ###
    def uninitializeProperty(self, property):
        xProp = self.d_ptr.m_propertyToX[property]
        if (xProp):
            self.d_ptr.m_xToProperty.remove(xProp)
            del xProp

        self.d_ptr.m_propertyToX.remove(property)

        yProp = self.d_ptr.m_propertyToY[property]
        if (yProp):
            self.d_ptr.m_yToProperty.remove(yProp)
            del yProp

        self.d_ptr.m_propertyToY.remove(property)

        self.d_ptr.m_values.remove(property)

class QtPointFPropertyManagerPrivate():
    class Data():
        val = QPointF()
        decimals = 2

    def __init__(self):
        self.q_ptr = None
        self.m_values = QMap()
        self.m_propertyToX = QMap()
        self.m_propertyToY = QMap()
        self.m_xToProperty = QMap()
        self.m_yToProperty = QMap()
        self.Data = QtPointFPropertyManagerPrivate.Data()

    def slotDoubleChanged(self, property, value):
        prop = self.m_xToProperty.get(property, 0)
        if prop:
            p = copy.copy(self.m_values[prop].val)
            p.setX(value)
            self.q_ptr.setValue(prop, p)
        else:
            prop = self.m_yToProperty.get(property, 0)
            if prop:
                p = copy.copy(self.m_values[prop].val)
                p.setY(value)
                self.q_ptr.setValue(prop, p)

    def slotPropertyDestroyed(self, property):
        pointProp = self.m_xToProperty.get(property, 0)
        if pointProp:
            self.m_propertyToX[pointProp] = 0
            self.m_xToProperty.remove(property)
        else:
            pointProp = self.m_yToProperty.get(property, 0)
            if pointProp:
                self.m_propertyToY[pointProp] = 0
                self.m_yToProperty.remove(property)

###  \class QtPointFPropertyManager

#    \brief The QtPointFPropertyManager provides and manages properties.
#
#    A point property has nested \e x and \e y subproperties. The
#    top-level property's value can be retrieved using the value()
#    function, and set using the setValue() slot.
#
#    The subproperties are created by a QtDoublePropertyManager object. This
#    manager can be retrieved using the subDoublePropertyManager() function. In
#    order to provide editing widgets for the subproperties in a
#    property browser widget, this manager must be associated with an
#    editor factory.
#
#    In addition, QtPointFPropertyManager provides the valueChanged() signal which
#    is emitted whenever a property created by this manager changes.
#
#    \sa QtAbstractPropertyManager, QtDoublePropertyManager, QtPointPropertyManager
###
#
###
#    \fn void QtPointFPropertyManager.valueChanged(property, value)
#
#    This signal is emitted whenever a property created by this manager
#    changes its value, passing a pointer to the \a property and the
#    new \a value as parameters.
#
#    \sa setValue()
###
#
###
#    \fn void QtPointFPropertyManager.decimalsChanged(property, prec)
#
#    This signal is emitted whenever a property created by this manager
#    changes its precision of value, passing a pointer to the
#    \a property and the new \a prec value
#
#    \sa setDecimals()
###
#
###
#    Creates a manager with the given \a parent.
###
class QtPointFPropertyManager(QtAbstractPropertyManager):
    valueChangedSignal = pyqtSignal(QtProperty, QPointF)
    decimalsChangedSignal = pyqtSignal(QtProperty, int)
    ###
    #    Creates a manager with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtPointFPropertyManager, self).__init__(parent)

        self.d_ptr = QtPointFPropertyManagerPrivate()
        self.d_ptr.q_ptr = self

        self.d_ptr.m_doublePropertyManager = QtDoublePropertyManager(self)
        self.d_ptr.m_doublePropertyManager.valueChangedSignal.connect(self.d_ptr.slotDoubleChanged)
        self.d_ptr.m_doublePropertyManager.propertyDestroyedSignal.connect(self.d_ptr.slotPropertyDestroyed)

    #
    ###
    #    Destroys this manager, and all the properties it has created.
    ###
    def __del__(self):
        self.clear()
        del self.d_ptr

    #
    ###
    #    Returns the manager that creates the nested \e x and \e y
    #    subproperties.
    #
    #    In order to provide editing widgets for the subproperties in a
    #    property browser widget, this manager must be associated with an
    #    editor factory.
    #
    #    \sa QtAbstractPropertyBrowser.setFactoryForManager()
    ###
    def subDoublePropertyManager(self):
        return self.d_ptr.m_doublePropertyManager

    #
    ###
    #    Returns the given \a property's value.
    #
    #    If the given \a property is not managed by this manager, this:
    #    function returns a point with coordinates (0, 0).
    #
    #    \sa setValue()
    ###
    def value(self, property):
        return getValue(self.d_ptr.m_values, property, QPointF())

    #
    ###
    #    Returns the given \a property's precision, in decimals.
    #
    #    \sa setDecimals()
    ###
    def decimals(self, property):
        return getData(self.d_ptr.m_values, DATA_DECIMALS, property, 0)

    #
    ###
    #    \reimp
    ###
    def valueText(self, property):
        if not property in self.d_ptr.m_values.keys():
            return ''
        v = self.d_ptr.m_values[property].val
        dec = self.d_ptr.m_values[property].decimals
        fs = '%%.%df, %%.%df'%(dec, dec)
        return self.tr(fs%(v.x(), v.y()))

    #
    ###
    #    \fn void QtPointFPropertyManager.setValue(property, value)
    #
    #    Sets the value of the given \a property to \a value. Nested
    #    properties are updated automatically.
    #
    #    \sa value(), valueChanged()
    ###
    def setValue(self, property, val):
        if not property in self.d_ptr.m_values.keys():
            return

        if (self.d_ptr.m_values[property].val == val):
            return

        self.d_ptr.m_values[property].val = val
        self.d_ptr.m_doublePropertyManager.setValue(self.d_ptr.m_propertyToX[property], val.x())
        self.d_ptr.m_doublePropertyManager.setValue(self.d_ptr.m_propertyToY[property], val.y())

        self.propertyChangedSignal.emit(property)
        self.valueChangedSignal.emit(property, val)

    #
    ###
    #    \fn void QtPointFPropertyManager.setDecimals(property, prec)
    #
    #    Sets the precision of the given \a property to \a prec.
    #
    #    The valid decimal range is 0-13. The default is 2.
    #
    #    \sa decimals()
    ###
    def setDecimals(self, property, prec):
        if not property in self.d_ptr.m_values.keys():
            return

        data = self.d_ptr.m_values[property]

        if (prec > 13):
            prec = 13
        elif (prec < 0):
            prec = 0

        if (data.decimals == prec):
            return

        data.decimals = prec
        self.d_ptr.m_doublePropertyManager.setDecimals(self.d_ptr.m_propertyToX[property], prec)
        self.d_ptr.m_doublePropertyManager.setDecimals(self.d_ptr.m_propertyToY[property], prec)

        self.d_ptr.m_values[property] = data

        self.decimalsChangedSignal.emit(property, data.decimals)

    #
    ###
    #    \reimp
    ###
    def initializeProperty(self, property):
        self.d_ptr.m_values[property] = QtPointFPropertyManagerPrivate.Data()

        xProp = self.d_ptr.m_doublePropertyManager.addProperty()
        xProp.setPropertyName(self.tr("X"))
        self.d_ptr.m_doublePropertyManager.setDecimals(xProp, self.decimals(property))
        self.d_ptr.m_doublePropertyManager.setValue(xProp, 0)
        self.d_ptr.m_propertyToX[property] = xProp
        self.d_ptr.m_xToProperty[xProp] = property
        property.addSubProperty(xProp)

        yProp = self.d_ptr.m_doublePropertyManager.addProperty()
        yProp.setPropertyName(self.tr("Y"))
        self.d_ptr.m_doublePropertyManager.setDecimals(yProp, self.decimals(property))
        self.d_ptr.m_doublePropertyManager.setValue(yProp, 0)
        self.d_ptr.m_propertyToY[property] = yProp
        self.d_ptr.m_yToProperty[yProp] = property
        property.addSubProperty(yProp)

    #
    ###
    #    \reimp
    ###
    def uninitializeProperty(self, property):
        xProp = self.d_ptr.m_propertyToX[property]
        if (xProp):
            self.d_ptr.m_xToProperty.remove(xProp)
            del xProp

        self.d_ptr.m_propertyToX.remove(property)

        yProp = self.d_ptr.m_propertyToY[property]
        if (yProp):
            self.d_ptr.m_yToProperty.remove(yProp)
            del yProp

        self.d_ptr.m_propertyToY.remove(property)

        self.d_ptr.m_values.remove(property)

class QtSizePropertyManagerPrivate():
    class Data():
        val = QSize(0, 0)
        minVal = QSize(0, 0)
        minVal = QSize(0, 0)
        maxVal = QSize(INT_MAX, INT_MAX)
        def minimumValue(self):
            return self.minVal

        def maximumValue(self):
            return self.maxVal

        def setMinimumValue(self, newMinVal):
            setSizeMinimumData(self, newMinVal)

        def setMaximumValue(self, newMaxVal):
            setSizeMaximumData(self, newMaxVal)

    def __init__(self):
        self.q_ptr = None
        self.m_values = QMap()
        self.m_propertyToW = QMap()
        self.m_propertyToH = QMap()
        self.m_wToProperty = QMap()
        self.m_hToProperty = QMap()
        self.Data = QtSizePropertyManagerPrivate.Data()

    def slotIntChanged(self, property, value):
        prop = self.m_wToProperty.get(property, 0)
        if prop:
            s = copy.copy(self.m_values[prop].val)
            s.setWidth(value)
            self.q_ptr.setValue(prop, s)
        else:
            prop = self.m_hToProperty.get(property, 0)
            if prop:
                s = copy.copy(self.m_values[prop].val)
                s.setHeight(value)
                self.q_ptr.setValue(prop, s)

    def slotPropertyDestroyed(self, property):
        pointProp = self.m_wToProperty.get(property, 0)
        if pointProp:
            self.m_propertyToW[pointProp] = 0
            self.m_wToProperty.remove(property)
        else:
            pointProp = self.m_hToProperty.get(property, 0)
            if pointProp:
                self.m_propertyToH[pointProp] = 0
                self.m_hToProperty.remove(property)

    def setValue(self, property, val):
        self.m_intPropertyManager.setValue(self.m_propertyToW[property], val.width())
        self.m_intPropertyManager.setValue(self.m_propertyToH[property], val.height())

    def setRange(self, property, minVal, maxVal, val):
        wProperty = self.m_propertyToW[property]
        hProperty = self.m_propertyToH[property]
        self.m_intPropertyManager.setRange(wProperty, minVal.width(), maxVal.width())
        self.m_intPropertyManager.setValue(wProperty, val.width())
        self.m_intPropertyManager.setRange(hProperty, minVal.height(), maxVal.height())
        self.m_intPropertyManager.setValue(hProperty, val.height())

#
###
#    \class QtSizePropertyManager
#
#    \brief The QtSizePropertyManager provides and manages QSize properties.
#
#    A size property has nested \e width and \e height
#    subproperties. The top-level property's value can be retrieved
#    using the value() function, and set using the setValue() slot.
#
#    The subproperties are created by a QtIntPropertyManager object. This
#    manager can be retrieved using the subIntPropertyManager() function. In
#    order to provide editing widgets for the subproperties in a
#    property browser widget, this manager must be associated with an
#    editor factory.
#
#    A size property also has a range of valid values defined by a
#    minimum size and a maximum size. These sizes can be retrieved
#    using the minimum() and the maximum() functions, and set using the
#    setMinimum() and setMaximum() slots. Alternatively, the range can
#    be defined in one go using the setRange() slot.
#
#    In addition, QtSizePropertyManager provides the valueChanged() signal
#    which is emitted whenever a property created by this manager
#    changes, and the rangeChanged() signal which is emitted whenever
#    such a property changes its range of valid sizes.
#
#    \sa QtAbstractPropertyManager, QtIntPropertyManager, QtSizeFPropertyManager
###
#
###
#    \fn void QtSizePropertyManager.valueChanged(property, value)
#
#    This signal is emitted whenever a property created by this manager
#    changes its value, passing a pointer to the \a property and the new
#    \a value as parameters.
#
#    \sa setValue()
###
#
###
#    \fn void QtSizePropertyManager.rangeChanged(property, minimum, maximum)
#
#    This signal is emitted whenever a property created by this manager
#    changes its range of valid sizes, passing a pointer to the \a
#    property and the new \a minimum and \a maximum sizes.
#
#    \sa setRange()
###
#
class QtSizePropertyManager(QtAbstractPropertyManager):
    valueChangedSignal = pyqtSignal(QtProperty, QSize)
    rangeChangedSignal = pyqtSignal(QtProperty, QSize, QSize)

    ###
    #    Creates a manager with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtSizePropertyManager, self).__init__(parent)

        self.d_ptr = QtSizePropertyManagerPrivate()
        self.d_ptr.q_ptr = self

        self.d_ptr.m_intPropertyManager = QtIntPropertyManager(self)
        self.d_ptr.m_intPropertyManager.valueChangedSignal.connect(self.d_ptr.slotIntChanged)
        self.d_ptr.m_intPropertyManager.propertyDestroyedSignal.connect(self.d_ptr.slotPropertyDestroyed)

    #
    ###
    #    Destroys this manager, and all the properties it has created.
    ###
    def __del__(self):
        self.clear()
        del self.d_ptr

    #
    ###
    #    Returns the manager that creates the nested \e width and \e height
    #    subproperties.
    #
    #    In order to provide editing widgets for the \e width and \e height
    #    properties in a property browser widget, this manager must be
    #    associated with an editor factory.
    #
    #    \sa QtAbstractPropertyBrowser.setFactoryForManager()
    ###
    def subIntPropertyManager(self):
        return self.d_ptr.m_intPropertyManager

    #
    ###
    #    Returns the given \a property's value.
    #
    #    If the given \a property is not managed by this manager, this:
    #    function returns an invalid size
    #
    #    \sa setValue()
    ###
    def value(self, property):
        return getValue(self.d_ptr.m_values, property, QSize())

    ###
    #    Returns the given \a property's minimum size value.
    #
    #    \sa setMinimum(), maximum(), setRange()
    ###
    def minimum(self, property):
        return getMinimum(self.d_ptr.m_values, property, QSize())

    #
    ###
    #    Returns the given \a property's maximum size value.

    #    \sa setMaximum(), minimum(), setRange()
    ###
    def maximum(self, property):
        return getMaximum(self.d_ptr.m_values, property, QSize())

    #
    ###
    #    \reimp
    ###
    def valueText(self, property):
        if not property in self.d_ptr.m_values.keys():
            return ''
        v = self.d_ptr.m_values[property].val
        return self.tr("%d x %d"%(v.width(), v.height()))

    #
    ###
    #    \fn void QtSizePropertyManager.setValue(property, value)

    #    Sets the value of the given \a property to \a value.

    #    If the specified \a value is not valid according to the given \a:
    #    property's size range, the \a value is adjusted to the nearest
    #    valid value within the size range.

    #    \sa value(), setRange(), valueChanged()
    ###
    def setValue(self, property, val):
        setValueInRange(self,
                    self.d_ptr,
                    self.propertyChangedSignal,
                    self.valueChangedSignal,
                    property, val, self.d_ptr.setValue)

    #
    ###
    #    Sets the minimum size value for the given \a property to \a minVal.

    #    When setting the minimum size value, the maximum and current
    #    values are adjusted if necessary (ensuring that the size range
    #    remains valid and that the current value is within the range).

    #    \sa minimum(), setRange(), rangeChanged()
    ###
    def setMinimum(self, property, minVal):
        setBorderValue(self, self.d_ptr,
                    self.propertyChangedSignal,
                    self.valueChangedSignal,
                    self.rangeChangedSignal,
                    property,
                    DATA_GETMINVAL,
                    DATA_SETMINVAL,
                    minVal, self.d_ptr.setRange)

    #
    ###
    #    Sets the maximum size value for the given \a property to \a maxVal.

    #    When setting the maximum size value, the minimum and current
    #    values are adjusted if necessary (ensuring that the size range
    #    remains valid and that the current value is within the range).

    #    \sa maximum(), setRange(), rangeChanged()
    ###
    def setMaximum(self, property, maxVal):
        setBorderValue(self, self.d_ptr,
                    self.propertyChangedSignal,
                    self.valueChangedSignal,
                    self.rangeChangedSignal,
                    property,
                    DATA_GETMAXVAL,
                    DATA_SETMAXVAL,
                    maxVal, self.d_ptr.setRange)

    #
    ###
    #    \fn void QtSizePropertyManager.setRange(property, minimum, maximum)

    #    Sets the range of valid values.

    #    This is a convenience function defining the range of valid values
    #    in one go; setting the \a minimum and \a maximum values for the
    #    given \a property with a single function call.

    #    When setting a new range, the current value is adjusted if
    #    necessary (ensuring that the value remains within the range).

    #    \sa setMinimum(), setMaximum(), rangeChanged()
    ###
    def setRange(self, property, minVal, maxVal):
        setBorderValues(self, self.d_ptr,
                    self.propertyChangedSignal,
                    self.valueChangedSignal,
                    self.rangeChangedSignal,
                    property, minVal, maxVal, self.d_ptr.setRange)

    #
    ###
    #    \reimp
    ###
    def initializeProperty(self, property):
        self.d_ptr.m_values[property] = QtSizePropertyManagerPrivate.Data()

        wProp = self.d_ptr.m_intPropertyManager.addProperty()
        wProp.setPropertyName(self.tr("Width"))
        self.d_ptr.m_intPropertyManager.setValue(wProp, 0)
        self.d_ptr.m_intPropertyManager.setMinimum(wProp, 0)
        self.d_ptr.m_propertyToW[property] = wProp
        self.d_ptr.m_wToProperty[wProp] = property
        property.addSubProperty(wProp)

        hProp = self.d_ptr.m_intPropertyManager.addProperty()
        hProp.setPropertyName(self.tr("Height"))
        self.d_ptr.m_intPropertyManager.setValue(hProp, 0)
        self.d_ptr.m_intPropertyManager.setMinimum(hProp, 0)
        self.d_ptr.m_propertyToH[property] = hProp
        self.d_ptr.m_hToProperty[hProp] = property
        property.addSubProperty(hProp)

    ###
    #    \reimp
    ###
    def uninitializeProperty(self, property):
        wProp = self.d_ptr.m_propertyToW[property]
        if (wProp):
            self.d_ptr.m_wToProperty.remove(wProp)
            del wProp

        self.d_ptr.m_propertyToW.remove(property)

        hProp = self.d_ptr.m_propertyToH[property]
        if (hProp):
            self.d_ptr.m_hToProperty.remove(hProp)
            del hProp

        self.d_ptr.m_propertyToH.remove(property)

        self.d_ptr.m_values.remove(property)

class QtSizeFPropertyManagerPrivate():
    class Data():
        val = QSizeF(0, 0)
        minVal = QSizeF(0, 0)
        maxVal = QSizeF(INT_MAX, INT_MAX)
        decimals = 2
        def minimumValue(self):
            return self.minVal

        def maximumValue(self):
            return self.maxVal

        def setMinimumValue(self, newMinVal):
            setSizeMinimumData(self, newMinVal)

        def setMaximumValue(self, newMaxVal):
            setSizeMaximumData(self, newMaxVal)

    def __init__(self):
        self.q_ptr = None
        self.m_values = QMap()
        self.m_propertyToW = QMap()
        self.m_propertyToH = QMap()
        self.m_wToProperty = QMap()
        self.m_hToProperty = QMap()
        self.Data = QtSizeFPropertyManagerPrivate.Data()

    def slotDoubleChanged(self, property, value):
        prop = self.m_wToProperty.get(property, 0)
        if (prop):
            s = copy.copy(self.m_values[prop].val)
            s.setWidth(value)
            self.q_ptr.setValue(prop, s)
        else:
            prop = self.m_hToProperty.get(property, 0)
            if prop:
                s = copy.copy(self.m_values[prop].val)
                s.setHeight(value)
                self.q_ptr.setValue(prop, s)

    def slotPropertyDestroyed(self, property):
        pointProp = self.m_wToProperty.get(property, 0)
        if pointProp:
            self.m_propertyToW[pointProp] = 0
            self.m_wToProperty.remove(property)
        else:
            pointProp = self.m_hToProperty.get(property, 0)
            if pointProp:
                self.m_propertyToH[pointProp] = 0
                self.m_hToProperty.remove(property)

    def setValue(self, property, val):
        self.m_doublePropertyManager.setValue(self.m_propertyToW[property], val.width())
        self.m_doublePropertyManager.setValue(self.m_propertyToH[property], val.height())

    def setRange(self, property, minVal, maxVal, val):
        self.m_doublePropertyManager.setRange(self.m_propertyToW[property], minVal.width(), maxVal.width())
        self.m_doublePropertyManager.setValue(self.m_propertyToW[property], val.width())
        self.m_doublePropertyManager.setRange(self.m_propertyToH[property], minVal.height(), maxVal.height())
        self.m_doublePropertyManager.setValue(self.m_propertyToH[property], val.height())
###
#    \class QtSizeFPropertyManager
#
#    \brief The QtSizeFPropertyManager provides and manages QSizeF properties.
#
#    A size property has nested \e width and \e height
#    subproperties. The top-level property's value can be retrieved
#    using the value() function, and set using the setValue() slot.
#
#    The subproperties are created by a QtDoublePropertyManager object. This
#    manager can be retrieved using the subDoublePropertyManager() function. In
#    order to provide editing widgets for the subproperties in a
#    property browser widget, this manager must be associated with an
#    editor factory.
#
#    A size property also has a range of valid values defined by a
#    minimum size and a maximum size. These sizes can be retrieved
#    using the minimum() and the maximum() functions, and set using the
#    setMinimum() and setMaximum() slots. Alternatively, the range can
#    be defined in one go using the setRange() slot.
#
#    In addition, QtSizeFPropertyManager provides the valueChanged() signal
#    which is emitted whenever a property created by this manager
#    changes, and the rangeChanged() signal which is emitted whenever
#    such a property changes its range of valid sizes.

#    \sa QtAbstractPropertyManager, QtDoublePropertyManager, QtSizePropertyManager
###
#
###
#    \fn void QtSizeFPropertyManager.valueChanged(property, value)

#    This signal is emitted whenever a property created by this manager
#    changes its value, passing a pointer to the \a property and the new
#    \a value as parameters.

#    \sa setValue()
###
#
###
#    \fn void QtSizeFPropertyManager.rangeChanged(property, minimum, maximum)

#    This signal is emitted whenever a property created by this manager
#    changes its range of valid sizes, passing a pointer to the \a
#    property and the new \a minimum and \a maximum sizes.

#    \sa setRange()
###
#
###
#    \fn void QtSizeFPropertyManager.decimalsChanged(property, prec)

#    This signal is emitted whenever a property created by this manager
#    changes its precision of value, passing a pointer to the
#    \a property and the new \a prec value

#    \sa setDecimals()
###
#
class QtSizeFPropertyManager(QtAbstractPropertyManager):
    valueChangedSignal = pyqtSignal(QtProperty, QSizeF)
    rangeChangedSignal = pyqtSignal(QtProperty, QSizeF, QSizeF)
    decimalsChangedSignal = pyqtSignal(QtProperty, int)
    ###
    #    Creates a manager with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtSizeFPropertyManager, self).__init__(parent)

        self.d_ptr = QtSizeFPropertyManagerPrivate()
        self.d_ptr.q_ptr = self

        self.d_ptr.m_doublePropertyManager = QtDoublePropertyManager(self)
        self.d_ptr.m_doublePropertyManager.valueChangedSignal.connect(self.d_ptr.slotDoubleChanged)
        self.d_ptr.m_doublePropertyManager.propertyDestroyedSignal.connect(self.d_ptr.slotPropertyDestroyed)

    #
    ###
    #    Destroys this manager, and all the properties it has created.
    ###
    def __del__(self):
        self.clear()
        del self.d_ptr

    ###
    #    Returns the manager that creates the nested \e width and \e height
    #    subproperties.
    #
    #    In order to provide editing widgets for the \e width and \e height
    #    properties in a property browser widget, this manager must be
    #    associated with an editor factory.

    #    \sa QtAbstractPropertyBrowser.setFactoryForManager()
    ###
    def subDoublePropertyManager(self):
        return self.d_ptr.m_doublePropertyManager

    #
    ###
    #    Returns the given \a property's value.

    #    If the given \a property is not managed by this manager, this:
    #    function returns an invalid size

    #    \sa setValue()
    ###
    def value(self, property):
        return getValue(self.d_ptr.m_values, property, QSizeF())

    ###
    #    Returns the given \a property's precision, in decimals.

    #    \sa setDecimals()
    ###
    def decimals(self, property):
        return getData(self.d_ptr.m_values, DATA_DECIMALS, property, 0)

    ###
    #    Returns the given \a property's minimum size value.

    #    \sa setMinimum(), maximum(), setRange()
    ###
    def minimum(self, property):
        return getMinimum(self.d_ptr.m_values, property, QSizeF())

    ###
    #    Returns the given \a property's maximum size value.

    #    \sa setMaximum(), minimum(), setRange()
    ###
    def maximum(self, property):
        return getMaximum(self.d_ptr.m_values, property, QSizeF())

    ###
    #    \reimp
    ###
    def valueText(self, property):
        if not property in self.d_ptr.m_values.keys():
            return ''
        v = self.d_ptr.m_values[property].val
        dec = self.d_ptr.m_values[property].decimals
        fs = '%%.%df x %%.%df'%(dec, dec)
        return self.tr(fs%(v.width(), v.height()))

    ###
    #    \fn void QtSizeFPropertyManager.setValue(property, value)

    #    Sets the value of the given \a property to \a value.

    #    If the specified \a value is not valid according to the given \a:
    #    property's size range, the \a value is adjusted to the nearest
    #    valid value within the size range.

    #    \sa value(), setRange(), valueChanged()
    ###
    def setValue(self, property, val):
        setValueInRange(self,
                    self.d_ptr,
                    self.propertyChangedSignal,
                    self.valueChangedSignal,
                    property, val, self.d_ptr.setValue)

    ###
    #    \fn void QtSizeFPropertyManager.setDecimals(property, prec)

    #    Sets the precision of the given \a property to \a prec.

    #    The valid decimal range is 0-13. The default is 2.

    #    \sa decimals()
    ###
    def setDecimals(self, property, prec):

        if not property in self.d_ptr.m_values.keys():
            return

        data = self.d_ptr.m_values[property]

        if (prec > 13):
            prec = 13
        elif (prec < 0):
            prec = 0

        if (data.decimals == prec):
            return

        data.decimals = prec
        self.d_ptr.m_doublePropertyManager.setDecimals(self.d_ptr.m_propertyToW[property], prec)
        self.d_ptr.m_doublePropertyManager.setDecimals(self.d_ptr.m_propertyToH[property], prec)

        self.d_ptr.m_values[property] = data

        self.decimalsChangedSignal.emit(property, data.decimals)

    ###
    #    Sets the minimum size value for the given \a property to \a minVal.

    #    When setting the minimum size value, the maximum and current
    #    values are adjusted if necessary (ensuring that the size range
    #    remains valid and that the current value is within the range).

    #    \sa minimum(), setRange(), rangeChanged()
    ###
    def setMinimum(self, property, minVal):
        setBorderValue(self, self.d_ptr,
                    self.propertyChangedSignal,
                    self.valueChangedSignal,
                    self.rangeChangedSignal,
                    property,
                    DATA_GETMINVAL,
                    DATA_SETMINVAL,
                    minVal, self.d_ptr.setRange)

    ###
    #    Sets the maximum size value for the given \a property to \a maxVal.

    #    When setting the maximum size value, the minimum and current
    #    values are adjusted if necessary (ensuring that the size range
    #    remains valid and that the current value is within the range).

    #    \sa maximum(), setRange(), rangeChanged()
    ###
    def setMaximum(self, property, maxVal):
        setBorderValue(self, self.d_ptr,
                    self.propertyChangedSignal,
                    self.valueChangedSignal,
                    self.rangeChangedSignal,
                    property,
                    DATA_GETMAXVAL,
                    DATA_SETMAXVAL,
                    maxVal, self.d_ptr.setRange)

    ###
    #    \fn void QtSizeFPropertyManager.setRange(property, minimum, maximum)

    #    Sets the range of valid values.

    #    This is a convenience function defining the range of valid values
    #    in one go; setting the \a minimum and \a maximum values for the
    #    given \a property with a single function call.

    #    When setting a new range, the current value is adjusted if
    #    necessary (ensuring that the value remains within the range).

    #    \sa setMinimum(), setMaximum(), rangeChanged()
    ###
    def setRange(self, property, minVal, maxVal):
        setBorderValues(self, self.d_ptr,
                    self.propertyChangedSignal,
                    self.valueChangedSignal,
                    self.rangeChangedSignal,
                    property, minVal, maxVal, self.d_ptr.setRange)

    ###
    #    \reimp
    ###
    def initializeProperty(self, property):
        self.d_ptr.m_values[property] = QtSizeFPropertyManagerPrivate.Data()

        wProp = self.d_ptr.m_doublePropertyManager.addProperty()
        wProp.setPropertyName(self.tr("Width"))
        self.d_ptr.m_doublePropertyManager.setDecimals(wProp, self.decimals(property))
        self.d_ptr.m_doublePropertyManager.setValue(wProp, 0)
        self.d_ptr.m_doublePropertyManager.setMinimum(wProp, 0)
        self.d_ptr.m_propertyToW[property] = wProp
        self.d_ptr.m_wToProperty[wProp] = property
        property.addSubProperty(wProp)

        hProp = self.d_ptr.m_doublePropertyManager.addProperty()
        hProp.setPropertyName(self.tr("Height"))
        self.d_ptr.m_doublePropertyManager.setDecimals(hProp, self.decimals(property))
        self.d_ptr.m_doublePropertyManager.setValue(hProp, 0)
        self.d_ptr.m_doublePropertyManager.setMinimum(hProp, 0)
        self.d_ptr.m_propertyToH[property] = hProp
        self.d_ptr.m_hToProperty[hProp] = property
        property.addSubProperty(hProp)

    ###
    #    \reimp
    ###
    def uninitializeProperty(self, property):
        wProp = self.d_ptr.m_propertyToW[property]
        if (wProp):
            self.d_ptr.m_wToProperty.remove(wProp)
            del wProp

        self.d_ptr.m_propertyToW.remove(property)

        hProp = self.d_ptr.m_propertyToH[property]
        if (hProp):
            self.d_ptr.m_hToProperty.remove(hProp)
            del hProp

        self.d_ptr.m_propertyToH.remove(property)

        self.d_ptr.m_values.remove(property)

class QtRectPropertyManagerPrivate():
    class Data():
        val = QRect(0, 0, 0, 0)
        constraint = QRect(0, 0, 0, 0)

    def __init__(self):
        self.q_ptr = None

        self.m_values = QMap()
        self.m_propertyToX = QMap()
        self.m_propertyToY = QMap()
        self.m_propertyToW = QMap()
        self.m_propertyToH = QMap()
        self.m_xToProperty = QMap()
        self.m_yToProperty = QMap()
        self.m_wToProperty = QMap()
        self.m_hToProperty = QMap()
        self.Data = QtRectPropertyManagerPrivate.Data()

    def slotIntChanged(self, property, value):
        prop = self.m_xToProperty.get(property, 0)
        if prop:
            r = copy.copy(self.m_values[prop].val)
            r.moveLeft(value)
            self.q_ptr.setValue(prop, r)
        else:
            prop = self.m_yToProperty.get(property)
            if prop:
                r = copy.copy(self.m_values[prop].val)
                r.moveTop(value)
                self.q_ptr.setValue(prop, r)
            else:
                prop = self.m_wToProperty.get(property)
                if prop:
                    data = copy.copy(self.m_values[prop])
                    r = copy.copy(data.val)
                    r.setWidth(value)
                    if (not data.constraint.isNull() and data.constraint.x() + data.constraint.width() < r.x() + r.width()):
                        r.moveLeft(data.constraint.left() + data.constraint.width() - r.width())

                    self.q_ptr.setValue(prop, r)
                else:
                    prop = self.m_hToProperty.get(property, 0)
                    if prop:
                        data = copy.copy(self.m_values[prop])
                        r = copy.copy(data.val)
                        r.setHeight(value)
                        if (not data.constraint.isNull() and data.constraint.y() + data.constraint.height() < r.y() + r.height()):
                            r.moveTop(data.constraint.top() + data.constraint.height() - r.height())

                        self.q_ptr.setValue(prop, r)

    def slotPropertyDestroyed(self, property):
        pointProp = self.m_xToProperty.get(property, 0)
        if pointProp:
            self.m_propertyToX[pointProp] = 0
            self.m_xToProperty.remove(property)
        else:
            pointProp = self.m_yToProperty.get(property, 0)
            if pointProp:
                self.m_propertyToY[pointProp] = 0
                self.m_yToProperty.remove(property)
            else:
                pointProp = self.m_wToProperty.get(property, 0)
                if pointProp:
                    self.m_propertyToW[pointProp] = 0
                    self.m_wToProperty.remove(property)
                else:
                    pointProp = self.m_hToProperty.get(property, 0)
                    if pointProp:
                        self.m_propertyToH[pointProp] = 0
                        self.m_hToProperty.remove(property)

    def setConstraint(self, property, constraint, val):
        isNull = constraint.isNull()
        if isNull:
            left   = INT_MIN
            right  = INT_MAX
            top    = INT_MIN
            bottom = INT_MAX
            width  = INT_MAX
            height = INT_MAX
        else:
            left   = constraint.left()
            right  = constraint.left() + constraint.width()
            top    = constraint.top()
            bottom = constraint.top() + constraint.height()
            width  = constraint.width()
            height = constraint.height()

        self.m_intPropertyManager.setRange(self.m_propertyToX[property], left, right)
        self.m_intPropertyManager.setRange(self.m_propertyToY[property], top, bottom)
        self.m_intPropertyManager.setRange(self.m_propertyToW[property], 0, width)
        self.m_intPropertyManager.setRange(self.m_propertyToH[property], 0, height)

        self.m_intPropertyManager.setValue(self.m_propertyToX[property], val.x())
        self.m_intPropertyManager.setValue(self.m_propertyToY[property], val.y())
        self.m_intPropertyManager.setValue(self.m_propertyToW[property], val.width())
        self.m_intPropertyManager.setValue(self.m_propertyToH[property], val.height())

###
#    \class QtRectPropertyManager
#
#    \brief The QtRectPropertyManager provides and manages QRect properties.
#
#    A rectangle property has nested \e x, \e y, \e width and \e height
#    subproperties. The top-level property's value can be retrieved
#    using the value() function, and set using the setValue() slot.
#
#    The subproperties are created by a QtIntPropertyManager object. This
#    manager can be retrieved using the subIntPropertyManager() function. In
#    order to provide editing widgets for the subproperties in a
#    property browser widget, this manager must be associated with an
#    editor factory.
#
#    A rectangle property also has a constraint rectangle which can be
#    retrieved using the constraint() function, and set using the
#    setConstraint() slot.
#
#    In addition, QtRectPropertyManager provides the valueChanged() signal
#    which is emitted whenever a property created by this manager
#    changes, and the constraintChanged() signal which is emitted
#    whenever such a property changes its constraint rectangle.

#    \sa QtAbstractPropertyManager, QtIntPropertyManager, QtRectFPropertyManager
###
#
###
#    \fn void QtRectPropertyManager.valueChanged(property, value)

#    This signal is emitted whenever a property created by this manager
#    changes its value, passing a pointer to the \a property and the new
#    \a value as parameters.

#    \sa setValue()
###
#
###
#    \fn void QtRectPropertyManager.constraintChanged(property, constraint)

#    This signal is emitted whenever property changes its constraint
#    rectangle, passing a pointer to the \a property and the new \a
#    constraint rectangle as parameters.

#    \sa setConstraint()
###
#
class QtRectPropertyManager(QtAbstractPropertyManager):
    valueChangedSignal = pyqtSignal(QtProperty, QRect)
    constraintChangedSignal = pyqtSignal(QtProperty, QRect)

    ###
    #    Creates a manager with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtRectPropertyManager, self).__init__(parent)

        self.d_ptr = QtRectPropertyManagerPrivate()
        self.d_ptr.q_ptr = self

        self.d_ptr.m_intPropertyManager = QtIntPropertyManager(self)
        self.d_ptr.m_intPropertyManager.valueChangedSignal.connect(self.d_ptr.slotIntChanged)
        self.d_ptr.m_intPropertyManager.propertyDestroyedSignal.connect(self.d_ptr.slotPropertyDestroyed)

    #
    ###
    #    Destroys this manager, and all the properties it has created.
    ###
    def __del__(self):
        self.clear()
        del self.d_ptr

    ###
    #    Returns the manager that creates the nested \e x, \e y, \e width
    #    and \e height subproperties.
    #
    #    In order to provide editing widgets for the mentioned
    #    subproperties in a property browser widget, this manager must be
    #    associated with an editor factory.

    #    \sa QtAbstractPropertyBrowser.setFactoryForManager()
    ###
    def subIntPropertyManager(self):
        return self.d_ptr.m_intPropertyManager

    #
    ###
    #    Returns the given \a property's value.

    #    If the given \a property is not managed by this manager, this:
    #    function returns an invalid rectangle.

    #    \sa setValue(), constraint()
    ###
    def value(self, property):
        return getValue(self.d_ptr.m_values, property, QRect())

    ###
    #    Returns the given \a property's constraining rectangle. If returned value is null QRect it means there is no constraint applied.

    #    \sa value(), setConstraint()
    ###
    def constraint(self, property):
        return getData(self.d_ptr.m_values, DATA_CONSTRAINT, property, QRect())

    ###
    #    \reimp
    ###
    def valueText(self, property):
        if not property in self.d_ptr.m_values.keys():
            return ''
        v = self.d_ptr.m_values[property].val
        return self.tr("[(%d, %d), %d x %d]"%(v.x(), v.y(),v.width(),v.height()))

    ###
    #    \fn void QtRectPropertyManager.setValue(property, value)

    #    Sets the value of the given \a property to \a value. Nested
    #    properties are updated automatically.

    #    If the specified \a value is not inside the given \a property's:
    #    constraining rectangle, the value is adjusted accordingly to fit
    #    within the constraint.

    #    \sa value(), setConstraint(), valueChanged()
    ###
    def setValue(self, property, val):

        if not property in self.d_ptr.m_values.keys():
            return

        data = self.d_ptr.m_values[property]

        newRect = val.normalized()
        if (not data.constraint.isNull() and not data.constraint.contains(newRect)):
            r1 = data.constraint
            r2 = newRect
            newRect.setLeft(max(r1.left(), r2.left()))
            newRect.setRight(min(r1.right(), r2.right()))
            newRect.setTop(max(r1.top(), r2.top()))
            newRect.setBottom(min(r1.bottom(), r2.bottom()))
            if (newRect.width() < 0 or newRect.height() < 0):
                return

        if (data.val == newRect):
            return

        data.val = newRect

        self.d_ptr.m_values[property] = data
        self.d_ptr.m_intPropertyManager.setValue(self.d_ptr.m_propertyToX[property], newRect.x())
        self.d_ptr.m_intPropertyManager.setValue(self.d_ptr.m_propertyToY[property], newRect.y())
        self.d_ptr.m_intPropertyManager.setValue(self.d_ptr.m_propertyToW[property], newRect.width())
        self.d_ptr.m_intPropertyManager.setValue(self.d_ptr.m_propertyToH[property], newRect.height())

        self.propertyChangedSignal.emit(property)
        self.valueChangedSignal.emit(property, data.val)

    ###
    #    Sets the given \a property's constraining rectangle to \a
    #    constraint.

    #    When setting the constraint, the current value is adjusted if
    #    necessary (ensuring that the current rectangle value is inside the
    #    constraint). In order to reset the constraint pass a null QRect value.

    #    \sa setValue(), constraint(), constraintChanged()
    ###
    def setConstraint(self, property, constraint):

        if not property in self.d_ptr.m_values.keys():
            return

        data = self.d_ptr.m_values[property]

        newConstraint = constraint.normalized()
        if (data.constraint == newConstraint):
            return

        oldVal = data.val

        data.constraint = newConstraint

        if (not data.constraint.isNull() and not data.constraint.contains(oldVal)):
            r1 = data.constraint
            r2 = data.val

            if (r2.width() > r1.width()):
                r2.setWidth(r1.width())
            if (r2.height() > r1.height()):
                r2.setHeight(r1.height())
            if (r2.left() < r1.left()):
                r2.moveLeft(r1.left())
            elif (r2.right() > r1.right()):
                r2.moveRight(r1.right())
            if (r2.top() < r1.top()):
                r2.moveTop(r1.top())
            elif (r2.bottom() > r1.bottom()):
                r2.moveBottom(r1.bottom())

            data.val = r2

        self.d_ptr.m_values[property] = data

        self.constraintChangedSignal.emit(property, data.constraint)

        self.d_ptr.setConstraint(property, data.constraint, data.val)

        if (data.val == oldVal):
            return

        self.propertyChangedSignal.emit(property)
        self.valueChangedSignal.emit(property, data.val)

    ###
    #    \reimp
    ###
    def initializeProperty(self, property):
        self.d_ptr.m_values[property] = QtRectPropertyManagerPrivate.Data()

        xProp = self.d_ptr.m_intPropertyManager.addProperty()
        xProp.setPropertyName(self.tr("X"))
        self.d_ptr.m_intPropertyManager.setValue(xProp, 0)
        self.d_ptr.m_propertyToX[property] = xProp
        self.d_ptr.m_xToProperty[xProp] = property
        property.addSubProperty(xProp)

        yProp = self.d_ptr.m_intPropertyManager.addProperty()
        yProp.setPropertyName(self.tr("Y"))
        self.d_ptr.m_intPropertyManager.setValue(yProp, 0)
        self.d_ptr.m_propertyToY[property] = yProp
        self.d_ptr.m_yToProperty[yProp] = property
        property.addSubProperty(yProp)

        wProp = self.d_ptr.m_intPropertyManager.addProperty()
        wProp.setPropertyName(self.tr("Width"))
        self.d_ptr.m_intPropertyManager.setValue(wProp, 0)
        self.d_ptr.m_intPropertyManager.setMinimum(wProp, 0)
        self.d_ptr.m_propertyToW[property] = wProp
        self.d_ptr.m_wToProperty[wProp] = property
        property.addSubProperty(wProp)

        hProp = self.d_ptr.m_intPropertyManager.addProperty()
        hProp.setPropertyName(self.tr("Height"))
        self.d_ptr.m_intPropertyManager.setValue(hProp, 0)
        self.d_ptr.m_intPropertyManager.setMinimum(hProp, 0)
        self.d_ptr.m_propertyToH[property] = hProp
        self.d_ptr.m_hToProperty[hProp] = property
        property.addSubProperty(hProp)

    ###
    #    \reimp
    ###
    def uninitializeProperty(self, property):
        xProp = self.d_ptr.m_propertyToX[property]
        if (xProp):
            self.d_ptr.m_xToProperty.remove(xProp)
            del xProp

        self.d_ptr.m_propertyToX.remove(property)

        yProp = self.d_ptr.m_propertyToY[property]
        if (yProp):
            self.d_ptr.m_yToProperty.remove(yProp)
            del yProp

        self.d_ptr.m_propertyToY.remove(property)

        wProp = self.d_ptr.m_propertyToW[property]
        if (wProp):
            self.d_ptr.m_wToProperty.remove(wProp)
            del wProp

        self.d_ptr.m_propertyToW.remove(property)

        hProp = self.d_ptr.m_propertyToH[property]
        if (hProp):
            self.d_ptr.m_hToProperty.remove(hProp)
            del hProp

        self.d_ptr.m_propertyToH.remove(property)

        self.d_ptr.m_values.remove(property)

class QtRectFPropertyManagerPrivate():
    class Data():
        val = QRectF(0, 0, 0, 0)
        constraint = QRectF(0, 0, 0, 0)
        decimals = 2

    def __init__(self):
        self.q_ptr = None
        self.m_values = QMap()
        self.m_propertyToX = QMap()
        self.m_propertyToY = QMap()
        self.m_propertyToW = QMap()
        self.m_propertyToH = QMap()
        self.m_xToProperty = QMap()
        self.m_yToProperty = QMap()
        self.m_wToProperty = QMap()
        self.m_hToProperty = QMap()
        self.m_doublePropertyManager = None

    def slotDoubleChanged(self, property, value):
        prop = self.m_xToProperty.get(property, 0)
        if prop:
            r = QRectF(self.m_values[prop].val)
            r.moveLeft(value)
            self.q_ptr.setValue(prop, r)
        else:
            prop = self.m_yToProperty.get(property, 0)
            if prop:
                r = QRectF(self.m_values[prop].val)
                r.moveTop(value)
                self.q_ptr.setValue(prop, r)
            else:
                prop = self.m_wToProperty.get(property, 0)
                if prop:
                    data = self.m_values[prop]
                    r = QRectF(data.val)
                    r.setWidth(value)
                    if (not data.constraint.isNull() and data.constraint.x() + data.constraint.width() < r.x() + r.width()):
                        r.moveLeft(data.constraint.left() + data.constraint.width() - r.width())
                    self.q_ptr.setValue(prop, r)
                else:
                    prop = self.m_hToProperty.get(property, 0)
                    if prop:
                        data = self.m_values[prop]
                        r = QRectF(data.val)
                        r.setHeight(value)
                        if (not data.constraint.isNull() and data.constraint.y() + data.constraint.height() < r.y() + r.height()):
                            r.moveTop(data.constraint.top() + data.constraint.height() - r.height())

                        self.q_ptr.setValue(prop, r)

    def slotPropertyDestroyed(self, property):
        pointProp = self.m_xToProperty.get(property, 0)
        if pointProp:
            self.m_propertyToX[pointProp] = 0
            self.m_xToProperty.remove(property)
        else:
            pointProp = self.m_yToProperty.get(property, 0)
            if pointProp:
                self.m_propertyToY[pointProp] = 0
                self.m_yToProperty.remove(property)
            else:
                pointProp = self.m_wToProperty.get(property, 0)
                if pointProp:
                    self.m_propertyToW[pointProp] = 0
                    self.m_wToProperty.remove(property)
                else:
                    pointProp = self.m_hToProperty.get(property, 0)
                    if pointProp:
                        self.m_propertyToH[pointProp] = 0
                        self.m_hToProperty.remove(property)

    def setConstraint(self, property, constraint, val):
        isNull = constraint.isNull()
        if isNull:
            left   = INT_MIN
            right  = INT_MAX
            top    = INT_MIN
            bottom = INT_MAX
            width  = INT_MAX
            height = INT_MAX
        else:
            left   = constraint.left()
            right  = constraint.left() + constraint.width()
            top    = constraint.top()
            bottom = constraint.top() + constraint.height()
            width  = constraint.width()
            height = constraint.height()

        self.m_doublePropertyManager.setRange(self.m_propertyToX[property], left, right)
        self.m_doublePropertyManager.setRange(self.m_propertyToY[property], top, bottom)
        self.m_doublePropertyManager.setRange(self.m_propertyToW[property], 0, width)
        self.m_doublePropertyManager.setRange(self.m_propertyToH[property], 0, height)

        self.m_doublePropertyManager.setValue(self.m_propertyToX[property], val.x())
        self.m_doublePropertyManager.setValue(self.m_propertyToY[property], val.y())
        self.m_doublePropertyManager.setValue(self.m_propertyToW[property], val.width())
        self.m_doublePropertyManager.setValue(self.m_propertyToH[property], val.height())

###
#    \class QtRectFPropertyManager
#
#    \brief The QtRectFPropertyManager provides and manages QRectF properties.
#
#    A rectangle property has nested \e x, \e y, \e width and \e height
#    subproperties. The top-level property's value can be retrieved
#    using the value() function, and set using the setValue() slot.
#
#    The subproperties are created by a QtDoublePropertyManager object. This
#    manager can be retrieved using the subDoublePropertyManager() function. In
#    order to provide editing widgets for the subproperties in a
#    property browser widget, this manager must be associated with an
#    editor factory.
#
#    A rectangle property also has a constraint rectangle which can be
#    retrieved using the constraint() function, and set using the
#    setConstraint() slot.
#
#    In addition, QtRectFPropertyManager provides the valueChanged() signal
#    which is emitted whenever a property created by this manager
#    changes, and the constraintChanged() signal which is emitted
#    whenever such a property changes its constraint rectangle.

#    \sa QtAbstractPropertyManager, QtDoublePropertyManager, QtRectPropertyManager
###
#
###
#    \fn void QtRectFPropertyManager.valueChanged(property, value)

#    This signal is emitted whenever a property created by this manager
#    changes its value, passing a pointer to the \a property and the new
#    \a value as parameters.

#    \sa setValue()
###
#
###
#    \fn void QtRectFPropertyManager.constraintChanged(property, constraint)

#    This signal is emitted whenever property changes its constraint
#    rectangle, passing a pointer to the \a property and the new \a
#    constraint rectangle as parameters.

#    \sa setConstraint()
###
#
###
#    \fn void QtRectFPropertyManager.decimalsChanged(property, prec)

#    This signal is emitted whenever a property created by this manager
#    changes its precision of value, passing a pointer to the
#    \a property and the new \a prec value

#    \sa setDecimals()
###
#
class QtRectFPropertyManager(QtAbstractPropertyManager):
    valueChangedSignal = pyqtSignal(QtProperty, QRectF)
    constraintChangedSignal = pyqtSignal(QtProperty, QRectF)
    decimalsChangedSignal = pyqtSignal(QtProperty, int)

    ###
    #    Creates a manager with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtRectFPropertyManager, self).__init__(parent)

        self.d_ptr = QtRectFPropertyManagerPrivate()
        self.d_ptr.q_ptr = self

        self.d_ptr.m_doublePropertyManager = QtDoublePropertyManager(self)
        self.d_ptr.m_doublePropertyManager.valueChangedSignal.connect(self.d_ptr.slotDoubleChanged)
        self.d_ptr.m_doublePropertyManager.propertyDestroyedSignal.connect(self.d_ptr.slotPropertyDestroyed)

    #
    ###
    #    Destroys this manager, and all the properties it has created.
    ###
    def __del__(self):
        self.clear()
        del self.d_ptr

    ###
    #    Returns the manager that creates the nested \e x, \e y, \e width
    #    and \e height subproperties.
    #
    #    In order to provide editing widgets for the mentioned
    #    subproperties in a property browser widget, this manager must be
    #    associated with an editor factory.

    #    \sa QtAbstractPropertyBrowser.setFactoryForManager()
    ###
    def subDoublePropertyManager(self):
        return self.d_ptr.m_doublePropertyManager

    #
    ###
    #    Returns the given \a property's value.

    #    If the given \a property is not managed by this manager, this:
    #    function returns an invalid rectangle.

    #    \sa setValue(), constraint()
    ###
    def value(self, property):
        return getValue(self.d_ptr.m_values, property,  QRectF())

    ###
    #    Returns the given \a property's precision, in decimals.

    #    \sa setDecimals()
    ###
    def decimals(self, property):
        return getData(self.d_ptr.m_values, DATA_DECIMALS, property, 0)

    ###
    #    Returns the given \a property's constraining rectangle. If returned value is null QRectF it means there is no constraint applied.

    #    \sa value(), setConstraint()
    ###
    def constraint(self, property):
        return getData(self.d_ptr.m_values, DATA_CONSTRAINT, property, QRect())

    ###
    #    \reimp
    ###
    def valueText(self, property):

        if not property in self.d_ptr.m_values.keys():
            return ''
        v = self.d_ptr.m_values[property].val
        dec = self.d_ptr.m_values[property].decimals
        fs = '[(%%.%df, %%.%df), %%.%df, %%.%df]'%(dec, dec, dec, dec)
        return self.tr(fs%(v.x(), v.y(), v.width(), v.height()))

    ###
    #    \fn void QtRectFPropertyManager.setValue(property, value)

    #    Sets the value of the given \a property to \a value. Nested
    #    properties are updated automatically.

    #    If the specified \a value is not inside the given \a property's:
    #    constraining rectangle, the value is adjusted accordingly to fit
    #    within the constraint.

    #    \sa value(), setConstraint(), valueChanged()
    ###
    def setValue(self, property, val):

        if not property in self.d_ptr.m_values.keys():
            return

        data = self.d_ptr.m_values[property]

        newRect = val.normalized()
        if (not data.constraint.isNull() and not data.constraint.contains(newRect)):
            r1 = data.constraint
            r2 = newRect
            newRect.setLeft(max(r1.left(), r2.left()))
            newRect.setRight(min(r1.right(), r2.right()))
            newRect.setTop(max(r1.top(), r2.top()))
            newRect.setBottom(min(r1.bottom(), r2.bottom()))
            if (newRect.width() < 0 or newRect.height() < 0):
                return

        if (data.val == newRect):
            return

        data.val = newRect

        self.d_ptr.m_values[property] = data
        self.d_ptr.m_doublePropertyManager.setValue(self.d_ptr.m_propertyToX[property], newRect.x())
        self.d_ptr.m_doublePropertyManager.setValue(self.d_ptr.m_propertyToY[property], newRect.y())
        self.d_ptr.m_doublePropertyManager.setValue(self.d_ptr.m_propertyToW[property], newRect.width())
        self.d_ptr.m_doublePropertyManager.setValue(self.d_ptr.m_propertyToH[property], newRect.height())

        self.propertyChangedSignal.emit(property)
        self.valueChangedSignal.emit(property, data.val)

    ###
    #    Sets the given \a property's constraining rectangle to \a
    #    constraint.

    #    When setting the constraint, the current value is adjusted if
    #    necessary (ensuring that the current rectangle value is inside the
    #    constraint). In order to reset the constraint pass a null QRectF value.

    #    \sa setValue(), constraint(), constraintChanged()
    ###
    def setConstraint(self, property, constraint):

        if not property in self.d_ptr.m_values.keys():
            return

        data = self.d_ptr.m_values[property]

        newConstraint = constraint.normalized()
        if (data.constraint == newConstraint):
            return

        oldVal = data.val

        data.constraint = newConstraint

        if (not data.constraint.isNull() and not data.constraint.contains(oldVal)):
            r1 = data.constraint
            r2 = data.val

            if (r2.width() > r1.width()):
                r2.setWidth(r1.width())
            if (r2.height() > r1.height()):
                r2.setHeight(r1.height())
            if (r2.left() < r1.left()):
                r2.moveLeft(r1.left())
            elif (r2.right() > r1.right()):
                r2.moveRight(r1.right())
            if (r2.top() < r1.top()):
                r2.moveTop(r1.top())
            elif (r2.bottom() > r1.bottom()):
                r2.moveBottom(r1.bottom())

            data.val = r2

        self.d_ptr.m_values[property] = data

        self.constraintChangedSignal.emit(property, data.constraint)

        self.d_ptr.setConstraint(property, data.constraint, data.val)

        if (data.val == oldVal):
            return

        self.propertyChangedSignal.emit(property)
        self.valueChangedSignal.emit(property, data.val)

    ###
    #    \fn void QtRectFPropertyManager.setDecimals(property, prec)

    #    Sets the precision of the given \a property to \a prec.

    #    The valid decimal range is 0-13. The default is 2.

    #    \sa decimals()
    ###
    def setDecimals(self, property, prec):

        if not property in self.d_ptr.m_values.keys():
            return

        data = self.d_ptr.m_values[property]

        if (prec > 13):
            prec = 13
        elif (prec < 0):
            prec = 0

        if (data.decimals == prec):
            return

        data.decimals = prec
        self.d_ptr.m_doublePropertyManager.setDecimals(self.d_ptr.m_propertyToX[property], prec)
        self.d_ptr.m_doublePropertyManager.setDecimals(self.d_ptr.m_propertyToY[property], prec)
        self.d_ptr.m_doublePropertyManager.setDecimals(self.d_ptr.m_propertyToW[property], prec)
        self.d_ptr.m_doublePropertyManager.setDecimals(self.d_ptr.m_propertyToH[property], prec)

        self.d_ptr.m_values[property] = data

        self.decimalsChangedSignal.emit(property, data.decimals)

    ###
    #    \reimp
    ###
    def initializeProperty(self, property):
        self.d_ptr.m_values[property] = QtRectFPropertyManagerPrivate.Data()

        xProp = self.d_ptr.m_doublePropertyManager.addProperty()
        xProp.setPropertyName(self.tr("X"))
        self.d_ptr.m_doublePropertyManager.setDecimals(xProp, self.decimals(property))
        self.d_ptr.m_doublePropertyManager.setValue(xProp, 0)
        self.d_ptr.m_propertyToX[property] = xProp
        self.d_ptr.m_xToProperty[xProp] = property
        property.addSubProperty(xProp)

        yProp = self.d_ptr.m_doublePropertyManager.addProperty()
        yProp.setPropertyName(self.tr("Y"))
        self.d_ptr.m_doublePropertyManager.setDecimals(yProp, self.decimals(property))
        self.d_ptr.m_doublePropertyManager.setValue(yProp, 0)
        self.d_ptr.m_propertyToY[property] = yProp
        self.d_ptr.m_yToProperty[yProp] = property
        property.addSubProperty(yProp)

        wProp = self.d_ptr.m_doublePropertyManager.addProperty()
        wProp.setPropertyName(self.tr("Width"))
        self.d_ptr.m_doublePropertyManager.setDecimals(wProp, self.decimals(property))
        self.d_ptr.m_doublePropertyManager.setValue(wProp, 0)
        self.d_ptr.m_doublePropertyManager.setMinimum(wProp, 0)
        self.d_ptr.m_propertyToW[property] = wProp
        self.d_ptr.m_wToProperty[wProp] = property
        property.addSubProperty(wProp)

        hProp = self.d_ptr.m_doublePropertyManager.addProperty()
        hProp.setPropertyName(self.tr("Height"))
        self.d_ptr.m_doublePropertyManager.setDecimals(hProp, self.decimals(property))
        self.d_ptr.m_doublePropertyManager.setValue(hProp, 0)
        self.d_ptr.m_doublePropertyManager.setMinimum(hProp, 0)
        self.d_ptr.m_propertyToH[property] = hProp
        self.d_ptr.m_hToProperty[hProp] = property
        property.addSubProperty(hProp)

    ###
    #    \reimp
    ###
    def uninitializeProperty(self, property):
        xProp = self.d_ptr.m_propertyToX[property]
        if (xProp):
            self.d_ptr.m_xToProperty.remove(xProp)
            del xProp

        self.d_ptr.m_propertyToX.remove(property)

        yProp = self.d_ptr.m_propertyToY[property]
        if (yProp):
            self.d_ptr.m_yToProperty.remove(yProp)
            del yProp

        self.d_ptr.m_propertyToY.remove(property)

        wProp = self.d_ptr.m_propertyToW[property]
        if (wProp):
            self.d_ptr.m_wToProperty.remove(wProp)
            del wProp

        self.d_ptr.m_propertyToW.remove(property)

        hProp = self.d_ptr.m_propertyToH[property]
        if (hProp):
            self.d_ptr.m_hToProperty.remove(hProp)
            del hProp

        self.d_ptr.m_propertyToH.remove(property)

        self.d_ptr.m_values.remove(property)

class QtEnumPropertyManagerPrivate():
    class Data():
        val = -1
        enumNames = QList()
        enumIcons = QMap()

    def __init__(self):
        self.q_ptr = None
        self.m_values = QMap()
        self.Data = QtEnumPropertyManagerPrivate.Data()

###
#    \class QtEnumPropertyManager
#
#    \brief The QtEnumPropertyManager provides and manages enum properties.
#
#    Each enum property has an associated list of enum names which can
#    be retrieved using the enumNames() function, and set using the
#    corresponding setEnumNames() function. An enum property's value is
#    represented by an index in this list, and can be retrieved and set
#    using the value() and setValue() slots respectively.
#
#    Each enum value can also have an associated icon. The mapping from
#    values to icons can be set using the setEnumIcons() function and
#    queried with the enumIcons() function.
#
#    In addition, QtEnumPropertyManager provides the valueChanged() signal
#    which is emitted whenever a property created by this manager
#    changes. The enumNamesChanged() or enumIconsChanged() signal is emitted
#    whenever the list of enum names or icons is altered.

#    \sa QtAbstractPropertyManager, QtEnumEditorFactory
###
#
###
#    \fn void QtEnumPropertyManager.valueChanged(property, value)

#    This signal is emitted whenever a property created by this manager
#    changes its value, passing a pointer to the \a property and the new
#    \a value as parameters.

#    \sa setValue()
###
#
###
#    \fn void QtEnumPropertyManager.enumNamesChanged(property, names)

#    This signal is emitted whenever a property created by this manager
#    changes its enum names, passing a pointer to the \a property and
#    the new \a names as parameters.

#    \sa setEnumNames()
###
#
###
#    \fn void QtEnumPropertyManager.enumIconsChanged(property, icons)

#    This signal is emitted whenever a property created by this manager
#    changes its enum icons, passing a pointer to the \a property and
#    the new mapping of values to \a icons as parameters.

#    \sa setEnumIcons()
###
#
class QtEnumPropertyManager(QtAbstractPropertyManager):
    valueChangedSignal = pyqtSignal(QtProperty, int)
    enumNamesChangedSignal = pyqtSignal(QtProperty, QList)
    enumIconsChangedSignal = pyqtSignal(QtProperty, QMap)

    ###
    #    Creates a manager with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtEnumPropertyManager, self).__init__(parent)

        self.d_ptr = QtEnumPropertyManagerPrivate()
        self.d_ptr.q_ptr = self

    ###
    #    Destroys this manager, and all the properties it has created.
    ###
    def __del__(self):
        self.clear()
        del self.d_ptr

    ###
    #    Returns the given \a property's value which is an index in the
    #    list returned by enumNames()

    #    If the given property is not managed by this manager, this:
    #    function returns -1.

    #    \sa enumNames(), setValue()
    ###
    def value(self, property):
        return getValue(self.d_ptr.m_values, property, -1)

    ###
    #    Returns the given \a property's list of enum names.

    #    \sa value(), setEnumNames()
    ###
    def enumNames(self, property):
        return getData(self.d_ptr.m_values, DATA_ENUMNAMES, property, [])

    ###
    #    Returns the given \a property's map of enum values to their icons.

    #    \sa value(), setEnumIcons()
    ###
    def enumIcons(self, property):
        return getData(self.d_ptr.m_values, DATA_ENUMICONS, property, {})

    ###
    #    \reimp
    ###
    def valueText(self, property):
        if not property in self.d_ptr.m_values.keys():
            return ''

        data = self.d_ptr.m_values[property]

        v = data.val
        if (v >= 0 and v < len(data.enumNames)):
            return data.enumNames[v]
        return ''

    ###
    #    \reimp
    ###
    def valueIcon(self, property):
        if not property in self.d_ptr.m_values.keys():
            return QIcon()

        data = self.d_ptr.m_values[property]

        v = data.val
        return data.enumIcons.value(v)

    ###
    #    \fn void QtEnumPropertyManager.setValue(property, value)

    #    Sets the value of the given  \a property to \a value.

    #    The specified \a value must be less than the size of the given \a
    #    property's enumNames() list, and larger than (or equal to) 0.

    #    \sa value(), valueChanged()
    ###
    def setValue(self, property, val):
        if not property in self.d_ptr.m_values.keys():
            return

        data = self.d_ptr.m_values[property]

        if (val >= len(data.enumNames)):
            return

        if (val < 0 and len(data.enumNames)>0):
            return

        if (val < 0):
            val = -1

        if (data.val == val):
            return

        data.val = val

        self.d_ptr.m_values[property] = data

        self.propertyChangedSignal.emit(property)
        self.valueChangedSignal.emit(property, data.val)

    ###
    #    Sets the given \a property's list of enum names to \a
    #    enumNames. The \a property's current value is reset to 0
    #    indicating the first item of the list.

    #    If the specified \a enumNames list is empty, the \a property's:
    #    current value is set to -1.

    #    \sa enumNames(), enumNamesChanged()
    ###
    def setEnumNames(self, property, enumNames):

        if not property in self.d_ptr.m_values.keys():
            return

        data = self.d_ptr.m_values[property]

        if (data.enumNames == enumNames):
            return

        data.enumNames = enumNames

        data.val = -1

        if (len(enumNames) > 0):
            data.val = 0

        self.d_ptr.m_values[property] = data

        self.enumNamesChangedSignal.emit(property, data.enumNames)

        self.propertyChangedSignal.emit(property)
        self.valueChangedSignal.emit(property, data.val)

    ###
    #    Sets the given \a property's map of enum values to their icons to \a
    #    enumIcons.
    #
    #    Each enum value can have associated icon. This association is represented with passed \a enumIcons map.

    #    \sa enumNames(), enumNamesChanged()
    ###
    def setEnumIcons(self, property, enumIcons):

        if not property in self.d_ptr.m_values.keys():
            return

        self.d_ptr.m_values[property].enumIcons = enumIcons

        self.enumIconsChangedSignal.emit(property, self.d_ptr.m_values[property].enumIcons)

        self.propertyChangedSignal.emit(property)

    ###
    #    \reimp
    ###
    def initializeProperty(self, property):
        self.d_ptr.m_values[property] = QtEnumPropertyManagerPrivate.Data()

    ###
    #    \reimp
    ###
    def uninitializeProperty(self, property):
        self.d_ptr.m_values.remove(property)

class QtFlagPropertyManagerPrivate():
    class Data():
        val = -1
        flagNames = QList()

    def __init__(self):
        self.q_ptr = None

        self.m_values = QMap()
        self.m_propertyToFlags = QMapList()
        self.m_flagToProperty = QMap()
        self.Data = QtFlagPropertyManagerPrivate.Data()

    def slotBoolChanged(self, property, value):
        prop = self.m_flagToProperty.get(property, 0)
        if (prop == 0):
            return

        level = 0
        for p in self.m_propertyToFlags[prop]:
            if (p == property):
                v = copy.copy(self.m_values[prop].val)
                if (value):
                    v |= (1 << level)
                else:
                    v &= ~(1 << level)

                self.q_ptr.setValue(prop, v)
                return

            level += 1

    def slotPropertyDestroyed(self, property):
        flagProperty = self.m_flagToProperty.get(property, 0)
        if (flagProperty == 0):
            return

        self.m_propertyToFlags[flagProperty].replace(self.m_propertyToFlags[flagProperty].indexOf(property), 0)
        self.m_flagToProperty.remove(property)

###
#    \class QtFlagPropertyManager
#
#    \brief The QtFlagPropertyManager provides and manages flag properties.
#
#    Each flag property has an associated list of flag names which can
#    be retrieved using the flagNames() function, and set using the
#    corresponding setFlagNames() function.

#    The flag manager provides properties with nested boolean
#    subproperties representing each flag, i.e. a flag property's value
#    is the binary combination of the subproperties' values. A
#    property's value can be retrieved and set using the value() and
#    setValue() slots respectively. The combination of flags is represented
#    by single int value - that's why it's possible to store up to
#    32 independent flags in one flag property.

#    The subproperties are created by a QtBoolPropertyManager object. This
#    manager can be retrieved using the subBoolPropertyManager() function. In
#    order to provide editing widgets for the subproperties in a
#    property browser widget, this manager must be associated with an
#    editor factory.
#
#    In addition, QtFlagPropertyManager provides the valueChanged() signal
#    which is emitted whenever a property created by this manager
#    changes, and the flagNamesChanged() signal which is emitted
#    whenever the list of flag names is altered.

#    \sa QtAbstractPropertyManager, QtBoolPropertyManager
###
#
###
#    \fn void QtFlagPropertyManager.valueChanged(property, value)

#    This signal is emitted whenever a property created by this manager
#    changes its value, passing a pointer to the \a  property and the new
#    \a value as parameters.

#    \sa setValue()
###
#
###
#    \fn void QtFlagPropertyManager.flagNamesChanged(property, names)

#    This signal is emitted whenever a property created by this manager
#    changes its flag names, passing a pointer to the \a property and the
#    new \a names as parameters.

#    \sa setFlagNames()
###
#
class QtFlagPropertyManager(QtAbstractPropertyManager):
    valueChangedSignal = pyqtSignal(QtProperty, int)
    flagNamesChangedSignal = pyqtSignal(QtProperty, QList)

    ###
    #    Creates a manager with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtFlagPropertyManager, self).__init__(parent)

        self.d_ptr = QtFlagPropertyManagerPrivate()
        self.d_ptr.q_ptr = self

        self.d_ptr.m_boolPropertyManager = QtBoolPropertyManager(self)
        self.d_ptr.m_boolPropertyManager.valueChangedSignal.connect(self.d_ptr.slotBoolChanged)
        self.d_ptr.m_boolPropertyManager.propertyDestroyedSignal.connect(self.d_ptr.slotPropertyDestroyed)

    #
    ###
    #    Destroys this manager, and all the properties it has created.
    ###
    def __del__(self):
        self.clear()
        del self.d_ptr

    ###
    #    Returns the manager that produces the nested boolean subproperties
    #    representing each flag.
    #
    #    In order to provide editing widgets for the subproperties in a
    #    property browser widget, this manager must be associated with an
    #    editor factory.

    #    \sa QtAbstractPropertyBrowser.setFactoryForManager()
    ###
    def subBoolPropertyManager(self):
        return self.d_ptr.m_boolPropertyManager

    #
    ###
    #    Returns the given \a property's value.

    #    If the given property is not managed by this manager, this:
    #    function returns 0.

    #    \sa flagNames(), setValue()
    ###
    def value(self, property):
        return getValue(self.d_ptr.m_values, property, 0)

    ###
    #    Returns the given \a property's list of flag names.

    #    \sa value(), setFlagNames()
    ###
    def flagNames(self, property):
        return getData(self.d_ptr.m_values, DATA_FLAGNAMES, property, [])

    ###
    #    \reimp
    ###
    def valueText(self, property):

        if not property in self.d_ptr.m_values.keys():
            return ''

        data = self.d_ptr.m_values[property]

        s = ''
        level = 0
        bar = '|'
        for it in data.flagNames:
            if (data.val & (1 << level)):
                if s!='':
                    s += bar
                s += it

            level += 1

        return s

    ###
    #    \fn void QtFlagPropertyManager.setValue(property, value)

    #    Sets the value of the given \a property to \a value. Nested
    #    properties are updated automatically.

    #    The specified \a value must be less than the binary combination of
    #    The property's flagNames() list size (i.e. less than 2\sup n,
    #    where \c n is the size of the list) and larger than (or equal to)
    #    0.

    #    \sa value(), valueChanged()
    ###
    def setValue(self, property, val):

        if not property in self.d_ptr.m_values.keys():
            return

        data = self.d_ptr.m_values[property]

        if (data.val == val):
            return

        if (val > (1 << len(data.flagNames)) - 1):
            return

        if (val < 0):
            return

        data.val = val

        self.d_ptr.m_values[property] = data
        level = 0
        for prop in self.d_ptr.m_propertyToFlags[property]:
            if (prop):
                self.d_ptr.m_boolPropertyManager.setValue(prop, val & (1 << level))
            level += 1

        self.propertyChangedSignal.emit(property)
        self.valueChangedSignal.emit(property, data.val)

    ###
    #    Sets the given \a property's list of flag names to \a flagNames. The
    #    property's current value is reset to 0 indicating the first item
    #    of the list.

    #    \sa flagNames(), flagNamesChanged()
    ###
    def setFlagNames(self, property, flagNames):

        if not property in self.d_ptr.m_values.keys():
            return

        data = self.d_ptr.m_values[property]

        if (data.flagNames == flagNames):
            return

        data.flagNames = flagNames
        data.val = 0

        self.d_ptr.m_values[property] = data

        for prop in self.d_ptr.m_propertyToFlags[property]:
            if (prop):
                del prop

        self.d_ptr.m_propertyToFlags[property].clear()

        for flagName in flagNames:
            prop = self.d_ptr.m_boolPropertyManager.addProperty()
            prop.setPropertyName(flagName)
            property.addSubProperty(prop)
            self.d_ptr.m_propertyToFlags[property].append(prop)
            self.d_ptr.m_flagToProperty[prop] = property

        self.flagNamesChangedSignal.emit(property, data.flagNames)

        self.propertyChangedSignal.emit(property)
        self.valueChangedSignal.emit(property, data.val)

    ###
    #    \reimp
    ###
    def initializeProperty(self, property):
        self.d_ptr.m_values[property] = QtFlagPropertyManagerPrivate.Data()

        self.d_ptr.m_propertyToFlags[property] = QList()

    ###
    #    \reimp
    ###
    def uninitializeProperty(self, property):
        for prop in self.d_ptr.m_propertyToFlags[property]:
            if (prop):
                del prop

        self.d_ptr.m_propertyToFlags.remove(property)
        self.d_ptr.m_values.remove(property)

class QtSizePolicyPropertyManagerPrivate():
    def __init__(self):
        self.q_ptr = None

        self.m_values = QMap()
        self.m_propertyToHPolicy = QMap()
        self.m_propertyToVPolicy = QMap()
        self.m_propertyToHStretch = QMap()
        self.m_propertyToVStretch = QMap()
        self.m_hPolicyToProperty = QMap()
        self.m_vPolicyToProperty = QMap()
        self.m_hStretchToProperty = QMap()
        self.m_vStretchToProperty = QMap()

        self.m_intPropertyManager = None
        self.m_enumPropertyManager = None

    def slotIntChanged(self, property, value):
        prop = self.m_hStretchToProperty.get(property, 0)
        if prop:
            sp = QSizePolicy(self.m_values[prop])
            sp.setHorizontalStretch(value)
            self.q_ptr.setValue(prop, sp)
        else:
            prop = self.m_vStretchToProperty.get(property, 0)
            if prop:
                sp = QSizePolicy(self.m_values[prop])
                sp.setVerticalStretch(value)
                self.q_ptr.setValue(prop, sp)

    def slotEnumChanged(self, property, value):
        prop = self.m_hPolicyToProperty.get(property, 0)
        if prop:
            sp = QSizePolicy(self.m_values[prop])
            sp.setHorizontalPolicy(metaEnumProvider().indexToSizePolicy(value))
            self.q_ptr.setValue(prop, sp)
        else:
            prop = self.m_vPolicyToProperty.get(property, 0)
            if prop:
                sp = QSizePolicy(self.m_values[prop])
                sp.setVerticalPolicy(metaEnumProvider().indexToSizePolicy(value))
                self.q_ptr.setValue(prop, sp)

    def slotPropertyDestroyed(self, property):
        pointProp = self.m_hStretchToProperty.get(property, 0)

        if pointProp:
            self.m_propertyToHStretch[pointProp] = 0
            self.m_hStretchToProperty.remove(property)
        else:
            pointProp = self.m_vStretchToProperty.get(property, 0)
            if pointProp:
                self.m_propertyToVStretch[pointProp] = 0
                self.m_vStretchToProperty.remove(property)
            else:
                pointProp = self.m_hPolicyToProperty.get(property, 0)
                if pointProp:
                    self.m_propertyToHPolicy[pointProp] = 0
                    self.m_hPolicyToProperty.remove(property)
                else:
                    pointProp = self.m_vPolicyToProperty.get(property, 0)
                    if pointProp:
                        self.m_propertyToVPolicy[pointProp] = 0
                        self.m_vPolicyToProperty.remove(property)

###
#    \class QtSizePolicyPropertyManager
#
#    \brief The QtSizePolicyPropertyManager provides and manages QSizePolicy properties.
#
#    A size policy property has nested \e horizontalPolicy, \e
#    verticalPolicy, \e horizontalStretch and \e verticalStretch
#    subproperties. The top-level property's value can be retrieved
#    using the value() function, and set using the setValue() slot.

#    The subproperties are created by QtIntPropertyManager and QtEnumPropertyManager
#    objects. These managers can be retrieved using the subIntPropertyManager()
#    and subEnumPropertyManager() functions respectively. In order to provide
#    editing widgets for the subproperties in a property browser widget,
#    these managers must be associated with editor factories.
#
#    In addition, QtSizePolicyPropertyManager provides the valueChanged()
#    signal which is emitted whenever a property created by this
#    manager changes.

#    \sa QtAbstractPropertyManager, QtIntPropertyManager, QtEnumPropertyManager
###
#
###
#    \fn void QtSizePolicyPropertyManager.valueChanged(property, value)

#    This signal is emitted whenever a property created by this manager
#    changes its value, passing a pointer to the \a property and the
#    new \a value as parameters.

#    \sa setValue()
###
#
class QtSizePolicyPropertyManager(QtAbstractPropertyManager):
    valueChangedSignal = pyqtSignal(QtProperty, QSizePolicy)

    ###
    #    Creates a manager with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtSizePolicyPropertyManager, self).__init__(parent)

        self.d_ptr = QtSizePolicyPropertyManagerPrivate()
        self.d_ptr.q_ptr = self

        self.d_ptr.m_intPropertyManager = QtIntPropertyManager(self)
        self.d_ptr.m_intPropertyManager.valueChangedSignal.connect(self.d_ptr.slotIntChanged)
        self.d_ptr.m_enumPropertyManager = QtEnumPropertyManager(self)
        self.d_ptr.m_enumPropertyManager.valueChangedSignal.connect(self.d_ptr.slotEnumChanged)

        self.d_ptr.m_intPropertyManager.propertyDestroyedSignal.connect(self.d_ptr.slotPropertyDestroyed)
        self.d_ptr.m_enumPropertyManager.propertyDestroyedSignal.connect(self.d_ptr.slotPropertyDestroyed)

    #
    ###
    #    Destroys this manager, and all the properties it has created.
    ###
    def __del__(self):
        self.clear()
        del self.d_ptr

    ###
    #    Returns the manager that creates the nested \e horizontalStretch
    #    and \e verticalStretch subproperties.
    #
    #    In order to provide editing widgets for the mentioned subproperties
    #    in a property browser widget, this manager must be associated with
    #    an editor factory.

    #    \sa QtAbstractPropertyBrowser.setFactoryForManager()
    ###
    def subIntPropertyManager(self):
        return self.d_ptr.m_intPropertyManager

    ###
    #    Returns the manager that creates the nested \e horizontalPolicy
    #    and \e verticalPolicy subproperties.
    #
    #    In order to provide editing widgets for the mentioned subproperties
    #    in a property browser widget, this manager must be associated with
    #    an editor factory.

    #    \sa QtAbstractPropertyBrowser.setFactoryForManager()
    ###
    def subEnumPropertyManager(self):
        return self.d_ptr.m_enumPropertyManager

    ###
    #    Returns the given \a property's value.

    #    If the given property is not managed by this manager, this:
    #    function returns the default size policy.

    #    \sa setValue()
    ###
    def value(self, property):
        return self.d_ptr.m_values.get(property, QSizePolicy())

    ###
    #    \reimp
    ###
    def valueText(self, property):
        if not property in self.d_ptr.m_values.keys():
            return ''

        sp = self.d_ptr.m_values[property]
        mep = metaEnumProvider()
        hIndex = mep.sizePolicyToIndex(sp.horizontalPolicy())
        vIndex = mep.sizePolicyToIndex(sp.verticalPolicy())
        #! Unknown size policy on reading invalid uic3 files
        if hIndex != -1:
            hPolicy = mep.policyEnumValueNames()[sp.horizontalPolicy()]
        else:
            hPolicy = self.tr("<Invalid>")
        if vIndex != -1:
            vPolicy = mep.policyEnumValueNames()[sp.verticalPolicy()]
        else:
            vPolicy = self.tr("<Invalid>")
        plNames = mep.policyEnumValueNames()
        hPolicy = plNames.get(sp.horizontalPolicy(), 0)
        vPolicy = plNames.get(sp.verticalPolicy(), 0)
        s = self.tr("[%s, %s, %d, %d]"%(hPolicy, vPolicy,sp.horizontalStretch(),sp.verticalStretch()))
        return s

    ###
    #    \fn void QtSizePolicyPropertyManager.setValue(property, value)

    #    Sets the value of the given \a property to \a value. Nested
    #    properties are updated automatically.

    #    \sa value(), valueChanged()
    ###
    def setValue(self, property, val):

        if not property in self.d_ptr.m_values.keys():
            return

        if (self.d_ptr.m_values[property] == val):
            return

        self.d_ptr.m_values[property] = val

        self.d_ptr.m_enumPropertyManager.setValue(self.d_ptr.m_propertyToHPolicy[property],
                    metaEnumProvider().sizePolicyToIndex(val.horizontalPolicy()))
        self.d_ptr.m_enumPropertyManager.setValue(self.d_ptr.m_propertyToVPolicy[property],
                    metaEnumProvider().sizePolicyToIndex(val.verticalPolicy()))
        self.d_ptr.m_intPropertyManager.setValue(self.d_ptr.m_propertyToHStretch[property],
                    val.horizontalStretch())
        self.d_ptr.m_intPropertyManager.setValue(self.d_ptr.m_propertyToVStretch[property],
                    val.verticalStretch())

        self.propertyChangedSignal.emit(property)
        self.valueChangedSignal.emit(property, val)

    ###
    #    \reimp
    ###
    def initializeProperty(self, property):
        val = QSizePolicy()
        self.d_ptr.m_values[property] = val

        hPolicyProp = self.d_ptr.m_enumPropertyManager.addProperty()
        hPolicyProp.setPropertyName(self.tr("Horizontal Policy"))
        self.d_ptr.m_enumPropertyManager.setEnumNames(hPolicyProp, metaEnumProvider().policyEnumNames())
        self.d_ptr.m_enumPropertyManager.setValue(hPolicyProp,
                    metaEnumProvider().sizePolicyToIndex(val.horizontalPolicy()))
        self.d_ptr.m_propertyToHPolicy[property] = hPolicyProp
        self.d_ptr.m_hPolicyToProperty[hPolicyProp] = property
        property.addSubProperty(hPolicyProp)

        vPolicyProp = self.d_ptr.m_enumPropertyManager.addProperty()
        vPolicyProp.setPropertyName(self.tr("Vertical Policy"))
        self.d_ptr.m_enumPropertyManager.setEnumNames(vPolicyProp, metaEnumProvider().policyEnumNames())
        self.d_ptr.m_enumPropertyManager.setValue(vPolicyProp,
                    metaEnumProvider().sizePolicyToIndex(val.verticalPolicy()))
        self.d_ptr.m_propertyToVPolicy[property] = vPolicyProp
        self.d_ptr.m_vPolicyToProperty[vPolicyProp] = property
        property.addSubProperty(vPolicyProp)

        hStretchProp = self.d_ptr.m_intPropertyManager.addProperty()
        hStretchProp.setPropertyName(self.tr("Horizontal Stretch"))
        self.d_ptr.m_intPropertyManager.setValue(hStretchProp, val.horizontalStretch())
        self.d_ptr.m_intPropertyManager.setRange(hStretchProp, 0, 0xff)
        self.d_ptr.m_propertyToHStretch[property] = hStretchProp
        self.d_ptr.m_hStretchToProperty[hStretchProp] = property
        property.addSubProperty(hStretchProp)

        vStretchProp = self.d_ptr.m_intPropertyManager.addProperty()
        vStretchProp.setPropertyName(self.tr("Vertical Stretch"))
        self.d_ptr.m_intPropertyManager.setValue(vStretchProp, val.verticalStretch())
        self.d_ptr.m_intPropertyManager.setRange(vStretchProp, 0, 0xff)
        self.d_ptr.m_propertyToVStretch[property] = vStretchProp
        self.d_ptr.m_vStretchToProperty[vStretchProp] = property
        property.addSubProperty(vStretchProp)

    ###
    #    \reimp
    ###
    def uninitializeProperty(self, property):
        hPolicyProp = self.d_ptr.m_propertyToHPolicy[property]
        if (hPolicyProp):
            self.d_ptr.m_hPolicyToProperty.remove(hPolicyProp)
            del hPolicyProp

        self.d_ptr.m_propertyToHPolicy.remove(property)

        vPolicyProp = self.d_ptr.m_propertyToVPolicy[property]
        if (vPolicyProp):
            self.d_ptr.m_vPolicyToProperty.remove(vPolicyProp)
            del vPolicyProp

        self.d_ptr.m_propertyToVPolicy.remove(property)

        hStretchProp = self.d_ptr.m_propertyToHStretch[property]
        if (hStretchProp):
            self.d_ptr.m_hStretchToProperty.remove(hStretchProp)
            del hStretchProp

        self.d_ptr.m_propertyToHStretch.remove(property)

        vStretchProp = self.d_ptr.m_propertyToVStretch[property]
        if (vStretchProp):
            self.d_ptr.m_vStretchToProperty.remove(vStretchProp)
            del vStretchProp

        self.d_ptr.m_propertyToVStretch.remove(property)

        self.d_ptr.m_values.remove(property)

g_fontDatabaseVar = None
def fontDatabase():
    global g_fontDatabaseVar
    if not g_fontDatabaseVar:
        g_fontDatabaseVar = QFontDatabase()
    return g_fontDatabaseVar

class QtFontPropertyManagerPrivate():
    def __init__(self):
        self.q_ptr = None
        self.m_familyNames = QList()
        self.m_values = QMap()
        self.m_propertyToFamily = QMap()
        self.m_propertyToPointSize = QMap()
        self.m_propertyToBold = QMap()
        self.m_propertyToItalic = QMap()
        self.m_propertyToUnderline = QMap()
        self.m_propertyToStrikeOut = QMap()
        self.m_propertyToKerning = QMap()
        self.m_familyToProperty = QMap()
        self.m_pointSizeToProperty = QMap()
        self.m_boldToProperty = QMap()
        self.m_italicToProperty = QMap()
        self.m_underlineToProperty = QMap()
        self.m_strikeOutToProperty = QMap()
        self.m_kerningToProperty = QMap()
        self.m_settingValue = False
        self.m_fontDatabaseChangeTimer = None

        self.m_intPropertyManager = None
        self.m_enumPropertyManager = None
        self.m_boolPropertyManager = None

    def slotIntChanged(self, property, value):
        if (self.m_settingValue):
            return
        prop = self.m_pointSizeToProperty.get(property, 0)
        if prop:
            f = QFont(self.m_values[prop])
            f.setPointSize(value)
            self.q_ptr.setValue(prop, f)

    def slotEnumChanged(self, property, value):
        if (self.m_settingValue):
            return
        prop = self.m_familyToProperty.get(property, 0)
        if prop:
            f = QFont(self.m_values[prop])
            f.setFamily(self.m_familyNames[value])
            self.q_ptr.setValue(prop, f)

    def slotBoolChanged(self, property, value):
        if (self.m_settingValue):
            return
        prop = self.m_boldToProperty.get(property, 0)
        if prop:
            f = QFont(self.m_values[prop])
            f.setBold(value)
            self.q_ptr.setValue(prop, f)
        else:
            prop = self.m_italicToProperty.get(property, 0)
            if prop:
                f = QFont(self.m_values[prop])
                f.setItalic(value)
                self.q_ptr.setValue(prop, f)
            else:
                prop = self.m_underlineToProperty.get(property, 0)
                if prop:
                    f = QFont(self.m_values[prop])
                    f.setUnderline(value)
                    self.q_ptr.setValue(prop, f)
                else:
                    prop = self.m_strikeOutToProperty.get(property, 0)
                    if prop:
                        f = QFont(self.m_values[prop])
                        f.setStrikeOut(value)
                        self.q_ptr.setValue(prop, f)
                    else:
                        prop = self.m_kerningToProperty.get(property, 0)
                        if prop:
                            f = QFont(self.m_values[prop])
                            f.setKerning(value)
                            self.q_ptr.setValue(prop, f)

    def slotPropertyDestroyed(self, property):
        pointProp = self.m_pointSizeToProperty.get(property, 0)
        if pointProp:
            self.m_propertyToPointSize[pointProp] = 0
            self.m_pointSizeToProperty.remove(property)
        else:
            pointProp = self.m_familyToProperty.get(property, 0)
            if pointProp:
                self.m_propertyToFamily[pointProp] = 0
                self.m_familyToProperty.remove(property)
            else:
                pointProp = self.m_boldToProperty.get(property, 0)
                if pointProp:
                    self.m_propertyToBold[pointProp] = 0
                    self.m_boldToProperty.remove(property)
                else:
                    pointProp = self.m_italicToProperty.get(property, 0)
                    if pointProp:
                        self.m_propertyToItalic[pointProp] = 0
                        self.m_italicToProperty.remove(property)
                    else:
                        pointProp = self.m_underlineToProperty.get(property, 0)
                        if pointProp:
                            self.m_propertyToUnderline[pointProp] = 0
                            self.m_underlineToProperty.remove(property)
                        else:
                            pointProp = self.m_strikeOutToProperty.get(property, 0)
                            if pointProp:
                                self.m_propertyToStrikeOut[pointProp] = 0
                                self.m_strikeOutToProperty.remove(property)
                            else:
                                pointProp = self.m_kerningToProperty.get(property, 0)
                                if pointProp:
                                    self.m_propertyToKerning[pointProp] = 0
                                    self.m_kerningToProperty.remove(property)

    def slotFontDatabaseChanged(self):
        if (not  self.m_fontDatabaseChangeTimer):
            self.m_fontDatabaseChangeTimer = QTimer(self.q_ptr)
            self.m_fontDatabaseChangeTimer.setInterval(0)
            self.m_fontDatabaseChangeTimer.setSingleShot(True)
            self.m_fontDatabaseChangeTimer.timeout.connect(self.q_ptr.slotFontDatabaseDelayedChange)

        if (not  self.m_fontDatabaseChangeTimer.isActive()):
            self.m_fontDatabaseChangeTimer.start()

    def slotFontDatabaseDelayedChange(self):
        # rescan available font names
        oldFamilies = self.m_familyNames
        self.m_familyNames = fontDatabase().families()

        # Adapt all existing properties
        if len(self.m_propertyToFamily) > 0:
            for familyProp in self.m_propertyToFamily:
                oldIdx = self.m_enumPropertyManager[familyProp]
                newIdx = self.m_familyNames.indexOf(oldFamilies[oldIdx])
                if (newIdx < 0):
                    newIdx = 0
                self.m_enumPropertyManager.setEnumNames(familyProp, self.m_familyNames)
                self.m_enumPropertyManager.setValue(familyProp, newIdx)

###
#    \class QtFontPropertyManager
#
#    \brief The QtFontPropertyManager provides and manages QFont properties.
#
#    A font property has nested \e family, \e pointSize, \e bold, \e
#    italic, \e underline, \e strikeOut and \e kerning subproperties. The top-level
#    property's value can be retrieved using the value() function, and
#    set using the setValue() slot.

#    The subproperties are created by QtIntPropertyManager, QtEnumPropertyManager and
#    QtBoolPropertyManager objects. These managers can be retrieved using the
#    corresponding subIntPropertyManager(), subEnumPropertyManager() and
#    subBoolPropertyManager() functions. In order to provide editing widgets
#    for the subproperties in a property browser widget, these managers
#    must be associated with editor factories.
#
#    In addition, QtFontPropertyManager provides the valueChanged() signal
#    which is emitted whenever a property created by this manager
#    changes.

#    \sa QtAbstractPropertyManager, QtEnumPropertyManager, QtIntPropertyManager, QtBoolPropertyManager
###
#
###
#    \fn void QtFontPropertyManager.valueChanged(property, value)

#    This signal is emitted whenever a property created by this manager
#    changes its value, passing a pointer to the \a property and the
#    new \a value as parameters.

#    \sa setValue()
###
#
class QtFontPropertyManager(QtAbstractPropertyManager):
    valueChangedSignal = pyqtSignal(QtProperty, QFont)

    ###
    #    Creates a manager with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtFontPropertyManager, self).__init__(parent)

        self.d_ptr = QtFontPropertyManagerPrivate()
        self.d_ptr.q_ptr = self

        QCoreApplication.instance().fontDatabaseChanged.connect(self.d_ptr.slotFontDatabaseChanged)

        self.d_ptr.m_intPropertyManager = QtIntPropertyManager(self)
        self.d_ptr.m_intPropertyManager.valueChangedSignal.connect(self.d_ptr.slotIntChanged)
        self.d_ptr.m_enumPropertyManager = QtEnumPropertyManager(self)
        self.d_ptr.m_enumPropertyManager.valueChangedSignal.connect(self.d_ptr.slotEnumChanged)
        self.d_ptr.m_boolPropertyManager = QtBoolPropertyManager(self)
        self.d_ptr.m_boolPropertyManager.valueChangedSignal.connect(self.d_ptr.slotBoolChanged)
        self.d_ptr.m_intPropertyManager.propertyDestroyedSignal.connect(self.d_ptr.slotPropertyDestroyed)
        self.d_ptr.m_enumPropertyManager.propertyDestroyedSignal.connect(self.d_ptr.slotPropertyDestroyed)
        self.d_ptr.m_boolPropertyManager.propertyDestroyedSignal.connect(self.d_ptr.slotPropertyDestroyed)

    ###
    #    Destroys this manager, and all the properties it has created.
    ###
    def __del__(self):
        self.clear()
        del self.d_ptr

    ###
    #    Returns the manager that creates the \e pointSize subproperty.

    #    In order to provide editing widgets for the \e pointSize property
    #    in a property browser widget, this manager must be associated
    #    with an editor factory.

    #    \sa QtAbstractPropertyBrowser.setFactoryForManager()
    ###
    def subIntPropertyManager(self):
        return self.d_ptr.m_intPropertyManager

    ###
    #    Returns the manager that create the \e family subproperty.

    #    In order to provide editing widgets for the \e family property
    #    in a property browser widget, this manager must be associated
    #    with an editor factory.

    #    \sa QtAbstractPropertyBrowser.setFactoryForManager()
    ###
    def subEnumPropertyManager(self):
        return self.d_ptr.m_enumPropertyManager

    ###
    #    Returns the manager that creates the  \e bold, \e italic, \e underline,
    #    \e strikeOut and \e kerning subproperties.
    #
    #    In order to provide editing widgets for the mentioned properties
    #    in a property browser widget, this manager must be associated with
    #    an editor factory.

    #    \sa QtAbstractPropertyBrowser.setFactoryForManager()
    ###
    def subBoolPropertyManager(self):
        return self.d_ptr.m_boolPropertyManager

    ###
    #    Returns the given \a property's value.

    #    If the given property is not managed by this manager, this:
    #    function returns a font object that uses the application's default
    #    font.

    #    \sa setValue()
    ###
    def value(self, property):
        return self.d_ptr.m_values.get(property, QFont())

    ###
    #    \reimp
    ###
    def valueText(self, property):
        if not property in self.d_ptr.m_values.keys():
            return ''

        return QtPropertyBrowserUtils.fontValueText(self.d_ptr.m_values[property])

    ###
    #    \reimp
    ###
    def valueIcon(self, property):
        if not property in self.d_ptr.m_values.keys():
            return QIcon()

        return QtPropertyBrowserUtils.fontValueIcon(self.d_ptr.m_values[property])

    ###
    #    \fn void QtFontPropertyManager.setValue(property, value)

    #    Sets the value of the given \a property to \a value. Nested
    #    properties are updated automatically.

    #    \sa value(), valueChanged()
    ###
    def setValue(self, property, val):
        if not property in self.d_ptr.m_values.keys():
            return

        oldVal = self.d_ptr.m_values[property]
        if oldVal == val:
            return

        self.d_ptr.m_values[property] = val

        idx = self.d_ptr.m_familyNames.indexOf(val.family())
        if (idx == -1):
            idx = 0
        settingValue = self.d_ptr.m_settingValue
        self.d_ptr.m_settingValue = True
        self.d_ptr.m_enumPropertyManager.setValue(self.d_ptr.m_propertyToFamily[property], idx)
        self.d_ptr.m_intPropertyManager.setValue(self.d_ptr.m_propertyToPointSize[property], val.pointSize())
        self.d_ptr.m_boolPropertyManager.setValue(self.d_ptr.m_propertyToBold[property], val.bold())
        self.d_ptr.m_boolPropertyManager.setValue(self.d_ptr.m_propertyToItalic[property], val.italic())
        self.d_ptr.m_boolPropertyManager.setValue(self.d_ptr.m_propertyToUnderline[property], val.underline())
        self.d_ptr.m_boolPropertyManager.setValue(self.d_ptr.m_propertyToStrikeOut[property], val.strikeOut())
        self.d_ptr.m_boolPropertyManager.setValue(self.d_ptr.m_propertyToKerning[property], val.kerning())
        self.d_ptr.m_settingValue = settingValue

        self.propertyChangedSignal.emit(property)
        self.valueChangedSignal.emit(property, val)

    ###
    #    \reimp
    ###
    def initializeProperty(self, property):
        val = QFont()
        self.d_ptr.m_values[property] = val

        familyProp = self.d_ptr.m_enumPropertyManager.addProperty()
        familyProp.setPropertyName(self.tr("Family"))
        if len(self.d_ptr.m_familyNames)<=0:
            self.d_ptr.m_familyNames += fontDatabase().families()
        self.d_ptr.m_enumPropertyManager.setEnumNames(familyProp, self.d_ptr.m_familyNames)
        idx = self.d_ptr.m_familyNames.indexOf(val.family())
        if (idx == -1):
            idx = 0
        self.d_ptr.m_enumPropertyManager.setValue(familyProp, idx)
        self.d_ptr.m_propertyToFamily[property] = familyProp
        self.d_ptr.m_familyToProperty[familyProp] = property
        property.addSubProperty(familyProp)

        pointSizeProp = self.d_ptr.m_intPropertyManager.addProperty()
        pointSizeProp.setPropertyName(self.tr("Point Size"))
        self.d_ptr.m_intPropertyManager.setValue(pointSizeProp, val.pointSize())
        self.d_ptr.m_intPropertyManager.setMinimum(pointSizeProp, 1)
        self.d_ptr.m_propertyToPointSize[property] = pointSizeProp
        self.d_ptr.m_pointSizeToProperty[pointSizeProp] = property
        property.addSubProperty(pointSizeProp)

        boldProp = self.d_ptr.m_boolPropertyManager.addProperty()
        boldProp.setPropertyName(self.tr("Bold"))
        self.d_ptr.m_boolPropertyManager.setValue(boldProp, val.bold())
        self.d_ptr.m_propertyToBold[property] = boldProp
        self.d_ptr.m_boldToProperty[boldProp] = property
        property.addSubProperty(boldProp)

        italicProp = self.d_ptr.m_boolPropertyManager.addProperty()
        italicProp.setPropertyName(self.tr("Italic"))
        self.d_ptr.m_boolPropertyManager.setValue(italicProp, val.italic())
        self.d_ptr.m_propertyToItalic[property] = italicProp
        self.d_ptr.m_italicToProperty[italicProp] = property
        property.addSubProperty(italicProp)

        underlineProp = self.d_ptr.m_boolPropertyManager.addProperty()
        underlineProp.setPropertyName(self.tr("Underline"))
        self.d_ptr.m_boolPropertyManager.setValue(underlineProp, val.underline())
        self.d_ptr.m_propertyToUnderline[property] = underlineProp
        self.d_ptr.m_underlineToProperty[underlineProp] = property
        property.addSubProperty(underlineProp)

        strikeOutProp = self.d_ptr.m_boolPropertyManager.addProperty()
        strikeOutProp.setPropertyName(self.tr("Strikeout"))
        self.d_ptr.m_boolPropertyManager.setValue(strikeOutProp, val.strikeOut())
        self.d_ptr.m_propertyToStrikeOut[property] = strikeOutProp
        self.d_ptr.m_strikeOutToProperty[strikeOutProp] = property
        property.addSubProperty(strikeOutProp)

        kerningProp = self.d_ptr.m_boolPropertyManager.addProperty()
        kerningProp.setPropertyName(self.tr("Kerning"))
        self.d_ptr.m_boolPropertyManager.setValue(kerningProp, val.kerning())
        self.d_ptr.m_propertyToKerning[property] = kerningProp
        self.d_ptr.m_kerningToProperty[kerningProp] = property
        property.addSubProperty(kerningProp)

    ###
    #    \reimp
    ###
    def uninitializeProperty(self, property):
        familyProp = self.d_ptr.m_propertyToFamily[property]
        if (familyProp):
            self.d_ptr.m_familyToProperty.remove(familyProp)
            del familyProp

        self.d_ptr.m_propertyToFamily.remove(property)

        pointSizeProp = self.d_ptr.m_propertyToPointSize[property]
        if (pointSizeProp):
            self.d_ptr.m_pointSizeToProperty.remove(pointSizeProp)
            del pointSizeProp

        self.d_ptr.m_propertyToPointSize.remove(property)

        boldProp = self.d_ptr.m_propertyToBold[property]
        if (boldProp):
            self.d_ptr.m_boldToProperty.remove(boldProp)
            del boldProp

        self.d_ptr.m_propertyToBold.remove(property)

        italicProp = self.d_ptr.m_propertyToItalic[property]
        if (italicProp):
            self.d_ptr.m_italicToProperty.remove(italicProp)
            self.d_ptr.m_propertyToItalic.remove(italicProp)

        self.d_ptr.m_propertyToItalic.remove(property)

        underlineProp = self.d_ptr.m_propertyToUnderline[property]
        if (underlineProp):
            self.d_ptr.m_underlineToProperty.remove(underlineProp)
            del underlineProp

        self.d_ptr.m_propertyToUnderline.remove(property)

        strikeOutProp = self.d_ptr.m_propertyToStrikeOut[property]
        if (strikeOutProp):
            self.d_ptr.m_strikeOutToProperty.remove(strikeOutProp)
            del strikeOutProp

        self.d_ptr.m_propertyToStrikeOut.remove(property)

        kerningProp = self.d_ptr.m_propertyToKerning[property]
        if (kerningProp):
            self.d_ptr.m_kerningToProperty.remove(kerningProp)
            del kerningProp

        self.d_ptr.m_propertyToKerning.remove(property)

        self.d_ptr.m_values.remove(property)

class QtColorPropertyManagerPrivate():
    def __init__(self):
        self.q_ptr = None

        self.m_values = QMap()
        self.m_propertyToR = QMap()
        self.m_propertyToG = QMap()
        self.m_propertyToB = QMap()
        self.m_propertyToA = QMap()
        self.m_rToProperty = QMap()
        self.m_gToProperty = QMap()
        self.m_bToProperty = QMap()
        self.m_aToProperty = QMap()
        self.m_intPropertyManager = None

    def slotIntChanged(self, property, value):
        prop = self.m_rToProperty.get(property, 0)
        if prop:
            c = copy.copy(self.m_values[prop])
            c.setRed(value)
            self.q_ptr.setValue(prop, c)
        else:
            prop = self.m_gToProperty.get(property, 0)
            if prop:
                c = copy.copy(self.m_values[prop])
                c.setGreen(value)
                self.q_ptr.setValue(prop, c)
            else:
                prop = self.m_bToProperty.get(property, 0)
                if prop:
                    c = copy.copy(self.m_values[prop])
                    c.setBlue(value)
                    self.q_ptr.setValue(prop, c)
                else:
                    prop = self.m_aToProperty.get(property, 0)
                    if prop:
                        c = copy.copy(self.m_values[prop])
                        c.setAlpha(value)
                        self.q_ptr.setValue(prop, c)

    def slotPropertyDestroyed(self, property):
        pointProp = self.m_rToProperty.get(property, 0)
        if pointProp:
            self.m_propertyToR[pointProp] = 0
            self.m_rToProperty.remove(property)
        else:
            pointProp = self.m_gToProperty.get(property, 0)
            if pointProp:
                self.m_propertyToG[pointProp] = 0
                self.m_gToProperty.remove(property)
            else:
                pointProp = self.m_bToProperty.get(property, 0)
                if pointProp:
                    self.m_propertyToB[pointProp] = 0
                    self.m_bToProperty.remove(property)
                else:
                    pointProp = self.m_aToProperty.get(property, 0)
                    if pointProp:
                        self.m_propertyToA[pointProp] = 0
                        self.m_aToProperty.remove(property)

###
#    \class QtColorPropertyManager
#
#    \brief The QtColorPropertyManager provides and manages QColor properties.
#
#    A color property has nested \e red, \e green and \e blue
#    subproperties. The top-level property's value can be retrieved
#    using the value() function, and set using the setValue() slot.

#    The subproperties are created by a QtIntPropertyManager object. This
#    manager can be retrieved using the subIntPropertyManager() function.  In
#    order to provide editing widgets for the subproperties in a
#    property browser widget, this manager must be associated with an
#    editor factory.
#
#    In addition, QtColorPropertyManager provides the valueChanged() signal
#    which is emitted whenever a property created by this manager
#    changes.

#    \sa QtAbstractPropertyManager, QtAbstractPropertyBrowser, QtIntPropertyManager
###
#
###
#    \fn void QtColorPropertyManager.valueChanged(property, value)

#    This signal is emitted whenever a property created by this manager
#    changes its value, passing a pointer to the \a property and the new
#    \a value as parameters.

#    \sa setValue()
###
#
class QtColorPropertyManager(QtAbstractPropertyManager):
    valueChangedSignal = pyqtSignal(QtProperty, QColor)
    ###
    #    Creates a manager with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtColorPropertyManager, self).__init__(parent)

        self.d_ptr = QtColorPropertyManagerPrivate()
        self.d_ptr.q_ptr = self

        self.d_ptr.m_intPropertyManager = QtIntPropertyManager(self)
        self.d_ptr.m_intPropertyManager.valueChangedSignal.connect(self.d_ptr.slotIntChanged)
        self.d_ptr.m_intPropertyManager.propertyDestroyedSignal.connect(self.d_ptr.slotPropertyDestroyed)

    ###
    #    Destroys this manager, and all the properties it has created.
    ###
    def __del__(self):
        self.clear()
        del self.d_ptr

    ###
    #    Returns the manager that produces the nested \e red, \e green and
    #    \e blue subproperties.
    #
    #    In order to provide editing widgets for the subproperties in a
    #    property browser widget, this manager must be associated with an
    #    editor factory.

    #    \sa QtAbstractPropertyBrowser.setFactoryForManager()
    ###
    def subIntPropertyManager(self):
        return self.d_ptr.m_intPropertyManager

    ###
    #    Returns the given \a property's value.

    #    If the given \a property is not managed by \e this manager, this:
    #    function returns an invalid color.

    #    \sa setValue()
    ###
    def value(self, property):
        return self.d_ptr.m_values.get(property, QColor())

    ###
    #    \reimp
    ###
    #
    def valueText(self, property):
        if not property in self.d_ptr.m_values.keys():
            return ''

        return QtPropertyBrowserUtils.colorValueText(self.d_ptr.m_values[property])

    ###
    #    \reimp
    ###
    #
    def valueIcon(self, property):
        if not property in self.d_ptr.m_values.keys():
            return QIcon()
        return QtPropertyBrowserUtils.brushValueIcon(QBrush(self.d_ptr.m_values[property]))

    ###
    #    \fn void QtColorPropertyManager.setValue(property, value)

    #    Sets the value of the given \a property to \a value.  Nested
    #    properties are updated automatically.

    #    \sa value(), valueChanged()
    ###
    def setValue(self, property, val):
        if not property in self.d_ptr.m_values.keys():
            return

        if (self.d_ptr.m_values[property] == val):
            return

        self.d_ptr.m_values[property] = val

        self.d_ptr.m_intPropertyManager.setValue(self.d_ptr.m_propertyToR[property], val.red())
        self.d_ptr.m_intPropertyManager.setValue(self.d_ptr.m_propertyToG[property], val.green())
        self.d_ptr.m_intPropertyManager.setValue(self.d_ptr.m_propertyToB[property], val.blue())
        self.d_ptr.m_intPropertyManager.setValue(self.d_ptr.m_propertyToA[property], val.alpha())

        self.propertyChangedSignal.emit(property)
        self.valueChangedSignal.emit(property, val)

    ###
    #    \reimp
    ###
    def initializeProperty(self, property):
        val = QColor()
        self.d_ptr.m_values[property] = val

        rProp = self.d_ptr.m_intPropertyManager.addProperty()
        rProp.setPropertyName(self.tr("Red"))
        self.d_ptr.m_intPropertyManager.setValue(rProp, val.red())
        self.d_ptr.m_intPropertyManager.setRange(rProp, 0, 0xFF)
        self.d_ptr.m_propertyToR[property] = rProp
        self.d_ptr.m_rToProperty[rProp] = property
        property.addSubProperty(rProp)

        gProp = self.d_ptr.m_intPropertyManager.addProperty()
        gProp.setPropertyName(self.tr("Green"))
        self.d_ptr.m_intPropertyManager.setValue(gProp, val.green())
        self.d_ptr.m_intPropertyManager.setRange(gProp, 0, 0xFF)
        self.d_ptr.m_propertyToG[property] = gProp
        self.d_ptr.m_gToProperty[gProp] = property
        property.addSubProperty(gProp)

        bProp = self.d_ptr.m_intPropertyManager.addProperty()
        bProp.setPropertyName(self.tr("Blue"))
        self.d_ptr.m_intPropertyManager.setValue(bProp, val.blue())
        self.d_ptr.m_intPropertyManager.setRange(bProp, 0, 0xFF)
        self.d_ptr.m_propertyToB[property] = bProp
        self.d_ptr.m_bToProperty[bProp] = property
        property.addSubProperty(bProp)

        aProp = self.d_ptr.m_intPropertyManager.addProperty()
        aProp.setPropertyName(self.tr("Alpha"))
        self.d_ptr.m_intPropertyManager.setValue(aProp, val.alpha())
        self.d_ptr.m_intPropertyManager.setRange(aProp, 0, 0xFF)
        self.d_ptr.m_propertyToA[property] = aProp
        self.d_ptr.m_aToProperty[aProp] = property
        property.addSubProperty(aProp)

    ###
    #    \reimp
    ###
    def uninitializeProperty(self, property):
        rProp = self.d_ptr.m_propertyToR[property]
        if (rProp):
            self.d_ptr.m_rToProperty.remove(rProp)
            del rProp

        self.d_ptr.m_propertyToR.remove(property)

        gProp = self.d_ptr.m_propertyToG[property]
        if (gProp):
            self.d_ptr.m_gToProperty.remove(gProp)
            del gProp

        self.d_ptr.m_propertyToG.remove(property)

        bProp = self.d_ptr.m_propertyToB[property]
        if (bProp):
            self.d_ptr.m_bToProperty.remove(bProp)
            del bProp

        self.d_ptr.m_propertyToB.remove(property)

        aProp = self.d_ptr.m_propertyToA[property]
        if (aProp):
            self.d_ptr.m_aToProperty.remove(aProp)
            del aProp

        self.d_ptr.m_propertyToA.remove(property)

        self.d_ptr.m_values.remove(property)

class QtCursorPropertyManagerPrivate():
    def __init__(self):
        self.q_ptr = None
        self.m_values = QMap()

###
#    \class QtCursorPropertyManager
#
#    \brief The QtCursorPropertyManager provides and manages QCursor properties.
#
#    A cursor property has a current value which can be
#    retrieved using the value() function, and set using the setValue()
#    slot. In addition, QtCursorPropertyManager provides the
#    valueChanged() signal which is emitted whenever a property created
#    by this manager changes.

#    \sa QtAbstractPropertyManager
###
#
###
#    \fn void QtCursorPropertyManager.valueChanged(property, value)

#    This signal is emitted whenever a property created by this manager
#    changes its value, passing a pointer to the \a property and the new
#    \a value as parameters.

#    \sa setValue()
###
#

def cursorDatabase():
    global g_cursorDatabase
    if not g_cursorDatabase:
        g_cursorDatabase = QtCursorDatabase()
    return g_cursorDatabase
g_cursorDatabase = None

# QtCursorPropertyManager

# Make sure icons are removed as soon as QApplication is destroyed, otherwise,
# handles are leaked on X11.
class CursorDatabase(QtCursorDatabase):
    def __init__(self):
        super(CursorDatabase, self).__init__()
        qAddPostRoutine(clearCursorDatabase)

def clearCursorDatabase():
    cursorDatabase().clear()

class QtCursorPropertyManager(QtAbstractPropertyManager):
    valueChangedSignal = pyqtSignal(QtProperty, QCursor)
    ###
    #    Creates a manager with the given \a parent.
    ###
    def __init__(self, parent=None):
        super(QtCursorPropertyManager, self).__init__(parent)

        self.d_ptr = QtCursorPropertyManagerPrivate()
        self.d_ptr.q_ptr = self

    ###
    #    Destroys this manager, and all the properties it has created.
    ###
    def __del__(self):
        self.clear()
        del self.d_ptr

    ###
    #    Returns the given \a property's value.

    #    If the given \a property is not managed by this manager, this:
    #    function returns a default QCursor object.

    #    \sa setValue()
    ###
    def value(self, property):
        return self.d_ptr.m_values.get(property, QCursor())

    ###
    #    \reimp
    ###
    def valueText(self, property):
        if not property in self.d_ptr.m_values.keys():
            return ''

        return cursorDatabase().cursorToShapeName(self.d_ptr.m_values[property])

    ###
    #    \reimp
    ###
    def valueIcon(self, property):
        if not property in self.d_ptr.m_values.keys():
            return QIcon()

        return cursorDatabase().cursorToShapeIcon(self.d_ptr.m_values[property])

    ###
    #    \fn void QtCursorPropertyManager.setValue(property, value)

    #    Sets the value of the given \a property to \a value.

    #    \sa value(), valueChanged()
    ###
    def setValue(self, property, value):
        if not property in self.d_ptr.m_values.keys():
            return

        if (self.d_ptr.m_values[property].shape() == value.shape() and value.shape() != Qt.BitmapCursor):
            return

        self.d_ptr.m_values[property] = value

        self.propertyChangedSignal.emit(property)
        self.valueChangedSignal.emit(property, value)

    ###
    #    \reimp
    ###
    def initializeProperty(self, property):
        self.d_ptr.m_values[property] = QCursor()

    ###
    #    \reimp
    ###
    def uninitializeProperty(self, property):
        self.d_ptr.m_values.remove(property)

