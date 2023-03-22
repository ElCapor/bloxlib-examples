# -*- coding: utf-8 -*-
##
# pyqtcore.py
#
# This file is part of Tiled.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
##

INT_MAX = 0x7fffffff
INT_MIN = -0x7fffffff

RAND_MAX = 0x7FFF

import random
import os
def Int(s, defValue = 0):
    try:
        return int(s)
    except:
        return defValue

def Int2(s, defValue = 0):
    try:
        return int(s), True
    except:
        return defValue, False
        
def Float(s, defValue = 0.0):
    try:
        return float(s)
    except:
        return defValue

def Float2(s, defValue = 0.0):
    try:
        return float(s), True
    except:
        return defValue, False
def rand():
    return int(random.random()*RAND_MAX)

qrand = rand
qgetenv = os.getenv

from PyQt5.QtCore import (
    QSize, 
    QSizeF, 
    QByteArray
)

g_metaTypeIds = {}
def qMetaTypeId(classType):
    typeId = g_metaTypeIds.get(classType)
    if typeId is None:
        typeId = len(g_metaTypeIds)+1200
        g_metaTypeIds[classType] = typeId
    return typeId

def qMettaTypeIds():
    return g_metaTypeIds.values()
    
def dynamic_cast(object, _type):
    if type(object) == _type:
        return object
    return None
    
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

class QSet(set):
    def insert(self, item):
        self.add(item)

    def toList(self):
        return QList(self)

    def contains(self, item):
        return item in self
    
    def isEmpty(self):
        return self.__len__()==0
    
    def at(self, index):
        if index<0 or index>=self.__len__():
            return None
        i = 0
        for x in self.__iter__():
            if i==index:
                return x
            i += 1
            
    def begin(self):
        return self.at(0)
    
    def size(self):
        return self.__len__()
        
    def remove(self, item):
        if self.__contains__(item):
            super().remove(item)
            
class QList(list):
    def __init__(self, args=[]):
        if args is not None:
            super(QList, self).__init__(args)
    
    def contains(self, item):
        return self.__contains__(item)
        
    def removeAll(self, item):
        n = 0
        for i in range(self.__len__()-1, -1, -1):
            if self.__getitem__(i) == item:
                self.__delitem__(i)
                n += 1
        return n
    
    def remove(self, index):
        if index < 0 or index >= self.__len__():
            return
        self.__delitem__(index)
        
    def removeAt(self, index):
        if index < 0 or index >= self.__len__():
            return
        self.__delitem__(index)

    def indexOf(self, item):
        for i in range(self.__len__()):
            if self.__getitem__(i) == item:
                return i
        return -1

    def first(self):
        if self.__len__()>0:
            return self.__getitem__(0)
        else:
            return None

    def removeFirst(self):
        if self.__len__()>0:
            self.__delitem__(0)

    def removeLast(self):
        if self.__len__()>0:
            self.__delitem__(self.__len__()-1)

    def count(self):
        return self.__len__()

    def size(self):
        return self.__len__()

    def at(self, i):
        if i < 0 or i >= self.__len__():
            return None
        return self.__getitem__(i)

    def prepend(self, item):
        self.insert(0, item)

    def isEmpty(self):
        return self.__len__()==0

    def length(self):
        return self.__len__()

    def takeFirst(self):
        if self.__len__()==0:
            return None
        x = self.__getitem__(0)
        self.removeFirst()
        return x

    def takeLast(self):
        if self.__len__()==0:
            return None
        x = self.__getitem__(self.__len__()-1)
        self.removeLast()
        return x

    def empty(self):
        return self.__len__()==0

    def last(self):
        if self.__len__()>0:
            return self.__getitem__(self.__len__()-1)
        return None

    def erase(self, _from, to=None):
        if to is None:
            to = _from + 1
        
        l = self.__len__()
        if l < 1:
            return
        if to >= l:
            to = l - 1
        if _from < 0:
            _from = 0
        count = to - _from
        
        if count < 1:
            return
        for i in range(count):
            self.__delitem__[_from]
    
    def takeAt(self, index):
        if index<0 or index>=self.__len__():
            return None
        item = self.__getitem__(index)
        self.__delitem__(index)
        return item
    
    def move(self, index, to):
        l = self.__len__()
        if index<0 or index>=l:
            return
        if to>=l:
            to = l-1
        if index==to:#dont move
            return
        item = self.__getitem__(index)
        self.__delitem__(index)
        self.insert(to, item)
            
class QMap(QList):
    def __init__(self, key=None, value=None):
        super(QMap, self).__init__()

        self.insert = self.__setitem__
        self.find = self.get
        if key or value:
            self.__setitem__(key, value)

    def __getitem__(self, key):
        for x in self.__iter__():
            if x[0]==key:
                return x[1]
        return None

    def __setitem__(self, key, value):
        for i in range(self.__len__()):
            x = super(QMap, self).__getitem__(i)
            if x[0]==key:
                super(QMap, self).__setitem__(i, [key, value])
                return
        self.append([key, value])
        return self.__len__()

    def keys(self):
        r = []
        for x in self.__iter__():
            r.append(x[0])
        return r

    def values(self):
        r = []
        for x in self.__iter__():
            r.append(x[1])
        return r

    def value(self, key, defValue = None):
        return self.get(key, defValue)

    def get(self, key, defvalue=None):
        v = self.__getitem__(key)
        if v==None:
            return defvalue
        return v

    def remove(self, key):
        for x in self.__iter__():
            if x[0]==key:
                index = self.index(x)
                self.__delitem__(index)
                return

    def erase(self, iter):
        self.remove(iter)

    def count(self):
        return self.__len__()

    def end(self):
        return None

    def contains(self, key):
        return self.get(key)!=None

    def take(self, key):
        v = self.__getitem__(key)
        if v==None:
            return None 
        self.remove(key)
        return v

    def lowerBound(self, key):
        keys = sorted(self.keys())
        _keyfind = len(keys)

        _keys = QSet(keys)

        index = 0
        for _key in _keys:
            if key <= _key:
                _keyfind = index
                break
            index += 1

        return _keyfind
        
    def upperBound(self, key):
        keys = self.keys()
        _keyfind = len(keys)

        _keys = QSet(keys)
        
        _keys = sorted(_keys)
        index = 0
        for _key in _keys:
            if key < _key:
                _keyfind = index
                break
            index += 1

        return _keyfind

    def itemByIndex(self, index):
        if index<0 or index>=self.__len__():
            return None
        return super().__getitem__(index)

class QMapList(QMap):
    def __init__(self, key=None, value=None):
        super(QMapList, self).__init__(key, value)

    def __getitem__(self, key):
        v = super(QMapList, self).__getitem__(key)
        if not v:
            v = QList()
            super(QMapList, self).__setitem__(key, v)
        return v

    def get(self, key, defvalue=QList()):
        v = super(QMapList, self).__getitem__(key)
        if not v:
            return defvalue
        return v
    
    def value(self, key, defvalue=QList()):
        v = super(QMapList, self).__getitem__(key)
        if not v:
            return defvalue
        return v

class QMapMap(QMap):
    def __init__(self, key=None, value=None):
        super(QMapMap, self).__init__(key, value)

    def __getitem__(self, key):
        v = super(QMapMap, self).__getitem__(key)
        if not v:
            v = QMap()
            super(QMapMap, self).__setitem__(key, v)
        return v

    def get(self, key, defvalue=QMap()):
        v = super(QMapMap, self).__getitem__(key)
        if not v:
            return defvalue
        return v

class QMapMapList(QMap):
    def __init__(self, key=None, value=None):
        super(QMapMapList, self).__init__(key, value)

    def __getitem__(self, key):
        v = super(QMapMapList, self).__getitem__(key)
        if not v:
            v = QMapList()
            super(QMapMapList, self).__setitem__(key, v)
        return v

    def get(self, key, defvalue=None):
        v = super(QMapMapList, self).__getitem__(key)
        if not v:
            return defvalue
        return v

class QVector(QList):
    def __init__(self, *args):
        super().__init__(args)

    def resize(self, n):
        l = self.__len__()
        for i in range(l-1, n-1, -1):
            self.__delitem__(i)

        for i in range(n-l):
            self.append(0)

    def reserve(self, n):
        l = self.__len__()

        for i in range(n-l):
            self.append(0)
        
class QString(str):
    def __init__(self, s=''):
        super(QString, self).__init__()
        
        self.length = self.__len__
        self.startsWith = self.startswith
        self.endsWith = self.endswith

    def isEmpty(self):
        return self.__len__()==0

    def at(self, i):
        return QChar(self.__str__()[i])

    def startsWith(self, source, sensitive = True):
        if sensitive:
            return self.startswith(source)
        else:
            return self.lower().startswith(source.lower())

    def endsWith(self, source, sensitive = True):
        if sensitive:
            return self.endswith(source)
        else:
            return self.lower().endswith(source.lower())

    def toLatin1(self):
        if self.__len__()==0:
            return QByteArray()
        return QByteArray(self.__str__(), self.__len__())

    def number(value, base=10):
        try:
            nv = int(str(value), base)
        except:
            return QString()
        return QString(nv)

    def index(self, subStr, _fromIndex=0):
        s = self.__str__()
        ls = len(s)
        if _fromIndex < 0:
            _fromIndex = 0
        if _fromIndex >= ls:
            _fromIndex = ls - 1
        s = s[_fromIndex:]
        if self.__contains__(subStr):
            return super().index(subStr)
        return -1
        
class QChar(str):
    def __init__(self, s=''):
        super(QChar, self).__init__()

class QStringList(QList):
    def __init__(self, arg=[]):
        super().__init__(arg)

    def takeFirst(self):
        return QString(super().takeFirst())

    def takeLast(self):
        return QString(super().takeLast())

class QHash(dict):
    def __init__(self, *args):
        super().__init__(args)

        self.value = self.__getitem__
        self.insert = self.__setitem__
        self.contains = self.__contains__

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except:
            return None

    def take(self, key):
        value = self.__getitem__(key)
        if value:
            self.__delitem__(key)
        return value
