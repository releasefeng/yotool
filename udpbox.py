# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'udpbox.ui'
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

class Udpbox_Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(375, 349)
        self.groupBox_8 = QtGui.QGroupBox(Dialog)
        self.groupBox_8.setGeometry(QtCore.QRect(10, 160, 351, 181))
        self.groupBox_8.setObjectName(_fromUtf8("groupBox_8"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox_8)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_40 = QtGui.QLabel(self.groupBox_8)
        self.label_40.setObjectName(_fromUtf8("label_40"))
        self.gridLayout.addWidget(self.label_40, 0, 0, 1, 1)
        self.delaytime = QtGui.QSpinBox(self.groupBox_8)
        self.delaytime.setMinimum(1)
        self.delaytime.setMaximum(2000)
        self.delaytime.setSingleStep(3)
        self.delaytime.setProperty("value", 5)
        self.delaytime.setObjectName(_fromUtf8("delaytime"))
        self.gridLayout.addWidget(self.delaytime, 0, 1, 1, 2)
        self.label_39 = QtGui.QLabel(self.groupBox_8)
        self.label_39.setObjectName(_fromUtf8("label_39"))
        self.gridLayout.addWidget(self.label_39, 1, 0, 1, 2)
        self.leftmotorvalue = QtGui.QSpinBox(self.groupBox_8)
        self.leftmotorvalue.setMaximum(2000)
        self.leftmotorvalue.setSingleStep(3)
        self.leftmotorvalue.setObjectName(_fromUtf8("leftmotorvalue"))
        self.gridLayout.addWidget(self.leftmotorvalue, 1, 2, 1, 1)
        self.label_38 = QtGui.QLabel(self.groupBox_8)
        self.label_38.setObjectName(_fromUtf8("label_38"))
        self.gridLayout.addWidget(self.label_38, 1, 3, 1, 1)
        self.rightmotorvalue = QtGui.QSpinBox(self.groupBox_8)
        self.rightmotorvalue.setMaximum(2000)
        self.rightmotorvalue.setSingleStep(3)
        self.rightmotorvalue.setObjectName(_fromUtf8("rightmotorvalue"))
        self.gridLayout.addWidget(self.rightmotorvalue, 1, 4, 1, 1)
        self.comboBox = QtGui.QComboBox(self.groupBox_8)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox, 2, 0, 1, 1)
        self.leftmotorcontrol = QtGui.QComboBox(self.groupBox_8)
        self.leftmotorcontrol.setObjectName(_fromUtf8("leftmotorcontrol"))
        self.leftmotorcontrol.addItem(_fromUtf8(""))
        self.leftmotorcontrol.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.leftmotorcontrol, 2, 2, 1, 1)
        self.comboBox_2 = QtGui.QComboBox(self.groupBox_8)
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox_2, 2, 3, 1, 1)
        self.rightmotorcontrol = QtGui.QComboBox(self.groupBox_8)
        self.rightmotorcontrol.setObjectName(_fromUtf8("rightmotorcontrol"))
        self.rightmotorcontrol.addItem(_fromUtf8(""))
        self.rightmotorcontrol.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.rightmotorcontrol, 2, 4, 1, 1)
        self.loop = QtGui.QPushButton(self.groupBox_8)
        self.loop.setObjectName(_fromUtf8("loop"))
        self.gridLayout.addWidget(self.loop, 3, 0, 1, 2)
        self.return_2 = QtGui.QPushButton(self.groupBox_8)
        self.return_2.setEnabled(False)
        self.return_2.setObjectName(_fromUtf8("return_2"))
        self.gridLayout.addWidget(self.return_2, 3, 2, 1, 1)
        self.pause = QtGui.QPushButton(self.groupBox_8)
        self.pause.setObjectName(_fromUtf8("pause"))
        self.gridLayout.addWidget(self.pause, 3, 4, 1, 1)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 351, 141))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 20, 61, 31))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 60, 61, 31))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.charge = QtGui.QTextBrowser(self.groupBox)
        self.charge.setGeometry(QtCore.QRect(80, 20, 201, 31))
        self.charge.setObjectName(_fromUtf8("charge"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(40, 100, 31, 31))
        self.label.setObjectName(_fromUtf8("label"))
        self.count = QtGui.QTextBrowser(self.groupBox)
        self.count.setGeometry(QtCore.QRect(80, 100, 201, 31))
        self.count.setObjectName(_fromUtf8("count"))
        self.battery = QtGui.QTextBrowser(self.groupBox)
        self.battery.setGeometry(QtCore.QRect(80, 60, 201, 31))
        self.battery.setObjectName(_fromUtf8("battery"))
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(290, 60, 54, 31))
        self.label_4.setObjectName(_fromUtf8("label_4"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.groupBox_8.setTitle(_translate("Dialog", "电机控制", None))
        self.label_40.setText(_translate("Dialog", "后退延时：", None))
        self.label_39.setText(_translate("Dialog", "左电机速度：", None))
        self.label_38.setText(_translate("Dialog", "右电机速度：", None))
        self.comboBox.setItemText(0, _translate("Dialog", "正向", None))
        self.comboBox.setItemText(1, _translate("Dialog", "反向", None))
        self.leftmotorcontrol.setItemText(0, _translate("Dialog", "使能", None))
        self.leftmotorcontrol.setItemText(1, _translate("Dialog", "释放", None))
        self.comboBox_2.setItemText(0, _translate("Dialog", "正向", None))
        self.comboBox_2.setItemText(1, _translate("Dialog", "反向", None))
        self.rightmotorcontrol.setItemText(0, _translate("Dialog", "使能", None))
        self.rightmotorcontrol.setItemText(1, _translate("Dialog", "释放", None))
        self.loop.setText(_translate("Dialog", "开始", None))
        self.return_2.setText(_translate("Dialog", "往返", None))
        self.pause.setText(_translate("Dialog", "暂停", None))
        self.groupBox.setTitle(_translate("Dialog", "电池", None))
        self.label_2.setText(_translate("Dialog", " 充电状态：", None))
        self.label_3.setText(_translate("Dialog", "剩余电量：", None))
        self.label.setText(_translate("Dialog", "次数：", None))
        self.label_4.setText(_translate("Dialog", "%", None))

import image_rc
