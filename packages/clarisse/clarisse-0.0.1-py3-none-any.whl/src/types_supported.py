"""
Clrsarisse

types_supported module.
Defines all types that are able to be displayed by PyQt widgets.

by 1MLightyears@gmail.com

on 20201208
"""

from PySide2.QtWidgets import QLabel, QSpinBox, QLineEdit, QDoubleSpinBox, QTextEdit, QTableWidget, QCheckBox, QTableWidgetItem
from PySide2.QtCore import Qt
import typing

import log

__all__ = ["ClrsUnknown","ClrsInt", "ClrsFloat","ClrsString","ClrsList","ClrsBool","ClrsDict"]

class ClrsUnknown(QLineEdit):
    __name__ = "ClrsUnknown"

    def __init__(self, name:str="",target_kwargs:dict={},*args,**kwargs):
        super(ClrsUnknown, self).__init__(*args, **kwargs)
        if name!="":
            self.setObjectName(name)
        self.target_kwargs = target_kwargs

    def setDefault(self, default=None):
        if default!=None:
            self.setPlaceholderText(str(default))

    def getValue(self):
        return self.text() or self.placeholderText()

class ClrsString(QLineEdit):
    __name__ = "ClrsString"

    def __init__(self, name:str="",target_kwargs:dict={},*args,**kwargs):
        super(ClrsString, self).__init__(*args, **kwargs)
        if name!="":
            self.setObjectName(name)
        self.target_kwargs = target_kwargs

    def setDefault(self, default=None):
        if default!=None:
            self.setPlaceholderText(default)

    def getValue(self):
        return self.text() or self.placeholderText()

class ClrsInt(QSpinBox):
    __name__ = "ClrsInt"

    def __init__(self, name:str="",target_kwargs:dict={},*args,**kwargs):
        super(ClrsInt, self).__init__(*args, **kwargs)
        if name!="":
            self.setObjectName(name)
        self.target_kwargs = target_kwargs

    def setDefault(self, default=None):
        if default != None:
            self.setValue(default)

    def getValue(self):
        return self.value()

class ClrsFloat(QDoubleSpinBox):
    __name__ = "ClrsFloat"

    def __init__(self, name:str="",target_kwargs:dict={},*args,**kwargs):
        super(ClrsFloat, self).__init__(*args, **kwargs)
        if name!="":
            self.setObjectName(name)
        self.target_kwargs = target_kwargs

    def setDefault(self, default=None):
        if default!=None:
            self.setValue(default)

    def getValue(self):
        return self.value()

class ClrsList(QTextEdit):
    __name__ = "ClrsList"

    def __init__(self,
            name: str = "",
            target_kwargs: dict = {},
            ElementType: type = None,
            *args,**kwargs):
        super(ClrsList, self).__init__(*args, **kwargs)
        if name!="":
            self.setObjectName(name)
        self.target_kwargs = target_kwargs
        self.ElementType=ElementType

    def setDefault(self, default=None):
        if isinstance(default,list):
            self.setPlaceholderText("\n".join([str(i) for i in default]))

    def getValue(self):
        t = self.placeholderText() if self.toPlainText() == "" else self.toPlainText()
        if self.ElementType:
            return [self.ElementType(i) for i in t.split("\n")]
        return [i for i in t.split("\n")]

class ClrsBool(QCheckBox):
    __name__ = "ClrsBool"

    def __init__(self, name:str="",target_kwargs:dict={},*args,**kwargs):
        super(ClrsBool, self).__init__(*args, **kwargs)
        if name!="":
            self.setObjectName(name)
        self.target_kwargs = target_kwargs

    def setDefault(self, default=None):
        if default!=None:
            self.setChecked(default)

    def getValue(self):
        return self.isChecked()

class ClrsDict(QTableWidget):
    __name__ = "ClrsDict"

    def __init__(self,
            name: str = "",
            target_kwargs: dict = {},
            ElementType = None,
            *args, **kwargs
        ):
        super(ClrsDict, self).__init__(*args, **kwargs)
        if name!="":
            self.setObjectName(name)
        self.target_kwargs = target_kwargs
        self.setDefaultDropAction(Qt.TargetMoveAction)
        self.ElementType=ElementType

    def setDefault(self, default=None):
        if default != None:
            # create a 2 column table
            keys = list(default.keys())
            keys_count = len(keys)
            self.setRowCount(keys_count)
            self.setColumnCount(2)
            for i in range(keys_count):
                k, v = QTableWidgetItem(), QTableWidgetItem()
                k.setText(str(keys[i])); v.setText(str(default[keys[i]]))
                self.setItem(i, 0, k)
                self.setItem(i, 1, v)
        # TODO:add approaches to add/delete items

    def getValue(self):
        ret = {}
        for i in range(self.rowCount()):
            k, v = self.item(i, 0).text(), self.item(i, 1).text()
            if isinstance(self.ElementType,tuple):
                if len(self.ElementType)>0:
                    k=self.ElementType[0](k)
                if len(self.ElementType)>1:
                    v=self.ElementType[1](v)
            ret.update({k:v})
        return ret