# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'deviceSet.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(320, 246)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.deviceSetbutton = QtGui.QPushButton(Dialog)
        self.deviceSetbutton.setGeometry(QtCore.QRect(140, 150, 71, 23))
        self.deviceSetbutton.setObjectName(_fromUtf8("deviceSetbutton"))
        self.deviceType = QtGui.QComboBox(Dialog)
        self.deviceType.setGeometry(QtCore.QRect(140, 50, 69, 22))
        self.deviceType.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.deviceType.setObjectName(_fromUtf8("deviceType"))
        self.deviceType.addItem(_fromUtf8(""))
        self.deviceType.addItem(_fromUtf8(""))
        self.portSelect = QtGui.QComboBox(Dialog)
        self.portSelect.setGeometry(QtCore.QRect(140, 100, 69, 22))
        self.portSelect.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.portSelect.setEditable(True)
        self.portSelect.setObjectName(_fromUtf8("portSelect"))
        self.portSelect.addItem(_fromUtf8(""))
        self.portSelect.addItem(_fromUtf8(""))
        self.portSelect.addItem(_fromUtf8(""))
        self.portSelect.addItem(_fromUtf8(""))
        self.portSelect.addItem(_fromUtf8(""))
        self.portSelect.addItem(_fromUtf8(""))
        self.portSelect.addItem(_fromUtf8(""))
        self.portSelect.addItem(_fromUtf8(""))
        self.portSelect.addItem(_fromUtf8(""))
        self.portSelect.addItem(_fromUtf8(""))
        self.portSelect.addItem(_fromUtf8(""))
        self.portSelect.addItem(_fromUtf8(""))
        self.portSelect.addItem(_fromUtf8(""))
        self.portSelect.addItem(_fromUtf8(""))
        self.portSelect.addItem(_fromUtf8(""))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(70, 50, 54, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(80, 100, 41, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "设备设置", None))
        self.deviceSetbutton.setText(_translate("Dialog", "设置", None))
        self.deviceType.setItemText(0, _translate("Dialog", "kago", None))
        self.deviceType.setItemText(1, _translate("Dialog", "mingo", None))
        self.portSelect.setItemText(0, _translate("Dialog", "COM1", None))
        self.portSelect.setItemText(1, _translate("Dialog", "COM2", None))
        self.portSelect.setItemText(2, _translate("Dialog", "COM3", None))
        self.portSelect.setItemText(3, _translate("Dialog", "COM4", None))
        self.portSelect.setItemText(4, _translate("Dialog", "COM5", None))
        self.portSelect.setItemText(5, _translate("Dialog", "COM6", None))
        self.portSelect.setItemText(6, _translate("Dialog", "COM7", None))
        self.portSelect.setItemText(7, _translate("Dialog", "COM8", None))
        self.portSelect.setItemText(8, _translate("Dialog", "COM9", None))
        self.portSelect.setItemText(9, _translate("Dialog", "COM10", None))
        self.portSelect.setItemText(10, _translate("Dialog", "COM11", None))
        self.portSelect.setItemText(11, _translate("Dialog", "COM12", None))
        self.portSelect.setItemText(12, _translate("Dialog", "COM13", None))
        self.portSelect.setItemText(13, _translate("Dialog", "COM14", None))
        self.portSelect.setItemText(14, _translate("Dialog", "COM15", None))
        self.label.setText(_translate("Dialog", "设备类型：", None))
        self.label_2.setText(_translate("Dialog", "串口号：", None))

import image_rc
