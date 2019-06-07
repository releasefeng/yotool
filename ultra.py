# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ultra.ui'
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

class Ultra_Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(405, 504)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 70, 41, 31))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(200, 70, 41, 31))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 190, 41, 31))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(200, 190, 41, 31))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(10, 320, 41, 31))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(200, 320, 41, 31))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.start = QtGui.QPushButton(Dialog)
        self.start.setGeometry(QtCore.QRect(200, 430, 71, 31))
        self.start.setObjectName(_fromUtf8("start"))
        self.stop = QtGui.QPushButton(Dialog)
        self.stop.setGeometry(QtCore.QRect(290, 430, 71, 31))
        self.stop.setObjectName(_fromUtf8("stop"))
        self.ch1 = QtGui.QTextBrowser(Dialog)
        self.ch1.setGeometry(QtCore.QRect(60, 70, 121, 31))
        self.ch1.setObjectName(_fromUtf8("ch1"))
        self.ch2 = QtGui.QTextBrowser(Dialog)
        self.ch2.setGeometry(QtCore.QRect(250, 70, 121, 31))
        self.ch2.setObjectName(_fromUtf8("ch2"))
        self.ch3 = QtGui.QTextBrowser(Dialog)
        self.ch3.setGeometry(QtCore.QRect(60, 190, 121, 31))
        self.ch3.setObjectName(_fromUtf8("ch3"))
        self.ch5 = QtGui.QTextBrowser(Dialog)
        self.ch5.setGeometry(QtCore.QRect(60, 320, 121, 31))
        self.ch5.setObjectName(_fromUtf8("ch5"))
        self.ch4 = QtGui.QTextBrowser(Dialog)
        self.ch4.setGeometry(QtCore.QRect(250, 190, 121, 31))
        self.ch4.setObjectName(_fromUtf8("ch4"))
        self.ch6 = QtGui.QTextBrowser(Dialog)
        self.ch6.setGeometry(QtCore.QRect(250, 320, 121, 31))
        self.ch6.setObjectName(_fromUtf8("ch6"))
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(10, 10, 51, 21))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.sername = QtGui.QComboBox(Dialog)
        self.sername.setGeometry(QtCore.QRect(60, 10, 69, 22))
        self.sername.setEditable(True)
        self.sername.setObjectName(_fromUtf8("sername"))
        self.seropen = QtGui.QPushButton(Dialog)
        self.seropen.setGeometry(QtCore.QRect(140, 10, 61, 21))
        self.seropen.setObjectName(_fromUtf8("seropen"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "超声调试", None))
        self.label.setText(_translate("Dialog", "超声1：", None))
        self.label_2.setText(_translate("Dialog", "超声2：", None))
        self.label_3.setText(_translate("Dialog", "超声3：", None))
        self.label_4.setText(_translate("Dialog", "超声4：", None))
        self.label_5.setText(_translate("Dialog", "超声5：", None))
        self.label_6.setText(_translate("Dialog", "超声6：", None))
        self.start.setText(_translate("Dialog", "开始", None))
        self.stop.setText(_translate("Dialog", "暂停", None))
        self.label_7.setText(_translate("Dialog", "端口号：", None))
        self.seropen.setText(_translate("Dialog", "打开", None))

