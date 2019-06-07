# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
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

class Login_Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(612, 424)
        Dialog.setInputMethodHints(QtCore.Qt.ImhNone)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(280, 20, 311, 165))
        self.groupBox.setMaximumSize(QtCore.QSize(311, 347))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.stationedit = QtGui.QPushButton(self.groupBox)
        self.stationedit.setGeometry(QtCore.QRect(10, 132, 75, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stationedit.sizePolicy().hasHeightForWidth())
        self.stationedit.setSizePolicy(sizePolicy)
        self.stationedit.setObjectName(_fromUtf8("stationedit"))
        self.cancel = QtGui.QPushButton(self.groupBox)
        self.cancel.setGeometry(QtCore.QRect(91, 132, 75, 23))
        self.cancel.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.cancel.setObjectName(_fromUtf8("cancel"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(178, 22, 54, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 22, 54, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.hostname = QtGui.QTextEdit(self.groupBox)
        self.hostname.setGeometry(QtCore.QRect(10, 40, 162, 31))
        self.hostname.setMaximumSize(QtCore.QSize(16777215, 31))
        self.hostname.setObjectName(_fromUtf8("hostname"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 77, 54, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.username = QtGui.QTextEdit(self.groupBox)
        self.username.setGeometry(QtCore.QRect(10, 95, 161, 31))
        self.username.setMaximumSize(QtCore.QSize(16777215, 31))
        self.username.setObjectName(_fromUtf8("username"))
        self.port = QtGui.QTextEdit(self.groupBox)
        self.port.setGeometry(QtCore.QRect(178, 40, 123, 31))
        self.port.setMaximumSize(QtCore.QSize(16777215, 31))
        self.port.setObjectName(_fromUtf8("port"))
        self.password = QtGui.QLineEdit(self.groupBox)
        self.password.setGeometry(QtCore.QRect(180, 95, 121, 31))
        self.password.setMaximumSize(QtCore.QSize(129, 31))
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setObjectName(_fromUtf8("password"))
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(178, 77, 42, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.stationlist = QtGui.QListWidget(Dialog)
        self.stationlist.setGeometry(QtCore.QRect(20, 20, 256, 351))
        self.stationlist.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.stationlist.setObjectName(_fromUtf8("stationlist"))
        item = QtGui.QListWidgetItem()
        self.stationlist.addItem(item)
        self.login = QtGui.QPushButton(Dialog)
        self.login.setGeometry(QtCore.QRect(460, 380, 61, 24))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.login.sizePolicy().hasHeightForWidth())
        self.login.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/login.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.login.setIcon(icon)
        self.login.setObjectName(_fromUtf8("login"))
        self.deletestation = QtGui.QPushButton(Dialog)
        self.deletestation.setGeometry(QtCore.QRect(20, 380, 75, 23))
        self.deletestation.setObjectName(_fromUtf8("deletestation"))
        self.close = QtGui.QPushButton(Dialog)
        self.close.setGeometry(QtCore.QRect(530, 380, 61, 23))
        self.close.setObjectName(_fromUtf8("close"))
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(280, 200, 311, 171))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.messinfo = QtGui.QTextBrowser(self.groupBox_2)
        self.messinfo.setObjectName(_fromUtf8("messinfo"))
        self.horizontalLayout.addWidget(self.messinfo)

        self.retranslateUi(Dialog)
        self.stationlist.setCurrentRow(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.groupBox.setTitle(_translate("Dialog", "会话", None))
        self.stationedit.setText(_translate("Dialog", "保存(S)", None))
        self.cancel.setText(_translate("Dialog", "取消", None))
        self.label_2.setText(_translate("Dialog", "端口号(P)", None))
        self.label.setText(_translate("Dialog", "主机IP(H)", None))
        self.label_3.setText(_translate("Dialog", "用户名(U)", None))
        self.label_4.setText(_translate("Dialog", "密码(P)", None))
        __sortingEnabled = self.stationlist.isSortingEnabled()
        self.stationlist.setSortingEnabled(False)
        item = self.stationlist.item(0)
        item.setText(_translate("Dialog", "新建站点", None))
        self.stationlist.setSortingEnabled(__sortingEnabled)
        self.login.setText(_translate("Dialog", "登录", None))
        self.deletestation.setText(_translate("Dialog", "删除", None))
        self.close.setText(_translate("Dialog", "关闭", None))
        self.groupBox_2.setTitle(_translate("Dialog", "登录提示", None))

import image_rc
