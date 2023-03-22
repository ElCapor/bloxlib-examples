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
from pyqtcore import QList
from qtvariantproperty import QtVariantEditorFactory, QtVariantPropertyManager
from qttreepropertybrowser import QtTreePropertyBrowser

if __name__ == '__main__':
    app = QApplication(sys.argv)
    trans = QTranslator()
    variantManager = QtVariantPropertyManager()
    i = 0
    topItem = variantManager.addProperty(QtVariantPropertyManager.groupTypeId(), str(i) + " Group Property")
    i += 1

    item = variantManager.addProperty(QVariant.Bool, str(i) + " Bool Property")
    i += 1
    item.setValue(True)
    topItem.addSubProperty(item)

    item = variantManager.addProperty(QVariant.Int, str(i) + " Int Property")
    i += 1
    item.setValue(20)
    item.setAttribute("minimum", 0)
    item.setAttribute("maximum", 100)
    item.setAttribute("singleStep", 10)
    topItem.addSubProperty(item)

    item = variantManager.addProperty(QVariant.Int, str(i) + " Int Property (ReadOnly)")
    i += 1
    item.setValue(20)
    item.setAttribute("minimum", 0)
    item.setAttribute("maximum", 100)
    item.setAttribute("singleStep", 10)
    item.setAttribute("readOnly", True)
    topItem.addSubProperty(item)

    item = variantManager.addProperty(QVariant.Double, str(i) + " Double Property")
    i += 1
    item.setValue(1.2345)
    item.setAttribute("singleStep", 0.1)
    item.setAttribute("decimals", 3)
    topItem.addSubProperty(item)

    item = variantManager.addProperty(QVariant.Double, str(i) + " Double Property (ReadOnly)")
    i += 1
    item.setValue(1.23456)
    item.setAttribute("singleStep", 0.1)
    item.setAttribute("decimals", 5)
    item.setAttribute("readOnly", True)
    topItem.addSubProperty(item)

    item = variantManager.addProperty(QVariant.String, str(i) + " String Property")
    i += 1
    item.setValue("Value")
    topItem.addSubProperty(item)

    item = variantManager.addProperty(QVariant.String, str(i) + " String Property (Password)")
    i += 1
    item.setAttribute("echoMode", QLineEdit.Password)
    item.setValue("Password")
    topItem.addSubProperty(item)

    # Readonly String Property
    item = variantManager.addProperty(QVariant.String, str(i) + " String Property (ReadOnly)")
    i += 1
    item.setAttribute("readOnly", True)
    item.setValue("readonly text")
    topItem.addSubProperty(item)

    item = variantManager.addProperty(QVariant.Date, str(i) + " Date Property")
    i += 1
    item.setValue(QDate.currentDate().addDays(2))
    topItem.addSubProperty(item)

    item = variantManager.addProperty(QVariant.Time, str(i) + " Time Property")
    i += 1
    item.setValue(QTime.currentTime())
    topItem.addSubProperty(item)

    item = variantManager.addProperty(QVariant.DateTime, str(i) + " DateTime Property")
    i += 1
    item.setValue(QDateTime.currentDateTime())
    topItem.addSubProperty(item)

    item = variantManager.addProperty(QVariant.KeySequence, str(i) + " KeySequence Property")
    i += 1
    item.setValue(QKeySequence(Qt.ControlModifier | Qt.Key_Q))
    topItem.addSubProperty(item)

    item = variantManager.addProperty(QVariant.Char, str(i) + " Char Property")
    i += 1
    item.setValue(chr(386))
    topItem.addSubProperty(item)

    item = variantManager.addProperty(QVariant.Locale, str(i) + " Locale Property")
    i += 1
    item.setValue(QLocale(QLocale.Polish, QLocale.Poland))
    topItem.addSubProperty(item)

    item = variantManager.addProperty(QVariant.Point, str(i) + " PoProperty")
    i += 1
    item.setValue(QPoint(10, 10))
    topItem.addSubProperty(item)

    item = variantManager.addProperty(QVariant.PointF, str(i) + " PointF Property")
    i += 1
    item.setValue(QPointF(1.2345, -1.23451))
    item.setAttribute("decimals", 3)
    topItem.addSubProperty(item)

    item = variantManager.addProperty(QVariant.Size, str(i) + " Size Property")
    i += 1
    item.setValue(QSize(20, 20))
    item.setAttribute("minimum", QSize(10, 10))
    item.setAttribute("maximum", QSize(30, 30))
    topItem.addSubProperty(item)

    item = variantManager.addProperty(QVariant.SizeF, str(i) + " SizeF Property")
    i += 1
    item.setValue(QSizeF(1.2345, 1.2345))
    item.setAttribute("decimals", 3)
    item.setAttribute("minimum", QSizeF(0.12, 0.34))
    item.setAttribute("maximum", QSizeF(20.56, 20.78))
    topItem.addSubProperty(item)

    item = variantManager.addProperty(QVariant.Rect, str(i) + " Rect Property")
    i += 1
    item.setValue(QRect(10, 10, 20, 20))
    topItem.addSubProperty(item)
    item.setAttribute("constraint", QRect(0, 0, 50, 50))

    item = variantManager.addProperty(QVariant.RectF, str(i) + " RectF Property")
    i += 1
    item.setValue(QRectF(1.2345, 1.2345, 1.2345, 1.2345))
    topItem.addSubProperty(item)
    item.setAttribute("constraint", QRectF(0, 0, 50, 50))
    item.setAttribute("decimals", 3)

    item = variantManager.addProperty(QtVariantPropertyManager.enumTypeId(), str(i) + " Enum Property")
    i += 1
    enumNames = QList()
    enumNames.append("Enum0")
    enumNames.append("Enum1")
    enumNames.append("Enum2")
    item.setAttribute("enumNames", enumNames)
    item.setValue(1)
    topItem.addSubProperty(item)

    item = variantManager.addProperty(QtVariantPropertyManager.flagTypeId(), str(i) + " Flag Property")
    i += 1
    flagNames = QList()
    flagNames.append("Flag0")
    flagNames.append("Flag1")
    flagNames.append("Flag2")
    item.setAttribute("flagNames", flagNames)
    item.setValue(5)
    topItem.addSubProperty(item)

    item = variantManager.addProperty(QVariant.SizePolicy, str(i) + " SizePolicy Property")
    i += 1
    topItem.addSubProperty(item)

    item = variantManager.addProperty(QVariant.Font, str(i) + " Font Property")
    i += 1
    topItem.addSubProperty(item)

    item = variantManager.addProperty(QVariant.Cursor, str(i) + " Cursor Property")
    i += 1
    topItem.addSubProperty(item)

    item = variantManager.addProperty(QVariant.Color, str(i) + " Color Property")
    i += 1
    topItem.addSubProperty(item)

    variantFactory = QtVariantEditorFactory()

    variantEditor = QtTreePropertyBrowser()
    variantEditor.setFactoryForManager(variantManager, variantFactory)
    variantEditor.addProperty(topItem)
    variantEditor.setPropertiesWithoutValueMarked(True)
    variantEditor.setRootIsDecorated(False)

    variantEditor.showMaximized()
    variantEditor.show()
    ret = app.exec_()
    del variantManager
    del variantFactory
    del variantEditor
