# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ucboard.ui'
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

class Ucboard_Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(893, 587)
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.horizontalLayout = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.testmessage = QtGui.QTextBrowser(self.groupBox)
        self.testmessage.setObjectName(_fromUtf8("testmessage"))
        self.gridLayout_4.addWidget(self.testmessage, 0, 0, 1, 2)
        self.messclear = QtGui.QPushButton(self.groupBox)
        self.messclear.setObjectName(_fromUtf8("messclear"))
        self.gridLayout_4.addWidget(self.messclear, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 1, 0, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox, 1, 3, 1, 1)
        self.groupBox_7 = QtGui.QGroupBox(Dialog)
        self.groupBox_7.setTitle(_fromUtf8(""))
        self.groupBox_7.setObjectName(_fromUtf8("groupBox_7"))
        self.gridLayout_8 = QtGui.QGridLayout(self.groupBox_7)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.label = QtGui.QLabel(self.groupBox_7)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_8.addWidget(self.label, 0, 0, 1, 1)
        self.progressBar = QtGui.QProgressBar(self.groupBox_7)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout_8.addWidget(self.progressBar, 0, 1, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox_7, 2, 0, 1, 1)
        self.groupBox_3 = QtGui.QGroupBox(Dialog)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.tabWidget = QtGui.QTabWidget(self.groupBox_3)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Triangular)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.gridLayout_10 = QtGui.QGridLayout(self.tab_3)
        self.gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))
        self.boardlist = QtGui.QListWidget(self.tab_3)
        self.boardlist.setEnabled(True)
        self.boardlist.setObjectName(_fromUtf8("boardlist"))
        item = QtGui.QListWidgetItem()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/firmware.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon)
        self.boardlist.addItem(item)
        item = QtGui.QListWidgetItem()
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/set.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon1)
        self.boardlist.addItem(item)
        item = QtGui.QListWidgetItem()
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/wifi.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon2)
        self.boardlist.addItem(item)
        item = QtGui.QListWidgetItem()
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/montor.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon3)
        self.boardlist.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setIcon(icon3)
        self.boardlist.addItem(item)
        item = QtGui.QListWidgetItem()
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/open.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon4)
        self.boardlist.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setIcon(icon4)
        self.boardlist.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setIcon(icon4)
        self.boardlist.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setIcon(icon4)
        self.boardlist.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setIcon(icon)
        self.boardlist.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setIcon(icon)
        self.boardlist.addItem(item)
        item = QtGui.QListWidgetItem()
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/IR.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon5)
        self.boardlist.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setIcon(icon5)
        self.boardlist.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setIcon(icon5)
        self.boardlist.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setIcon(icon5)
        self.boardlist.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setIcon(icon5)
        self.boardlist.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setIcon(icon5)
        self.boardlist.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setIcon(icon5)
        self.boardlist.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setIcon(icon5)
        self.boardlist.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setIcon(icon5)
        self.boardlist.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setIcon(icon5)
        self.boardlist.addItem(item)
        item = QtGui.QListWidgetItem()
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/denguang.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon6)
        self.boardlist.addItem(item)
        self.gridLayout_10.addWidget(self.boardlist, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName(_fromUtf8("tab_4"))
        self.otalist = QtGui.QListWidget(self.tab_4)
        self.otalist.setEnabled(True)
        self.otalist.setGeometry(QtCore.QRect(10, 10, 251, 191))
        self.otalist.setObjectName(_fromUtf8("otalist"))
        item = QtGui.QListWidgetItem()
        item.setIcon(icon)
        self.otalist.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setIcon(icon1)
        self.otalist.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setIcon(icon2)
        self.otalist.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setIcon(icon3)
        self.otalist.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setIcon(icon4)
        self.otalist.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setIcon(icon)
        self.otalist.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setIcon(icon5)
        self.otalist.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setIcon(icon6)
        self.otalist.addItem(item)
        self.tabWidget.addTab(self.tab_4, _fromUtf8(""))
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox_3, 0, 0, 1, 1)
        self.groupBox_6 = QtGui.QGroupBox(Dialog)
        self.groupBox_6.setObjectName(_fromUtf8("groupBox_6"))
        self.gridLayout_7 = QtGui.QGridLayout(self.groupBox_6)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.testitem = QtGui.QListWidget(self.groupBox_6)
        self.testitem.setObjectName(_fromUtf8("testitem"))
        self.gridLayout_7.addWidget(self.testitem, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox_6, 1, 0, 1, 1)
        self.groupBox_8 = QtGui.QGroupBox(Dialog)
        self.groupBox_8.setObjectName(_fromUtf8("groupBox_8"))
        self.gridLayout_12 = QtGui.QGridLayout(self.groupBox_8)
        self.gridLayout_12.setObjectName(_fromUtf8("gridLayout_12"))
        self.subtest = QtGui.QListWidget(self.groupBox_8)
        self.subtest.setObjectName(_fromUtf8("subtest"))
        self.gridLayout_12.addWidget(self.subtest, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox_8, 1, 1, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_7 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 2, 0, 1, 1)
        self.SN = QtGui.QTextEdit(self.groupBox_2)
        self.SN.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SN.sizePolicy().hasHeightForWidth())
        self.SN.setSizePolicy(sizePolicy)
        self.SN.setMaximumSize(QtCore.QSize(173, 36))
        self.SN.setObjectName(_fromUtf8("SN"))
        self.gridLayout.addWidget(self.SN, 0, 1, 1, 1)
        self.BID = QtGui.QTextEdit(self.groupBox_2)
        self.BID.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BID.sizePolicy().hasHeightForWidth())
        self.BID.setSizePolicy(sizePolicy)
        self.BID.setMaximumSize(QtCore.QSize(173, 35))
        self.BID.setObjectName(_fromUtf8("BID"))
        self.gridLayout.addWidget(self.BID, 1, 1, 1, 1)
        self.label_8 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 3, 0, 1, 1)
        self.hardver = QtGui.QTextEdit(self.groupBox_2)
        self.hardver.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hardver.sizePolicy().hasHeightForWidth())
        self.hardver.setSizePolicy(sizePolicy)
        self.hardver.setMaximumSize(QtCore.QSize(173, 35))
        self.hardver.setObjectName(_fromUtf8("hardver"))
        self.gridLayout.addWidget(self.hardver, 2, 1, 1, 1)
        self.label_11 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout.addWidget(self.label_11, 1, 0, 1, 1)
        self.softver = QtGui.QTextEdit(self.groupBox_2)
        self.softver.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.softver.sizePolicy().hasHeightForWidth())
        self.softver.setSizePolicy(sizePolicy)
        self.softver.setMaximumSize(QtCore.QSize(173, 35))
        self.softver.setObjectName(_fromUtf8("softver"))
        self.gridLayout.addWidget(self.softver, 3, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.protover = QtGui.QTextEdit(self.groupBox_2)
        self.protover.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.protover.sizePolicy().hasHeightForWidth())
        self.protover.setSizePolicy(sizePolicy)
        self.protover.setMaximumSize(QtCore.QSize(173, 36))
        self.protover.setObjectName(_fromUtf8("protover"))
        self.gridLayout.addWidget(self.protover, 4, 1, 1, 1)
        self.label_9 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 4, 0, 1, 1)
        self.label_10 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 5, 0, 1, 1)
        self.bootver = QtGui.QTextEdit(self.groupBox_2)
        self.bootver.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bootver.sizePolicy().hasHeightForWidth())
        self.bootver.setSizePolicy(sizePolicy)
        self.bootver.setMaximumSize(QtCore.QSize(173, 36))
        self.bootver.setObjectName(_fromUtf8("bootver"))
        self.gridLayout.addWidget(self.bootver, 5, 1, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox_2, 0, 3, 1, 1)
        self.groupBox_4 = QtGui.QGroupBox(Dialog)
        self.groupBox_4.setTitle(_fromUtf8(""))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_4)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_13 = QtGui.QLabel(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout_3.addWidget(self.label_13, 0, 0, 1, 1)
        self.testcount = QtGui.QLabel(self.groupBox_4)
        self.testcount.setObjectName(_fromUtf8("testcount"))
        self.gridLayout_3.addWidget(self.testcount, 0, 1, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox_4, 2, 1, 1, 1)
        self.groupBox_5 = QtGui.QGroupBox(Dialog)
        self.groupBox_5.setTitle(_fromUtf8(""))
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.gridLayout_6 = QtGui.QGridLayout(self.groupBox_5)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.label_6 = QtGui.QLabel(self.groupBox_5)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_6.addWidget(self.label_6, 0, 0, 1, 1)
        self.workmodel = QtGui.QLabel(self.groupBox_5)
        self.workmodel.setObjectName(_fromUtf8("workmodel"))
        self.gridLayout_6.addWidget(self.workmodel, 0, 1, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox_5, 2, 3, 1, 1)
        self.groupBox_9 = QtGui.QGroupBox(Dialog)
        self.groupBox_9.setObjectName(_fromUtf8("groupBox_9"))
        self.gridLayout_13 = QtGui.QGridLayout(self.groupBox_9)
        self.gridLayout_13.setObjectName(_fromUtf8("gridLayout_13"))
        self.reginfo = QtGui.QTextBrowser(self.groupBox_9)
        self.reginfo.setObjectName(_fromUtf8("reginfo"))
        self.gridLayout_13.addWidget(self.reginfo, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox_9, 0, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_5)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.boardlist.setCurrentRow(-1)
        self.otalist.setCurrentRow(-1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "YG协议单板C测试", None))
        self.groupBox.setTitle(_translate("Dialog", "消息区", None))
        self.messclear.setText(_translate("Dialog", "清除", None))
        self.label.setText(_translate("Dialog", "进度：", None))
        self.groupBox_3.setTitle(_translate("Dialog", "设置", None))
        self.boardlist.setToolTip(_translate("Dialog", "右键可设置为测试设备", None))
        __sortingEnabled = self.boardlist.isSortingEnabled()
        self.boardlist.setSortingEnabled(False)
        item = self.boardlist.item(0)
        item.setText(_translate("Dialog", "Board-C", None))
        item = self.boardlist.item(1)
        item.setText(_translate("Dialog", "IMU", None))
        item = self.boardlist.item(2)
        item.setText(_translate("Dialog", "2.4G", None))
        item = self.boardlist.item(3)
        item.setText(_translate("Dialog", "左轮毂电机", None))
        item = self.boardlist.item(4)
        item.setText(_translate("Dialog", "右轮毂电机", None))
        item = self.boardlist.item(5)
        item.setText(_translate("Dialog", "直流电机1", None))
        item = self.boardlist.item(6)
        item.setText(_translate("Dialog", "直流电机2", None))
        item = self.boardlist.item(7)
        item.setText(_translate("Dialog", "直流电机3", None))
        item = self.boardlist.item(8)
        item.setText(_translate("Dialog", "直流电机4", None))
        item = self.boardlist.item(9)
        item.setText(_translate("Dialog", "左箱体控制板", None))
        item = self.boardlist.item(10)
        item.setText(_translate("Dialog", "右箱体控制板", None))
        item = self.boardlist.item(11)
        item.setText(_translate("Dialog", "红外1", None))
        item = self.boardlist.item(12)
        item.setText(_translate("Dialog", "红外2", None))
        item = self.boardlist.item(13)
        item.setText(_translate("Dialog", "红外3", None))
        item = self.boardlist.item(14)
        item.setText(_translate("Dialog", "红外4", None))
        item = self.boardlist.item(15)
        item.setText(_translate("Dialog", "红外5", None))
        item = self.boardlist.item(16)
        item.setText(_translate("Dialog", "红外6", None))
        item = self.boardlist.item(17)
        item.setText(_translate("Dialog", "红外7", None))
        item = self.boardlist.item(18)
        item.setText(_translate("Dialog", "红外8", None))
        item = self.boardlist.item(19)
        item.setText(_translate("Dialog", "红外9", None))
        item = self.boardlist.item(20)
        item.setText(_translate("Dialog", "红外10", None))
        item = self.boardlist.item(21)
        item.setText(_translate("Dialog", "灯光控制", None))
        self.boardlist.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "测试板型号", None))
        self.otalist.setToolTip(_translate("Dialog", "右键可设置为测试设备", None))
        __sortingEnabled = self.otalist.isSortingEnabled()
        self.otalist.setSortingEnabled(False)
        item = self.otalist.item(0)
        item.setText(_translate("Dialog", "Board-C", None))
        item = self.otalist.item(1)
        item.setText(_translate("Dialog", "IMU", None))
        item = self.otalist.item(2)
        item.setText(_translate("Dialog", "2.4G", None))
        item = self.otalist.item(3)
        item.setText(_translate("Dialog", "轮毂电机", None))
        item = self.otalist.item(4)
        item.setText(_translate("Dialog", "开门电机", None))
        item = self.otalist.item(5)
        item.setText(_translate("Dialog", "左右箱体控制板", None))
        item = self.otalist.item(6)
        item.setText(_translate("Dialog", "红外传感器", None))
        item = self.otalist.item(7)
        item.setText(_translate("Dialog", "灯光控制", None))
        self.otalist.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Dialog", "OTA", None))
        self.groupBox_6.setTitle(_translate("Dialog", "测试项-单击可刷新测试子项", None))
        self.groupBox_8.setTitle(_translate("Dialog", "测试子项-双击可开始测试", None))
        self.groupBox_2.setTitle(_translate("Dialog", "通用寄存器-可修改", None))
        self.label_7.setText(_translate("Dialog", "硬件版本号：", None))
        self.label_8.setText(_translate("Dialog", "软件版本号：", None))
        self.label_11.setText(_translate("Dialog", "       BID：", None))
        self.label_3.setText(_translate("Dialog", "        SN：", None))
        self.label_9.setText(_translate("Dialog", "协议版本号：", None))
        self.label_10.setText(_translate("Dialog", "Boot版本号：", None))
        self.label_13.setText(_translate("Dialog", "失败次数：", None))
        self.testcount.setText(_translate("Dialog", "0", None))
        self.label_6.setText(_translate("Dialog", "C板工作模式：", None))
        self.workmodel.setText(_translate("Dialog", "正常", None))
        self.groupBox_9.setTitle(_translate("Dialog", "通用寄存器-只读", None))

import image_rc
