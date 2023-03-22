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
############################################################################/

from PyQt5.QtCore import Qt, QCoreApplication, QRectF, QEvent, pyqtSignal
from PyQt5.QtWidgets import (
    QLineEdit,
    QWidget,
    QApplication,
    QHBoxLayout,
    QCheckBox,
    QStyleOption,
    QAction,
    QStyle)
from PyQt5.QtGui import QIcon, QPainter, QCursor, QImage, QPixmap, QTextOption, QKeySequence, QFont
from pyqtcore import QList, QMap
import qtpropertybrowser_rc

class QtCursorDatabase():
    def __init__(self):
        self.m_cursorNames = QList()
        self.m_cursorIcons = QMap()
        self.m_valueToCursorShape = QMap()
        self.m_cursorShapeToValue = QMap()

        self.appendCursor(Qt.ArrowCursor, QCoreApplication.translate("QtCursorDatabase", "Arrow"),
                     QIcon(":/qt-project.org/qtpropertybrowser/images/cursor-arrow.png"))
        self.appendCursor(Qt.UpArrowCursor, QCoreApplication.translate("QtCursorDatabase", "Up Arrow"),
                     QIcon(":/qt-project.org/qtpropertybrowser/images/cursor-uparrow.png"))
        self.appendCursor(Qt.CrossCursor, QCoreApplication.translate("QtCursorDatabase", "Cross"),
                     QIcon(":/qt-project.org/qtpropertybrowser/images/cursor-cross.png"))
        self.appendCursor(Qt.WaitCursor, QCoreApplication.translate("QtCursorDatabase", "Wait"),
                     QIcon(":/qt-project.org/qtpropertybrowser/images/cursor-wait.png"))
        self.appendCursor(Qt.IBeamCursor, QCoreApplication.translate("QtCursorDatabase", "IBeam"),
                     QIcon(":/qt-project.org/qtpropertybrowser/images/cursor-ibeam.png"))
        self.appendCursor(Qt.SizeVerCursor, QCoreApplication.translate("QtCursorDatabase", "Size Vertical"),
                     QIcon(":/qt-project.org/qtpropertybrowser/images/cursor-sizev.png"))
        self.appendCursor(Qt.SizeHorCursor, QCoreApplication.translate("QtCursorDatabase", "Size Horizontal"),
                     QIcon(":/qt-project.org/qtpropertybrowser/images/cursor-sizeh.png"))
        self.appendCursor(Qt.SizeFDiagCursor, QCoreApplication.translate("QtCursorDatabase", "Size Backslash"),
                     QIcon(":/qt-project.org/qtpropertybrowser/images/cursor-sizef.png"))
        self.appendCursor(Qt.SizeBDiagCursor, QCoreApplication.translate("QtCursorDatabase", "Size Slash"),
                     QIcon(":/qt-project.org/qtpropertybrowser/images/cursor-sizeb.png"))
        self.appendCursor(Qt.SizeAllCursor, QCoreApplication.translate("QtCursorDatabase", "Size All"),
                     QIcon(":/qt-project.org/qtpropertybrowser/images/cursor-sizeall.png"))
        self.appendCursor(Qt.BlankCursor, QCoreApplication.translate("QtCursorDatabase", "Blank"),
                     QIcon())
        self.appendCursor(Qt.SplitVCursor, QCoreApplication.translate("QtCursorDatabase", "Split Vertical"),
                     QIcon(":/qt-project.org/qtpropertybrowser/images/cursor-vsplit.png"))
        self.appendCursor(Qt.SplitHCursor, QCoreApplication.translate("QtCursorDatabase", "Split Horizontal"),
                     QIcon(":/qt-project.org/qtpropertybrowser/images/cursor-hsplit.png"))
        self.appendCursor(Qt.PointingHandCursor, QCoreApplication.translate("QtCursorDatabase", "Pointing Hand"),
                     QIcon(":/qt-project.org/qtpropertybrowser/images/cursor-hand.png"))
        self.appendCursor(Qt.ForbiddenCursor, QCoreApplication.translate("QtCursorDatabase", "Forbidden"),
                     QIcon(":/qt-project.org/qtpropertybrowser/images/cursor-forbidden.png"))
        self.appendCursor(Qt.OpenHandCursor, QCoreApplication.translate("QtCursorDatabase", "Open Hand"),
                     QIcon(":/qt-project.org/qtpropertybrowser/images/cursor-openhand.png"))
        self.appendCursor(Qt.ClosedHandCursor, QCoreApplication.translate("QtCursorDatabase", "Closed Hand"),
                     QIcon(":/qt-project.org/qtpropertybrowser/images/cursor-closedhand.png"))
        self.appendCursor(Qt.WhatsThisCursor, QCoreApplication.translate("QtCursorDatabase", "What's This"),
                     QIcon(":/qt-project.org/qtpropertybrowser/images/cursor-whatsthis.png"))
        self.appendCursor(Qt.BusyCursor, QCoreApplication.translate("QtCursorDatabase", "Busy"),
                     QIcon(":/qt-project.org/qtpropertybrowser/images/cursor-busy.png"))

    def clear(self):
        self.m_cursorNames.clear()
        self.m_cursorIcons.clear()
        self.m_valueToCursorShape.clear()
        self.m_cursorShapeToValue.clear()

    def appendCursor(self,shape, name, icon):
        if self.m_cursorShapeToValue.get(shape):
            return
        value = len(self.m_cursorNames)
        self.m_cursorNames.append(name)
        self.m_cursorIcons[value] = icon
        self.m_valueToCursorShape[value] = shape
        self.m_cursorShapeToValue[shape] = value

    def cursorShapeNames(self):
        return self.m_cursorNames

    def cursorShapeIcons(self):
        return self.m_cursorIcons

    def cursorToShapeName(self,cursor):
        val = self.cursorToValue(cursor)
        if val >= 0:
            return self.m_cursorNames[val]
        return ''

    def cursorToShapeIcon(self,cursor):
        val = self.cursorToValue(cursor)
        return self.m_cursorIcons[val]

    def cursorToValue(self,cursor):
        shape = cursor.shape()
        return self.m_cursorShapeToValue.get(shape, -1)

    def valueToCursor(self,value):
        if value in self.m_valueToCursorShape:
            return QCursor(self.m_valueToCursorShape[value])
        return QCursor()

class QtPropertyBrowserUtils():
    def __init__(self):
        pass

    def brushValuePixmap(b):
        img = QImage(16, 16, QImage.Format_ARGB32_Premultiplied)
        img.fill(0)
        painter = QPainter(img)
        #painter.begin()
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        painter.fillRect(0, 0, img.width(), img.height(), b)
        color = b.color()
        if (color.alpha() != 255):  # indicate alpha by an inset
            opaqueBrush = b
            color.setAlpha(255)
            opaqueBrush.setColor(color)
            painter.fillRect(img.width() / 4, img.height() / 4,
                             img.width() / 2, img.height() / 2, opaqueBrush)

        painter.end()
        return QPixmap.fromImage(img)

    def brushValueIcon(b):
        return QIcon(QtPropertyBrowserUtils.brushValuePixmap(b))

    def colorValueText(c):
        return QCoreApplication.translate("QtPropertyBrowserUtils", "[%d, %d, %d] (%d)"%(c.red(), c.green(), c.blue(), c.alpha()))

    def fontValuePixmap(font):
        f = QFont(font)
        img = QImage(16, 16, QImage.Format_ARGB32_Premultiplied)
        img.fill(0)
        p = QPainter(img)
        p.setRenderHint(QPainter.TextAntialiasing, True)
        p.setRenderHint(QPainter.Antialiasing, True)
        f.setPointSize(13)
        p.setFont(f)
        t = QTextOption()
        t.setAlignment(Qt.AlignCenter)
        p.drawText(QRectF(0, 0, 16, 16), 'A', t)
        p.end()
        return QPixmap.fromImage(img)

    def fontValueIcon(f):
        return QIcon(QtPropertyBrowserUtils.fontValuePixmap(f))

    def fontValueText(f):
        return QCoreApplication.translate("QtPropertyBrowserUtils", "[%s, %d]"%(f.family(), f.pointSize()))

class QtBoolEdit(QWidget):
    toggledSignal = pyqtSignal(bool)
    def __init__(self,parent=None):
        super(QtBoolEdit, self).__init__(parent)
        self.m_checkBox = QCheckBox(self)
        self.m_textVisible = True
        lt = QHBoxLayout()
        if (QApplication.layoutDirection() == Qt.LeftToRight):
            lt.setContentsMargins(4, 0, 0, 0)
        else:
            lt.setContentsMargins(0, 0, 4, 0)
        lt.addWidget(self.m_checkBox)
        self.setLayout(lt)
        self.m_checkBox.toggled.connect(self.toggledSignal)
        self.setFocusProxy(self.m_checkBox)
        self.m_checkBox.setText(self.tr("True"))

    def textVisible(self):
        return self.m_textVisible

    def setTextVisible(self,textVisible):
        if (self.m_textVisible == textVisible):
            return

        self.m_textVisible = textVisible
        if self.m_textVisible:
            if self.isChecked():
                self.m_checkBox.setText(self.tr("True"))
            else:
                self.m_checkBox.setText(self.tr("False"))
        else:
            self.m_checkBox.setText('')

    def checkState(self):
        return self.m_checkBox.checkState()

    def setCheckState(self,state):
        self.m_checkBox.setCheckState(state)

    def isChecked(self):
        return self.m_checkBox.isChecked()

    def setChecked(self,c):
        self.m_checkBox.setChecked(c)
        if self.m_textVisible==False:
            return
        if self.isChecked():
            self.m_checkBox.setText(self.tr("True"))
        else:
            self.m_checkBox.setText(self.tr("False"))

    def blockCheckBoxSignals(self,block):
        return self.m_checkBox.blockSignals(block)

    def mousePressEvent(self, event):
        if (event.buttons() == Qt.LeftButton):
            self.m_checkBox.click()
            event.accept()
        else:
            super(QtBoolEdit, self).mousePressEvent(event)

    def paintEvent(self, pt_QPaintEvent):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

class QtKeySequenceEdit(QWidget):
    keySequenceChangedSignal = pyqtSignal(QKeySequence)
    def __init__(self,parent=None):
        super(QtKeySequenceEdit, self).__init__(parent)

        self.m_keySequence = QKeySequence()
        self.m_num = 0
        self.m_lineEdit = QLineEdit(self)
        layout = QHBoxLayout(self)
        layout.addWidget(self.m_lineEdit)
        layout.setContentsMargins(0, 0, 0, 0)
        self.m_lineEdit.installEventFilter(self)
        self.m_lineEdit.setReadOnly(True)
        self.m_lineEdit.setFocusProxy(self)
        self.setFocusPolicy(self.m_lineEdit.focusPolicy())
        self.setAttribute(Qt.WA_InputMethodEnabled)

    def eventFilter(self, o, e):
        if o == self.m_lineEdit and e.type() == QEvent.ContextMenu:
            c = e
            menu = self.m_lineEdit.createStandardContextMenu()
            actions = menu.actions()
            for action in actions:
                action.setShortcut(QKeySequence())
                actionString = action.text()
                pos = actionString.rfind('\t')
                if (pos > 0):
                    actionString = actionString[:pos]
                action.setText(actionString)

            actionBefore = None
            if (len(actions) > 0):
                actionBefore = actions[0]
            clearAction = QAction(self.tr("Clear Shortcut"), menu)
            menu.insertAction(actionBefore, clearAction)
            menu.insertSeparator(actionBefore)
            clearAction.setEnabled(not len(self.m_keySequence)<=0)
            clearAction.triggered.connect(self.slotClearShortcut)
            menu.exec(c.globalPos())
            e.accept()
            return True

        return super(QtKeySequenceEdit, self).eventFilter(o, e)

    def slotClearShortcut(self):
        if len(self.m_keySequence) <= 0:
            return
        self.setKeySequence(QKeySequence())
        self.keySequenceChangedSignal.emit(self.m_keySequence)

    def handleKeyEvent(self, e):
        nextKey = e.key()
        if (nextKey == Qt.Key_Control or nextKey == Qt.Key_Shift or
                nextKey == Qt.Key_Meta or nextKey == Qt.Key_Alt or
                nextKey == Qt.Key_Super_L or nextKey == Qt.Key_AltGr):
            return

        nextKey |= self.translateModifiers(e.modifiers(), e.text())
        k0 = 0
        k1 = 0
        k2 = 0
        k3 = 0
        l = len(self.m_keySequence)
        if l==1:
            k0 = self.m_keySequence[0]
        elif l==2:
            k0 = self.m_keySequence[0]
            k1 = self.m_keySequence[1]
        elif l==3:
            k0 = self.m_keySequence[0]
            k1 = self.m_keySequence[1]
            k2 = self.m_keySequence[2]
        elif l==4:
            k0 = self.m_keySequence[0]
            k1 = self.m_keySequence[1]
            k2 = self.m_keySequence[2]
            k3 = self.m_keySequence[3]
        if self.m_num==0:
            k0 = nextKey
            k1 = 0
            k2 = 0
            k3 = 0
        elif self.m_num==1:
            k1 = nextKey
            k2 = 0
            k3 = 0
        elif self.m_num==2:
            k2 = nextKey
            k3 = 0
        elif self.m_num==3:
            k3 = nextKey
        else:
            pass

        self.m_num += 1
        if (self.m_num > 3):
            self.m_num = 0
        self.m_keySequence = QKeySequence(k0, k1, k2, k3)
        self.m_lineEdit.setText(self.m_keySequence.toString(QKeySequence.NativeText))
        e.accept()
        self.keySequenceChangedSignal.emit(self.m_keySequence)

    def setKeySequence(self, sequence):
        if (sequence == self.m_keySequence):
            return
        self.m_num = 0
        self.m_keySequence = sequence
        self.m_lineEdit.setText(self.m_keySequence.toString(QKeySequence.NativeText))

    def keySequence(self):
        return self.m_keySequence

    def translateModifiers(self, state, text):
        result = 0
        if ((state & Qt.ShiftModifier) and (len(text) == 0 or not text[0].isprintable() or text[0].isalpha() or text[0].isspace())):
            result |= Qt.SHIFT
        if (state & Qt.ControlModifier):
            result |= Qt.CTRL
        if (state & Qt.MetaModifier):
            result |= Qt.META
        if (state & Qt.AltModifier):
            result |= Qt.ALT
        return result

    def focusInEvent(self, e):
        self.m_lineEdit.event(e)
        self.m_lineEdit.selectAll()
        super(QtKeySequenceEdit, self).focusInEvent(e)

    def focusOutEvent(self, e):
        self.m_num = 0
        self.m_lineEdit.event(e)
        super(QtKeySequenceEdit, self).focusOutEvent(e)

    def keyPressEvent(self, e):
        self.handleKeyEvent(e)
        e.accept()

    def keyReleaseEvent(self, e):
        self.m_lineEdit.event(e)

    def paintEvent(self, ptQPaintEvent):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

    def event(self,e):
        if (e.type() == QEvent.Shortcut or
                e.type() == QEvent.ShortcutOverride  or
                e.type() == QEvent.KeyRelease):
            e.accept()
            return True

        return super(QtKeySequenceEdit, self).event(e)

