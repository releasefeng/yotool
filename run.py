#-*- coding: utf-8 -*-
from __future__ import division
import ctypes
myappid = u'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
from PyQt4 import QtGui,QtCore
import sys
import subprocess
import paramiko
import re
import os
import locale
import shutil
import serial
import binascii
import time
import serial.tools.list_ports
import crcmod
import hashlib
import socket

from ui.ui import Ui_MainWindow
from ui.deviceSet import Ui_Dialog
from ui.login import Login_Ui_Dialog
from ui.manual import Manual_Ui_Dialog
from ui.dboard import Dboard_Ui_Dialog
from ui.cboard import Cboard_Ui_Dialog
from ui.ota import Update_Ui_Dialog
from ui.tito import Tito_Ui_Dialog
from ui.motor import Motor_Ui_Dialog
from ui.box import Box_Ui_Dialog
from ui.udpbox import Udpbox_Ui_Dialog
from ui.udptito import Udp_Ui_Dialog
from ui.ucboard import Ucboard_Ui_Dialog
from ui.uds import Uds_Ui_Dialog
from ui.xtboard import Xt_Ui_Dialog

class MyWindow(QtGui.QMainWindow):

    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.createActions()
        self.createMenus()
        self.createToolBar()

    def createActions(self):
        self.deviceSelect=QtGui.QAction(self.trUtf8("设备设置"),self)
        self.deviceSelect.setShortcut("Ctrl+K")
        self.deviceSelect.setToolTip(self.trUtf8("设备设置"))
        self.connect(self.deviceSelect,QtCore.SIGNAL("triggered()"),self.deviceSetWindow)

        self.bboardtest=QtGui.QAction(self.trUtf8("Board-B"),self)
        self.bboardtest.setShortcut("Ctrl+B")
        self.bboardtest.setToolTip(self.trUtf8("Board-B"))
        #self.connect(self.deviceSelect,QtCore.SIGNAL("triggered()"),self.deviceSetWindow)

        self.cboardtest=QtGui.QAction(self.trUtf8("Board-C"),self)
        self.cboardtest.setShortcut("Ctrl+C")
        self.cboardtest.setToolTip(self.trUtf8("Board-C"))
        self.connect(self.cboardtest,QtCore.SIGNAL("triggered()"),self.cboardwindow)

        self.Ucboardtest=QtGui.QAction(self.trUtf8("UDP_CBoard"),self)
        self.Ucboardtest.setShortcut("Ctrl+X")
        self.Ucboardtest.setToolTip(self.trUtf8("UDP_CBoard"))
        self.connect(self.Ucboardtest,QtCore.SIGNAL("triggered()"),self.ucboardwindow)

        self.dboardtest=QtGui.QAction(self.trUtf8("Board-D"),self)
        self.dboardtest.setShortcut("Ctrl+D")
        self.dboardtest.setToolTip(self.trUtf8("Board-D"))
        self.connect(self.dboardtest,QtCore.SIGNAL("triggered()"),self.dboardwindow)

        self.titotest=QtGui.QAction(self.trUtf8("Titotest"),self)
        self.titotest.setShortcut("Ctrl+T")
        self.titotest.setToolTip(self.trUtf8("titotest"))
        self.connect(self.titotest,QtCore.SIGNAL("triggered()"),self.titowindow)

        self.udptitotest=QtGui.QAction(self.trUtf8("UDPTito"),self)
        self.udptitotest.setShortcut("Ctrl+U")
        self.udptitotest.setToolTip(self.trUtf8("UDPTito"))
        self.connect(self.udptitotest,QtCore.SIGNAL("triggered()"),self.udptitowindow)

        self.boxtest=QtGui.QAction(self.trUtf8("Boxtest"),self)
        self.boxtest.setShortcut("Ctrl+R")
        self.boxtest.setToolTip(self.trUtf8("boxtest"))
        self.connect(self.boxtest,QtCore.SIGNAL("triggered()"),self.boxwindow)

        self.udpboxtest=QtGui.QAction(self.trUtf8("Udpboxtest"),self)
        self.udpboxtest.setShortcut("Ctrl+F")
        self.udpboxtest.setToolTip(self.trUtf8("udpboxtest"))
        self.connect(self.udpboxtest,QtCore.SIGNAL("triggered()"),self.udpboxwindow)

        self.udparmtest=QtGui.QAction(self.trUtf8("ArmTest"),self)
        self.udparmtest.setShortcut("Ctrl+A")
        self.udparmtest.setToolTip(self.trUtf8("ArmTest"))
        #self.connect(self.udparmtest,QtCore.SIGNAL("triggered()"),self.udparmwindow)

        self.manual=QtGui.QAction(QtGui.QIcon("ui/icons/set.png"),self.trUtf8("手动维护"),self)
        self.manual.setShortcut("Ctrl+S")
        self.manual.setToolTip(self.trUtf8("手动维护"))
        self.connect(self.manual,QtCore.SIGNAL("triggered()"),self.loginselect)

        self.uds=QtGui.QAction(self.trUtf8("故障查询"),self)
        self.uds.setShortcut("Ctrl+F")
        self.uds.setToolTip(self.trUtf8("故障查询"))
        self.connect(self.uds,QtCore.SIGNAL("triggered()"),self.udsfind)

        self.versioncheck=QtGui.QAction(QtGui.QIcon("ui/icons/validation.png"),self.trUtf8("版本校验"),self)
        self.versioncheck.setShortcut("Ctrl+V")
        self.versioncheck.setToolTip(self.trUtf8("版本校验"))
        #self.connect(self.versioncheck,QtCore.SIGNAL("triggered()"),self.validationwin)
        self.autoversion=QtGui.QAction(self.trUtf8("一键获取版本"),self)
        self.autoversion.setShortcut("Ctrl+W")
        self.autoversion.setToolTip(self.trUtf8("一键获取版本"))
        self.connect(self.autoversion,QtCore.SIGNAL("triggered()"),self.autoversions)

        self.chaoshentest=QtGui.QAction(QtGui.QIcon("ui/icons/wifi.png"),self.trUtf8("2.4G测试"),self)
        self.chaoshentest.setShortcut("Ctrl+U")
        self.chaoshentest.setToolTip(self.trUtf8("2.4G测试"))

        self.lightest=QtGui.QAction(QtGui.QIcon("ui/icons/denguang.png"),self.trUtf8("灯光测试"),self)
        self.lightest.setShortcut("Ctrl+L")
        self.lightest.setToolTip(self.trUtf8("灯光测试"))

        self.gyrotest=QtGui.QAction(QtGui.QIcon("ui/icons/tuoluo.png"),self.trUtf8("陀螺仪测试"),self)
        self.gyrotest.setShortcut("Ctrl+G")
        self.gyrotest.setToolTip(self.trUtf8("陀螺仪测试"))

        self.motor=QtGui.QAction(QtGui.QIcon("ui/icons/montor.png"),self.trUtf8("电机测试"),self)
        self.motor.setShortcut("Ctrl+O")
        self.motor.setToolTip(self.trUtf8("电机测试"))

        self.downconfig=QtGui.QAction(QtGui.QIcon("ui/icons/montor.png"),self.trUtf8("获取配置"),self)
        self.downconfig.setShortcut("Ctrl+F")
        self.downconfig.setToolTip(self.trUtf8("获取配置"))
        self.connect(self.downconfig,QtCore.SIGNAL("triggered()"),self.getconfiger)

    def createToolBar(self):
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(self.lightest)
        self.toolbar.addAction(self.gyrotest)
        self.toolbar.addAction(self.chaoshentest)
        self.toolbar.addAction(self.motor)

    def createMenus(self):
        self.ui.menu.addAction(self.deviceSelect)
        self.ui.manual.addAction(self.manual)
        self.ui.toolmenu.addAction(self.versioncheck)
        self.ui.toolmenu.addAction(self.uds)
        self.ui.toolmenu.addAction(self.autoversion)
        self.ui.protomenu.addAction(self.bboardtest)
        self.ui.protomenu.addAction(self.cboardtest)
        self.ui.protomenu.addAction(self.Ucboardtest)
        self.ui.protomenu.addAction(self.dboardtest)
        self.ui.protomenu.addAction(self.titotest)
        self.ui.protomenu.addAction(self.boxtest)
        self.ui.protomenu.addAction(self.udpboxtest)
        self.ui.protomenu.addAction(self.udptitotest)
        self.ui.protomenu.addAction(self.udparmtest)

    def createContextMenuRemote(self):
        self.manualChild.remotelist.customContextMenuRequested.connect(self.showContextMenuRemote)

        self.contextMenuRemote = QtGui.QMenu(self)
        self.actionSRemote = self.contextMenuRemote.addAction(u'设为initMap')
        self.actionSRemote.triggered.connect(self.testmapinit)
        self.actionARemote = self.contextMenuRemote.addAction(u'设为Map0')
        self.actionARemote.triggered.connect(self.testmap0set)
        self.actionBRemote = self.contextMenuRemote.addAction(u'设为Map1')
        self.actionBRemote.triggered.connect(self.testmap1set)
        self.actionCRemote = self.contextMenuRemote.addAction(u'设为Map2')
        self.actionCRemote.triggered.connect(self.testmap2set)
        self.actionDRemote = self.contextMenuRemote.addAction(u'设为Map3')
        self.actionDRemote.triggered.connect(self.testmap3set)
        self.actionERemote = self.contextMenuRemote.addAction(u'设为Map4')
        self.actionERemote.triggered.connect(self.testmap4set)
        self.actionFRemote = self.contextMenuRemote.addAction(u'设为Map5')
        self.actionFRemote.triggered.connect(self.testmap5set)
        self.actionGRemote = self.contextMenuRemote.addAction(u'设为Map6')
        self.actionGRemote.triggered.connect(self.testmap6set)
        self.actionHRemote = self.contextMenuRemote.addAction(u'移除此项')
        self.actionHRemote.triggered.connect(self.testmapointclear)

    def showContextMenuRemote(self, pos):
        self.contextMenuRemote.move(self.pos() + pos)
        self.contextMenuRemote.exec_(QtGui.QCursor.pos())#设置在鼠标位置显示

    def createContextMenuLocal(self):
        self.manualChild.localist.customContextMenuRequested.connect(self.showContextMenuLocal)

        self.contextMenuLocal = QtGui.QMenu(self)
        self.actionSLocal = self.contextMenuLocal.addAction(u'设为initMap')
        self.actionSLocal.triggered.connect(self.testmapinit)
        self.actionALocal = self.contextMenuLocal.addAction(u'设为Map0')
        self.actionALocal.triggered.connect(self.testmap0set)
        self.actionBLocal = self.contextMenuLocal.addAction(u'设为Map1')
        self.actionBLocal.triggered.connect(self.testmap1set)
        self.actionCLocal = self.contextMenuLocal.addAction(u'设为Map2')
        self.actionCLocal.triggered.connect(self.testmap2set)
        self.actionDLocal = self.contextMenuLocal.addAction(u'设为Map3')
        self.actionDLocal.triggered.connect(self.testmap3set)
        self.actionELocal = self.contextMenuLocal.addAction(u'设为Map4')
        self.actionELocal.triggered.connect(self.testmap4set)
        self.actionFLocal = self.contextMenuLocal.addAction(u'设为Map5')
        self.actionFLocal.triggered.connect(self.testmap5set)
        self.actionGLocal = self.contextMenuLocal.addAction(u'设为Map6')
        self.actionGLocal.triggered.connect(self.testmap6set)
        self.actionHLocal = self.contextMenuLocal.addAction(u'移除此项')
        self.actionHLocal.triggered.connect(self.testmapointclear)

    def showContextMenuLocal(self, pos):
        self.contextMenuLocal.move(self.pos() + pos)
        self.contextMenuLocal.exec_(QtGui.QCursor.pos())#设置在鼠标位置显示

    def createContextMenuMap(self):
        self.manualChild.maplist.customContextMenuRequested.connect(self.showContextMenuMap)

        self.contextMenuMap = QtGui.QMenu(self)
        self.actionSMap = self.contextMenuMap.addAction(u'设为initMap')
        self.actionSMap.triggered.connect(self.testmapinit)

    def showContextMenuMap(self, pos):
        self.contextMenuMap.move(self.pos() + pos)
        self.contextMenuMap.exec_(QtGui.QCursor.pos())#设置在鼠标位置显示

    def createContextMenuduoji(self):
        try:
            self.titoChild.leftduojilist.customContextMenuRequested.connect(self.showContextMenuduoji)
        except:
            self.dboardChild.duojicontrol.customContextMenuRequested.connect(self.showContextMenuduoji)

        self.contextMenuduoji = QtGui.QMenu(self)
        self.actiononcmd = self.contextMenuduoji.addAction(u'无动作')
        self.actiononcmd.triggered.connect(self.duojinoncmd)
        self.actionopen = self.contextMenuduoji.addAction(u'打开')
        self.actionopen.triggered.connect(self.duojiopencmd)
        self.actionclose = self.contextMenuduoji.addAction(u'关闭')
        self.actionclose.triggered.connect(self.duojiclosecmd)

    def showContextMenuduoji(self, pos):
        self.contextMenuduoji.move(self.pos() + pos)
        self.contextMenuduoji.exec_(QtGui.QCursor.pos())#设置在鼠标位置显示

    def testmap0set(self):
        currentabindex=int(self.manualChild.maptablewidget.currentIndex())
        if currentabindex==0:
            currentmap=(unicode(self.manualChild.remotelist.currentItem().text()))
        else:
            currentmap=(unicode(self.manualChild.localist.currentItem().text()))
        mapattern='.+=.+'
        initpattern='.+initMap'
        if currentmap == u'无地图文件':
            pass
        else:
            if currentabindex==0:
                currentrow=self.manualChild.remotelist.currentRow()
                self.manualChild.remotelist.takeItem(currentrow)
            else:
                currentrow=self.manualChild.localist.currentRow()
                self.manualChild.localist.takeItem(currentrow)
            self.setmaplist(currentrow,'MAP0')
            #self.manualChild.maplist.takeItem(currentrow)#删除原有的站点
            match=re.search(mapattern,currentmap)
            if match:
                templist=currentmap.split('=')
                initmatch=re.search(initpattern,templist[1])
                if initmatch:
                    dumplist=templist[1].split('    ')
                    if currentabindex==0:
                        self.manualChild.remotelist.insertItem(currentrow,'MAP0 = '+dumplist[0])
                    else:
                        self.manualChild.localist.insertItem(currentrow,'MAP0 = '+dumplist[0])
                    self.writeinit('MAP0',dumplist[0],'None')
                else:
                    if currentabindex==0:
                        self.manualChild.remotelist.insertItem(currentrow,'MAP0 = '+templist[1])
                    else:
                        self.manualChild.localist.insertItem(currentrow,'MAP0 = '+templist[1])
                    self.writeinit('MAP0',templist[1],'None')
            else:
                if currentabindex==0:
                    self.manualChild.remotelist.insertItem(currentrow,'MAP0 = '+currentmap)
                else:
                    self.manualChild.localist.insertItem(currentrow,'MAP0 = '+currentmap)
                self.writeinit('MAP0',currentmap,'None')
            if currentabindex==0:
                self.manualChild.remotelist.setCurrentRow(currentrow)
            else:
                self.manualChild.localist.setCurrentRow(currentrow)

    def testmap1set(self):
        currentabindex=int(self.manualChild.maptablewidget.currentIndex())
        if currentabindex==0:
            currentmap=(unicode(self.manualChild.remotelist.currentItem().text()))
        else:
            currentmap=(unicode(self.manualChild.localist.currentItem().text()))
        mapattern='.+=.+'
        initpattern='.+initMap'
        if currentmap == u'无地图文件':
            pass
        else:
            if currentabindex==0:
                currentrow=self.manualChild.remotelist.currentRow()
                self.manualChild.remotelist.takeItem(currentrow)
            else:
                currentrow=self.manualChild.localist.currentRow()
                self.manualChild.localist.takeItem(currentrow)
            self.setmaplist(currentrow,'MAP1')
            #self.manualChild.maplist.takeItem(currentrow)#删除原有的站点
            match=re.search(mapattern,currentmap)
            if match:
                templist=currentmap.split('=')
                initmatch=re.search(initpattern,templist[1])
                if initmatch:
                    dumplist=templist[1].split('    ')
                    if currentabindex==0:
                        self.manualChild.remotelist.insertItem(currentrow,'MAP1 = '+dumplist[0])
                    else:
                        self.manualChild.localist.insertItem(currentrow,'MAP1 = '+dumplist[0])
                    self.writeinit('MAP1',dumplist[0],'None')
                else:
                    if currentabindex==0:
                        self.manualChild.remotelist.insertItem(currentrow,'MAP1 = '+templist[1])
                    else:
                        self.manualChild.localist.insertItem(currentrow,'MAP1 = '+templist[1])
                    self.writeinit('MAP1',templist[1],'None')
            else:
                if currentabindex==0:
                    self.manualChild.remotelist.insertItem(currentrow,'MAP1 = '+currentmap)
                else:
                    self.manualChild.localist.insertItem(currentrow,'MAP1 = '+currentmap)
                self.writeinit('MAP1',currentmap,'None')
            if currentabindex==0:
                self.manualChild.remotelist.setCurrentRow(currentrow)
            else:
                self.manualChild.localist.setCurrentRow(currentrow)

    def testmap2set(self):
        currentabindex=int(self.manualChild.maptablewidget.currentIndex())
        if currentabindex==0:
            currentmap=(unicode(self.manualChild.remotelist.currentItem().text()))
        else:
            currentmap=(unicode(self.manualChild.localist.currentItem().text()))
        mapattern='.+=.+'
        initpattern='.+initMap'
        if currentmap == u'无地图文件':
            pass
        else:
            if currentabindex==0:
                currentrow=self.manualChild.remotelist.currentRow()
                self.manualChild.remotelist.takeItem(currentrow)
            else:
                currentrow=self.manualChild.localist.currentRow()
                self.manualChild.localist.takeItem(currentrow)
            self.setmaplist(currentrow,'MAP2')
            #self.manualChild.maplist.takeItem(currentrow)#删除原有的站点
            match=re.search(mapattern,currentmap)
            if match:
                templist=currentmap.split('=')
                initmatch=re.search(initpattern,templist[1])
                if initmatch:
                    dumplist=templist[1].split('    ')
                    if currentabindex==0:
                        self.manualChild.remotelist.insertItem(currentrow,'MAP2 = '+dumplist[0])
                    else:
                        self.manualChild.localist.insertItem(currentrow,'MAP2 = '+dumplist[0])
                    self.writeinit('MAP2',dumplist[0],'None')
                else:
                    if currentabindex==0:
                        self.manualChild.remotelist.insertItem(currentrow,'MAP2 = '+templist[1])
                    else:
                        self.manualChild.localist.insertItem(currentrow,'MAP2 = '+templist[1])
                    self.writeinit('MAP2',templist[1],'None')
            else:
                if currentabindex==0:
                    self.manualChild.remotelist.insertItem(currentrow,'MAP2 = '+currentmap)
                else:
                    self.manualChild.localist.insertItem(currentrow,'MAP2 = '+currentmap)
                self.writeinit('MAP2',currentmap,'None')
            if currentabindex==0:
                self.manualChild.remotelist.setCurrentRow(currentrow)
            else:
                self.manualChild.localist.setCurrentRow(currentrow)

    def testmap3set(self):
        currentabindex=int(self.manualChild.maptablewidget.currentIndex())
        if currentabindex==0:
            currentmap=(unicode(self.manualChild.remotelist.currentItem().text()))
        else:
            currentmap=(unicode(self.manualChild.localist.currentItem().text()))
        mapattern='.+=.+'
        initpattern='.+initMap'
        if currentmap == u'无地图文件':
            pass
        else:
            if currentabindex==0:
                currentrow=self.manualChild.remotelist.currentRow()
                self.manualChild.remotelist.takeItem(currentrow)
            else:
                currentrow=self.manualChild.localist.currentRow()
                self.manualChild.localist.takeItem(currentrow)
            self.setmaplist(currentrow,'MAP3')
            #self.manualChild.maplist.takeItem(currentrow)#删除原有的站点
            match=re.search(mapattern,currentmap)
            if match:
                templist=currentmap.split('=')
                initmatch=re.search(initpattern,templist[1])
                if initmatch:
                    dumplist=templist[1].split('    ')
                    if currentabindex==0:
                        self.manualChild.remotelist.insertItem(currentrow,'MAP3 = '+dumplist[0])
                    else:
                        self.manualChild.localist.insertItem(currentrow,'MAP3 = '+dumplist[0])
                    self.writeinit('MAP3',dumplist[0],'None')
                else:
                    if currentabindex==0:
                        self.manualChild.remotelist.insertItem(currentrow,'MAP3 = '+templist[1])
                    else:
                        self.manualChild.localist.insertItem(currentrow,'MAP3 = '+templist[1])
                    self.writeinit('MAP3',templist[1],'None')
            else:
                if currentabindex==0:
                    self.manualChild.remotelist.insertItem(currentrow,'MAP3 = '+currentmap)
                else:
                    self.manualChild.localist.insertItem(currentrow,'MAP3 = '+currentmap)
                self.writeinit('MAP3',currentmap,'None')
            if currentabindex==0:
                self.manualChild.remotelist.setCurrentRow(currentrow)
            else:
                self.manualChild.localist.setCurrentRow(currentrow)

    def testmap4set(self):
        currentabindex=int(self.manualChild.maptablewidget.currentIndex())
        if currentabindex ==0:
            currentmap=(unicode(self.manualChild.remotelist.currentItem().text()))
        else:
            currentmap=(unicode(self.manualChild.localist.currentItem().text()))
        mapattern='.+=.+'
        initpattern='.+initMap'
        if currentmap == u'无地图文件':
            pass
        else:
            if currentabindex==0:
                currentrow=self.manualChild.remotelist.currentRow()
                self.manualChild.remotelist.takeItem(currentrow)
            else:
                currentrow=self.manualChild.localist.currentRow()
                self.manualChild.localist.takeItem(currentrow)
            self.setmaplist(currentrow,'MAP4')
            #self.manualChild.maplist.takeItem(currentrow)#删除原有的站点
            match=re.search(mapattern,currentmap)
            if match:
                templist=currentmap.split('=')
                initmatch=re.search(initpattern,templist[1])
                if initmatch:
                    dumplist=templist[1].split('    ')
                    if currentabindex==0:
                        self.manualChild.remotelist.insertItem(currentrow,'MAP4 = '+dumplist[0])
                    else:
                        self.manualChild.localist.insertItem(currentrow,'MAP4 = '+dumplist[0])
                    self.writeinit('MAP4',dumplist[0],'None')
                else:
                    if currentabindex==0:
                        self.manualChild.remotelist.insertItem(currentrow,'MAP4 = '+templist[1])
                    else:
                        self.manualChild.localist.insertItem(currentrow,'MAP4 = '+templist[1])
                    self.writeinit('MAP4',templist[1],'None')
            else:
                if currentabindex==0:
                    self.manualChild.remotelist.insertItem(currentrow,'MAP4 = '+currentmap)
                else:
                    self.manualChild.localist.insertItem(currentrow,'MAP4 = '+currentmap)
                self.writeinit('MAP4',currentmap,'None')
            if currentabindex==0:
                self.manualChild.remotelist.setCurrentRow(currentrow)
            else:
                self.manualChild.localist.setCurrentRow(currentrow)

    def testmap5set(self):
        currentabindex=int(self.manualChild.maptablewidget.currentIndex())
        if currentabindex==0:
            currentmap=(unicode(self.manualChild.remotelist.currentItem().text()))
        else:
            currentmap=(unicode(self.manualChild.localist.currentItem().text()))
        mapattern='.+=.+'
        initpattern='.+initMap'
        if currentmap == u'无地图文件':
            pass
        else:
            if currentabindex==0:
                currentrow=self.manualChild.remotelist.currentRow()
                self.manualChild.remotelist.takeItem(currentrow)
            else:
                currentrow=self.manualChild.localist.currentRow()
                self.manualChild.localist.takeItem(currentrow)
            self.setmaplist(currentrow,'MAP5')
            #self.manualChild.maplist.takeItem(currentrow)#删除原有的站点
            match=re.search(mapattern,currentmap)
            if match:
                templist=currentmap.split('=')
                initmatch=re.search(initpattern,templist[1])
                if initmatch:
                    dumplist=templist[1].split('    ')
                    if currentabindex==0:
                        self.manualChild.remotelist.insertItem(currentrow,'MAP5 = '+dumplist[0])
                    else:
                        self.manualChild.localist.insertItem(currentrow,'MAP5 = '+dumplist[0])
                    self.writeinit('MAP5',dumplist[0],'None')
                else:
                    if currentabindex==0:
                        self.manualChild.remotelist.insertItem(currentrow,'MAP5 = '+templist[1])
                    else:
                        self.manualChild.localist.insertItem(currentrow,'MAP5 = '+templist[1])
                    self.writeinit('MAP5',templist[1],'None')
            else:
                if currentabindex==0:
                    self.manualChild.remotelist.insertItem(currentrow,'MAP5 = '+currentmap)
                else:
                    self.manualChild.localist.insertItem(currentrow,'MAP5 = '+currentmap)
                self.writeinit('MAP5',currentmap,'None')
            if currentabindex==0:
                self.manualChild.remotelist.setCurrentRow(currentrow)
            else:
                self.manualChild.localist.setCurrentRow(currentrow)

    def testmap6set(self):
        currentabindex=int(self.manualChild.maptablewidget.currentIndex())
        if currentabindex ==0:
            currentmap=(unicode(self.manualChild.remotelist.currentItem().text()))
        else:
            currentmap=(unicode(self.manualChild.localist.currentItem().text()))
        mapattern='.+=.+'
        initpattern='.+initMap'
        if currentmap == u'无地图文件':
            pass
        else:
            if currentabindex == 0:
                currentrow=self.manualChild.remotelist.currentRow()
                self.manualChild.remotelist.takeItem(currentrow)
            else:
                currentrow=self.manualChild.localist.currentRow()
                self.manualChild.localist.takeItem(currentrow)
            self.setmaplist(currentrow,'MAP6')
            #self.manualChild.maplist.takeItem(currentrow)#删除原有的站点
            match=re.search(mapattern,currentmap)
            if match:
                templist=currentmap.split('=')
                initmatch=re.search(initpattern,templist[1])
                if initmatch:
                    dumplist=templist[1].split('    ')
                    if currentabindex==0:
                        self.manualChild.remotelist.insertItem(currentrow,'MAP6 = '+dumplist[0])
                    else:
                        self.manualChild.localist.insertItem(currentrow,'MAP6 = '+dumplist[0])
                    self.writeinit('MAP6',dumplist[0],'None')
                else:
                    if currentabindex == 0:
                        self.manualChild.remotelist.insertItem(currentrow,'MAP6 = '+templist[1])
                    else:
                        self.manualChild.localist.insertItem(currentrow,'MAP6 = '+templist[1])
                    self.writeinit('MAP6',templist[1],'None')
            else:
                if currentabindex==0:
                    self.manualChild.remotelist.insertItem(currentrow,'MAP6 = '+currentmap)
                else:
                    self.manualChild.localist.insertItem(currentrow,'MAP6 = '+currentmap)
                self.writeinit('MAP6',currentmap,'None')
            if currentabindex==0:
                self.manualChild.remotelist.setCurrentRow(currentrow)
            else:
                self.manualChild.localist.setCurrentRow(currentrow)

    def testmapointclear(self):
        currentabindex=int(self.manualChild.maptablewidget.currentIndex())
        if currentabindex ==0:
            currentmap=(unicode(self.manualChild.remotelist.currentItem().text()))
        else:
            currentmap=(unicode(self.manualChild.localist.currentItem().text()))
        if currentmap == u'无地图文件':
            pass
        else:
            if currentabindex == 0:
                currentrow=self.manualChild.remotelist.currentRow()
                self.manualChild.remotelist.takeItem(currentrow)
            else:
                currentrow=self.manualChild.localist.currentRow()
                self.manualChild.localist.takeItem(currentrow)

    def testmapinit(self):
        self.manualChild.mapname.clear()
        currentabindex=int(self.manualChild.maptablewidget.currentIndex())
        if currentabindex == 2:
            currentrow=self.manualChild.maplist.currentRow()
            currentmap=(unicode(self.manualChild.maplist.currentItem().text()))
        elif currentabindex == 0:
            currentrow=self.manualChild.remotelist.currentRow()
            currentmap=(unicode(self.manualChild.remotelist.currentItem().text()))
        else:
            currentrow=self.manualChild.localist.currentRow()
            currentmap=(unicode(self.manualChild.localist.currentItem().text()))
        self.setinitmaplist(currentrow)#先除去已经有的initMap
        mapattern='.+=.+'
        initpattern='.+initMap'
        if currentmap == u'无地图文件':
            pass
        else:
            if currentabindex == 2:
                self.manualChild.maplist.takeItem(currentrow)
            elif currentabindex==0:
                self.manualChild.remotelist.takeItem(currentrow)
            else:
                self.manualChild.localist.takeItem(currentrow)
            match=re.search(mapattern,currentmap)
            if match:#已经设置过MPx
                self.manualChild.mapnum.clear()
                templist=currentmap.split('=')
                self.manualChild.mapnum.setText(templist[0][3])
                initmatch=re.search(initpattern,templist[1])
                if initmatch:#名称已经带有initMap
                    if currentabindex == 2:
                        self.manualChild.maplist.insertItem(currentrow,currentmap)
                    elif currentabindex == 0:
                        self.manualChild.remotelist.insertItem(currentrow,currentmap)
                    else:
                        self.manualChild.localist.insertItem(currentrow,currentmap)
                    mapn=templist[1].rstrip('    initMap')
                    self.manualChild.mapname.setText(mapn)
                else:
                    self.manualChild.mapname.setText(templist[1])
                    if currentabindex == 2:
                        self.manualChild.maplist.insertItem(currentrow,currentmap+'    initMap')
                    elif currentabindex == 0:
                        self.manualChild.remotelist.insertItem(currentrow,currentmap+'    initMap')
                    else:
                        self.manualChild.localist.insertItem(currentrow,currentmap+'    initMap')
            else:#原始地图名称
                self.manualChild.mapname.setText(currentmap)
                initmapnum=str(self.manualChild.mapnum.toPlainText())
                mapindex='MAP'+initmapnum
                if currentabindex == 2:
                    self.manualChild.maplist.insertItem(currentrow,mapindex+'='+currentmap+'    initMap')
                elif currentabindex == 0:
                    self.manualChild.remotelist.insertItem(currentrow,mapindex+'='+currentmap+'    initMap')
                else:
                    self.manualChild.localist.insertItem(currentrow,mapindex+'='+currentmap+'    initMap')
            if currentabindex == 2:
                self.manualChild.maplist.setCurrentRow(currentrow)
            elif currentabindex ==0:
                self.manualChild.remotelist.setCurrentRow(currentrow)
            else:
                self.manualChild.localist.setCurrentRow(currentrow)

    def setinitmaplist(self,row):
        currentabindex=int(self.manualChild.maptablewidget.currentIndex())
        if currentabindex == 2:
            itemCount=int(self.manualChild.maplist.count())
        elif currentabindex == 0:
            itemCount=int(self.manualChild.remotelist.count())
        else:
            itemCount=int(self.manualChild.localist.count())
        initpattern='.+initMap'
        for itemindex in range(0,itemCount):
            if itemindex == row:
                pass
            else:
                if currentabindex == 2:
                    currentitem=str(self.manualChild.maplist.item(itemindex).text())
                elif currentabindex == 0:
                    currentitem=str(self.manualChild.remotelist.item(itemindex).text())
                else:
                    currentitem=str(self.manualChild.localist.item(itemindex).text())
                initmatch=re.search(initpattern,currentitem)
                if initmatch:
                    temp=currentitem.split('    ')
                    if int(self.manualChild.maptablewidget.currentIndex()) == 2:
                        self.manualChild.maplist.takeItem(itemindex)
                        self.manualChild.maplist.insertItem(itemindex,temp[0])
                    else:
                        templist=temp[0].split('=')
                        mapitem=templist[1]
                        if currentabindex == 0:
                            self.manualChild.remotelist.takeItem(itemindex)
                            self.manualChild.remotelist.insertItem(itemindex,mapitem)
                        else:
                            self.manualChild.localist.takeItem(itemindex)
                            self.manualChild.localist.insertItem(itemindex,mapitem)
                else:
                    pass

    def setmaplist(self,row,mapsn):
        currentabindex=int(self.manualChild.maptablewidget.currentIndex())
        if currentabindex == 2:
            itemCount=int(self.manualChild.maplist.count())
        elif currentabindex ==0:
            itemCount=int(self.manualChild.remotelist.count())
        else:
            itemCount=int(self.manualChild.localist.count())
        mapattern=mapsn+'.+'
        initmapattern='.+initMap'
        for itemindex in range(0,itemCount):
            if itemindex == row:
                pass
            else:
                if currentabindex == 2:
                    currentitem=str(self.manualChild.maplist.item(itemindex).text())
                elif currentabindex ==0:
                    currentitem=str(self.manualChild.remotelist.item(itemindex).text())
                else:
                    currentitem=str(self.manualChild.localist.item(itemindex).text())
                mapmatch=re.search(mapattern,currentitem)
                if mapmatch:
                    tempmaplist=currentitem.split('=')
                    initmatch=re.search(initmapattern,tempmaplist[1])
                    if initmatch:
                        mapitem=tempmaplist[1].rstrip('    initMap')
                    else:
                        mapitem=tempmaplist[1]
                    if currentabindex == 2:
                        self.manualChild.maplist.takeItem(itemindex)
                        self.manualChild.maplist.insertItem(itemindex,mapitem)
                    elif currentabindex ==0:
                        self.manualChild.remotelist.takeItem(itemindex)
                        self.manualChild.remotelist.insertItem(itemindex,mapitem)
                    else:
                        self.manualChild.localist.takeItem(itemindex)
                        self.manualChild.localist.insertItem(itemindex,mapitem)
                else:
                    pass

    def writeinit(self,datatype,placeindex,initnum):
        self.writer=initwriter(datatype,placeindex,initnum)
        self.writer.mapwriteSingnal.connect(self.mapwriteresult)
        self.writer.start()

    def mapwriteresult(self,result):
        self.manualChild.textBrowser.append(u'已写入'+result+u'至本地yogoCC.ini文件')

    def duojinoncmd(self):
        currentestitem=unicode(self.titoChild.leftduojilist.currentItem().text())
        currentrow=self.titoChild.leftduojilist.currentRow()
        itemlist=currentestitem.split('    ')
        self.titoChild.leftduojilist.takeItem(currentrow)
        self.titoChild.leftduojilist.insertItem(currentrow,itemlist[0]+u'    NoAction')
        self.titoChild.leftduojilist.setCurrentRow(currentrow)

    def duojiopencmd(self):
        currentestitem=unicode(self.titoChild.leftduojilist.currentItem().text())
        currentrow=self.titoChild.leftduojilist.currentRow()
        itemlist=currentestitem.split('    ')
        self.titoChild.leftduojilist.takeItem(currentrow)
        self.titoChild.leftduojilist.insertItem(currentrow,itemlist[0]+u'    OPEN')
        self.titoChild.leftduojilist.setCurrentRow(currentrow)

    def duojiclosecmd(self):
        currentestitem=unicode(self.titoChild.leftduojilist.currentItem().text())
        currentrow=self.titoChild.leftduojilist.currentRow()
        itemlist=currentestitem.split('    ')
        self.titoChild.leftduojilist.takeItem(currentrow)
        self.titoChild.leftduojilist.insertItem(currentrow,itemlist[0]+u'    CLOSE')
        self.titoChild.leftduojilist.setCurrentRow(currentrow)

    def udsfind(self):
        self.udsChild = Uds_Ui_Dialog()
        self.Dialog = QtGui.QDialog(self)
        self.udsChild.setupUi(self.Dialog)

        self.udsChild.start.clicked.connect(self.udstart)

        self.Dialog.exec_()

    def udstart(self):
        devnum=str(self.udsChild.device.toPlainText()).lstrip(' ').rstrip(' ')
        if devnum=='':
            QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("请先设置机器编号"))
        else:
            #deviceip='10.42.5.'+devnum
            deviceip='192.168.80.201'
            self.udser=Udsthread(deviceip)
            self.udser.listSingnal.connect(self.udsupdate)
            self.udser.start()

    def udsupdate(self,messlist):
        self.udsChild.inch.setText(str(messlist[0]).decode('utf-8'))
        self.udsChild.fall.setText(str(messlist[1]).decode('utf-8'))
        self.udsChild.chargestat.setText(str(messlist[2]).decode('utf-8'))
        self.udsChild.soc.setProperty('value',messlist[3])
        bid=messlist[4]
        if bid=='ee':
            self.udsChild.errcode.setText(str(messlist[5]).decode('utf-8'))
        elif bid=='11':
            self.udsChild.leftmotorpos.setText(str(messlist[5]).decode('utf-8'))
        elif bid=='12':
            self.udsChild.rightmotorpos.setText(str(messlist[5]).decode('utf-8'))
        elif bid=='61':
            self.udsChild.leftwei1.setText(str(messlist[5]).decode('utf-8'))
        elif bid=='62':
            self.udsChild.rightwei1.setText(str(messlist[5]).decode('utf-8'))
        elif bid=='51':
            self.udsChild.irf1.setText(str(messlist[5]).decode('utf-8'))
        elif bid=='52':
            self.udsChild.irf2.setText(str(messlist[5]).decode('utf-8'))
        elif bid=='53':
            self.udsChild.irf3.setText(str(messlist[5]).decode('utf-8'))
        elif bid=='54':
            self.udsChild.irf4.setText(str(messlist[5]).decode('utf-8'))
        elif bid=='55':
            self.udsChild.irf5.setText(str(messlist[5]).decode('utf-8'))
        elif bid=='56':
            self.udsChild.irf6.setText(str(messlist[5]).decode('utf-8'))
        elif bid=='57':
            self.udsChild.irf7.setText(str(messlist[5]).decode('utf-8'))
        elif bid=='58':
            self.udsChild.irf8.setText(str(messlist[5]).decode('utf-8'))
        elif bid=='59':
            self.udsChild.irf9.setText(str(messlist[5]).decode('utf-8'))
        elif bid=='5a':
            self.udsChild.irfA.setText(str(messlist[5]).decode('utf-8'))
        elif bid=='25' or bid=='27':
            errinfo=str(messlist[5]).decode('utf-8')
            if errinfo==u'电机1关门位置严重错误' or errinfo==u'电机1关门角度太小' or errinfo==u'电机1关门角度太大':
                self.udsChild.leftupdoor.setText(str(messlist[5]).decode('utf-8'))
            elif errinfo==u'电机2关门位置严重错误' or errinfo==u'电机2关门角度太小' or errinfo==u'电机2关门角度太大':
                self.udsChild.leftdowndoor.setText(str(messlist[5]).decode('utf-8'))
            else:
                self.udsChild.leftupdoor.setText(str(messlist[5]).decode('utf-8'))
                self.udsChild.leftdowndoor.setText(str(messlist[5]).decode('utf-8'))
        elif bid=='26' or bid=='28':
            errinfo=str(messlist[5]).decode('utf-8')
            if errinfo==u'电机1关门位置严重错误' or errinfo==u'电机1关门角度太小' or errinfo==u'电机1关门角度太大':
                self.udsChild.rightupdoor.setText(str(messlist[5]).decode('utf-8'))
            elif errinfo==u'电机2关门位置严重错误' or errinfo==u'电机2关门角度太小' or errinfo==u'电机2关门角度太大':
                self.udsChild.rightdowndoor.setText(str(messlist[5]).decode('utf-8'))
            else:
                self.udsChild.rightupdoor.setText(str(messlist[5]).decode('utf-8'))
                self.udsChild.rightdowndoor.setText(str(messlist[5]).decode('utf-8'))
        elif bid=='e1':
            self.udsChild.fuyang.setText(str(messlist[5]).decode('utf-8'))
        else:
            pass

    def motorwindow(self,direct):
        self.mboardChild = Motor_Ui_Dialog()
        self.Dialog = QtGui.QDialog(self)
        self.mboardChild.setupUi(self.Dialog)

        global motorwin
        motorwin=self.mboardChild

        if direct==1:
            self.mboardChild.leftmotordial.setEnabled(True)
            self.mboardChild.leftmotorvalue.setEnabled(True)
        elif direct==2:
            self.mboardChild.rightmotordial.setEnabled(True)
            self.mboardChild.rightmotorvalue.setEnabled(True)
        else:
            self.mboardChild.leftmotordial.setEnabled(True)
            self.mboardChild.leftmotorvalue.setEnabled(True)
            self.mboardChild.rightmotordial.setEnabled(True)
            self.mboardChild.rightmotorvalue.setEnabled(True)
        self.connect(self.mboardChild.leftmotordial, QtCore.SIGNAL("valueChanged(int)"),self.mboardChild.leftmotorvalue.setValue)
        self.connect(self.mboardChild.leftmotorvalue, QtCore.SIGNAL("valueChanged(int)"),self.mboardChild.leftmotordial.setValue)
        self.connect(self.mboardChild.rightmotordial, QtCore.SIGNAL("valueChanged(int)"),self.mboardChild.rightmotorvalue.setValue)
        self.connect(self.mboardChild.rightmotorvalue, QtCore.SIGNAL("valueChanged(int)"),self.mboardChild.rightmotordial.setValue)
        self.mboardChild.test.clicked.connect(self.startest)
        self.mboardChild.stop.clicked.connect(self.stoptest)

        self.Dialog.exec_()

    def startest(self):
        stopflagexist=os.path.exists('log/motorstop.txt')
        if stopflagexist:
            os.remove('log/motorstop.txt')
        self.moter=motorthread()
        self.moter.countSingnal.connect(self.motorclear)
        self.moter.frameSingnal.connect(self.motorany)
        self.moter.messSingnal.connect(self.motormess)
        self.moter.start()

    def motorclear(self,count):
        if count>=30:
            self.mboardChild.titomessage.clear()

    def motorany(self,mess,motype):
        warringcode=mess[6:8]
        errcode=mess[8:10]
        if motype==3:
            pass
        elif motype==2:
            if self.mboardChild.comboBox_2.currentText() == u'正向':
                speedcode=str(mess[14]+mess[15]+mess[12]+mess[13])
                speed=int(speedcode,16)
            else:
                tempcode=str(mess[14]+mess[15]+mess[12]+mess[13])
                temp=int(tempcode,16)
                speed=65535-temp

            warring=u'右电机warringcode:'+warringcode
            err=u'右电机errcode:'+errcode
            speedstr=u'右电机速度:'+str(speed)
            self.mboardChild.titomessage.append(warring)
            self.mboardChild.titomessage.append(err)
            self.mboardChild.titomessage.append(speedstr)
        elif motype ==1:
            if self.mboardChild.comboBox_2.currentText() == u'正向':
                speedcode=str(mess[14]+mess[15]+mess[12]+mess[13])
                speed=int(speedcode,16)
            else:
                tempcode=str(mess[14]+mess[15]+mess[12]+mess[13])
                temp=int(tempcode,16)
                speed=65535-temp
            warring=u'左电机warringcode:'+warringcode
            err=u'左电机errcode:'+errcode
            speedstr=u'左电机速度:'+str(speed)
            self.mboardChild.titomessage.append(warring)
            self.mboardChild.titomessage.append(err)
            self.mboardChild.titomessage.append(speedstr)
        else:
            pass

    def motormess(self,mess):
        self.mboardChild.titomessage.append(mess)

    def stoptest(self):
        f=open('log/motorstop.txt','a')
        f.write('stop')
        f.close()

    def putconfig(self):
        pass

    def autoversions(self):
        pass

    def xtwindow(self):
        global xtwin
        self.xtboardChild = Xt_Ui_Dialog()
        self.Dialog = QtGui.QDialog(self)
        self.xtboardChild.setupUi(self.Dialog)

        xtwin=self.xtboardChild

        self.xtboardChild.uplock.clicked.connect(self.xtuplock)
        self.xtboardChild.upunlock.clicked.connect(self.xtupunlock)
        self.xtboardChild.downlock.clicked.connect(self.xtdownlock)
        self.xtboardChild.downunlock.clicked.connect(self.xtdownunlock)
        self.xtboardChild.uplighton.clicked.connect(self.xtuplighton)
        self.xtboardChild.uplightoff.clicked.connect(self.xtuplightoff)
        self.xtboardChild.downlighton.clicked.connect(self.xtdownlighton)
        self.xtboardChild.downlightoff.clicked.connect(self.xtdownlightoff)
        self.xtboardChild.start.clicked.connect(self.xtstartest)
        self.xtboardChild.pause.clicked.connect(self.xtpause)
        self.xtboardChild.manual.clicked.connect(self.xtmanual)
        self.xtboardChild.manpause.clicked.connect(self.xtmanpause)

        self.Dialog.exec_()

    def xtuplock(self):
        self.xtboardChild.uplock.setChecked(True)
        self.xtboardChild.upunlock.setChecked(False)

    def xtupunlock(self):
        self.xtboardChild.uplock.setChecked(False)
        self.xtboardChild.upunlock.setChecked(True)

    def xtdownlock(self):
        self.xtboardChild.downlock.setChecked(True)
        self.xtboardChild.downunlock.setChecked(False)

    def xtdownunlock(self):
        self.xtboardChild.downlock.setChecked(False)
        self.xtboardChild.downunlock.setChecked(True)

    def xtuplighton(self):
        self.xtboardChild.uplighton.setChecked(True)
        self.xtboardChild.uplightoff.setChecked(False)

    def xtuplightoff(self):
        self.xtboardChild.uplighton.setChecked(False)
        self.xtboardChild.uplightoff.setChecked(True)

    def xtdownlighton(self):
        self.xtboardChild.downlighton.setChecked(True)
        self.xtboardChild.downlightoff.setChecked(False)

    def xtdownlightoff(self):
        self.xtboardChild.downlighton.setChecked(False)
        self.xtboardChild.downlightoff.setChecked(True)

    def xtpause(self):
        self.xtboardChild.manual.setEnabled(True)
        f=open('ui/xtstop.txt','w')
        f.write('xtstoped')
        f.close()

    def xtstartest(self):
        self.xtboardChild.uplock.setEnabled(False)
        self.xtboardChild.upunlock.setEnabled(False)
        self.xtboardChild.downlock.setEnabled(False)
        self.xtboardChild.downunlock.setEnabled(False)
        self.xtboardChild.uplighton.setEnabled(False)
        self.xtboardChild.uplightoff.setEnabled(False)
        self.xtboardChild.downlighton.setEnabled(False)
        self.xtboardChild.downlightoff.setEnabled(False)
        self.xtboardChild.manual.setDisabled(True)
        titostopexist=os.path.exists('ui/xtstop.txt')
        if titostopexist:
            os.remove('ui/xtstop.txt')
        boardtype=unicode(self.dboardChild.boardlist.currentItem().text())
        if boardtype==u'左箱体控制板':
            self.xtester=xthread(0)
        elif boardtype==u'右箱体控制板':
            self.xtester=xthread(1)
        else:
            self.xtester=xthread(2)

        self.xtester.listSingnal.connect(self.xtany)
        self.xtester.start()

    def xtany(self,framelist):
        self.xtboardChild.warr.setText(framelist[0])
        self.xtboardChild.err.setText(framelist[1])
        self.xtboardChild.upwei.setText(framelist[2])
        self.xtboardChild.downwei.setText(framelist[3])
        self.xtboardChild.upswitch.setText(str(framelist[4]).decode('utf-8'))
        self.xtboardChild.downswitch.setText(str(framelist[5]).decode('utf-8'))

    def xtmanual(self):
        self.xtboardChild.uplock.setEnabled(True)
        self.xtboardChild.upunlock.setEnabled(True)
        self.xtboardChild.downlock.setEnabled(True)
        self.xtboardChild.downunlock.setEnabled(True)
        self.xtboardChild.uplighton.setEnabled(True)
        self.xtboardChild.uplightoff.setEnabled(True)
        self.xtboardChild.downlighton.setEnabled(True)
        self.xtboardChild.downlightoff.setEnabled(True)
        self.xtboardChild.start.setDisabled(True)
        titostopexist=os.path.exists('ui/xtmanualstop.txt')
        if titostopexist:
            os.remove('ui/xtmanualstop.txt')
        boardtype=unicode(self.dboardChild.boardlist.currentItem().text())
        if boardtype==u'左箱体控制板':
            self.xtester=manualxthread(0)
        elif boardtype==u'右箱体控制板':
            self.xtester=manualxthread(1)
        else:
            self.xtester=manualxthread(2)

        self.xtester.listSingnal.connect(self.xtmanualany)
        self.xtester.start()

    def xtmanpause(self):
        self.xtboardChild.start.setEnabled(True)
        f=open('ui/xtmanualstop.txt','w')
        f.write('xtmanualstop')
        f.close()

    def xtmanualany(self,framelist):
        self.xtboardChild.warr.setText(framelist[0])
        self.xtboardChild.err.setText(framelist[1])
        self.xtboardChild.upwei.setText(framelist[2])
        self.xtboardChild.downwei.setText(framelist[3])
        self.xtboardChild.upswitch.setText(str(framelist[4]).decode('utf-8'))
        self.xtboardChild.downswitch.setText(str(framelist[5]).decode('utf-8'))

    def dboardwindow(self):
        self.dboardChild = Dboard_Ui_Dialog()
        self.Dialog = QtGui.QDialog(self)
        self.dboardChild.setupUi(self.Dialog)

        global dboardwin
        dboardwin=self.dboardChild

        self.dboardsertimer=QtCore.QTimer(self)
        self.dboardsertimer.setSingleShot(True)
        self.dboardsertimer.timeout.connect(self.dboardserautoget)
        self.dboardsertimer.start(10)

        self.dboardChild.otalist.itemDoubleClicked.connect(self.dotaupdate)
        self.dboardChild.boardlist.itemClicked.connect(self.dtestitemupdate)
        self.dboardChild.boardlist.itemDoubleClicked.connect(self.boardcontrol)
        self.dboardChild.testitem.itemClicked.connect(self.dtestupdate)
        self.dboardChild.testitem.itemDoubleClicked.connect(self.dstartest)
        self.dboardChild.testitem_2.itemDoubleClicked.connect(self.dstarttestitem)
        self.dboardChild.testitem_2.itemClicked.connect(self.writenable)
        self.dboardChild.clear.clicked.connect(self.dclear)
        self.dboardChild.modelset.clicked.connect(self.cutmodel)
        self.dboardChild.close.clicked.connect(self.dclose)
        self.dboardChild.serialset.clicked.connect(self.YGtestdboardSer)

        self.dboardChild.box1non.clicked.connect(self.box1nonfun)
        self.dboardChild.box1open.clicked.connect(self.box1openfun)
        self.dboardChild.box1close.clicked.connect(self.box1closefun)
        self.dboardChild.box2non.clicked.connect(self.box2nonfun)
        self.dboardChild.box2open.clicked.connect(self.box2openfun)
        self.dboardChild.box2close.clicked.connect(self.box2closefun)

        self.Dialog.exec_()

    def boardcontrol(self):
        board=unicode(self.dboardChild.boardlist.currentItem().text())
        if board == u'左箱体控制板' or board == u'右箱体控制板':
            self.xtwindow()
        else:
            pass

    def box1nonfun(self):
        self.dboardChild.box1close.setChecked(False)
        self.dboardChild.box1open.setChecked(False)
        boardid='61'
        cmd='96'
        mess='59'+'61'+cmd+'02'+'00'+'00'+'01'
        tocksend=self.messmarge(mess,1)
        self.dboardChild.testmessage.append('command:'+tocksend.encode('hex'))
        Ygcboardev.write(tocksend)
        self.tockgeter=titothread(boardid,cmd)
        self.tockgeter.messSingnal.connect(self.dtockmess)
        self.tockgeter.start()

        boardid='62'
        cmd='96'
        mess='59'+'62'+cmd+'02'+'00'+'00'+'01'
        tocksend=self.messmarge(mess,1)
        self.dboardChild.testmessage.append('command:'+tocksend.encode('hex'))
        Ygcboardev.write(tocksend)
        self.tockgeter=titothread(boardid,cmd)
        self.tockgeter.messSingnal.connect(self.dtockmess)
        self.tockgeter.start()

    def box1openfun(self):
        self.dboardChild.box1non.setChecked(False)
        self.dboardChild.box1close.setChecked(False)
        boardid='61'
        cmd='96'
        mess='59'+'61'+cmd+'02'+'08'+'08'+'01'
        tocksend=self.messmarge(mess,1)
        self.dboardChild.testmessage.append('command:'+tocksend.encode('hex'))
        Ygcboardev.write(tocksend)
        self.tockgeter=titothread(boardid,cmd)
        self.tockgeter.messSingnal.connect(self.dtockmess)
        self.tockgeter.start()


        boardid='62'
        cmd='96'
        mess='59'+'62'+cmd+'02'+'08'+'08'+'01'
        tocksend=self.messmarge(mess,1)
        self.dboardChild.testmessage.append('command:'+tocksend.encode('hex'))
        Ygcboardev.write(tocksend)
        self.tockgeter=titothread(boardid,cmd)
        self.tockgeter.messSingnal.connect(self.dtockmess)
        self.tockgeter.start()

    def box1closefun(self):
        self.dboardChild.box1non.setChecked(False)
        self.dboardChild.box1open.setChecked(False)
        boardid='61'
        cmd='96'
        mess='59'+'61'+cmd+'02'+'04'+'04'+'01'
        tocksend=self.messmarge(mess,1)
        self.dboardChild.testmessage.append('command:'+tocksend.encode('hex'))
        Ygcboardev.write(tocksend)

        boardid='62'
        cmd='96'
        mess='59'+'62'+cmd+'02'+'04'+'04'+'01'
        tocksend=self.messmarge(mess,1)
        self.dboardChild.testmessage.append('command:'+tocksend.encode('hex'))
        Ygcboardev.write(tocksend)

    def box2nonfun(self):
        self.dboardChild.box2open.setChecked(False)
        self.dboardChild.box2close.setChecked(False)
        boardid='61'
        cmd='96'
        mess='59'+'61'+cmd+'02'+'00'+'00'+'01'
        tocksend=self.messmarge(mess,1)
        self.dboardChild.testmessage.append('command:'+tocksend.encode('hex'))
        Ygcboardev.write(tocksend)
        self.tockgeter=titothread(boardid,cmd)
        self.tockgeter.messSingnal.connect(self.dtockmess)
        self.tockgeter.start()

        boardid='62'
        cmd='96'
        mess='59'+'62'+cmd+'02'+'00'+'00'+'01'
        tocksend=self.messmarge(mess,1)
        self.dboardChild.testmessage.append('command:'+tocksend.encode('hex'))
        Ygcboardev.write(tocksend)
        self.tockgeter=titothread(boardid,cmd)
        self.tockgeter.messSingnal.connect(self.dtockmess)
        self.tockgeter.start()

    def box2openfun(self):
        self.dboardChild.box2close.setChecked(False)
        self.dboardChild.box2non.setChecked(False)
        boardid='61'
        cmd='96'
        mess='59'+'61'+cmd+'02'+'02'+'02'+'01'
        tocksend=self.messmarge(mess,1)
        self.dboardChild.testmessage.append('command:'+tocksend.encode('hex'))
        Ygcboardev.write(tocksend)
        self.tockgeter=titothread(boardid,cmd)
        self.tockgeter.messSingnal.connect(self.dtockmess)
        self.tockgeter.start()

        boardid='62'
        cmd='96'
        mess='59'+'62'+cmd+'02'+'02'+'02'+'01'
        tocksend=self.messmarge(mess,1)
        self.dboardChild.testmessage.append('command:'+tocksend.encode('hex'))
        Ygcboardev.write(tocksend)
        self.tockgeter=titothread(boardid,cmd)
        self.tockgeter.messSingnal.connect(self.dtockmess)
        self.tockgeter.start()

    def box2closefun(self):
        self.dboardChild.box2open.setChecked(False)
        self.dboardChild.box2non.setChecked(False)

        boardid='61'
        cmd='96'
        mess='59'+'61'+cmd+'02'+'01'+'01'+'01'
        tocksend=self.messmarge(mess,1)
        self.dboardChild.testmessage.append('command:'+tocksend.encode('hex'))
        Ygcboardev.write(tocksend)
        self.tockgeter=titothread(boardid,cmd)
        self.tockgeter.messSingnal.connect(self.dtockmess)
        self.tockgeter.start()

        boardid='62'
        cmd='96'
        mess='59'+'62'+cmd+'02'+'01'+'01'+'01'
        tocksend=self.messmarge(mess,1)
        self.dboardChild.testmessage.append('command:'+tocksend.encode('hex'))
        Ygcboardev.write(tocksend)
        self.tockgeter=titothread(boardid,cmd)
        self.tockgeter.messSingnal.connect(self.dtockmess)
        self.tockgeter.start()

    def dstartest(self):
        currentest=unicode(self.dboardChild.testitem.currentItem().text())
        if currentest == u'左轮毂电机控制':
            self.motorwindow(1)
        elif currentest == u'右轮毂电机控制':
            self.motorwindow(2)
        elif currentest == u'广播轮毂电机控制':
            self.motorwindow(3)
        elif currentest == u'获取红外信息':
            self.getdboardinfo()
        elif currentest == u'获取IMU状态':
            self.getdboardinfo()
        elif currentest == u'获取探测距离':
            self.getultradisinfo()
        elif currentest == u'获取电池信息':
            self.getbatteryinfo()
        else:
            pass

    def getultradisinfo(self):
        bid=self.getNonYGbid()
        self.threader=nonYGprothread(bid)
        self.threader.start()

    def getbatteryinfo(self):
        bid=self.getNonYGbid()
        self.threader=nonYGprothread(bid)
        self.threader.start()

    def getNonYGbid(self):
        currentdevice=unicode(self.dboardChild.boardlist.currentItem().text())
        if currentdevice=='BMS':
            bid=1
        elif currentdevice==u'超声D8':
            bid=2
        elif currentdevice==u'超声E8':
            bid=3
        elif currentdevice==u'超声F8':
            bid=4
        elif currentdevice==u'超声FA':
            bid=5
        elif currentdevice==u'超声FC':
            bid=6
        else:
            bid=7
        return bid

    def duojicontrol(self,channel):
        cmd='16'
        if channel==0:
            boardid='61'
            mess='59'+boardid+cmd+'02'+'00'
        tocksend=self.messmarge(mess,1)
        self.dboardChild.testmessage.append(tocksend.encode('hex'))
        Ygcboardev.write(tocksend)
        self.geter=dboardthread(boardid,cmd)
        self.geter.messSingnal.connect(self.errmess)
        self.geter.frameSingnal.connect(self.boardmess)
        self.geter.start()

    def getdboardinfo(self):
        currentobject=(unicode(self.dboardChild.boardlist.currentItem().text()))
        boardid=str(self.boardidset(currentobject))
        if boardid=='51' or boardid=='52' or boardid=='53' or boardid=='54' or boardid=='55' or boardid=='56' or boardid=='57' or boardid=='58' or boardid=='59' or boardid=='5A':
            cmd='95'
            mess='59'+boardid+'15'+'00'+'00'
        elif boardid=='E1':
            cmd='97'
            mess='59'+boardid+'17'+'00'+'00'
        elif boardid=='D8' or boardid=='E8' or boardid=='F8' or boardid=='FA' or boardid=='FC' or boardid=='FE':
            cmd='94'
            mess='59'+boardid+'14'+'00'+'00'
        tocksend=self.messmarge(mess,1)
        self.dboardChild.testmessage.append(tocksend.encode('hex'))
        Ygcboardev.write(tocksend)
        self.geter=dboardthread(boardid,cmd)
        self.geter.messSingnal.connect(self.errmess)
        self.geter.frameSingnal.connect(self.boardmess)
        self.geter.start()

    def errmess(self,mess):
        self.dboardChild.testmessage.append(mess)

    def boardmess(self,mess,bid):
        if bid == '51' or bid=='52' or bid == '53' or bid=='54' or bid == '55' or bid=='56' or bid == '57' or bid=='58' or bid == '59' or bid=='5A':
            if mess[12:14] == '01':
                self.dboardChild.testmessage.append(u'红外传感器数据读取成功')
                discode=str(mess[18:20])+str(mess[16:18])
                irfdis=str(float(int(discode,16)/100))
                result=u'红外传感器探测距离物体:'+irfdis+'cm'
                self.dboardChild.testmessage.append(result)
            else:
                self.dboardChild.testmessage.append(u'红外传感器数据读取失败')
        elif bid=='E1':
            warringcode=mess[6:8]
            self.dboardChild.reginfo.append(u'warringcode:'+warringcode)
            errcode=mess[8:10]
            self.dboardChild.reginfo.append(u'errcode:'+errcode)
            Accx=mess[12:14]+mess[10:12]
            self.dboardChild.reginfo.append(u'X轴加速度:'+Accx)
            Accy=mess[16:18]+mess[14:16]
            self.dboardChild.reginfo.append(u'Y轴加速度:'+Accy)
            Accz=mess[20:22]+mess[18:20]
            self.dboardChild.reginfo.append(u'Z轴加速度:'+Accz)
            Groupx=mess[24:26]+mess[22:24]
            self.dboardChild.reginfo.append(u'X轴角速度:'+Groupx)
            Groupy=mess[28:30]+mess[26:28]
            self.dboardChild.reginfo.append(u'Y轴角速度:'+Groupy)
            Groupz=mess[32:34]+mess[30:32]
            self.dboardChild.reginfo.append(u'Z轴角速度:'+Groupz)
            Cmpx=mess[36:38]+mess[34:36]
            self.dboardChild.reginfo.append(u'X轴磁场强度:'+Cmpx)
            Cmpy=mess[40:42]+mess[38:40]
            self.dboardChild.reginfo.append(u'Y轴磁场强度:'+Cmpy)
            Cmpz=mess[44:46]+mess[42:44]
            self.dboardChild.reginfo.append(u'Z轴磁场强度:'+Cmpz)
            pitch=mess[48:50]+mess[46:48]
            self.dboardChild.reginfo.append(u'俯仰角:'+pitch)
            roll=mess[52:54]+mess[50:52]
            self.dboardChild.reginfo.append(u'翻滚角:'+roll)
            yaw=mess[56:58]+mess[54:56]
            self.dboardChild.reginfo.append(u'偏航角:'+yaw)
            temphex=mess[60:62]
            temp=str(int(str(temphex),16))
            self.dboardChild.reginfo.append(u'板子温度:'+temp)
        elif bid == 'D8' or bid=='E8' or bid == 'F8' or bid=='FA' or bid == 'FC' or bid=='FE':
            if mess[12:14] == '01':
                discode=str(mess[18:20])+str(mess[16:18])
                ultradis=str(float(int(discode,16)*0.017))
                result=u'超声探测距离物体:'+ultradis+'cm'
                self.dboardChild.testmessage.append(result)
            else:
                self.dboardChild.testmessage.append(u'超声数据读取失败')
        else:
            pass

    def cutmodel(self):
        bid='EE'
        cmd='62'
        tockdata='0000000000000000000000000000000000000000'
        mess='59'+'EE'+'E2'+'15'+'10'+tockdata+'01000000'+'01'
        tocksend=self.messmarge(mess,1)
        self.dboardChild.testmessage.append('cmd:'+tocksend.encode('hex'))
        self.cuter=cutmodelthread(0)
        self.cuter.messSingnal.connect(self.cutmess)
        self.cuter.seqSingnal.connect(self.startock)
        self.cuter.start()

    def dclose(self):
        try:
            Ygcboardev.close()
            status=u'YG协议单板D测试-串口已关闭'
            self.Dialog.setWindowTitle(status)
            self.dboardChild.serialset.setEnabled(True)
        except:
            pass

    def dcutmess(self,mess):
        self.dboardChild.testmessage.append(mess)

    def dclear(self):
        self.dboardChild.testmessage.clear()

    def writenable(self):
        currentsubitem=unicode(self.dboardChild.testitem_2.currentItem().text())
        if currentsubitem == u'写入SN':
            self.dboardChild.boardsn.setEnabled(True)
            self.dboardChild.hardware.setEnabled(False)
            self.dboardChild.software.setEnabled(False)
            self.dboardChild.BID.setEnabled(False)
            self.dboardChild.protol.setEnabled(False)
        elif currentsubitem == u'写入硬件版本号':
            self.dboardChild.hardware.setEnabled(True)
            self.dboardChild.boardsn.setEnabled(False)
            self.dboardChild.software.setEnabled(False)
            self.dboardChild.BID.setEnabled(False)
            self.dboardChild.protol.setEnabled(False)
        elif currentsubitem == u'写入BID':

            self.dboardChild.BID.setEnabled(True)
            self.dboardChild.boardsn.setEnabled(False)
            self.dboardChild.hardware.setEnabled(False)
            self.dboardChild.software.setEnabled(False)
            self.dboardChild.protol.setEnabled(False)
        else:
            pass

    def dboardserautoget(self):
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list) <= 0:
            QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("端口号数量为零，请先连接串口"))
        else:
            pattern_serial='COM.+'
            for line in port_list:
                Match=re.search(pattern_serial,str(line))
                if Match:
                    new_line=str(line).split(' - ')
                    self.dboardChild.serialnum.addItem(new_line[0])

    def YGtestdboardSer(self):
        global Ygcboardev

        try:
            Ygcboardev.close()
        except:
            pass
        try:
            titodevice.close()
        except:
            pass
        sernum=str(self.dboardChild.serialnum.currentText())
        rate=int(self.dboardChild.boundrate.currentText())

        try:
            Ygcboardev=serial.Serial(sernum,rate,timeout=1)
            status=u'YG协议单板d测试-'+str.upper(sernum)+':'+str(rate)+':READ'
            self.Dialog.setWindowTitle(status)
            self.dboardChild.boardlist.setEnabled(True)
            self.dboardChild.otalist.setEnabled(True)
            self.dboardChild.serialset.setDisabled(True)
            self.dboardChild.close.setEnabled(True)
            self.dboardChild.modelset.setEnabled(True)
        except:
            QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("串口打开失败，请检查设置"))

    def dotaupdate(self):
        self.otaChild = Update_Ui_Dialog()
        self.Dialog = QtGui.QDialog(self)
        self.otaChild.setupUi(self.Dialog)

        currentboard=unicode(self.dboardChild.otalist.currentItem().text())
        self.Dialog.setWindowTitle(u'OTA升级界面_'+currentboard)
        self.otaChild.otamessage.append(u'已选择'+currentboard+u'升级')

        self.dboardChild.testitem.clear()
        self.dboardChild.testitem_2.clear()
        if currentboard==u'轮毂电机':
            self.otaChild.sublist.setEnabled(True)
            self.otaChild.sublist.addItem(u'轮毂广播升级')
            self.otaChild.sublist.addItem(u'左电机')
            self.otaChild.sublist.addItem(u'右电机')
        elif currentboard==u'开门电机':
            self.otaChild.sublist.setEnabled(True)
            self.otaChild.sublist.addItem(u'电机广播升级')
            self.otaChild.sublist.addItem(u'直流电机1')
            self.otaChild.sublist.addItem(u'直流电机2')
            #self.otaChild.sublist.addItem(u'直流电机驱动板三')
            #self.otaChild.sublist.addItem(u'直流电机驱动板四')
        elif currentboard==u'左右箱体控制板':
            self.otaChild.sublist.setEnabled(True)
            self.otaChild.sublist.addItem(u'左上箱体')
            self.otaChild.sublist.addItem(u'右上箱体')
            self.otaChild.sublist.addItem(u'左下箱体')
            self.otaChild.sublist.addItem(u'右下箱体')
        elif currentboard==u'红外传感器':
            self.otaChild.sublist.setEnabled(True)
            self.otaChild.sublist.addItem(u'红外广播升级')
            self.otaChild.sublist.addItem(u'红外1')
            self.otaChild.sublist.addItem(u'红外2')
            self.otaChild.sublist.addItem(u'红外3')
            self.otaChild.sublist.addItem(u'红外4')
            self.otaChild.sublist.addItem(u'红外5')
            self.otaChild.sublist.addItem(u'红外6')
            self.otaChild.sublist.addItem(u'红外7')
            self.otaChild.sublist.addItem(u'红外8')
            self.otaChild.sublist.addItem(u'红外9')
            self.otaChild.sublist.addItem(u'红外10')
        else:
            self.otaChild.verlist.setEnabled(True)

        self.dsoftimer=QtCore.QTimer(self)
        self.dsoftimer.setSingleShot(True)
        self.dsoftimer.timeout.connect(self.firmreload)
        self.dsoftimer.start(10)

        self.otaChild.firwareselect.clicked.connect(self.firwareadd)
        self.otaChild.sublist.clicked.connect(self.upenable)
        self.otaChild.verlist.itemDoubleClicked.connect(self.firmupdate)
        self.otaChild.pause.clicked.connect(self.upstop)
        self.otaChild.open.clicked.connect(self.reopenser)
        self.otaChild.clear.clicked.connect(self.clearmess)
        self.Dialog.exec_()

    def reopenser(self):
        try:
            Ygcboardev.open()
            status=u'OTA升级界面-串口已打开'
            self.Dialog.setWindowTitle(status)
            self.otaChild.open.setDisabled(True)
        except:
            QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("串口打开失败，请检查设置"))

    def dtestitemupdate(self):
        self.dboardChild.testitem.clear()
        self.dboardChild.BID.clear()
        currentitem=unicode(self.dboardChild.boardlist.currentItem().text())
        if currentitem==u'超声D8' or currentitem==u'超声E8' or currentitem==u'超声F8' or currentitem==u'超声FA' or currentitem==u'超声FC' or currentitem==u'超声FE' or currentitem==u'BMS':
            if currentitem==u'BMS':
                self.dboardChild.testitem.addItem(u'获取电池信息')
            else:
                self.dboardChild.testitem.addItem(u'获取探测距离')
        else:
            self.dboardChild.testitem.addItem(u'读取通用寄存器')
            self.dboardChild.testitem.addItem(u'BID')
            self.dboardChild.testitem.addItem(u'SN')
            self.dboardChild.testitem.addItem(u'硬件版本号')
            self.dboardChild.testitem.addItem(u'软件版本号')
            self.dboardChild.testitem.addItem(u'协议版本号')
            if currentitem == u'IMU':
                self.dboardChild.testitem.addItem(u'获取IMU状态')
            elif currentitem == u'2.4G':
                self.dboardChild.testitem.addItem(u'2.4G状态')
            elif currentitem == u'左轮毂电机':
                self.dboardChild.testitem.addItem(u'左轮毂电机控制')
                self.dboardChild.testitem.addItem(u'广播轮毂电机控制')
            elif currentitem == u'右轮毂电机':
                self.dboardChild.testitem.addItem(u'右轮毂电机控制')
                self.dboardChild.testitem.addItem(u'广播轮毂电机控制')
            elif currentitem == u'左箱体控制板':
                self.dboardChild.testitem.addItem(u'舵机控制')
            elif currentitem == u'右箱体控制板':
                self.dboardChild.testitem.addItem(u'舵机控制')
            elif currentitem==u'红外1' or currentitem==u'红外2' or currentitem==u'红外3' or currentitem==u'红外4' or currentitem==u'红外5':
                self.dboardChild.testitem.addItem(u'获取红外信息')
            elif currentitem==u'红外6' or currentitem==u'红外7' or currentitem==u'红外8' or currentitem==u'红外9' or currentitem==u'红外10':
                self.dboardChild.testitem.addItem(u'获取红外信息')
            else:
                pass

    def dtestupdate(self):
        self.dboardChild.testitem_2.clear()
        currentest=unicode(self.dboardChild.testitem.currentItem().text())
        if currentest==u'读取通用寄存器':
            self.dboardChild.testitem_2.addItem(u'读取指令测试')
            self.dboardChild.testitem_2.addItem(u'读取64byte')
            self.dboardChild.testitem_2.addItem(u'读取65byte')
            self.dboardChild.testitem_2.addItem(u'CRC错误帧')
            self.dboardChild.testitem_2.addItem(u'LEN错误帧')
        elif currentest==u'BID':
            self.dboardChild.testitem_2.addItem(u'写入BID')
            autobid=unicode(self.dboardChild.boardlist.currentItem().text())
            if autobid==u'红外1':
                bid='51'
            elif autobid==u'红外2':
                bid='52'
            elif autobid==u'红外3':
                bid='53'
            elif autobid==u'红外4':
                bid='54'
            elif autobid==u'红外5':
                bid='55'
            elif autobid==u'红外6':
                bid='56'
            elif autobid==u'红外7':
                bid='57'
            elif autobid==u'红外8':
                bid='58'
            elif autobid==u'红外9':
                bid='59'
            elif autobid==u'红外10':
                bid='5a'
            elif autobid==u'左箱体控制板':
                bid='61'
            elif autobid==u'右箱体控制板':
                bid='62'
            elif autobid==u'直流电机驱动板1':
                bid='25'
            elif autobid==u'直流电机驱动板2':
                bid='26'
            elif autobid==u'左轮毂电机':
                bid='11'
            elif autobid==u'右轮毂电机':
                bid='12'
            elif autobid==u'IMU':
                bid='E1'
            else:
                pass
            self.dboardChild.BID.setText(bid)
        elif currentest==u'SN':
            self.dboardChild.testitem_2.addItem(u'写入SN')
            self.dboardChild.testitem_2.addItem(u'读取SN')
        elif currentest==u'硬件版本号':
            self.dboardChild.testitem_2.addItem(u'写入硬件版本号')
            self.dboardChild.testitem_2.addItem(u'读取硬件版本号')
        elif currentest==u'软件版本号':
            self.dboardChild.testitem_2.addItem(u'读取软件版本号')
        elif currentest==u'协议版本号':
            self.dboardChild.testitem_2.addItem(u'读取协议版本号')
        elif currentest==u'IMU状态':
            self.dboardChild.testitem_2.addItem(u'获取IMU状态数据')
        elif currentest==u'2.4G状态':
            self.dboardChild.testitem_2.addItem(u'获取2.4G状态数据')
        elif currentest == u'舵机控制':
            self.dboardChild.tabWidget_2.setCurrentIndex(1)
            self.dboardChild.groupBox_11.setEnabled(True)
        else:
            pass

    def getboardaddress(self):
        address=''
        currentboard=unicode(self.dboardChild.boardlist.currentItem().text())
        if currentboard== u'左箱体控制板':
            address='60'
        elif currentboard== u'右箱体控制板':
            address='60'
        elif currentboard== u'红外1' or currentboard== u'红外2' or currentboard== u'红外3' or currentboard== u'红外4' or currentboard== u'红外5':
            address='50'
        elif currentboard== u'红外6' or currentboard== u'红外7' or currentboard== u'红外8' or currentboard== u'红外9' or currentboard== u'红外10':
            address='50'
        elif currentboard== u'左轮毂电机'  or currentboard== u'右轮毂电机':
            address='10'
        elif currentboard== u'IMU':
            address='E1'
        else:
            pass
        return address

    def dstarttestitem(self):
        seq='01'
        currentobject=(unicode(self.dboardChild.boardlist.currentItem().text()))
        boardid=str(self.boardidset(currentobject))
        currentitem=(unicode(self.dboardChild.testitem.currentItem().text()))
        currensubtitem=(unicode(self.dboardChild.testitem_2.currentItem().text()))
        if currentitem==u'读取通用寄存器':
            cmd='80'
            if currensubtitem == u'读取指令测试':
                mess='59'+str(boardid)+'00'+'02'+'00'+'00'+'01'
                tocksend=self.messmarge(mess,1)
                self.dboardChild.testmessage.append('command:'+tocksend.encode('hex'))
                Ygcboardev.write(tocksend)
                self.tockgeter=titothread(boardid,cmd)
                self.tockgeter.messSingnal.connect(self.dtockmess)
                self.tockgeter.start()
            elif currensubtitem == u'读取64byte':
                mess='59'+str(boardid)+'00'+'02'+'00'+'40'+'01'
                tocksend=self.messmarge(mess,1)
                self.dboardChild.testmessage.append('command:'+tocksend.encode('hex'))
                Ygcboardev.write(tocksend)
                self.tockgeter=titothread(boardid,cmd)
                self.tockgeter.messSingnal.connect(self.dtockmess)
                self.tockgeter.start()
            elif currensubtitem == u'读取65byte':
                mess='59'+str(boardid)+'00'+'02'+'00'+'41'+seq
                tocksend=self.messmarge(mess,1)
                self.dboardChild.testmessage.append('command:'+tocksend.encode('hex'))
                Ygcboardev.write(tocksend)
                self.tockgeter=titothread(boardid,cmd)
                self.tockgeter.messSingnal.connect(self.dtockmess)
                self.tockgeter.start()
            elif currensubtitem == u'读取起始地址65':
                mess='59'+str(boardid)+'00'+'02'+'41'+'02'+seq
                tocksend=self.messmarge(mess,1)
                self.dboardChild.testmessage.append('command:'+tocksend.encode('hex'))
                Ygcboardev.write(tocksend)
                self.tockgeter=titothread(boardid,cmd)
                self.tockgeter.messSingnal.connect(self.dtockmess)
                self.tockgeter.start()
            elif currensubtitem == u'CRC错误帧':
                mess='59'+str(boardid)+'00'+'02'+'00'+'02'+seq
                tocksend=self.messmarge(mess,0)
                self.dboardChild.testmessage.append('command:'+tocksend.encode('hex'))
                Ygcboardev.write(tocksend)
                self.tockgeter=titothread(boardid,cmd)
                self.tockgeter.messSingnal.connect(self.dtockmess)
                self.tockgeter.start()
            elif currensubtitem == u'LEN错误帧':
                mess='59'+str(boardid)+'00'+'03'+'00'+'02'+seq
                tocksend=self.messmarge(mess,1)
                self.dboardChild.testmessage.append('command:'+tocksend.encode('hex'))
                Ygcboardev.write(tocksend)
                self.tockgeter=titothread(boardid,cmd)
                self.tockgeter.messSingnal.connect(self.dtockmess)
                self.tockgeter.start()
            else:
                pass
        elif currentitem==u'SN':
            model=1
            if model:
                if currensubtitem == u'写入SN':
                    cmd='F1'
                    snchar=''
                    newsn=str(self.dboardChild.boardsn.toPlainText())
                    if newsn!='':
                        lensn=hex(len(newsn)).lstrip('0x')
                        if len(lensn)==1:
                            lensn='0'+lensn
                        for line in newsn:
                            hexline=hex(ord(line)).lstrip('0x')
                            if len(hexline)==1:
                                hexline='0'+hexline
                            snchar+=hexline
                        self.dboardChild.testmessage.append(u'SN长度:'+str(len(newsn)))
                        newlen=hex(len(snchar)+1).lstrip('0x')
                        if len(newlen)==1:
                            newlen='0'+newlen
                        mess='59'+str(boardid)+'71'+lensn+snchar+seq
                        tocksend=self.messmarge(mess,1)
                        self.dboardChild.testmessage.append('command:'+tocksend.encode('hex'))
                        Ygcboardev.write(tocksend)
                        self.tockgeter=titothread(boardid,cmd)
                        self.tockgeter.messSingnal.connect(self.dtockmess)
                        self.tockgeter.start()
                    else:
                        self.dboardChild.testmessage.append(u'不能写入空sn，请重新输入')
                else:
                    cmd='80'
                    mess='59'+str(boardid)+'00'+'02'+'0D'+'14'+seq
                    tocksend=self.messmarge(mess,1)
                    self.dboardChild.testmessage.append('command:'+tocksend.encode('hex'))
                    Ygcboardev.write(tocksend)
                    self.tockgeter=titothread(boardid,cmd)
                    self.tockgeter.messSingnal.connect(self.dtockmess)
                    self.tockgeter.start()

        elif currentitem==u'BID':
            if currensubtitem == u'写入BID':
                address=self.getboardaddress()
                cmd='F3'
                bid=str(self.dboardChild.BID.toPlainText()).lstrip(' ').rstrip(' ')
                if bid!='':
                    if len(bid)!=2:
                        self.dboardChild.testmessage.append(u'BID长度必须是2')
                    else:
                        mess='59'+address+'73'+'01'+bid+seq
                        tocksend=self.messmarge(mess,1)
                        Ygcboardev.write(tocksend)
                        self.dboardChild.testmessage.append('command:'+tocksend.encode('hex'))
                        self.tockgeter=titothread(bid,cmd)
                        self.tockgeter.messSingnal.connect(self.dtockmess)
                        self.tockgeter.start()
                else:
                    self.dboardChild.testmessage.append(u'不能写入空bid，请重新输入')
        elif currentitem==u'硬件版本号':
            if currensubtitem == u'写入硬件版本号':
                newhardver=str(self.dboardChild.hardware.toPlainText()).lstrip('V').rstrip(' ')
                cmd='F2'
                if newhardver!='':
                    self.dboardChild.testmessage.append(u'硬件版本号长度:'+str(len(newhardver)/2))
                    hardverlist=newhardver.split('.')
                    hardver=str(hardverlist[0]+hardverlist[1]+hardverlist[2]+hardverlist[3])
                    mess='59'+str(boardid)+'72'+'02'+hardver+seq
                    tocksend=self.messmarge(mess,1)
                    self.dboardChild.testmessage.append('command:'+tocksend.encode('hex'))
                    Ygcboardev.write(tocksend)
                    self.tockgeter=titothread(boardid,cmd)
                    self.tockgeter.messSingnal.connect(self.dtockmess)
                    self.tockgeter.start()
                else:
                    self.dboardChild.testmessage.append(u'不能写入空硬件版本号，请重新输入')
            else:
                cmd='80'
                mess='59'+str(boardid)+'00'+'02'+'21'+'02'+seq
                tocksend=self.messmarge(mess,1)
                self.dboardChild.testmessage.append('command:'+tocksend.encode('hex'))
                Ygcboardev.write(tocksend)
                self.tockgeter=titothread(boardid,cmd)
                self.tockgeter.messSingnal.connect(self.dtockmess)
                self.tockgeter.start()

        elif currentitem==u'软件版本号':
            if currensubtitem == u'读取软件版本号':
                cmd='80'
                mess='59'+str(boardid)+'00'+'02'+'23'+'02'+seq
                tocksend=self.messmarge(mess,1)
                self.dboardChild.testmessage.append('command:'+tocksend.encode('hex'))
                Ygcboardev.write(tocksend)
                self.tockgeter=titothread(boardid,cmd)
                self.tockgeter.messSingnal.connect(self.dtockmess)
                self.tockgeter.start()
        elif currentitem==u'协议版本号':
            if currensubtitem == u'读取协议版本号':
                cmd='80'
                mess='59'+str(boardid)+'00'+'02'+'25'+'02'+seq
                tocksend=self.messmarge(mess,1)
                self.dboardChild.testmessage.append('command:'+tocksend.encode('hex'))
                Ygcboardev.write(tocksend)
                self.tockgeter=titothread(boardid,cmd)
                self.tockgeter.messSingnal.connect(self.dtockmess)
                self.tockgeter.start()
            else:
                pass
        else:
            pass

    def gerinfoany(self,mess):
        self.dboardChild.reginfo.clear()
        devicesn=''
        cpuid=mess[16:40]
        self.dboardChild.reginfo.append('CPUID:'+cpuid)
        sn=str(mess[40:80])
        for i in range(0,40,2):
            devicesn+=chr(int(sn[i:i+2],16))
        self.dboardChild.boardsn.setText(devicesn)
        hardver=mess[80:84]
        self.dboardChild.hardware.setText('V'+hardver[0]+'.'+hardver[1]+'.'+hardver[2]+'.'+hardver[3])
        softver=mess[84:88]
        self.dboardChild.software.setText('V'+softver[0]+'.'+softver[1]+'.'+softver[2]+'.'+softver[3])
        protover=mess[88:92]
        self.dboardChild.protol.setText('V'+protover[0]+'.'+protover[1]+'.'+protover[2]+'.'+protover[3])
        boot=mess[92:96]
        self.dboardChild.bootver.setText('V'+boot[0]+'.'+boot[1]+'.'+boot[2]+'.'+boot[3])
        hextemp=str(mess[108:110])
        cputemp=int(hextemp,16)
        self.dboardChild.reginfo.append(u'板子温度:'+str(cputemp))

        hexsend=str(mess[116:118]+mess[114:116]+mess[112:114]+mess[110:112])
        sendcount=int(hexsend,16)
        self.dboardChild.reginfo.append(u'发出的包数:'+str(sendcount))

        hexrecv=str(mess[124:126]+mess[122:124]+mess[120:122]+mess[118:120])
        recvcount=int(hexrecv,16)
        self.dboardChild.reginfo.append(u'收到的包数:'+str(recvcount))

        hexrecverr=str(mess[132:134]+mess[130:132]+mess[128:130]+mess[126:128])
        errecvcount=int(hexrecverr,16)
        self.dboardChild.reginfo.append(u'收到的包解析错误个数:'+str(errecvcount))

        hexwarr=str(mess[134:136])
        warrcode=int(hexwarr,16)
        if warrcode==1:
            self.dboardChild.reginfo.append('WarningCode:'+u'丢包过多')
        elif warrcode==2:
            self.dboardChild.reginfo.append('WarningCode:'+u'重启过')
        elif warrcode==3:
            self.dboardChild.reginfo.append('WarningCode:'+u'丢包过多,重启过')
        elif warrcode==4:
            self.dboardChild.reginfo.append('WarningCode:'+u'CPU温度过高')
        elif warrcode==5:
            self.dboardChild.reginfo.append('WarningCode:'+u'丢包过多,CPU温度过高')
        elif warrcode==6:
            self.dboardChild.reginfo.append('WarningCode:'+u'重启过,CPU温度过高')
        elif warrcode==7:
            self.dboardChild.reginfo.append('WarningCode:'+u'丢包过多,重启过,CPU温度过高')
        else:
            self.dboardChild.reginfo.append('WarningCode:'+u'正常')

        hexerr=str(mess[136:138])
        if hexerr == '00':
            self.dboardChild.reginfo.append('ErrCode:'+u'正常')
        else:
            self.dboardChild.reginfo.append('ErrCode:'+u'设备故障')

    def dtockmess(self,mess):
        self.dboardChild.testmessage.append('result:'+mess)
        if self.dboardChild.groupBox_11.isEnabled():
            if mess[2:4]=='61':
                leftwei1=mess[12:16]
                leftwei2=mess[16:20]
                self.dboardChild.reginfo.append(u'左舵机应变片1:'+leftwei1)
                self.dboardChild.reginfo.append(u'左舵机应变片2:'+leftwei2)
            elif mess[2:4]=='62':
                rightwei1=mess[12:16]
                rightwei2=mess[16:20]
                self.dboardChild.reginfo.append(u'右舵机应变片1:'+rightwei1)
                self.dboardChild.reginfo.append(u'右舵机应变片2:'+rightwei2)
        else:
            currensubtitem=(unicode(self.dboardChild.testitem_2.currentItem().text()))
            if currensubtitem == u'读取指令测试':
                if mess[8:10] == '00':
                    self.dboardChild.testmessage.append(u'读取指令测试通过')
                else:
                    self.dboardChild.testmessage.append(u'读取指令测试失败')
            elif currensubtitem == u'读取64byte':
                if mess[8:10] == '00':
                    if mess[6:8] == '43':
                        self.gerinfoany(str(mess))
                        self.dboardChild.testmessage.append(u'读取64byte测试通过')
                    else:
                        self.dboardChild.testmessage.append(u'返回YG协议帧长度不是67,测试失败')
                else:
                    self.dboardChild.testmessage.append(u'读取64byte测试失败')
            elif currensubtitem == u'读取65byte':
                if mess[6:8] == '01':
                    if mess[8:10] == '00':
                        self.dboardChild.testmessage.append(u'读取65byte测试失败')
                    else:
                        self.dboardChild.testmessage.append(u'读取65byte测试通过')
                else:
                    self.dboardChild.testmessage.append(u'读取65byte测试失败')
            elif currensubtitem == u'读取起始地址65':
                if mess[6:8] == '01':
                    if mess[8:10] == '00':
                        self.dboardChild.testmessage.append(u'读取起始地址65测试失败')
                    else:
                        self.dboardChild.testmessage.append(u'读取起始地址65测试通过')
                else:
                    self.dboardChild.testmessage.append(u'读取起始地址65测试失败')
            elif currensubtitem == u'CRC错误帧':
                if mess[6:8] == '01':
                    if mess[8:10] == '00':
                        self.dboardChild.testmessage.append(u'CRC错误帧测试失败')
                    else:
                        self.dboardChild.testmessage.append(u'CRC错误帧测试通过')
                else:
                    self.dboardChild.testmessage.append(u'CRC错误帧测试失败')
            elif currensubtitem == u'LEN错误帧':
                if mess[6:8] == '01':
                    if mess[8:10] == '00':
                        self.dboardChild.testmessage.append(u'LEN错误帧测试失败')
                    else:
                        self.dboardChild.testmessage.append(u'LEN错误帧测试通过')
                else:
                    self.dboardChild.testmessage.append(u'LEN错误帧测试失败')
            elif currensubtitem == u'写入SN':
                if mess[4:6] == 'f1':
                    if mess[8:10] == '00':
                        self.dboardChild.testmessage.append(u'SN已写入')
                    else:
                        self.dboardChild.testmessage.append(u'SN写入失败')
                else:
                    self.dboardChild.testmessage.append(u'SN写入失败')
            elif currensubtitem == u'读取SN':
                self.dboardChild.boardsn.clear()
                devicesn=''
                if mess[8:10] == '00':
                    try:
                        readsn=str(mess[14:54])
                        for i in range(0,len(readsn),2):
                            devicesn+=chr(int(readsn[i:i+2],16))
                        self.dboardChild.boardsn.setText(devicesn)
                        self.dboardChild.testmessage.append(u'SN读取成功')
                    except:
                        self.dboardChild.testmessage.append(u'SN读取失败')
                else:
                    self.dboardChild.testmessage.append(u'SN读取失败')
            elif currensubtitem == u'写入BID':
                if mess[4:6] == 'f3':
                    if mess[8:10] == '00':
                        self.dboardChild.testmessage.append(u'BID已写入')
                    else:
                        self.dboardChild.testmessage.append(u'BID写入失败')
                else:
                    self.dboardChild.testmessage.append(u'BID写入失败')
            elif currensubtitem == u'读取BID':
                if mess[4:6] == '80':
                    if mess[8:10] == '00':
                        self.dboardChild.testmessage.append(u'BID已写入')
                    else:
                        self.dboardChild.testmessage.append(u'BID读取失败')
                else:
                    self.dboardChild.testmessage.append(u'BID读取失败')
            elif currensubtitem == u'写入硬件版本号':
                if mess[4:6] == 'f2':
                    if mess[8:10] == '00':
                        self.dboardChild.testmessage.append(u'硬件版本号已写入')
                    else:
                        self.dboardChild.testmessage.append(u'硬件版本号写入失败')
                else:
                    self.dboardChild.testmessage.append(u'硬件版本号写入失败')
            elif currensubtitem == u'读取硬件版本号':
                self.dboardChild.hardware.clear()
                if mess[4:6] == '80':
                    if mess[8:10] == '00':
                        ver=mess[14:18]
                        self.dboardChild.hardware.setText('V'+ver[0]+'.'+ver[1]+'.'+ver[2]+'.'+ver[3])
                        self.dboardChild.testmessage.append(u'硬件版本号已读取')
                    else:
                        self.dboardChild.testmessage.append(u'硬件版本号读取失败')
                else:
                    self.dboardChild.testmessage.append(u'硬件版本号读取失败')
            elif currensubtitem == u'读取软件版本号':
                if mess[4:6] == '80':
                    if mess[8:10] == '00':
                        ver=mess[14:18]
                        self.dboardChild.software.setText('V'+ver[0]+'.'+ver[1]+'.'+ver[2]+'.'+ver[3])
                        self.dboardChild.testmessage.append(u'软件版本号已读取')
                    else:
                        self.dboardChild.testmessage.append(u'软件版本号读取失败')
                else:
                    self.dboardChild.testmessage.append(u'软件版本号读取失败')
            elif currensubtitem == u'读取协议版本号':
                if mess[4:6] == '80':
                    if mess[8:10] == '00':
                        ver=mess[14:18]
                        self.dboardChild.protol.setText('V'+ver[0]+'.'+ver[1]+'.'+ver[2]+'.'+ver[3])
                        self.dboardChild.testmessage.append(u'协议版本号已读取')
                    else:
                        self.dboardChild.testmessage.append(u'协议版本号读取失败')
                else:
                    self.dboardChild.testmessage.append(u'协议版本号读取失败')
            elif currensubtitem == u'切换到转发':
                if mess[138:140] == '00':
                    self.cboardChild.testmessage.append(u'已切换到转发模式')
                else:
                    self.cboardChild.testmessage.append(u'切换到转发模式失败')
            else:
                pass

    def ucboardwindow(self):
        global cboardudp

        self.ucboardChild = Ucboard_Ui_Dialog()
        self.Dialog = QtGui.QDialog(self)
        self.ucboardChild.setupUi(self.Dialog)

        cboardudp=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cboardudp.settimeout(1)

        self.ucboardChild.boardlist.itemClicked.connect(self.utestitemupdate)
        self.ucboardChild.otalist.itemDoubleClicked.connect(self.uotaupdate)
        self.ucboardChild.testitem.itemClicked.connect(self.usubitemtest)
        self.ucboardChild.subtest.itemDoubleClicked.connect(self.uitemtest)
        self.ucboardChild.messclear.clicked.connect(self.ucleartestmess)
        self.Dialog.exec_()

    def utestitemupdate(self):
        self.ucboardChild.SN.setDisabled(True)
        self.ucboardChild.BID.setDisabled(True)
        self.ucboardChild.hardver.setDisabled(True)
        self.ucboardChild.softver.setDisabled(True)
        self.ucboardChild.protover.setDisabled(True)
        self.ucboardChild.testitem.clear()
        self.ucboardChild.subtest.clear()
        self.ucboardChild.testitem.addItem(u'读取通用寄存器信息')
        self.ucboardChild.testitem.addItem(u'SN')
        self.ucboardChild.testitem.addItem(u'BID')
        self.ucboardChild.testitem.addItem(u'硬件版本号')
        self.ucboardChild.testitem.addItem(u'软件版本号')
        self.ucboardChild.testitem.addItem(u'协议版本号')
        currentobject=(unicode(self.ucboardChild.boardlist.currentItem().text()))
        if currentobject ==u'Board-C':
            self.ucboardChild.testitem.addItem(u'模式切换')
            self.ucboardChild.testitem.addItem(u'电机状态')
            self.ucboardChild.testitem.addItem(u'电机故障')
        elif currentobject ==u'左轮毂电机' or currentobject ==u'右轮毂电机':
                self.ucboardChild.testitem.addItem(u'控制轮毂电机')
        elif currentobject ==u'直流电机1' or currentobject ==u'直流电机2' or currentobject ==u'直流电机3' or currentobject ==u'直流电机4':
            self.ucboardChild.testitem.addItem(u'开门')
            self.ucboardChild.testitem.addItem(u'关门')
        elif currentobject ==u'左箱体控制板' or currentobject ==u'右箱体控制板':
            self.ucboardChild.testitem.addItem(u'开门')
            self.ucboardChild.testitem.addItem(u'关门')
        elif currentobject ==u'灯光控制':
            self.ucboardChild.testitem.addItem(u'设置灯效')
        else:
            self.ucboardChild.testitem.addItem(u'获取状态')

    def usubitemtest(self):
        currentitem=unicode(self.ucboardChild.testitem.currentItem().text())
        self.ucboardChild.subtest.clear()
        if currentitem == u'读取通用寄存器信息':
            self.ucboardChild.subtest.addItem(u'读取指令测试')
            self.ucboardChild.subtest.addItem(u'读取64byte')
            self.ucboardChild.subtest.addItem(u'读取65byte')
            self.ucboardChild.subtest.addItem(u'读取起始地址65')
            self.ucboardChild.subtest.addItem(u'CRC错误帧')
            self.ucboardChild.subtest.addItem(u'LEN错误帧')
            self.ucboardChild.subtest.addItem(u'seq错误帧')
        elif currentitem == u'SN':
            self.ucboardChild.SN.setEnabled(True)
            self.ucboardChild.subtest.addItem(u'写入SN')
            self.ucboardChild.subtest.addItem(u'读取SN')
            self.ucboardChild.subtest.addItem(u'CRC错误帧')
            self.ucboardChild.subtest.addItem(u'LEN错误帧')
            self.ucboardChild.subtest.addItem(u'seq错误帧')
        elif currentitem == u'BID':
            self.ucboardChild.BID.setEnabled(True)
            self.ucboardChild.subtest.addItem(u'写入BID')
        elif currentitem == u'硬件版本号':
            self.ucboardChild.hardver.setEnabled(True)
            self.ucboardChild.subtest.addItem(u'写入硬件版本号')
            self.ucboardChild.subtest.addItem(u'读取硬件版本号')
            self.ucboardChild.subtest.addItem(u'CRC错误帧')
            self.ucboardChild.subtest.addItem(u'LEN错误帧')
            self.ucboardChild.subtest.addItem(u'seq错误帧')
        elif currentitem == u'软件版本号':
            self.ucboardChild.subtest.addItem(u'读取软件版本号')
            self.ucboardChild.subtest.addItem(u'CRC错误帧')
            self.ucboardChild.subtest.addItem(u'LEN错误帧')
            self.ucboardChild.subtest.addItem(u'seq错误帧')
        elif currentitem == u'协议版本号':
            self.ucboardChild.subtest.addItem(u'读取协议版本号')
            self.ucboardChild.subtest.addItem(u'CRC错误帧')
            self.ucboardChild.subtest.addItem(u'LEN错误帧')
            self.ucboardChild.subtest.addItem(u'seq错误帧')
        elif currentitem == u'模式切换':
            self.ucboardChild.subtest.addItem(u'切换到正常')
            self.ucboardChild.subtest.addItem(u'切换到转发')
            self.ucboardChild.subtest.addItem(u'CRC错误帧')
            self.ucboardChild.subtest.addItem(u'LEN错误帧')
            self.ucboardChild.subtest.addItem(u'seq错误帧')
        elif currentitem == u'电机状态':
            self.ucboardChild.subtest.addItem(u'左电机状态')
            self.ucboardChild.subtest.addItem(u'右电机状态')
        elif currentitem == u'电机故障':
            self.ucboardChild.subtest.addItem(u'左电机故障')
            self.ucboardChild.subtest.addItem(u'右电机故障')
        else:
            pass

    def uitemtest(self):
        currentsubitem=unicode(self.ucboardChild.subtest.currentItem().text())
        if currentsubitem == u'切换到正常':
            mess=str('59'+'EE'+'62'+'04'+'00'+'000000'+'01'+'90E547').decode('hex')
            cboardudp.sendto(mess,('192.168.80.201',6650))
            recvmess=cboardudp.recv(1024)
            self.ucboardChild.testmessage.append(mess.encode('hex'))
            self.ucboardChild.workmodel.setText(u'正常')
        elif currentsubitem == u'切换到转发':
            self.ucutmodeltotrans()
        elif currentsubitem == u'写入SN':
            pass
        elif currentsubitem == u'左电机状态' or currentsubitem == u'右电机状态' or currentsubitem == u'左电机故障' or currentsubitem == u'右电机故障':
            if currentsubitem == u'左电机状态' or currentsubitem == u'右电机状态':
                if currentsubitem == u'左电机状态':
                    bid='11'
                else:
                    bid='12'
                mastercmd='19'
                savlecmd='99'
            else:
                if currentsubitem == u'左电机故障':
                    bid='11'
                else:
                    bid='12'
                mastercmd='20'
                savlecmd='a0'
            self.udpmotor=udpmselecthread(bid,mastercmd,savlecmd)
            self.udpmotor.listSingnal.connect(self.udpmotorany)
            self.udpmotor.messSingnal.connect(self.udpmotorerrany)
            self.udpmotor.start()
        else:
            pass

    def udpmotorany(self,messlist):
        self.ucboardChild.reginfo.clear()
        if messlist[0]=='11':
            self.ucboardChild.reginfo.append(u'左电机:')
        else:
            self.ucboardChild.reginfo.append(u'右电机:')
        if messlist[1]=='19':
            self.ucboardChild.reginfo.append(u'电机电流:'+str(messlist[2]))
            self.ucboardChild.reginfo.append(u'位置:'+unicode(messlist[3]))
            self.ucboardChild.reginfo.append(u'电压:'+str(messlist[4]))
            self.ucboardChild.reginfo.append(u'反馈速度:'+unicode(messlist[5]))
            self.ucboardChild.reginfo.append(u'给定速度:'+unicode(messlist[6]))
        elif messlist[1]=='20':
            self.ucboardChild.reginfo.append(u'低字节版本号:'+messlist[2])
            self.ucboardChild.reginfo.append(u'错误码:'+unicode(messlist[3]))
            if unicode(messlist[3])==u'静态电流故障':
                part1=u'静态电流'+str(messlist[4])
                part2=u'A相电流'+str(messlist[5])
                part3=u'B相电流'+str(messlist[6])
                part4=u'C相电流'+str(messlist[7])
            elif unicode(messlist[3])==u'过压':
                part1=u'电压'+str(messlist[4])
                part2=u'part2:'+str(messlist[5])
                part3=u'part3:'+str(messlist[6])
                part4=u'part4:'+str(messlist[7])
            elif unicode(messlist[3])==u'欠压':
                part1=u'电压'+str(messlist[4])
                part2=u'part2:'+str(messlist[5])
                part3=u'part3:'+str(messlist[6])
                part4=u'part4:'+str(messlist[7])
            elif unicode(messlist[3])==u'堵转':
                part1=u'当前电流'+str(messlist[4])
                part2=u'part2:'+str(messlist[5])
                part3=u'part3:'+str(messlist[6])
                part4=u'part4:'+str(messlist[7])
            elif unicode(messlist[3])==u'上下桥故障':
                part1=u'mos桥:'+str(messlist[4])
                part2=u'part2:'+str(messlist[5])
                part3=u'part3:'+str(messlist[6])
                part4=u'part4:'+str(messlist[7])
            else:
                part1=u'part1:'+str(messlist[4])
                part2=u'part2:'+str(messlist[5])
                part3=u'part3:'+str(messlist[6])
                part4=u'part4:'+str(messlist[7])
            self.ucboardChild.reginfo.append(part1)
            self.ucboardChild.reginfo.append(part2)
            self.ucboardChild.reginfo.append(part3)
            self.ucboardChild.reginfo.append(part4)
        else:
            pass

    def udpmotorerrany(self,mess):
        self.ucboardChild.testmessage.append(unicode(mess))

    def ucutmodeltotrans(self):
        tockdata='00000000000000000000000000000000'
        mess='59'+'EE'+'E2'+'11'+'10'+tockdata+'01'
        tocksend=self.messmarge(mess,1)
        cboardudp.sendto(tocksend,('192.168.80.201',6650))
        self.ucboardChild.testmessage.append(tocksend.encode('hex'))
        try:
            recvmess=cboardudp.recv(1024)
            print(recvmess.encode('hex'))
        except:
            pass

    def ucleartestmess(self):
        self.ucboardChild.testmessage.clear()

    def uotaupdate(self):
        self.otaChild = Update_Ui_Dialog()
        self.Dialog = QtGui.QDialog(self)
        self.otaChild.setupUi(self.Dialog)

        currentboard=unicode(self.ucboardChild.otalist.currentItem().text())
        self.Dialog.setWindowTitle(u'OTA升级界面_'+currentboard)
        self.otaChild.otamessage.append(u'已选择'+currentboard+u'升级')
        self.ucboardChild.testitem.clear()
        self.ucboardChild.subtest.clear()
        if currentboard==u'轮毂电机':
            self.otaChild.sublist.setEnabled(True)
            self.otaChild.sublist.addItem(u'左电机')
            self.otaChild.sublist.addItem(u'右电机')
        elif currentboard==u'开门电机':
            self.otaChild.sublist.setEnabled(True)
            self.otaChild.sublist.addItem(u'直流电机1')
            self.otaChild.sublist.addItem(u'直流电机2')
            self.otaChild.sublist.addItem(u'直流电机3')
            self.otaChild.sublist.addItem(u'直流电机4')
        elif currentboard==u'左右箱体控制板':
            self.otaChild.sublist.setEnabled(True)
            self.otaChild.sublist.addItem(u'左箱体')
            self.otaChild.sublist.addItem(u'右箱体')
        elif currentboard==u'红外传感器':
            self.otaChild.sublist.setEnabled(True)
            self.otaChild.sublist.addItem(u'红外1')
            self.otaChild.sublist.addItem(u'红外2')
            self.otaChild.sublist.addItem(u'红外3')
            self.otaChild.sublist.addItem(u'红外4')
            self.otaChild.sublist.addItem(u'红外5')
            self.otaChild.sublist.addItem(u'红外6')
            self.otaChild.sublist.addItem(u'红外7')
            self.otaChild.sublist.addItem(u'红外8')
            self.otaChild.sublist.addItem(u'红外9')
            self.otaChild.sublist.addItem(u'红外10')
        elif currentboard==u'IMU':
            self.otaChild.sublist.setEnabled(True)
            self.otaChild.sublist.addItem(u'IMU')
        elif currentboard=='2.4G':
            self.otaChild.sublist.setEnabled(True)
            self.otaChild.sublist.addItem(u'2.4G')
        elif currentboard=='Board-C':
            self.otaChild.sublist.addItem(u'Board-C')
            self.otaChild.sublist.setEnabled(True)
        else:
            self.otaChild.verlist.setEnabled(True)

        self.softimer=QtCore.QTimer(self)
        self.softimer.setSingleShot(True)
        self.softimer.timeout.connect(self.firmreload)
        self.softimer.start(10)

        self.otaChild.firwareselect.clicked.connect(self.firwareadd)
        self.otaChild.sublist.clicked.connect(self.upenable)
        self.otaChild.verlist.itemDoubleClicked.connect(self.ufirmupdate)
        self.otaChild.pause.clicked.connect(self.upstop)
        self.otaChild.open.clicked.connect(self.reopenser)
        self.otaChild.clear.clicked.connect(self.clearmess)
        self.Dialog.exec_()

    def ufirmupdate(self):
        global errindexflag,errcrcflag
        errindexflag=int(self.otaChild.errindex.isChecked())
        errcrcflag=int(self.otaChild.errcrc.isChecked())
        upflagexist=os.path.exists('log/stopflag.txt')
        if upflagexist:
            os.remove('log/stopflag.txt')
        self.otaChild.upstat.setText(u'开始升级')
        currentfirmware=unicode(self.otaChild.verlist.currentItem().text())
        fullfirmware='firmwares/'+currentfirmware+'.bin'
        self.mdvaluehash(fullfirmware)
        devicebid=self.otabidget()
        self.otauper=uotaupdater(devicebid,fullfirmware)
        self.otauper.bootSingnal.connect(self.bootmessage)
        self.otauper.barSingnal.connect(self.updateprogess)
        self.otauper.start()

    def cboardwindow(self):
        self.cboardChild = Cboard_Ui_Dialog()
        self.Dialog = QtGui.QDialog(self)
        self.cboardChild.setupUi(self.Dialog)

        self.sertimer=QtCore.QTimer(self)
        self.sertimer.setSingleShot(True)
        self.sertimer.timeout.connect(self.serautoget)
        self.sertimer.start(10)

        self.cboardChild.serialset.clicked.connect(self.YGtestCboardSer)
        self.cboardChild.boardlist.itemClicked.connect(self.testitemupdate)
        self.cboardChild.otalist.itemDoubleClicked.connect(self.otaupdate)
        self.cboardChild.testitem.itemClicked.connect(self.subitemtest)
        self.cboardChild.testitem.itemDoubleClicked.connect(self.cstartest)
        self.cboardChild.subtest.itemDoubleClicked.connect(self.itemtest)
        self.cboardChild.close.clicked.connect(self.serialclose)
        self.cboardChild.messclear.clicked.connect(self.cleartestmess)
        self.Dialog.exec_()

    def cstartest(self):
        currentest=unicode(self.cboardChild.testitem.currentItem().text())
        if currentest==u'控制轮毂电机':
            self.motorwindow()
        else:
            pass

    def cleartestmess(self):
        self.cboardChild.testmessage.clear()

    def serautoget(self):
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list) <= 0:
            QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("端口号数量为零，请先连接串口"))
        else:
            pattern_serial='COM.+'
            for line in port_list:
                Match=re.search(pattern_serial,str(line))
                if Match:
                    new_line=str(line).split(' - ')
                    self.cboardChild.serialnum.addItem(new_line[0])

    def YGtestCboardSer(self):
        global Ygcboardev

        try:
            Ygcboardev.close()
        except:
            pass
        try:
            titodevice.close()
        except:
            pass
        sernum=str(self.cboardChild.serialnum.currentText())
        rate=int(self.cboardChild.boundrate.currentText())

        try:
            Ygcboardev=serial.Serial(sernum,rate,timeout=5)
            status=u'YG协议单板C测试-'+str.upper(sernum)+':'+str(rate)+':READ'
            self.Dialog.setWindowTitle(status)
            self.cboardChild.boardlist.setEnabled(True)
            self.cboardChild.otalist.setEnabled(True)
            self.cboardChild.serialset.setDisabled(True)
            self.cboardChild.close.setEnabled(True)
        except:
            QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("串口打开失败，请检查设置"))

    def serialclose(self):
        Ygcboardev.close()
        self.cboardChild.serialset.setEnabled(True)
        self.cboardChild.boardlist.setDisabled(True)
        self.cboardChild.otalist.setDisabled(True)
        status=u'YG协议单板C测试'
        self.Dialog.setWindowTitle(status)

    def testitemupdate(self):
        self.cboardChild.SN.setDisabled(True)
        self.cboardChild.BID.setDisabled(True)
        self.cboardChild.hardver.setDisabled(True)
        self.cboardChild.softver.setDisabled(True)
        self.cboardChild.protover.setDisabled(True)
        self.cboardChild.testitem.clear()
        self.cboardChild.subtest.clear()
        self.cboardChild.testitem.addItem(u'读取通用寄存器信息')
        self.cboardChild.testitem.addItem(u'SN')
        self.cboardChild.testitem.addItem(u'BID')
        self.cboardChild.testitem.addItem(u'硬件版本号')
        self.cboardChild.testitem.addItem(u'软件版本号')
        self.cboardChild.testitem.addItem(u'协议版本号')
        currentobject=(unicode(self.cboardChild.boardlist.currentItem().text()))
        if currentobject ==u'Board-C':
            self.cboardChild.testitem.addItem(u'模式切换')
            self.cboardChild.testitem.addItem(u'查询电机状态')
            self.cboardChild.testitem.addItem(u'查询电机故障')
        elif currentobject ==u'左轮毂电机' or currentobject ==u'右轮毂电机':
                self.cboardChild.testitem.addItem(u'控制轮毂电机')
        elif currentobject ==u'直流电机1' or currentobject ==u'直流电机2' or currentobject ==u'直流电机3' or currentobject ==u'直流电机4':
            self.cboardChild.testitem.addItem(u'开门')
            self.cboardChild.testitem.addItem(u'关门')
        elif currentobject ==u'左箱体控制板' or currentobject ==u'右箱体控制板':
            self.cboardChild.testitem.addItem(u'开门')
            self.cboardChild.testitem.addItem(u'关门')
        elif currentobject ==u'灯光控制':
            self.cboardChild.testitem.addItem(u'设置灯效')
        else:
            self.cboardChild.testitem.addItem(u'获取状态')

    def subitemtest(self):
        currentitem=unicode(self.cboardChild.testitem.currentItem().text())
        self.cboardChild.subtest.clear()
        if currentitem == u'读取通用寄存器信息':
            self.cboardChild.subtest.addItem(u'读取指令测试')
            self.cboardChild.subtest.addItem(u'读取64byte')
            self.cboardChild.subtest.addItem(u'读取65byte')
            self.cboardChild.subtest.addItem(u'读取起始地址65')
            self.cboardChild.subtest.addItem(u'CRC错误帧')
            self.cboardChild.subtest.addItem(u'LEN错误帧')
            self.cboardChild.subtest.addItem(u'seq错误帧')
        elif currentitem == u'SN':
            self.cboardChild.SN.setEnabled(True)
            self.cboardChild.subtest.addItem(u'写入SN')
            self.cboardChild.subtest.addItem(u'读取SN')
            self.cboardChild.subtest.addItem(u'CRC错误帧')
            self.cboardChild.subtest.addItem(u'LEN错误帧')
            self.cboardChild.subtest.addItem(u'seq错误帧')
            currentobject=(unicode(self.cboardChild.boardlist.currentItem().text()))
            boardid=str(self.boardidset(currentobject))
            if boardid=='EE':
                self.cboardChild.SN.setText('YOGOC201900000000001')
            else:
                pass
        elif currentitem == u'BID':
            self.cboardChild.BID.setEnabled(True)
            self.cboardChild.subtest.addItem(u'写入BID')
        elif currentitem == u'硬件版本号':
            self.cboardChild.hardver.setEnabled(True)
            self.cboardChild.subtest.addItem(u'写入硬件版本号')
            self.cboardChild.subtest.addItem(u'读取硬件版本号')
            self.cboardChild.subtest.addItem(u'CRC错误帧')
            self.cboardChild.subtest.addItem(u'LEN错误帧')
            self.cboardChild.subtest.addItem(u'seq错误帧')
        elif currentitem == u'软件版本号':
            self.cboardChild.subtest.addItem(u'读取软件版本号')
            self.cboardChild.subtest.addItem(u'CRC错误帧')
            self.cboardChild.subtest.addItem(u'LEN错误帧')
            self.cboardChild.subtest.addItem(u'seq错误帧')
        elif currentitem == u'协议版本号':
            self.cboardChild.subtest.addItem(u'读取协议版本号')
            self.cboardChild.subtest.addItem(u'CRC错误帧')
            self.cboardChild.subtest.addItem(u'LEN错误帧')
            self.cboardChild.subtest.addItem(u'seq错误帧')
        elif currentitem == u'模式切换':
            self.cboardChild.subtest.addItem(u'切换到正常')
            self.cboardChild.subtest.addItem(u'切换到转发')
            self.cboardChild.subtest.addItem(u'CRC错误帧')
            self.cboardChild.subtest.addItem(u'LEN错误帧')
            self.cboardChild.subtest.addItem(u'seq错误帧')
        elif currentitem == u'查询电机状态':
            self.cboardChild.subtest.addItem(u'左电机状态')
            self.cboardChild.subtest.addItem(u'右电机状态')
        elif currentitem == u'查询电机故障':
            self.cboardChild.subtest.addItem(u'左电机故障')
            self.cboardChild.subtest.addItem(u'右电机故障')
        else:
            pass

    def itemtest(self):
        currentsubitem=unicode(self.cboardChild.subtest.currentItem().text())
        if currentsubitem == u'切换到正常':
            self.cutmodeltonormal()
        elif currentsubitem == u'切换到转发':
            self.cutmodeltotrans()
        elif currentsubitem == u'写入SN':
            self.writeserialnumber()
        elif currentsubitem == u'写入硬件版本号':
            self.writehardware()
        else:
            self.cboardChild.testmessage.append(u'开始接收C板tick')
            self.ticker=tickrecvthread()
            self.ticker.startSingnal.connect(self.startock)
            self.ticker.messSingnal.connect(self.tickmess)
            self.ticker.start()

    def startock(self,seq):
        currentobject=(unicode(self.cboardChild.boardlist.currentItem().text()))
        boardid=str(self.boardidset(currentobject))
        currentitem=(unicode(self.cboardChild.testitem.currentItem().text()))
        currensubtitem=(unicode(self.cboardChild.subtest.currentItem().text()))
        tockdata='00000000000000000000000000000000'
        if currentitem==u'读取通用寄存器信息':
            cmd='00'
            if currensubtitem == u'读取指令测试':#用于测试读指令，没有data返回值
                mess='59'+str(boardid)+'80'+'13'+'10'+tockdata+'01'+'01'+seq
                tocksend=self.messmarge(mess,1)
                self.cboardChild.testmessage.append('tock:'+tocksend.encode('hex'))
                Ygcboardev.write(tocksend)
                Ygcboardev.flushInput()
                self.tockgeter=titothread(boardid,cmd)
                self.tockgeter.messSingnal.connect(self.tockmess)
                self.tockgeter.start()
            elif currensubtitem == u'读取64byte':
                mess='59'+str(boardid)+'80'+'13'+'10'+tockdata+'00'+'40'+seq
                tocksend=self.messmarge(mess,1)
                self.cboardChild.testmessage.append('tock:'+tocksend.encode('hex'))
                Ygcboardev.write(tocksend)
                Ygcboardev.flushInput()
                self.tockgeter=titothread(boardid,cmd)
                self.tockgeter.messSingnal.connect(self.tockmess)
                self.tockgeter.start()
            elif currensubtitem == u'读取65byte':
                mess='59'+str(boardid)+'80'+'13'+'10'+tockdata+'00'+'41'+seq
                tocksend=self.messmarge(mess,1)
                self.cboardChild.testmessage.append('tock:'+tocksend.encode('hex'))
                Ygcboardev.write(tocksend)
                Ygcboardev.flushInput()
                self.tockgeter=titothread(boardid,cmd)
                self.tockgeter.messSingnal.connect(self.tockmess)
                self.tockgeter.start()
            elif currensubtitem == u'读取起始地址65':
                mess='59'+str(boardid)+'80'+'13'+'10'+tockdata+'41'+'00'+seq
                tocksend=self.messmarge(mess,1)
                self.cboardChild.testmessage.append('tock:'+tocksend.encode('hex'))
                Ygcboardev.write(tocksend)
                Ygcboardev.flushInput()
                self.tockgeter=titothread(boardid,cmd)
                self.tockgeter.messSingnal.connect(self.tockmess)
                self.tockgeter.start()
            elif currensubtitem == u'CRC错误帧':
                mess='59'+str(boardid)+'80'+'13'+'10'+tockdata+'00'+'00'+seq
                tocksend=self.messmarge(mess,0)
                self.cboardChild.testmessage.append('tock:'+tocksend.encode('hex'))
                Ygcboardev.write(tocksend)
                Ygcboardev.flushInput()
                self.tockgeter=tickrecvthread()
                self.tockgeter.messSingnal.connect(self.tockmess)
                self.tockgeter.start()
            elif currensubtitem == u'LEN错误帧':
                mess='59'+str(boardid)+'80'+'15'+'10'+tockdata+'00'+'00'+seq
                tocksend=self.messmarge(mess,1)
                self.cboardChild.testmessage.append('tock:'+tocksend.encode('hex'))
                Ygcboardev.write(tocksend)
                Ygcboardev.flushInput()
                self.tockgeter=tickrecvthread()
                self.tockgeter.messSingnal.connect(self.tockmess)
                self.tockgeter.start()
            else:#tock回复错误seq
                newseq='0x'+str(seq)
                errseq=hex(int(newseq,16)+1).lstrip('0x')
                if len(errseq)==1:
                    errseq='0'+errseq
                mess='59'+str(boardid)+'80'+'13'+'10'+tockdata+'00'+'00'+errseq
                tocksend=self.messmarge(mess,1)
                self.cboardChild.testmessage.append('tock:'+tocksend.encode('hex'))
                Ygcboardev.write(tocksend)
                Ygcboardev.flushInput()
                self.tockgeter=titothread(boardid,cmd)
                self.tockgeter.messSingnal.connect(self.tockmess)
                self.tockgeter.start()
        elif currentitem==u'SN':
            model=1
            if model:
                if currensubtitem == u'写入SN':
                    cmd='71'
                    snchar=''
                    newsn=str(self.cboardChild.SN.toPlainText())
                    if newsn!='':
                        lensn=hex(len(newsn)).lstrip('0x')
                        if len(lensn)==1:
                            lensn='0'+lensn
                        for line in newsn:
                            hexline=hex(ord(line)).lstrip('0x')
                            if len(hexline)==1:
                                hexline='0'+hexline
                            snchar+=hexline
                        self.cboardChild.testmessage.append(u'SN长度:'+str(len(newsn)))
                        newlen=hex(len(snchar)+1).lstrip('0x')
                        if len(newlen)==1:
                            newlen='0'+newlen
                        #mess='59'+str(boardid)+'71'+newlen+lensn+snchar+seq
                        mess='59'+str(boardid)+'F1'+lensn+snchar+seq
                        tocksend=self.messmarge(mess,1)
                        self.cboardChild.testmessage.append('tock:'+tocksend.encode('hex'))
                        Ygcboardev.write(tocksend)
                        Ygcboardev.flushInput()
                        self.tockgeter=titothread(boardid,cmd)
                        self.tockgeter.messSingnal.connect(self.tockmess)
                        self.tockgeter.start()
                    else:
                        self.cboardChild.testmessage.append(u'不能写入空sn，请重新输入')
                elif currensubtitem == u'读取SN':
                    cmd='00'
                    mess='59'+str(boardid)+'80'+'13'+'10'+tockdata+'0D'+'14'+seq
                    tocksend=self.messmarge(mess,1)
                    self.cboardChild.testmessage.append('tock:'+tocksend.encode('hex'))
                    Ygcboardev.write(tocksend)
                    Ygcboardev.flushInput()
                    self.tockgeter=titothread(boardid,cmd)
                    self.tockgeter.messSingnal.connect(self.tockmess)
                    self.tockgeter.start()
                elif currensubtitem == u'CRC错误帧':
                    mess='59'+str(boardid)+'80'+'13'+'10'+tockdata+'0D'+'14'+seq
                    tocksend=self.messmarge(mess,0)
                    self.cboardChild.testmessage.append('tock:'+tocksend.encode('hex'))
                    Ygcboardev.write(tocksend)
                    Ygcboardev.flushInput()
                    self.tockgeter=tickrecvthread()
                    self.tockgeter.messSingnal.connect(self.tockmess)
                    self.tockgeter.start()
                elif currensubtitem == u'LEN错误帧':
                    mess='59'+str(boardid)+'80'+'15'+'10'+tockdata+'0D'+'14'+seq
                    tocksend=self.messmarge(mess,1)
                    self.cboardChild.testmessage.append('tock:'+tocksend.encode('hex'))
                    Ygcboardev.write(tocksend)
                    Ygcboardev.flushInput()
                    self.tockgeter=tickrecvthread()
                    self.tockgeter.messSingnal.connect(self.tockmess)
                    self.tockgeter.start()
                else:#tock回复错误seq
                    cmd='00'
                    newseq='0x'+str(seq)
                    errseq=hex(int(newseq,16)+1).lstrip('0x')
                    if len(errseq)==1:
                        errseq='0'+errseq
                    mess='59'+str(boardid)+'80'+'13'+'10'+tockdata+'0D'+'14'+errseq
                    tocksend=self.messmarge(mess,1)
                    self.cboardChild.testmessage.append('tock:'+tocksend.encode('hex'))
                    Ygcboardev.write(tocksend)
                    Ygcboardev.flushInput()
                    self.tockgeter=titothread(boardid,cmd)
                    self.tockgeter.messSingnal.connect(self.tockmess)
                    self.tockgeter.start()
        elif currentitem==u'BID':
            cmd='73'
            if currensubtitem == u'写入BID':
                bid=str(self.cboardChild.BID.toPlainText())
                if bid!='':
                    if len(bid)!=2:
                        self.cboardChild.testmessage.append(u'BID长度必须是2')
                    else:
                        mess='59'+str(boardid)+'F3'+'13'+'10'+tockdata+'01'+bid+seq
                        tocksend=self.messmarge(mess,1)
                        self.cboardChild.testmessage.append('tock:'+tocksend.encode('hex'))
                        Ygcboardev.write(tocksend)
                        Ygcboardev.flushInput()
                        self.tockgeter=titothread(boardid,cmd)
                        self.tockgeter.messSingnal.connect(self.tockmess)
                        self.tockgeter.start()
                else:
                    self.cboardChild.testmessage.append(u'不能写入空sn，请重新输入')
        elif currentitem==u'硬件版本号':
            newhardver=str(self.cboardChild.hardver.toPlainText())
            if currensubtitem == u'读取硬件版本号':
                cmd='00'
                mess='59'+str(boardid)+'80'+'13'+'10'+tockdata+'21'+'02'+seq
                tocksend=self.messmarge(mess,1)
                self.cboardChild.testmessage.append('tock:'+tocksend.encode('hex'))
                Ygcboardev.write(tocksend)
                Ygcboardev.flushInput()
                self.tockgeter=titothread(boardid,cmd)
                self.tockgeter.messSingnal.connect(self.tockmess)
                self.tockgeter.start()
            elif currensubtitem == u'CRC错误帧':
                cmd='00'
                mess='59'+str(boardid)+'80'+'13'+'10'+tockdata+'21'+'02'+seq
                tocksend=self.messmarge(mess,0)
                self.cboardChild.testmessage.append('tock:'+tocksend.encode('hex'))
                Ygcboardev.write(tocksend)
                Ygcboardev.flushInput()
                self.tockgeter=tickrecvthread()
                self.tockgeter.messSingnal.connect(self.tockmess)
                self.tockgeter.start()
            elif currensubtitem == u'LEN错误帧':
                cmd='00'
                mess='59'+str(boardid)+'80'+'15'+'10'+tockdata+'21'+'02'+seq
                tocksend=self.messmarge(mess,1)
                self.cboardChild.testmessage.append('tock:'+tocksend.encode('hex'))
                Ygcboardev.write(tocksend)
                Ygcboardev.flushInput()
                self.tockgeter=tickrecvthread()
                self.tockgeter.messSingnal.connect(self.tockmess)
                self.tockgeter.start()
            else:#tock回复错误seq
                cmd='00'
                newseq='0x'+str(seq)
                errseq=hex(int(newseq,16)+1).lstrip('0x')
                if len(errseq)==1:
                    errseq='0'+errseq
                mess='59'+str(boardid)+'80'+'13'+'10'+tockdata+'21'+'02'+errseq
                tocksend=self.messmarge(mess,1)
                self.cboardChild.testmessage.append('tock:'+tocksend.encode('hex'))
                Ygcboardev.write(tocksend)
                Ygcboardev.flushInput()
                self.tockgeter=tickrecvthread()
                self.tockgeter.messSingnal.connect(self.tockmess)
                self.tockgeter.start()
        elif currentitem==u'软件版本号':
            if currensubtitem == u'读取软件版本号':
                cmd='00'
                mess='59'+str(boardid)+'80'+'13'+'10'+tockdata+'23'+'02'+seq
                tocksend=self.messmarge(mess,1)
                self.cboardChild.testmessage.append('tock:'+tocksend.encode('hex'))

                Ygcboardev.write(tocksend)
                Ygcboardev.flushInput()
                self.tockgeter=titothread(boardid,cmd)
                self.tockgeter.messSingnal.connect(self.tockmess)
                self.tockgeter.start()
            elif currensubtitem == u'CRC错误帧':
                cmd='00'
                mess='59'+str(boardid)+'80'+'13'+'10'+tockdata+'23'+'02'+seq
                tocksend=self.messmarge(mess,0)
                self.cboardChild.testmessage.append('tock:'+tocksend.encode('hex'))
                Ygcboardev.flushInput()
                Ygcboardev.write(tocksend)
                self.tockgeter=tickrecvthread()
                self.tockgeter.messSingnal.connect(self.tockmess)
                self.tockgeter.start()
            elif currensubtitem == u'LEN错误帧':
                cmd='00'
                mess='59'+str(boardid)+'80'+'15'+'10'+tockdata+'23'+'02'+seq
                tocksend=self.messmarge(mess,1)
                self.cboardChild.testmessage.append('tock:'+tocksend.encode('hex'))
                Ygcboardev.write(tocksend)
                Ygcboardev.flushInput()
                self.tockgeter=tickrecvthread()
                self.tockgeter.messSingnal.connect(self.tockmess)
                self.tockgeter.start()
            else:#tock回复错误seq
                cmd='00'
                newseq='0x'+str(seq)
                errseq=hex(int(newseq,16)+1).lstrip('0x')
                if len(errseq)==1:
                    errseq='0'+errseq
                mess='59'+str(boardid)+'80'+'13'+'10'+tockdata+'23'+'02'+errseq
                tocksend=self.messmarge(mess,1)
                self.cboardChild.testmessage.append('tock:'+tocksend.encode('hex'))
                Ygcboardev.write(tocksend)
                Ygcboardev.flushInput()
                self.tockgeter=tickrecvthread()
                self.tockgeter.messSingnal.connect(self.tockmess)
                self.tockgeter.start()
        elif currentitem==u'协议版本号':
            if currensubtitem == u'读取协议版本号':
                cmd='00'
                mess='59'+str(boardid)+'80'+'13'+'10'+tockdata+'25'+'02'+seq
                tocksend=self.messmarge(mess,1)
                self.cboardChild.testmessage.append('tock:'+tocksend.encode('hex'))
                Ygcboardev.write(tocksend)
                Ygcboardev.flushInput()
                self.tockgeter=titothread(boardid,cmd)
                self.tockgeter.messSingnal.connect(self.tockmess)
                self.tockgeter.start()
            elif currensubtitem == u'CRC错误帧':
                cmd='00'
                mess='59'+str(boardid)+'80'+'13'+'10'+tockdata+'25'+'02'+seq
                tocksend=self.messmarge(mess,0)
                self.cboardChild.testmessage.append('tock:'+tocksend.encode('hex'))
                Ygcboardev.write(tocksend)
                Ygcboardev.flushInput()
                self.tockgeter=tickrecvthread()
                self.tockgeter.messSingnal.connect(self.tockmess)
                self.tockgeter.start()
            elif currensubtitem == u'LEN错误帧':
                cmd='00'
                mess='59'+str(boardid)+'80'+'15'+'10'+tockdata+'25'+'02'+seq
                tocksend=self.messmarge(mess,1)
                self.cboardChild.testmessage.append('tock:'+tocksend.encode('hex'))
                Ygcboardev.write(tocksend)
                Ygcboardev.flushInput()
                self.tockgeter=tickrecvthread()
                self.tockgeter.messSingnal.connect(self.tockmess)
                self.tockgeter.start()
            else:#tock回复错误seq
                cmd='00'
                newseq='0x'+str(seq)
                errseq=hex(int(newseq,16)+1).lstrip('0x')
                if len(errseq)==1:
                    errseq='0'+errseq
                mess='59'+str(boardid)+'80'+'13'+'10'+tockdata+'25'+'02'+errseq
                tocksend=self.messmarge(mess,1)
                self.cboardChild.testmessage.append('tock:'+tocksend.encode('hex'))
                Ygcboardev.write(tocksend)
                Ygcboardev.flushInput()
                self.tockgeter=tickrecvthread()
                self.tockgeter.messSingnal.connect(self.tockmess)
                self.tockgeter.start()
        elif currentitem==u'查询电机状态':
            mastercmd='19'
            savlecmd='99'
            if currensubtitem==u'左电机状态':
                boardid='11'
            else:
                boardid='12'
            self.tockgeter=mselecthread(boardid,mastercmd,savlecmd)
            self.tockgeter.listSingnal.connect(self.motorcmdany)
            self.tockgeter.start()
        elif currentitem==u'查询电机故障':
            mastercmd='20'
            savlecmd='a0'
            if currensubtitem==u'左电机故障':
                boardid='11'
            else:
                boardid='12'

            self.tockgeter=mselecthread(boardid,mastercmd,savlecmd)
            self.tockgeter.listSingnal.connect(self.motorcmdany)
            self.tockgeter.start()

        else:
            if currentitem==u'模式切换':
                pass
        #return boardid,cmd

    def motorcmdany(self,messlist):
        self.cboardChild.reginfo.clear()
        if messlist[0]=='11':
            self.cboardChild.reginfo.append(u'左电机:')
        else:
            self.cboardChild.reginfo.append(u'右电机:')
        if messlist[1]=='19':
            self.cboardChild.reginfo.append(u'电机电流:'+str(messlist[2]))
            self.cboardChild.reginfo.append(u'位置:'+unicode(messlist[3]))
            self.cboardChild.reginfo.append(u'电压:'+str(messlist[4]))
            self.cboardChild.reginfo.append(u'给定速度:'+unicode(messlist[5]))
            self.cboardChild.reginfo.append(u'反馈速度:'+unicode(messlist[6]))
        elif messlist[1]=='20':
            self.cboardChild.reginfo.append(u'低字节版本号:'+messlist[2])
            self.cboardChild.reginfo.append(u'错误码:'+unicode(messlist[3]))
            if unicode(messlist[3])==u'静态电流故障':
                part1=u'静态电流'+str(messlist[4])
                part2=u'A相电流'+str(messlist[5])
                part3=u'B相电流'+str(messlist[6])
                part4=u'C相电流'+str(messlist[7])
            elif unicode(messlist[3])==u'过压':
                part1=u'电压'+str(messlist[4])
                part2=u'part2:'+str(messlist[5])
                part3=u'part3:'+str(messlist[6])
                part4=u'part4:'+str(messlist[7])
            elif unicode(messlist[3])==u'欠压':
                part1=u'电压'+str(messlist[4])
                part2=u'part2:'+str(messlist[5])
                part3=u'part3:'+str(messlist[6])
                part4=u'part4:'+str(messlist[7])
            elif unicode(messlist[3])==u'堵转':
                part1=u'当前电流'+str(messlist[4])
                part2=u'part2:'+str(messlist[5])
                part3=u'part3:'+str(messlist[6])
                part4=u'part4:'+str(messlist[7])
            elif unicode(messlist[3])==u'上下桥故障':
                part1=u'mos桥:'+str(messlist[4])
                part2=u'part2:'+str(messlist[5])
                part3=u'part3:'+str(messlist[6])
                part4=u'part4:'+str(messlist[7])
            else:
                part1=u'part1:'+str(messlist[4])
                part2=u'part2:'+str(messlist[5])
                part3=u'part3:'+str(messlist[6])
                part4=u'part4:'+str(messlist[7])
            self.cboardChild.reginfo.append(part1)
            self.cboardChild.reginfo.append(part2)
            self.cboardChild.reginfo.append(part3)
            self.cboardChild.reginfo.append(part4)
        else:
            pass

    def tockmess(self,mess):
        self.cboardChild.testmessage.append('tick:'+mess)
        currensubtitem=(unicode(self.cboardChild.subtest.currentItem().text()))
        if currensubtitem == u'读取指令测试':
            if mess[138:140] == '00':
                self.cboardChild.testmessage.append(u'读取指令测试通过')
            else:
                self.cboardChild.testmessage.append(u'读取指令测试失败')
        elif currensubtitem == u'读取64byte':
            if mess[148:150] == '00':
                if mess[6:8] == '88':
                    self.tickany(mess)
                    self.cboardChild.testmessage.append(u'读取64byte测试通过')
            else:
                self.cboardChild.testmessage.append(u'读取64byte测试失败')
        elif currensubtitem == u'读取65byte':
            if mess[6:8] == '42':
                if mess[138:140] == '00':
                    self.cboardChild.testmessage.append(u'读取65byte测试失败')
                else:
                    self.cboardChild.testmessage.append(u'读取65byte测试通过')
            else:
                self.cboardChild.testmessage.append(u'读取65byte测试失败')
        elif currensubtitem == u'读取起始地址65':
            if mess[6:8] == '42':
                if mess[138:140] == '00':
                    self.cboardChild.testmessage.append(u'读取起始地址65测试失败')
                else:
                    self.cboardChild.testmessage.append(u'读取起始地址65测试通过')
            else:
                self.cboardChild.testmessage.append(u'读取起始地址65测试失败')
        elif currensubtitem == u'CRC错误帧':
            if len(mess) != 146:
                self.cboardChild.testmessage.append(u'CRC错误帧测试失败')
            else:
                self.cboardChild.testmessage.append(u'CRC错误帧测试通过')
        elif currensubtitem == u'LEN错误帧':
            if len(mess) != 146:
                self.cboardChild.testmessage.append(u'LEN错误帧测试失败')
            else:
                self.cboardChild.testmessage.append(u'LEN错误帧测试通过')
        elif currensubtitem == u'seq错误帧':
            if len(mess) != 146:
                self.cboardChild.testmessage.append(u'seq错误帧测试失败')
            else:
                self.cboardChild.testmessage.append(u'seq错误帧测试通过')
        elif currensubtitem == u'写入SN':
            if mess[4:6] == 'f1':
                if mess[8:10] == '00':
                    self.cboardChild.testmessage.append(u'SN已写入')
                else:
                    self.cboardChild.testmessage.append(u'SN写入失败')
            else:
                self.cboardChild.testmessage.append(u'SN写入失败')
        elif currensubtitem == u'读取SN':
            self.cboardChild.SN.clear()
            devicesn=''
            if mess[146:148] == '00':
                try:
                    readsn=str(mess[152:192])
                    for i in range(0,len(readsn),2):
                        devicesn+=chr(int(readsn[i:i+2],16))
                    self.cboardChild.SN.setText(devicesn)
                    self.cboardChild.testmessage.append(u'SN读取成功')
                except:
                    self.cboardChild.testmessage.append(u'SN读取失败')
            else:
                self.cboardChild.testmessage.append(u'SN读取失败')
        elif currensubtitem == u'写入BID':
            if mess[138:140] == '00':
                self.cboardChild.testmessage.append(u'BID不能在tick/tock更改，系统回复写入成功，测试失败')
            else:
                self.cboardChild.testmessage.append(u'系统回复BID不能写入，测试通过')
        elif currensubtitem == u'写入硬件版本号':
            if mess[8:10] == '00':
                self.cboardChild.testmessage.append(u'硬件版本号写入成功')
            else:
                self.cboardChild.testmessage.append(u'硬件版本号写入失败')
        elif currensubtitem == u'读取硬件版本号':
            if mess[146:148] == '00':
                hardver=mess[152:156]
                self.cboardChild.hardver.setText('V'+hardver[0]+'.'+hardver[1]+'.'+hardver[2]+'.'+hardver[3])
                self.cboardChild.testmessage.append(u'硬件版本号已读取')
            else:
                self.cboardChild.testmessage.append(u'硬件版本号读取失败')
        elif currensubtitem == u'写入软件版本号':
            if mess[138:140] == '00':
                self.cboardChild.testmessage.append(u'软件版本号已写入')
            else:
                self.cboardChild.testmessage.append(u'软件版本号写入失败')
        elif currensubtitem == u'读取软件版本号':
            if mess[146:148] == '00':
                softverinfo='V'+mess[152]+'.'+mess[153]+'.'+mess[154]+'.'+mess[155]
                self.cboardChild.softver.setText(softverinfo)
                self.cboardChild.testmessage.append(u'软件版本号已读取')
            else:
                self.cboardChild.testmessage.append(u'软件版本号读取失败')
        elif currensubtitem == u'写入协议版本号':
            if mess[138:140] == '00':
                self.cboardChild.testmessage.append(u'协议版本号已写入')
            else:
                self.cboardChild.testmessage.append(u'协议版本号写入失败')
        elif currensubtitem == u'读取协议版本号':
            if mess[146:148] == '00':
                protover=mess[152:156]
                self.cboardChild.protover.setText('V'+protover[0]+'.'+protover[1]+'.'+protover[2]+'.'+protover[3])
                self.cboardChild.testmessage.append(u'协议版本号已读取')
            else:
                self.cboardChild.testmessage.append(u'协议版本号读取失败')
        elif currensubtitem == u'切换到转发':
            if mess[138:140] == '00':
                self.cboardChild.testmessage.append(u'已切换到转发模式')
            else:
                self.cboardChild.testmessage.append(u'切换到转发模式失败')

    def tickany(self,mess):
        self.cboardChild.reginfo.clear()
        devicesn=''
        cpuid=mess[154:178]
        self.cboardChild.reginfo.append('CPUID:'+cpuid)
        sn=str(mess[178:218])
        for i in range(0,40,2):
            devicesn+=chr(int(sn[i:i+2],16))
        self.cboardChild.SN.setText(devicesn)
        hardver=mess[218:222]
        self.cboardChild.hardver.setText('V'+hardver[0]+'.'+hardver[1]+'.'+hardver[2]+'.'+hardver[3])
        softver=mess[222:226]
        self.cboardChild.softver.setText('V'+softver[0]+'.'+softver[1]+'.'+softver[2]+'.'+softver[3])
        protover=mess[226:230]
        self.cboardChild.protover.setText('V'+protover[0]+'.'+protover[1]+'.'+protover[2]+'.'+protover[3])
        bootver=mess[230:234]
        self.cboardChild.bootver.setText('V'+bootver[0]+'.'+bootver[1]+'.'+bootver[2]+'.'+bootver[3])
        hextemp=str(mess[246:248])
        cputemp=int(hextemp,16)
        self.cboardChild.reginfo.append(u'板子温度:'+str(cputemp))

        hexsend=str(mess[254:256]+mess[252:254]+mess[250:252]+mess[248:250])
        sendcount=int(hexsend,16)
        self.cboardChild.reginfo.append(u'发出的包数:'+str(sendcount))

        hexrecv=str(mess[262:263]+mess[260:262]+mess[258:260]+mess[256:258])
        recvcount=int(hexrecv,16)
        self.cboardChild.reginfo.append(u'收到的包数:'+str(recvcount))

        hexrecverr=str(mess[270:272]+mess[268:270]+mess[266:268]+mess[264:266])
        errecvcount=int(hexrecverr,16)
        self.cboardChild.reginfo.append(u'收到的包解析错误个数:'+str(errecvcount))

        hexwarr=str(mess[272:274])
        warrcode=int(hexwarr,16)
        if warrcode==1:
            self.cboardChild.reginfo.append('WarningCode:'+u'丢包过多')
        elif warrcode==2:
            self.cboardChild.reginfo.append('WarningCode:'+u'重启过')
        elif warrcode==3:
            self.cboardChild.reginfo.append('WarningCode:'+u'丢包过多,重启过')
        elif warrcode==4:
            self.cboardChild.reginfo.append('WarningCode:'+u'CPU温度过高')
        elif warrcode==5:
            self.cboardChild.reginfo.append('WarningCode:'+u'丢包过多,CPU温度过高')
        elif warrcode==6:
            self.cboardChild.reginfo.append('WarningCode:'+u'重启过,CPU温度过高')
        elif warrcode==7:
            self.cboardChild.reginfo.append('WarningCode:'+u'丢包过多,重启过,CPU温度过高')
        else:
            self.cboardChild.reginfo.append('WarningCode:'+u'正常')

        hexerr=str(mess[274:276])
        if hexerr == '00':
            self.cboardChild.reginfo.append('ErrCode:'+u'正常')
        else:
            self.cboardChild.reginfo.append('ErrCode:'+u'设备故障')

        hexmodel=str(mess[268:270])
        if hexmodel == '00':
            self.cboardChild.reginfo.append(u'工作模式:'+u'正常模式')
        else:
            self.cboardChild.reginfo.append(u'工作模式:'+u'转发模式')

    def writeserialnumber(self):
        currentobject=(unicode(self.cboardChild.boardlist.currentItem().text()))
        boardid=str(self.boardidset(currentobject))
        cmd='F1'
        snchar=''
        newsn=str(self.cboardChild.SN.toPlainText())
        if newsn!='':
            lensn=hex(len(newsn)).lstrip('0x')
            if len(lensn)==1:
                lensn='0'+lensn
            for line in newsn:
                hexline=hex(ord(line)).lstrip('0x')
                if len(hexline)==1:
                    hexline='0'+hexline
                snchar+=hexline
            self.cboardChild.testmessage.append(u'SN长度:'+str(len(newsn)))
            newlen=hex(len(snchar)+1).lstrip('0x')
            if len(newlen)==1:
                newlen='0'+newlen
            mess='59'+str(boardid)+'71'+lensn+snchar+'00'
            tocksend=self.messmarge(mess,1)
            self.cboardChild.testmessage.append('tock:'+tocksend.encode('hex'))
            Ygcboardev.write(tocksend)
            Ygcboardev.flushInput()
            self.tockgeter=titothread(boardid,cmd)
            self.tockgeter.messSingnal.connect(self.tockmess)
            self.tockgeter.start()
        else:
            self.cboardChild.testmessage.append(u'不能写入空sn，请重新输入')

    def writehardware(self):
        currentobject=(unicode(self.cboardChild.boardlist.currentItem().text()))
        boardid=str(self.boardidset(currentobject))
        cmd='F2'
        hardchar=''
        newhard=str(self.cboardChild.hardver.toPlainText())
        if newhard!='':
            lenhard=hex(int(len(newhard)/2)).lstrip('0x')
            if len(lenhard)==1:
                lenhard='0'+lenhard
            hardchar=newhard[0]+newhard[1]+newhard[2]+newhard[3]
            self.cboardChild.testmessage.append(u'SN长度:'+str(len(newhard)))
            mess='59'+str(boardid)+'72'+lenhard+hardchar+'00'
            print(mess)
            tocksend=self.messmarge(mess,1)
            self.cboardChild.testmessage.append('tock:'+tocksend.encode('hex'))
            Ygcboardev.write(tocksend)
            Ygcboardev.flushInput()
            self.tockgeter=titothread(boardid,cmd)
            self.tockgeter.messSingnal.connect(self.tockmess)
            self.tockgeter.start()
        else:
            self.cboardChild.testmessage.append(u'不能写入空硬件版本号，请重新输入')

    def cutmodeltotrans(self):
        tockdata='00000000000000000000000000000000'
        mess='59'+'EE'+'E2'+'15'+'10'+tockdata+'01000000'+'01'
        tocksend=self.messmarge(mess,1)
        Ygcboardev.flushInput()
        Ygcboardev.write(tocksend)
        self.cboardChild.testmessage.append(tocksend.encode('hex'))
        self.cuter=cutmodelthread(0)
        self.cuter.messSingnal.connect(self.cutmess)
        self.cuter.seqSingnal.connect(self.startock)
        self.cuter.start()

    def cutmodeltonormal(self):
        mess=str('59'+'EE'+'62'+'04'+'00'+'000000'+'01'+'90E547')
        tocksend=self.messmarge(mess,1)
        Ygcboardev.flushInput()
        Ygcboardev.write(tocksend)
        self.cboardChild.testmessage.append(tocksend.encode('hex'))
        self.cuter=cutmodelthread(1)
        self.cuter.messSingnal.connect(self.cutmess)
        self.cuter.seqSingnal.connect(self.startock)
        self.cuter.start()

    def udptitowindow(self):
        global udpclient,udpwin

        self.udpChild = Udp_Ui_Dialog()
        self.Dialog = QtGui.QDialog(self)
        self.udpChild.setupUi(self.Dialog)

        self.udpnontimer=QtCore.QTimer(self)
        self.udpnontimer.timeout.connect(self.udptitoget)

        udpwin=self.udpChild

        self.udpChild.titopause.clicked.connect(self.udptitostop)
        self.udpChild.pushButton_2.clicked.connect(self.udptitoclear)
        self.udpChild.comnon.clicked.connect(self.udpnoncomset)
        self.udpChild.commodel.clicked.connect(self.udpcomset)
        self.udpChild.turnleft.clicked.connect(self.udprobotturnleft)
        self.udpChild.turnright.clicked.connect(self.udprobotturnright)
        self.udpChild.doublemotor.clicked.connect(self.udprobotdouble)
        self.udpChild.turnrun_2.clicked.connect(self.udprobotturnrun)
        self.udpChild.loop.clicked.connect(self.urobotloop)
        self.udpChild.back.clicked.connect(self.urobotback)
        self.udpChild.speedadd.clicked.connect(self.urobotadd)
        self.udpChild.speedsub.clicked.connect(self.urobotsub)
        self.udpChild.burnstart.clicked.connect(self.urobotburn)
        self.udpChild.burnstop.clicked.connect(self.urobotstop)
        self.udpChild.stop.clicked.connect(self.motorstop)

        self.udpChild.upboxopen.clicked.connect(self.udpupbox1open)
        self.udpChild.upboxclose.clicked.connect(self.udpupbox1close)

        self.udpChild.downboxopen.clicked.connect(self.udpdownbox1open)
        self.udpChild.downboxclose.clicked.connect(self.udpdownbox1close)

        self.udpChild.updooropen.clicked.connect(self.udpdoorupopen)
        self.udpChild.updoorclose.clicked.connect(self.udpdoorupclose)

        self.udpChild.downdooropen.clicked.connect(self.udpdoordownopen)
        self.udpChild.downdoorclose.clicked.connect(self.udpdoordownclose)

        self.udpChild.leftduoji1open.clicked.connect(self.udpleftopenset)
        self.udpChild.leftduoji1close.clicked.connect(self.udpleftcloseset)

        self.udpChild.leftduoji2open.clicked.connect(self.udpsecleftopenset)
        self.udpChild.leftduoji2close.clicked.connect(self.udpsecleftcloseset)

        self.udpChild.leftlight1open.clicked.connect(self.udplightopenset)
        self.udpChild.leftlight1close.clicked.connect(self.udplightcloseset)

        self.udpChild.leftlight2open.clicked.connect(self.udpseclightopenset)
        self.udpChild.leftlight2close.clicked.connect(self.udpseclightcloseset)

        self.udpChild.rightduoji1open.clicked.connect(self.udprightopenset)
        self.udpChild.rightduoji1close.clicked.connect(self.udprightcloseset)

        self.udpChild.rightduoji2open.clicked.connect(self.udpsecrightopenset)
        self.udpChild.rightduoji2close.clicked.connect(self.udpsecrightcloseset)

        self.udpChild.rightlight1open.clicked.connect(self.udprightlightopenset)
        self.udpChild.rightlight1close.clicked.connect(self.udprightlightcloseset)

        self.udpChild.rightlight2open.clicked.connect(self.udpsecrightlightopenset)
        self.udpChild.rightlight2close.clicked.connect(self.udpsecrightlightcloseset)

        self.udpChild.uplightopen.clicked.connect(self.udpuplightopenset)
        self.udpChild.uplightclose.clicked.connect(self.udpuplightcloseset)

        self.udpChild.downlightopen.clicked.connect(self.udpdownlightopenset)
        self.udpChild.downlightclose.clicked.connect(self.udpdownlightcloseset)

        self.udpChild.lightsopen.clicked.connect(self.udplightsopenset)
        self.udpChild.lightsclose.clicked.connect(self.udplightscloseset)

        self.udpChild.rightupdooropen.clicked.connect(self.udprightupdooropenset)
        self.udpChild.rightupdoorclose.clicked.connect(self.udprightupdoorcloseset)

        self.udpChild.leftdupdooropen.clicked.connect(self.udpleftupdooropenset)
        self.udpChild.leftdupdoorclose.clicked.connect(self.udpleftupdoorcloseset)

        self.udpChild.rightdowndooropen.clicked.connect(self.udprightdowndooropenset)
        self.udpChild.rightdowndoorclose.clicked.connect(self.udprightdowndoorcloseset)

        self.udpChild.leftdowndooropen.clicked.connect(self.udpleftdowndooropenset)
        self.udpChild.leftdowndoorclose.clicked.connect(self.udpleftdowndoorcloseset)

        self.Dialog.exec_()

    def udpnoncomset(self):
        self.udpChild.commodel.setDisabled(True)
        self.udpChild.groupBox_11.setDisabled(True)
        self.udpChild.groupBox_12.setDisabled(True)
        self.udpChild.groupBox_13.setDisabled(True)
        self.udpChild.groupBox_14.setDisabled(True)
        self.udpChild.titopause.setEnabled(True)
        self.udpChild.runstat.setText(u'监控')
        udptitostopexist=os.path.exists('ui/udpstop.txt')
        if udptitostopexist:
            os.remove('ui/udpstop.txt')
        self.udper=udpthread(0)
        self.udper.listSingnal.connect(self.udptitoany)
        self.udper.messSingnal.connect(self.udpnetstat)
        self.udper.start()

    def udpcomset(self):
        self.udpChild.comnon.setDisabled(True)
        self.udpChild.groupBox_11.setEnabled(True)
        self.udpChild.groupBox_12.setEnabled(True)
        self.udpChild.groupBox_13.setEnabled(True)
        self.udpChild.groupBox_14.setEnabled(True)
        self.udpChild.titopause.setEnabled(True)
        self.udpChild.burnstart.setEnabled(True)
        self.udpChild.burnstop.setEnabled(True)
        self.udpChild.runstat.setText(u'控制')
        udptitostopexist=os.path.exists('ui/udpstop.txt')
        if udptitostopexist:
            os.remove('ui/udpstop.txt')
        self.udpcomer=udpthread(1)
        self.udpcomer.listSingnal.connect(self.udptitoany)
        self.udpcomer.messSingnal.connect(self.udpnetstat)
        self.udpcomer.start()

    def udptitoclear(self):
        self.udpChild.titomessage.clear()

    def udpnetstat(self,mess):
        self.udpChild.titomessage.append(mess)

    def urobotstop(self):
        self.udpChild.burnstart.setChecked(False)
        f=open('ui/burn.txt','w')
        f.write('stop')
        f.close()

    def motorstop(self):
        self.udpChild.turnright.setChecked(False)
        self.udpChild.doublemotor.setChecked(False)
        self.udpChild.back.setChecked(False)
        self.udpChild.loop.setChecked(False)
        self.udpChild.turnleft.setChecked(False)
        self.udpChild.turnrun_2.setChecked(False)
        self.udpChild.leftmotorvalue.setProperty('value',0)
        self.udpChild.rightmotorvalue.setProperty('value',0)

    def urobotburn(self):
        burnstopexist=os.path.exists('ui/burn.txt')
        if burnstopexist:
            os.remove('ui/burn.txt')
        self.udpChild.test.clear()
        self.udpChild.burnbar.setProperty('value',0)
        burncount=int(str(self.udpChild.burncount.toPlainText()).rstrip(' '))
        self.udpChild.burnstop.setChecked(False)
        self.burner=burnthread(burncount)
        self.burner.barSingnal.connect(self.upburn)
        self.burner.testSingnal.connect(self.upburntest)
        self.burner.start()

    def upburn(self,mess):
        self.udpChild.burnbar.setProperty('value',mess)

    def upburntest(self,mess):
        self.udpChild.test.setText(str(mess))

    def udptitostop(self):
        self.udpChild.commodel.setEnabled(True)
        self.udpChild.comnon.setEnabled(True)
        self.udpChild.speedadd.setDisabled(True)
        self.udpChild.speedsub.setDisabled(True)
        self.udpChild.runstat.setText(u'暂停')
        f=open('ui/udpstop.txt','w')
        f.write('udpstop')
        f.close()

    def udptitoget(self):
        self.udper=udpnonthread()
        self.udper.listSingnal.connect(self.udptitoany)
        self.udper.start()

    def udpupbox1open(self):
        #self.titoChild.leftduoji1non.setChecked(False)
        self.udpChild.leftduoji1open.setChecked(True)
        self.udpChild.leftduoji1close.setChecked(False)
        #self.titoChild.rightduoji1non.setChecked(False)
        self.udpChild.rightduoji1open.setChecked(True)
        self.udpChild.rightduoji1close.setChecked(False)
        self.udpChild.upboxclose.setChecked(False)
        #self.titoChild.upboxnon.setChecked(False)

    def udpupbox1close(self):
        #self.titoChild.leftduoji1non.setChecked(False)
        self.udpChild.leftduoji1open.setChecked(False)
        self.udpChild.leftduoji1close.setChecked(True)
        #self.titoChild.rightduoji1non.setChecked(False)
        self.udpChild.rightduoji1open.setChecked(False)
        self.udpChild.rightduoji1close.setChecked(True)
        #self.titoChild.upboxnon.setChecked(False)
        self.udpChild.upboxopen.setChecked(False)

    def udpdownbox1open(self):
        #self.titoChild.leftduoji2non.setChecked(False)
        self.udpChild.leftduoji2open.setChecked(True)
        self.udpChild.leftduoji2close.setChecked(False)
        #self.titoChild.rightduoji2non.setChecked(False)
        self.udpChild.rightduoji2open.setChecked(True)
        self.udpChild.rightduoji2close.setChecked(False)
        self.udpChild.downboxclose.setChecked(False)
        #self.titoChild.downboxnon.setChecked(False)

    def udpdownbox1close(self):
        #self.titoChild.leftduoji2non.setChecked(False)
        self.udpChild.leftduoji2open.setChecked(False)
        self.udpChild.leftduoji2close.setChecked(True)
        #self.titoChild.rightduoji2non.setChecked(False)
        self.udpChild.rightduoji2open.setChecked(False)
        self.udpChild.rightduoji2close.setChecked(True)
        #self.titoChild.downboxnon.setChecked(False)
        self.udpChild.downboxopen.setChecked(False)

    def udpdoorupopen(self):
        self.udpChild.rightupdooropen.setChecked(True)
        self.udpChild.leftdupdooropen.setChecked(True)

        self.udpChild.rightupdoorclose.setChecked(False)
        self.udpChild.leftdupdoorclose.setChecked(False)

        self.udpChild.updoorclose.setChecked(False)

    def udpdoorupclose(self):
        self.udpChild.rightupdooropen.setChecked(False)
        self.udpChild.leftdupdooropen.setChecked(False)

        self.udpChild.rightupdoorclose.setChecked(True)
        self.udpChild.leftdupdoorclose.setChecked(True)

        self.udpChild.updooropen.setChecked(False)

    def udpdoordownopen(self):
        self.udpChild.rightdowndooropen.setChecked(True)
        self.udpChild.leftdowndooropen.setChecked(True)

        self.udpChild.rightdowndoorclose.setChecked(False)
        self.udpChild.leftdowndoorclose.setChecked(False)

        self.udpChild.downdoorclose.setChecked(False)

    def udpdoordownclose(self):
        self.udpChild.rightdowndooropen.setChecked(False)
        self.udpChild.leftdowndooropen.setChecked(False)

        self.udpChild.rightdowndoorclose.setChecked(True)
        self.udpChild.leftdowndoorclose.setChecked(True)

        self.udpChild.downdooropen.setChecked(False)

    def udprightupdooropenset(self):
        #self.titoChild.leftdoormotornon1.setChecked(False)
        self.udpChild.rightupdoorclose.setChecked(False)

    def udprightupdoorcloseset(self):
        #self.titoChild.leftdoormotornon1.setChecked(False)
        self.udpChild.rightupdooropen.setChecked(False)

    def udpleftupdooropenset(self):
        #self.titoChild.leftdoormotornon2.setChecked(False)
        self.udpChild.leftdupdoorclose.setChecked(False)

    def udpleftupdoorcloseset(self):
        self.udpChild.leftdupdooropen.setChecked(False)
        #self.titoChild.leftdoormotornon2.setChecked(False)

    def udprightdowndooropenset(self):
        #self.titoChild.rightdoormotornon1.setChecked(False)
        self.udpChild.rightdowndoorclose.setChecked(False)

    def udprightdowndoorcloseset(self):
        #self.titoChild.rightdoormotornon1.setChecked(False)
        self.udpChild.rightdowndooropen.setChecked(False)

    def udpleftdowndooropenset(self):
        #self.titoChild.rightdoormotornon2.setChecked(False)
        self.udpChild.leftdowndoorclose.setChecked(False)

    def udpleftdowndoorcloseset(self):
        #self.titoChild.rightdoormotornon2.setChecked(False)
        self.udpChild.leftdowndooropen.setChecked(False)

    def udpleftopenset(self):
        #self.titoChild.leftduoji1non.setChecked(False)
        self.udpChild.leftduoji1close.setChecked(False)

    def udpleftcloseset(self):
        #self.titoChild.leftduoji1non.setChecked(False)
        self.udpChild.leftduoji1open.setChecked(False)

    def udpsecleftopenset(self):
        #self.titoChild.leftduoji2non.setChecked(False)
        self.udpChild.leftduoji2close.setChecked(False)

    def udpsecleftcloseset(self):
        #self.titoChild.leftduoji2non.setChecked(False)
        self.udpChild.leftduoji2open.setChecked(False)

    def udplightopenset(self):
        #self.titoChild.leftlight1non.setChecked(False)
        self.udpChild.leftlight1close.setChecked(False)

    def udplightcloseset(self):
        #self.titoChild.leftlight1non.setChecked(False)
        self.udpChild.leftlight1open.setChecked(False)

    def udpseclightopenset(self):
        #self.titoChild.leftlight2non.setChecked(False)
        self.udpChild.leftlight2close.setChecked(False)

    def udpseclightcloseset(self):
        #self.titoChild.leftlight2non.setChecked(False)
        self.udpChild.leftlight2open.setChecked(False)

    def udprightopenset(self):
        #self.titoChild.rightduoji1non.setChecked(False)
        self.udpChild.rightduoji1close.setChecked(False)

    def udprightcloseset(self):
        #self.titoChild.rightduoji1non.setChecked(False)
        self.udpChild.rightduoji1open.setChecked(False)

    def udpsecrightopenset(self):
        #self.titoChild.rightduoji2non.setChecked(False)
        self.udpChild.rightduoji2close.setChecked(False)

    def udpsecrightcloseset(self):
        #self.titoChild.rightduoji2non.setChecked(False)
        self.udpChild.rightduoji2open.setChecked(False)

    def udprightlightopenset(self):
        #self.titoChild.rightlight1non.setChecked(False)
        self.udpChild.rightlight1close.setChecked(False)

    def udprightlightcloseset(self):
        #self.titoChild.rightlight1non.setChecked(False)
        self.udpChild.rightlight1open.setChecked(False)

    def udpsecrightlightopenset(self):
        #self.titoChild.rightlight2non.setChecked(False)
        self.udpChild.rightlight2close.setChecked(False)

    def udpsecrightlightcloseset(self):
        #self.titoChild.rightlight2non.setChecked(False)
        self.udpChild.rightlight2open.setChecked(False)

    def udpuplightopenset(self):
        self.udpChild.rightlight1open.setChecked(True)
        self.udpChild.leftlight1open.setChecked(True)

        self.udpChild.rightlight1close.setChecked(False)
        self.udpChild.leftlight1close.setChecked(False)

        self.udpChild.uplightclose.setChecked(False)

    def udpuplightcloseset(self):
        self.udpChild.rightlight1open.setChecked(False)
        self.udpChild.leftlight1open.setChecked(False)

        self.udpChild.rightlight1close.setChecked(True)
        self.udpChild.leftlight1close.setChecked(True)

        self.udpChild.uplightopen.setChecked(False)

    def udpdownlightopenset(self):
        self.udpChild.rightlight2open.setChecked(True)
        self.udpChild.leftlight2open.setChecked(True)

        self.udpChild.rightlight2close.setChecked(False)
        self.udpChild.leftlight2close.setChecked(False)

        self.udpChild.downlightclose.setChecked(False)

    def udpdownlightcloseset(self):
        self.udpChild.rightlight2open.setChecked(False)
        self.udpChild.leftlight2open.setChecked(False)

        self.udpChild.rightlight2close.setChecked(True)
        self.udpChild.leftlight2close.setChecked(True)

        self.udpChild.downlightopen.setChecked(False)

    def udplightsopenset(self):
        self.udpChild.rightlight1open.setChecked(True)
        self.udpChild.leftlight1open.setChecked(True)
        self.udpChild.rightlight2open.setChecked(True)
        self.udpChild.leftlight2open.setChecked(True)
        self.udpChild.uplightopen.setChecked(True)
        self.udpChild.downlightopen.setChecked(True)

        self.udpChild.rightlight1close.setChecked(False)
        self.udpChild.leftlight1close.setChecked(False)
        self.udpChild.rightlight2close.setChecked(False)
        self.udpChild.leftlight2close.setChecked(False)
        self.udpChild.uplightclose.setChecked(False)
        self.udpChild.downlightclose.setChecked(False)

        self.udpChild.lightsclose.setChecked(False)

    def udplightscloseset(self):
        self.udpChild.rightlight1open.setChecked(False)
        self.udpChild.leftlight1open.setChecked(False)
        self.udpChild.rightlight2open.setChecked(False)
        self.udpChild.leftlight2open.setChecked(False)
        self.udpChild.uplightopen.setChecked(False)
        self.udpChild.downlightopen.setChecked(False)

        self.udpChild.rightlight1close.setChecked(True)
        self.udpChild.leftlight1close.setChecked(True)
        self.udpChild.rightlight2close.setChecked(True)
        self.udpChild.leftlight2close.setChecked(True)
        self.udpChild.uplightclose.setChecked(True)
        self.udpChild.downlightclose.setChecked(True)

        self.udpChild.lightsopen.setChecked(False)

    def udptitoany(self,messlist):
        #print(messlist)
        f=open('ui/imuyaw.txt','a')
        self.udpChild.warrcode.setText(str(messlist[0]).decode('utf-8'))
        self.udpChild.errcode.setText(str(messlist[1]).decode('utf-8'))
        self.udpChild.inch.setText(str(messlist[2]).decode('utf-8'))
        self.udpChild.leftmotorenable.setText(str(messlist[3]).decode('utf-8'))
        self.udpChild.rightmotorenable.setText(str(messlist[4]).decode('utf-8'))
        self.udpChild.leftmotorpos.setText(str(messlist[5]))
        self.udpChild.leftmotorspeed.setText(str(messlist[6]))
        self.udpChild.rightmotorpos.setText(str(messlist[7]))
        self.udpChild.rightmotorspeed.setText(str(messlist[8]))
        self.udpChild.xacc.setText(str(messlist[9]))
        self.udpChild.yacc.setText(str(messlist[10]))
        self.udpChild.zacc.setText(str(messlist[11]))
        self.udpChild.xraw.setText(str(messlist[12]))
        self.udpChild.yraw.setText(str(messlist[13]))
        self.udpChild.zraw.setText(str(messlist[14]))
        self.udpChild.fuyang.setText(str(messlist[15]))
        self.udpChild.pianhang.setText(str(messlist[16]))
        f.write(str(messlist[16])+'\n')
        f.close()
        self.udpChild.fangun.setText(str(messlist[17]))
        self.udpChild.fall.setText(messlist[18])

        self.udpChild.leftupdoor.setText(str(messlist[19]).decode('utf-8'))
        self.udpChild.leftdowndoor.setText(str(messlist[20]).decode('utf-8'))
        self.udpChild.rightupdoor.setText(str(messlist[21]).decode('utf-8'))
        self.udpChild.rightdowndoor.setText(str(messlist[22]).decode('utf-8'))
        self.udpChild.leftupduoji.setText(str(messlist[23]).decode('utf-8'))
        self.udpChild.leftdownduoji.setText(str(messlist[24]).decode('utf-8'))
        self.udpChild.rightupduoji.setText(str(messlist[25]).decode('utf-8'))
        self.udpChild.rightdownduoji.setText(str(messlist[26]).decode('utf-8'))
        self.udpChild.leftswitch1.setText(str(messlist[27]).decode('utf-8'))
        self.udpChild.leftswitch2.setText(str(messlist[28]).decode('utf-8'))

        self.udpChild.chargestat.setText(str(messlist[29]).decode('utf-8'))
        self.udpChild.soc.setProperty('value',messlist[30])
        self.udpChild.urat1.setText(messlist[31])
        self.udpChild.urat2.setText(messlist[32])
        self.udpChild.urat3.setText(messlist[33])
        self.udpChild.urat4.setText(messlist[34])
        self.udpChild.urat5.setText(messlist[35])
        self.udpChild.urat6.setText(messlist[36])
        self.udpChild.irf1.setText(messlist[37])
        self.udpChild.irf2.setText(messlist[38])
        self.udpChild.irf3.setText(messlist[39])
        self.udpChild.irf4.setText(messlist[40])
        self.udpChild.irf5.setText(messlist[41])
        self.udpChild.irf6.setText(messlist[42])
        self.udpChild.irf7.setText(messlist[43])
        self.udpChild.irf8.setText(messlist[44])
        self.udpChild.irf9.setText(messlist[45])
        self.udpChild.irfA.setText(messlist[46])

        self.udpChild.leftwei1.setText(str(messlist[47]))
        self.udpChild.rightwei1.setText(str(messlist[48]))
        self.udpChild.leftwei2.setText(str(messlist[49]))
        self.udpChild.rightwei2.setText(str(messlist[50]))
        #self.udpChild.totalup.setText(str(messlist[51]))
        #self.udpChild.totaldown.setText(str(messlist[52]))

    def udprobotturnleft(self):
        self.udpChild.speedadd.setEnabled(False)
        self.udpChild.speedsub.setEnabled(False)
        self.udpChild.rightmotorvalue.setValue(50)
        self.udpChild.leftmotorvalue.setValue(30)
        self.udpChild.comboBox.setCurrentIndex(0)
        self.udpChild.comboBox_2.setCurrentIndex(0)
        self.udpChild.turnright.setChecked(False)
        self.udpChild.doublemotor.setChecked(False)
        self.udpChild.back.setChecked(False)
        self.udpChild.loop.setChecked(False)
        self.udpChild.turnrun_2.setChecked(False)
        self.udpChild.stop.setChecked(False)

    def udprobotturnright(self):
        self.udpChild.speedadd.setEnabled(False)
        self.udpChild.speedsub.setEnabled(False)
        self.udpChild.rightmotorvalue.setValue(30)
        self.udpChild.leftmotorvalue.setValue(50)
        self.udpChild.comboBox.setCurrentIndex(0)
        self.udpChild.comboBox_2.setCurrentIndex(0)
        self.udpChild.turnleft.setChecked(False)
        self.udpChild.doublemotor.setChecked(False)
        self.udpChild.back.setChecked(False)
        self.udpChild.loop.setChecked(False)
        self.udpChild.turnrun_2.setChecked(False)
        self.udpChild.stop.setChecked(False)

    def udprobotdouble(self):
        self.udpChild.speedadd.setEnabled(True)
        self.udpChild.speedsub.setEnabled(True)
        self.udpChild.rightmotorvalue.setValue(50)
        self.udpChild.leftmotorvalue.setValue(50)
        self.udpChild.comboBox.setCurrentIndex(0)
        self.udpChild.comboBox_2.setCurrentIndex(0)
        self.udpChild.turnright.setChecked(False)
        self.udpChild.turnleft.setChecked(False)
        self.udpChild.back.setChecked(False)
        self.udpChild.loop.setChecked(False)
        self.udpChild.turnrun_2.setChecked(False)
        self.udpChild.stop.setChecked(False)

    def udprobotturnrun(self):
        self.udpChild.speedadd.setEnabled(True)
        self.udpChild.speedsub.setEnabled(True)
        self.udpChild.rightmotorvalue.setValue(100)
        self.udpChild.leftmotorvalue.setValue(100)
        self.udpChild.comboBox.setCurrentIndex(1)
        self.udpChild.comboBox_2.setCurrentIndex(0)
        self.udpChild.turnright.setChecked(False)
        self.udpChild.doublemotor.setChecked(False)
        self.udpChild.back.setChecked(False)
        self.udpChild.loop.setChecked(False)
        self.udpChild.turnleft.setChecked(False)
        self.udpChild.stop.setChecked(False)

    def urobotback(self):
        self.udpChild.speedadd.setEnabled(True)
        self.udpChild.speedsub.setEnabled(True)
        self.udpChild.rightmotorvalue.setValue(50)
        self.udpChild.leftmotorvalue.setValue(50)
        self.udpChild.comboBox.setCurrentIndex(1)
        self.udpChild.comboBox_2.setCurrentIndex(1)
        self.udpChild.turnright.setChecked(False)
        self.udpChild.doublemotor.setChecked(False)
        self.udpChild.turnleft.setChecked(False)
        self.udpChild.loop.setChecked(False)
        self.udpChild.turnrun_2.setChecked(False)
        self.udpChild.stop.setChecked(False)

    def urobotadd(self):
        current=self.udpChild.leftmotorvalue.value()
        target=current+10
        self.udpChild.leftmotorvalue.setProperty('value',target)
        self.udpChild.rightmotorvalue.setProperty('value',target)

    def urobotsub(self):
        current=self.udpChild.leftmotorvalue.value()
        if current==0:
            target=0
        else:
            target=current-10
        self.udpChild.leftmotorvalue.setProperty('value',target)
        self.udpChild.rightmotorvalue.setProperty('value',target)

    def urobotloop(self):
        self.udpChild.turnright.setChecked(False)
        self.udpChild.doublemotor.setChecked(False)
        self.udpChild.back.setChecked(False)
        self.udpChild.turnleft.setChecked(False)
        self.udpChild.turnrun_2.setChecked(False)
        self.udpChild.stop.setChecked(False)
        titostopexist=os.path.exists('ui/titostop.txt')
        if titostopexist:
            os.remove('ui/titostop.txt')
        self.looper=uloopthread()
        self.looper.start()

    def titowindow(self):
        global titowin

        self.titoChild = Tito_Ui_Dialog()
        self.Dialog = QtGui.QDialog(self)
        self.titoChild.setupUi(self.Dialog)

        titowin=self.titoChild

        self.sertimer=QtCore.QTimer(self)
        self.sertimer.setSingleShot(True)
        self.sertimer.timeout.connect(self.titoserautoget)
        self.sertimer.start(10)

        self.ultratimer=QtCore.QTimer(self)
        self.ultratimer.timeout.connect(self.ultradisinfoget)

        self.speedtimer=QtCore.QTimer(self)
        self.speedtimer.timeout.connect(self.leftmotorspeed)

        self.titoChild.titostart.clicked.connect(self.titodebugstart)
        self.titoChild.titopause.clicked.connect(self.titostop)
        self.titoChild.open.clicked.connect(self.titopen)
        self.titoChild.close.clicked.connect(self.tserialclose)
        self.titoChild.pushButton_2.clicked.connect(self.titoclear)
        self.titoChild.turnleft.clicked.connect(self.robotturnleft)
        self.titoChild.turnright.clicked.connect(self.robotturnright)
        self.titoChild.doublemotor.clicked.connect(self.robotdouble)
        self.titoChild.turnrun.clicked.connect(self.robotturnrun)
        self.titoChild.turnrun_2.clicked.connect(self.robotturnrunsec)
        self.titoChild.loop.clicked.connect(self.robotloop)
        self.titoChild.back.clicked.connect(self.robotback)
        self.titoChild.stop.clicked.connect(self.titorobotstop)
        self.titoChild.burnstart.clicked.connect(self.robotburnstart)
        self.titoChild.burnstop.clicked.connect(self.robotburnstop)
        self.titoChild.speedadd.clicked.connect(self.currentspeedadd)
        self.titoChild.speedsub.clicked.connect(self.currentspeedsub)
        self.titoChild.maxspeed.clicked.connect(self.maxspeedset)

        self.titoChild.upboxopen.clicked.connect(self.upbox1open)
        self.titoChild.upboxclose.clicked.connect(self.upbox1close)

        self.titoChild.downboxopen.clicked.connect(self.downbox1open)
        self.titoChild.downboxclose.clicked.connect(self.downbox1close)

        self.titoChild.updooropen.clicked.connect(self.doorupopen)
        self.titoChild.updoorclose.clicked.connect(self.doorupclose)

        self.titoChild.downdooropen.clicked.connect(self.doordownopen)
        self.titoChild.downdoorclose.clicked.connect(self.doordownclose)

        self.titoChild.leftduoji1open.clicked.connect(self.leftopenset)
        self.titoChild.leftduoji1close.clicked.connect(self.leftcloseset)

        self.titoChild.leftduoji2open.clicked.connect(self.secleftopenset)
        self.titoChild.leftduoji2close.clicked.connect(self.secleftcloseset)

        self.titoChild.leftlight1open.clicked.connect(self.lightopenset)
        self.titoChild.leftlight1close.clicked.connect(self.lightcloseset)

        self.titoChild.leftlight2open.clicked.connect(self.seclightopenset)
        self.titoChild.leftlight2close.clicked.connect(self.seclightcloseset)

        self.titoChild.rightduoji1open.clicked.connect(self.rightopenset)
        self.titoChild.rightduoji1close.clicked.connect(self.rightcloseset)

        self.titoChild.rightduoji2open.clicked.connect(self.secrightopenset)
        self.titoChild.rightduoji2close.clicked.connect(self.secrightcloseset)

        self.titoChild.rightlight1open.clicked.connect(self.rightlightopenset)
        self.titoChild.rightlight1close.clicked.connect(self.rightlightcloseset)

        self.titoChild.rightlight2open.clicked.connect(self.secrightlightopenset)
        self.titoChild.rightlight2close.clicked.connect(self.secrightlightcloseset)

        self.titoChild.openrightdoorup.clicked.connect(self.rightupdooropenset)
        self.titoChild.closerightdoorup.clicked.connect(self.rightupdoorcloseset)

        self.titoChild.openleftdoorup.clicked.connect(self.leftupdooropenset)
        self.titoChild.closeleftdoorup.clicked.connect(self.leftupdoorcloseset)

        self.titoChild.openrightdoordown.clicked.connect(self.rightdowndooropenset)
        self.titoChild.closerightdoordown.clicked.connect(self.rightdowndoorcloseset)

        self.titoChild.openleftdoordown.clicked.connect(self.leftdowndooropenset)
        self.titoChild.closeleftdoordown.clicked.connect(self.leftdowndoorcloseset)

        self.titoChild.leftlight1open_2.clicked.connect(self.uplightopen)
        self.titoChild.leftlight1close_2.clicked.connect(self.uplightclose)

        self.titoChild.leftlight1open_3.clicked.connect(self.downlightopen)
        self.titoChild.leftlight1close_3.clicked.connect(self.downlightclose)

        self.Dialog.exec_()

    def robotburnstart(self):
        burnstopexist=os.path.exists('ui/titoburn.txt')
        if burnstopexist:
            os.remove('ui/titoburn.txt')
        self.titoChild.test.clear()
        self.titoChild.burnbar.setProperty('value',0)
        #burncount=int(str(self.titoChild.burncount.toPlainText()).rstrip(' '))
        self.titoChild.burnstop.setChecked(False)
        self.burner=titoburnthread()
        #self.burner=titoburnthread(burncount)
        self.burner.barSingnal.connect(self.titoupburn)
        self.burner.testSingnal.connect(self.titoupburntest)
        self.burner.start()

    def titoupburn(self,mess):
        self.titoChild.burnbar.setProperty('value',mess)

    def titoupburntest(self,mess):
        self.titoChild.test.setText(str(mess))

    def robotburnstop(self):
        self.titoChild.burnstart.setChecked(False)
        f=open('ui/titoburn.txt','w')
        f.write('stop')
        f.close()

    def leftmotorspeed(self):
        self.speeder=speedthread()
        self.speeder.messSingnal.connect(self.updatespeed)
        self.speeder.start()

    def updatespeed(self,speed):
        self.titoChild.leftmotorvalue.setValue(speed)
        self.titoChild.rightmotorvalue.setValue(speed)

    def ultradisinfoget(self):
        titostopexist=os.path.exists('ui/titostop.txt')
        if titostopexist:
            self.ultratimer.stop()
            self.speedtimer.stop()
        self.ulter=ultrathread()
        self.ulter.start()

    def upbox1non(self):
        self.titoChild.leftduoji1non.setChecked(True)
        self.titoChild.leftduoji1open.setChecked(False)
        self.titoChild.leftduoji1close.setChecked(False)
        self.titoChild.rightduoji1non.setChecked(True)
        self.titoChild.rightduoji1open.setChecked(False)
        self.titoChild.rightduoji1close.setChecked(False)
        self.titoChild.upboxopen.setChecked(False)
        self.titoChild.upboxclose.setChecked(False)

    def upbox1open(self):
        #self.titoChild.leftduoji1non.setChecked(False)
        self.titoChild.leftduoji1open.setChecked(True)
        self.titoChild.leftduoji1close.setChecked(False)
        #self.titoChild.rightduoji1non.setChecked(False)
        self.titoChild.rightduoji1open.setChecked(True)
        self.titoChild.rightduoji1close.setChecked(False)
        self.titoChild.upboxclose.setChecked(False)
        #self.titoChild.upboxnon.setChecked(False)

    def upbox1close(self):
        #self.titoChild.leftduoji1non.setChecked(False)
        self.titoChild.leftduoji1open.setChecked(False)
        self.titoChild.leftduoji1close.setChecked(True)
        #self.titoChild.rightduoji1non.setChecked(False)
        self.titoChild.rightduoji1open.setChecked(False)
        self.titoChild.rightduoji1close.setChecked(True)
        #self.titoChild.upboxnon.setChecked(False)
        self.titoChild.upboxopen.setChecked(False)

    def downbox1non(self):
        self.titoChild.leftduoji2non.setChecked(True)
        self.titoChild.leftduoji2open.setChecked(False)
        self.titoChild.leftduoji2close.setChecked(False)
        self.titoChild.rightduoji2non.setChecked(True)
        self.titoChild.rightduoji2open.setChecked(False)
        self.titoChild.rightduoji2close.setChecked(False)
        self.titoChild.downboxclose.setChecked(False)
        self.titoChild.downboxopen.setChecked(False)

    def downbox1open(self):
        #self.titoChild.leftduoji2non.setChecked(False)
        self.titoChild.leftduoji2open.setChecked(True)
        self.titoChild.leftduoji2close.setChecked(False)
        #self.titoChild.rightduoji2non.setChecked(False)
        self.titoChild.rightduoji2open.setChecked(True)
        self.titoChild.rightduoji2close.setChecked(False)
        self.titoChild.downboxclose.setChecked(False)
        #self.titoChild.downboxnon.setChecked(False)

    def downbox1close(self):
        #self.titoChild.leftduoji2non.setChecked(False)
        self.titoChild.leftduoji2open.setChecked(False)
        self.titoChild.leftduoji2close.setChecked(True)
        #self.titoChild.rightduoji2non.setChecked(False)
        self.titoChild.rightduoji2open.setChecked(False)
        self.titoChild.rightduoji2close.setChecked(True)
        #self.titoChild.downboxnon.setChecked(False)
        self.titoChild.downboxopen.setChecked(False)

    def doorupnon(self):
        self.titoChild.leftdoormotornon1.setChecked(True)
        self.titoChild.leftdoormotoropen1.setChecked(False)
        self.titoChild.leftdoormotorclose1.setChecked(False)
        self.titoChild.leftdoormotornon2.setChecked(True)
        self.titoChild.leftdoormotoropen2.setChecked(False)
        self.titoChild.leftdoormotorclose2.setChecked(False)
        self.titoChild.updooropen.setChecked(False)
        self.titoChild.updoorclose.setChecked(False)

    def doorupopen(self):
        #self.titoChild.leftdoormotornon1.setChecked(False)
        self.titoChild.openrightdoorup.setChecked(True)
        self.titoChild.closerightdoorup.setChecked(False)
        #self.titoChild.leftdoormotornon2.setChecked(False)
        self.titoChild.openleftdoorup.setChecked(True)
        self.titoChild.closeleftdoorup.setChecked(False)
        #self.titoChild.updoornon.setChecked(False)
        self.titoChild.updoorclose.setChecked(False)

    def doorupclose(self):
        #self.titoChild.leftdoormotornon1.setChecked(False)
        self.titoChild.openrightdoorup.setChecked(False)
        self.titoChild.closerightdoorup.setChecked(True)
        #self.titoChild.leftdoormotornon2.setChecked(False)
        self.titoChild.openleftdoorup.setChecked(False)
        self.titoChild.closeleftdoorup.setChecked(True)
        self.titoChild.updooropen.setChecked(False)
        #self.titoChild.updoornon.setChecked(False)

    def doordownnon(self):
        self.titoChild.rightdoormotornon1.setChecked(True)
        self.titoChild.rightdoormotoropen1.setChecked(False)
        self.titoChild.rightdoormotorclose1.setChecked(False)
        self.titoChild.rightdoormotornon2.setChecked(True)
        self.titoChild.rightdoormotoropen2.setChecked(False)
        self.titoChild.rightdoormotorclose2.setChecked(False)
        self.titoChild.downdoorclose.setChecked(False)
        self.titoChild.downdooropen.setChecked(False)

    def doordownopen(self):
        #self.titoChild.rightdoormotornon1.setChecked(False)
        self.titoChild.openrightdoordown.setChecked(True)
        self.titoChild.closerightdoordown.setChecked(False)
        #self.titoChild.rightdoormotornon2.setChecked(False)
        self.titoChild.openleftdoordown.setChecked(True)
        self.titoChild.closeleftdoordown.setChecked(False)
        self.titoChild.downdoorclose.setChecked(False)
        #self.titoChild.downdoornon.setChecked(False)

    def doordownclose(self):
        #self.titoChild.rightdoormotornon1.setChecked(False)
        self.titoChild.openrightdoordown.setChecked(False)
        self.titoChild.closerightdoordown.setChecked(True)
        #self.titoChild.rightdoormotornon2.setChecked(False)
        self.titoChild.openleftdoordown.setChecked(False)
        self.titoChild.closeleftdoordown.setChecked(True)
        #self.titoChild.downdoornon.setChecked(False)
        self.titoChild.downdooropen.setChecked(False)

    def doorleftnonset(self):
        self.titoChild.leftdoormotoropen1.setChecked(False)
        self.titoChild.leftdoormotorclose1.setChecked(False)

    def rightupdooropenset(self):
        self.titoChild.closerightdoorup.setChecked(False)

    def rightupdoorcloseset(self):
        self.titoChild.openrightdoorup.setChecked(False)

    def doorleftsecnonset(self):
        self.titoChild.leftdoormotoropen2.setChecked(False)
        self.titoChild.leftdoormotorclose2.setChecked(False)

    def leftupdooropenset(self):
        self.titoChild.closeleftdoorup.setChecked(False)

    def leftupdoorcloseset(self):
        self.titoChild.openleftdoorup.setChecked(False)

    def doorightnonset(self):
        self.titoChild.rightdoormotoropen1.setChecked(False)
        self.titoChild.rightdoormotorclose1.setChecked(False)

    def rightdowndooropenset(self):
        #self.titoChild.rightdoormotornon1.setChecked(False)
        self.titoChild.closerightdoordown.setChecked(False)

    def rightdowndoorcloseset(self):
        #self.titoChild.rightdoormotornon1.setChecked(False)
        self.titoChild.openrightdoordown.setChecked(False)

    def doorightsecnonset(self):
        self.titoChild.rightdoormotoropen2.setChecked(False)
        self.titoChild.rightdoormotorclose2.setChecked(False)

    def leftdowndooropenset(self):
        #self.titoChild.rightdoormotornon2.setChecked(False)
        self.titoChild.closeleftdoordown.setChecked(False)

    def leftdowndoorcloseset(self):
        #self.titoChild.rightdoormotornon2.setChecked(False)
        self.titoChild.openleftdoordown.setChecked(False)

    def uplightopen(self):
        self.titoChild.leftlight1open.setChecked(True)
        self.titoChild.rightlight1open.setChecked(True)
        self.titoChild.leftlight1close.setChecked(False)
        self.titoChild.rightlight1close.setChecked(False)
        self.titoChild.leftlight1close_2.setChecked(False)

    def uplightclose(self):
        self.titoChild.leftlight1open.setChecked(False)
        self.titoChild.rightlight1open.setChecked(False)
        self.titoChild.leftlight1close.setChecked(True)
        self.titoChild.rightlight1close.setChecked(True)
        self.titoChild.leftlight1open_2.setChecked(False)

    def downlightopen(self):
        self.titoChild.leftlight2open.setChecked(True)
        self.titoChild.rightlight2open.setChecked(True)
        self.titoChild.leftlight2close.setChecked(False)
        self.titoChild.rightlight2close.setChecked(False)
        self.titoChild.leftlight1close_3.setChecked(False)

    def downlightclose(self):
        self.titoChild.leftlight2open.setChecked(False)
        self.titoChild.rightlight2open.setChecked(False)
        self.titoChild.leftlight2close.setChecked(True)
        self.titoChild.rightlight2close.setChecked(True)
        self.titoChild.leftlight1open_3.setChecked(False)

    def robotloop(self):
        self.titoChild.turnleft.setChecked(False)
        self.titoChild.turnright.setChecked(False)
        self.titoChild.doublemotor.setChecked(False)
        self.titoChild.back.setChecked(False)
        self.titoChild.turnrun.setChecked(False)
        self.titoChild.turnrun_2.setChecked(False)
        self.titoChild.stop.setChecked(False)
        titostopexist=os.path.exists('ui/titostop.txt')
        if titostopexist:
            os.remove('ui/titostop.txt')
        self.looper=loopthread()
        self.looper.start()

    def noncomset(self):
        self.titoChild.groupBox_11.setEnabled(False)
        self.titoChild.groupBox_12.setEnabled(False)
        self.titoChild.groupBox_10.setEnabled(False)
        self.titoChild.groupBox_14.setEnabled(False)
        self.titoChild.commodel.setChecked(False)

    def comset(self):
        self.titoChild.comnon.setChecked(False)
        self.titoChild.groupBox_12.setEnabled(True)
        self.titoChild.groupBox_11.setEnabled(True)
        self.titoChild.groupBox_10.setEnabled(True)
        self.titoChild.groupBox_14.setEnabled(True)

    def titorobotstop(self):
        self.titoChild.leftmotorvalue.setProperty('value',0)
        self.titoChild.rightmotorvalue.setProperty('value',0)
        self.titoChild.turnright.setChecked(False)
        self.titoChild.turnleft.setChecked(False)
        self.titoChild.doublemotor.setChecked(False)
        self.titoChild.back.setChecked(False)
        self.titoChild.loop.setChecked(False)
        self.titoChild.turnrun.setChecked(False)
        self.titoChild.turnrun_2.setChecked(False)

    def robotturnleft(self):
        self.titoChild.loop.setChecked(False)
        self.titoChild.turnright.setChecked(False)
        self.titoChild.doublemotor.setChecked(False)
        self.titoChild.back.setChecked(False)
        self.titoChild.turnrun.setChecked(False)
        self.titoChild.turnrun_2.setChecked(False)
        self.titoChild.stop.setChecked(False)
        self.titoChild.speedadd.setEnabled(False)
        self.titoChild.speedsub.setEnabled(False)
        self.titoChild.rightmotorvalue.setValue(50)
        self.titoChild.leftmotorvalue.setValue(30)
        self.titoChild.comboBox.setCurrentIndex(0)
        self.titoChild.comboBox_2.setCurrentIndex(0)
        self.speedtimer.stop()

    def robotturnright(self):
        self.titoChild.turnleft.setChecked(False)
        self.titoChild.loop.setChecked(False)
        self.titoChild.doublemotor.setChecked(False)
        self.titoChild.back.setChecked(False)
        self.titoChild.turnrun.setChecked(False)
        self.titoChild.turnrun_2.setChecked(False)
        self.titoChild.stop.setChecked(False)
        self.titoChild.speedadd.setEnabled(False)
        self.titoChild.speedsub.setEnabled(False)
        self.titoChild.rightmotorvalue.setValue(30)
        self.titoChild.leftmotorvalue.setValue(50)
        self.titoChild.comboBox.setCurrentIndex(0)
        self.titoChild.comboBox_2.setCurrentIndex(0)
        self.speedtimer.stop()

    def robotdouble(self):
        self.titoChild.turnleft.setChecked(False)
        self.titoChild.turnright.setChecked(False)
        self.titoChild.loop.setChecked(False)
        self.titoChild.back.setChecked(False)
        self.titoChild.turnrun.setChecked(False)
        self.titoChild.turnrun_2.setChecked(False)
        self.titoChild.stop.setChecked(False)
        self.titoChild.speedadd.setEnabled(True)
        self.titoChild.speedsub.setEnabled(True)
        self.titoChild.rightmotorvalue.setValue(50)
        self.titoChild.leftmotorvalue.setValue(50)
        self.titoChild.comboBox.setCurrentIndex(0)
        self.titoChild.comboBox_2.setCurrentIndex(0)
        self.speedtimer.stop()

    def robotback(self):
        self.titoChild.turnleft.setChecked(False)
        self.titoChild.turnright.setChecked(False)
        self.titoChild.doublemotor.setChecked(False)
        self.titoChild.loop.setChecked(False)
        self.titoChild.turnrun.setChecked(False)
        self.titoChild.turnrun_2.setChecked(False)
        self.titoChild.stop.setChecked(False)
        self.titoChild.speedadd.setEnabled(True)
        self.titoChild.speedsub.setEnabled(True)
        self.titoChild.rightmotorvalue.setValue(50)
        self.titoChild.leftmotorvalue.setValue(50)
        self.titoChild.comboBox.setCurrentIndex(1)
        self.titoChild.comboBox_2.setCurrentIndex(1)
        self.speedtimer.stop()

    def maxspeedset(self):
        self.titoChild.leftmotorvalue.setProperty('value',2000)
        self.titoChild.rightmotorvalue.setProperty('value',2000)

    def robotturnrun(self):
        global initraw

        frontstopexist=os.path.exists('ui/fultra.txt')
        if frontstopexist:
            os.remove('ui/fultra.txt')
        front=open('ui/fultra.txt','w')
        front.write('front ultra information:'+'\n')
        front.close()

        infstopexist=os.path.exists('ui/inf.txt')
        if infstopexist:
            os.remove('ui/inf.txt')
        inf=open('ui/inf.txt','w')
        inf.write('inf information:'+'\n')
        inf.close()

        backstopexist=os.path.exists('ui/bultra.txt')
        if backstopexist:
            os.remove('ui/bultra.txt')
        back=open('ui/bultra.txt','w')
        back.write('back ultra information'+'\n')
        back.close()
        self.titoChild.turnleft.setChecked(False)
        self.titoChild.turnright.setChecked(False)
        self.titoChild.doublemotor.setChecked(False)
        self.titoChild.back.setChecked(False)
        self.titoChild.loop.setChecked(False)
        self.titoChild.turnrun_2.setChecked(False)
        self.titoChild.stop.setChecked(False)
        self.titoChild.rightmotorvalue.setValue(20)
        self.titoChild.leftmotorvalue.setValue(20)
        self.titoChild.comboBox.setCurrentIndex(1)
        self.titoChild.comboBox_2.setCurrentIndex(0)
        self.titoChild.speedadd.setDisabled(True)
        self.titoChild.speedsub.setDisabled(True)
        temp=str(self.titoChild.pianhang.toPlainText())
        try:
            if temp[0]=='-':
                initraw=360-float(temp.lstrip('-'))
            else:
                initraw=float(temp)
        except:
            pass
        self.ultratimer.start(100)
        self.speedtimer.start(10)

    def robotturnrunsec(self):
        self.titoChild.turnleft.setChecked(False)
        self.titoChild.turnright.setChecked(False)
        self.titoChild.doublemotor.setChecked(False)
        self.titoChild.back.setChecked(False)
        self.titoChild.turnrun.setChecked(False)
        self.titoChild.stop.setChecked(False)
        self.titoChild.loop.setChecked(False)
        self.titoChild.speedadd.setEnabled(True)
        self.titoChild.speedsub.setEnabled(True)
        self.speedtimer.stop()
        self.titoChild.rightmotorvalue.setValue(40)
        self.titoChild.leftmotorvalue.setValue(40)
        self.titoChild.comboBox.setCurrentIndex(1)
        self.titoChild.comboBox_2.setCurrentIndex(0)

    def currentspeedadd(self):
        current=self.titoChild.leftmotorvalue.value()
        target=current+10
        self.titoChild.leftmotorvalue.setProperty('value',target)
        self.titoChild.rightmotorvalue.setProperty('value',target)

    def currentspeedsub(self):
        current=self.titoChild.leftmotorvalue.value()
        if current==0:
            target=0
        else:
            target=current-10
        self.titoChild.leftmotorvalue.setProperty('value',target)
        self.titoChild.rightmotorvalue.setProperty('value',target)

    def nonset(self):
        self.titoChild.leftduoji1open.setChecked(False)
        self.titoChild.leftduoji1close.setChecked(False)

    def leftopenset(self):
        #self.titoChild.leftduoji1non.setChecked(False)
        self.titoChild.leftduoji1close.setChecked(False)

    def leftcloseset(self):
        #self.titoChild.leftduoji1non.setChecked(False)
        self.titoChild.leftduoji1open.setChecked(False)

    def secnonset(self):
        self.titoChild.leftduoji2open.setChecked(False)
        self.titoChild.leftduoji2close.setChecked(False)

    def secleftopenset(self):
        #self.titoChild.leftduoji2non.setChecked(False)
        self.titoChild.leftduoji2close.setChecked(False)

    def secleftcloseset(self):
        #self.titoChild.leftduoji2non.setChecked(False)
        self.titoChild.leftduoji2open.setChecked(False)

    def lightnonset(self):
        self.titoChild.leftlight1open.setChecked(False)
        self.titoChild.leftlight1close.setChecked(False)

    def lightopenset(self):
        #self.titoChild.leftlight1non.setChecked(False)
        self.titoChild.leftlight1close.setChecked(False)

    def lightcloseset(self):
        #self.titoChild.leftlight1non.setChecked(False)
        self.titoChild.leftlight1open.setChecked(False)

    def seclightnonset(self):
        self.titoChild.leftlight2open.setChecked(False)
        self.titoChild.leftlight2close.setChecked(False)

    def seclightopenset(self):
        #self.titoChild.leftlight2non.setChecked(False)
        self.titoChild.leftlight2close.setChecked(False)

    def seclightcloseset(self):
        #self.titoChild.leftlight2non.setChecked(False)
        self.titoChild.leftlight2open.setChecked(False)

    def rightnonset(self):
        self.titoChild.rightduoji1open.setChecked(False)
        self.titoChild.rightduoji1close.setChecked(False)

    def rightopenset(self):
        #self.titoChild.rightduoji1non.setChecked(False)
        self.titoChild.rightduoji1close.setChecked(False)

    def rightcloseset(self):
        #self.titoChild.rightduoji1non.setChecked(False)
        self.titoChild.rightduoji1open.setChecked(False)

    def secrightnonset(self):
        self.titoChild.rightduoji2open.setChecked(False)
        self.titoChild.rightduoji2close.setChecked(False)

    def secrightopenset(self):
        #self.titoChild.rightduoji2non.setChecked(False)
        self.titoChild.rightduoji2close.setChecked(False)

    def secrightcloseset(self):
        #self.titoChild.rightduoji2non.setChecked(False)
        self.titoChild.rightduoji2open.setChecked(False)

    def rightlightnonset(self):
        self.titoChild.rightlight1open.setChecked(False)
        self.titoChild.rightlight1close.setChecked(False)

    def rightlightopenset(self):
        #self.titoChild.rightlight1non.setChecked(False)
        self.titoChild.rightlight1close.setChecked(False)

    def rightlightcloseset(self):
        #self.titoChild.rightlight1non.setChecked(False)
        self.titoChild.rightlight1open.setChecked(False)

    def secrightlightnonset(self):
        self.titoChild.rightlight2open.setChecked(False)
        self.titoChild.rightlight2close.setChecked(False)

    def secrightlightopenset(self):
        #self.titoChild.rightlight2non.setChecked(False)
        self.titoChild.rightlight2close.setChecked(False)

    def secrightlightcloseset(self):
        #self.titoChild.rightlight2non.setChecked(False)
        self.titoChild.rightlight2open.setChecked(False)

    def dedaultset(self):
        currentestitem=unicode(self.titoChild.leftduojilist.currentItem().text())
        currentrow=self.titoChild.leftduojilist.currentRow()
        itemlist=currentestitem.split('    ')
        self.titoChild.leftduojilist.takeItem(currentrow)
        self.titoChild.leftduojilist.insertItem(currentrow,itemlist[0]+u'    OPEN')
        self.titoChild.leftduojilist.setCurrentRow(currentrow)

    def titopen(self):
        global titodevice
        try:
            titodevice.close()
        except:
            pass
        try:
            Ygcboardev.close()
        except:
            pass
        sernum=str(self.titoChild.sernum.currentText())
        rate=int(self.titoChild.boundrate.currentText())

        try:
            titodevice=serial.Serial(sernum,rate,timeout=5)
            status=u'YG协议Tito联调测试-'+str.upper(sernum)+':'+str(rate)+':READ'
            self.Dialog.setWindowTitle(status)
            #self.titoChild.comnon.setEnabled(True)
            #self.titoChild.commodel.setEnabled(True)
            self.titoChild.titostart.setEnabled(True)
            self.titoChild.titopause.setEnabled(True)
            self.titoChild.open.setDisabled(True)
        except:
            QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("串口打开失败，请检查设置"))

    def tserialclose(self):
        try:
            titodevice.close()
        except:
            pass
        #self.titoChild.comnon.setEnabled(False)
        #self.titoChild.commodel.setEnabled(False)
        self.titoChild.titostart.setEnabled(False)
        self.titoChild.titopause.setEnabled(False)
        self.titoChild.open.setEnabled(True)
        status=u'YG协议tito联调测试-串口已关闭'
        self.Dialog.setWindowTitle(status)

    def titoserautoget(self):
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list) <= 0:
            QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("端口号数量为零，请先连接串口"))
        else:
            pattern_serial='COM.+'
            for line in port_list:
                Match=re.search(pattern_serial,str(line))
                if Match:
                    new_line=str(line).split(' - ')
                    self.titoChild.sernum.addItem(new_line[0])

    def titononcmdmodel(self):
        self.titoChild.titostart.setEnabled(True)
        self.titoChild.titopause.setEnabled(True)
        self.titoChild.commandselet.setDisabled(True)

    def titocmdmodel(self):
        self.titoChild.titostart.setEnabled(True)
        self.titoChild.titopause.setEnabled(True)
        self.titoChild.commandselet.setEnable(True)

    def testcontrol(self):
        currenttest=unicode(self.titoChild.commandselet.currentItem().text())
        if currenttest == u'舵机-双击使能':
            self.titoChild.groupBox_11.setEnabled(True)
        else:
            pass

    def titoclear(self):
        self.titoChild.titomessage.clear()

    def titodebugstart(self):
        titodevice.flush()
        self.titoChild.titomessage.clear()
        self.titoChild.comboBox.setCurrentIndex(0)
        self.titoChild.comboBox_2.setCurrentIndex(0)
        self.titoChild.runstat.setText(u'测试中')
        self.titoChild.titostart.setDisabled(True)
        #if self.titoChild.comnon.isChecked() and self.titoChild.commodel.isChecked():
            #QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("不能同时选择无命令和有命令模式"))
        #else:
        titostopexist=os.path.exists('ui/titostop.txt')
        if titostopexist:
            os.remove('ui/titostop.txt')
        self.titotest=titodebug()
        self.titotest.messSingnal.connect(self.titomess)
        self.titotest.listSingnal.connect(self.titoany)
        #self.titotest.titocountSingnal.connect(self.titocount)
        #self.titotest.errSingnal.connect(self.titoerrmess)
        self.titotest.start()

    def titoerrmess(self,mess):
        self.titoChild.titomessage.append(mess)

    def titostop(self):
        self.titoChild.speedadd.setEnabled(False)
        self.titoChild.speedsub.setEnabled(False)
        self.titoChild.titostart.setEnabled(True)
        self.titoallclear()
        self.titoChild.runstat.setText(u'已暂停')
        self.ultratimer.stop()
        self.speedtimer.stop()
        f=open('ui/titostop.txt','w')
        f.write('titostoped')
        f.close()

    def titoallclear(self):
        self.titoChild.urat1.clear()
        self.titoChild.urat2.clear()
        self.titoChild.urat3.clear()
        self.titoChild.urat4.clear()
        self.titoChild.urat5.clear()
        self.titoChild.urat6.clear()
        self.titoChild.leftmotorpos.clear()
        self.titoChild.leftmotorspeed.clear()
        self.titoChild.rightmotorpos.clear()
        self.titoChild.rightmotorspeed.clear()
        self.titoChild.irf1.clear()
        self.titoChild.irf2.clear()
        self.titoChild.irf3.clear()
        self.titoChild.irf4.clear()
        self.titoChild.irf5.clear()
        self.titoChild.irf6.clear()
        self.titoChild.irf7.clear()
        self.titoChild.irf8.clear()
        self.titoChild.irf9.clear()
        self.titoChild.irfA.clear()
        self.titoChild.xacc.clear()
        self.titoChild.yacc.clear()
        self.titoChild.zacc.clear()
        self.titoChild.xraw.clear()
        self.titoChild.yraw.clear()
        self.titoChild.zraw.clear()
        self.titoChild.xvalue.clear()
        self.titoChild.yvalue.clear()
        self.titoChild.zvalue.clear()
        self.titoChild.fuyang.clear()
        self.titoChild.fangun.clear()
        self.titoChild.pianhang.clear()
        self.titoChild.errcode.clear()
        self.titoChild.warrcode.clear()
        self.titoChild.workmodel.clear()
        self.titoChild.leftwei1.clear()
        self.titoChild.leftwei2.clear()
        self.titoChild.leftswitch1.clear()
        self.titoChild.leftswitch2.clear()
        self.titoChild.rightwei1.clear()
        self.titoChild.rightwei2.clear()
        self.titoChild.chargestat.clear()
        self.titoChild.soc.setProperty('value',0)
        self.titoChild.inch.clear()
        self.titoChild.fall.clear()
        self.titoChild.leftmotorvalue.setProperty('value',0)
        self.titoChild.rightmotorvalue.setProperty('value',0)

    def titocount(self,count):
        if count>=10:
            self.titoChild.titomessage.clear()

    def titomess(self,mess):
        f=open('log/log.txt','a')
        f.write(mess)
        f.close()
        #pass
        #self.titoChild.titomessage.append(mess)

    def titoany(self,messlist):
        #print(messlist)
        self.titoChild.warrcode.setText(str(messlist[0]).decode('utf-8'))
        self.titoChild.errcode.setText(str(messlist[1]).decode('utf-8'))
        self.titoChild.inch.setText(str(messlist[2]).decode('utf-8'))
        self.titoChild.leftmotorenable.setText(str(messlist[3]).decode('utf-8'))
        self.titoChild.rightmotorenable.setText(str(messlist[4]).decode('utf-8'))
        self.titoChild.leftmotorpos.setText(str(messlist[5]))
        self.titoChild.leftmotorspeed.setText(str(messlist[6]))
        self.titoChild.rightmotorpos.setText(str(messlist[7]))
        self.titoChild.rightmotorspeed.setText(str(messlist[8]))
        self.titoChild.xacc.setText(str(messlist[9]))
        self.titoChild.yacc.setText(str(messlist[10]))
        self.titoChild.zacc.setText(str(messlist[11]))
        self.titoChild.xraw.setText(str(messlist[12]))
        self.titoChild.yraw.setText(str(messlist[13]))
        self.titoChild.zraw.setText(str(messlist[14]))
        self.titoChild.fuyang.setText(str(messlist[15]))
        self.titoChild.pianhang.setText(str(messlist[16]))
        self.titoChild.fangun.setText(str(messlist[17]))
        self.titoChild.fall.setText(messlist[18])

        self.titoChild.leftupdoor.setText(str(messlist[19]).decode('utf-8'))
        self.titoChild.leftdowndoor.setText(str(messlist[20]).decode('utf-8'))
        self.titoChild.rightupdoor.setText(str(messlist[21]).decode('utf-8'))
        self.titoChild.rightdowndoor.setText(str(messlist[22]).decode('utf-8'))
        self.titoChild.leftupduoji.setText(str(messlist[23]).decode('utf-8'))
        self.titoChild.leftdownduoji.setText(str(messlist[24]).decode('utf-8'))
        self.titoChild.rightupduoji.setText(str(messlist[25]).decode('utf-8'))
        self.titoChild.rightdownduoji.setText(str(messlist[26]).decode('utf-8'))
        self.titoChild.leftswitch1.setText(str(messlist[27]).decode('utf-8'))
        self.titoChild.leftswitch2.setText(str(messlist[28]).decode('utf-8'))

        self.titoChild.chargestat.setText(str(messlist[29]).decode('utf-8'))
        self.titoChild.soc.setProperty('value',messlist[30])
        self.titoChild.urat1.setText(messlist[31])
        self.titoChild.urat2.setText(messlist[32])
        self.titoChild.urat3.setText(messlist[33])
        self.titoChild.urat4.setText(messlist[34])
        self.titoChild.urat5.setText(messlist[35])
        self.titoChild.urat6.setText(messlist[36])
        self.titoChild.irf1.setText(messlist[37])
        self.titoChild.irf2.setText(messlist[38])
        self.titoChild.irf3.setText(messlist[39])
        self.titoChild.irf4.setText(messlist[40])
        self.titoChild.irf5.setText(messlist[41])
        self.titoChild.irf6.setText(messlist[42])
        self.titoChild.irf7.setText(messlist[43])
        self.titoChild.irf8.setText(messlist[44])
        self.titoChild.irf9.setText(messlist[45])
        self.titoChild.irfA.setText(messlist[46])
        self.titoChild.leftwei1.setText(str(messlist[47]))
        self.titoChild.rightwei1.setText(str(messlist[48]))
        self.titoChild.leftwei2.setText(str(messlist[49]))
        self.titoChild.rightwei2.setText(str(messlist[50]))
        self.titoChild.totalup.setText(str(messlist[51]))
        self.titoChild.totaldown.setText(str(messlist[52]))

    def tickmess(self,mess):
        self.cboardChild.testmessage.append('tick:'+mess)

    def boxwindow(self):
        global boxwin,commandstat

        self.boxChild = Box_Ui_Dialog()
        self.Dialog = QtGui.QDialog(self)
        self.boxChild.setupUi(self.Dialog)

        boxwin=self.boxChild
        #commandstat=[]

        self.boxtimer=QtCore.QTimer(self)
        self.boxtimer.setSingleShot(True)
        self.boxtimer.timeout.connect(self.boxserautoget)
        self.boxtimer.start(10)

        self.boxinit=QtCore.QTimer(self)
        self.boxinit.setSingleShot(True)
        self.boxinit.timeout.connect(self.boxinitget)
        self.boxinit.start(10)

        self.boxerr=QtCore.QTimer(self)
        self.boxerr.setSingleShot(True)
        self.boxerr.timeout.connect(self.boxerrget)
        self.boxerr.start(10)

        self.ultradis=QtCore.QTimer(self)
        self.ultradis.timeout.connect(self.ultradisget)

        self.statgeter=QtCore.QTimer(self)
        self.statgeter.timeout.connect(self.updatestat)
        self.statgeter.start(5)


        #self.boxcounter=QtCore.QTimer(self)
        #self.boxcounter.timeout.connect(self.boxtotal)
        #self.boxcounter.start(10)

        self.boxChild.titostart.clicked.connect(self.boxdebugstart)
        self.boxChild.titopause.clicked.connect(self.boxstop)
        self.boxChild.open.clicked.connect(self.boxopen)
        self.boxChild.close.clicked.connect(self.boxserclose)
        self.boxChild.loop.clicked.connect(self.boxloop)

        self.Dialog.exec_()

    def updatestat(self):
        global commandstat
        commandstat=[]
        if unicode(self.boxChild.chargestat.toPlainText())==u'开启':
            commandstat.append(1)
        else:
            commandstat.append(0)
        commandstat.append(int(self.boxChild.leftmotorvalue.value()))
        commandstat.append(int(self.boxChild.rightmotorvalue.value()))
        if unicode(self.boxChild.comboBox.currentText())==u'正向':
            commandstat.append(1)
        else:
            commandstat.append(0)
        if unicode(self.boxChild.comboBox_2.currentText())==u'正向':
            commandstat.append(1)
        else:
            commandstat.append(0)

    def ultradisget(self):
        currentcount=int(self.boxChild.lcdNumber_2.value())
        #if unicode(self.boxChild.chargestat.toPlainText())==u'关闭':
        if unicode(self.boxChild.leftswitch1.toPlainText())==u'未到位':
            if unicode(self.boxChild.comboBox.currentText())==u'正向':
                currentcount+=1
            else:
                currentcount=0
        else:
            currentcount=0
        self.boxChild.lcdNumber_2.setProperty('value',currentcount)
        if int(self.boxChild.lcdNumber_2.value())>=10:
            self.boxChild.comboBox.setCurrentIndex(1)
            self.boxChild.comboBox_2.setCurrentIndex(1)
            self.boxChild.leftmotorvalue.setProperty('value',50)
            self.boxChild.rightmotorvalue.setProperty('value',50)
            errcount=int(self.boxChild.lcdNumber_3.value())
            errcount+=1
            self.boxChild.lcdNumber_3.setProperty('value',errcount)
            self.boxChild.lcdNumber_2.setProperty('value',0)
            #self.boxChild.leftmotorcontrol.setCurrentIndex(0)
            #self.boxChild.rightmotorcontrol.setCurrentIndex(0)
            f=open('ui/boxerrcount.txt','w')
            f.write(str(errcount)+'\n')
            f.close()
            f_w=open('ui/boxerrflag.txt','w')
            f_w.write('boxerr')
            f_w.close()
        else:
            pass

    def boxtotal(self):
        count=str(self.boxChild.lcdNumber.value()).rstrip('.0')
        f=open('ui/boxcount.txt','r')
        hisvalue=f.readline()
        if hisvalue==count:
            f.close()
        else:
            f.close()
            f_w=open('ui/boxcount.txt','w')
            f_w.write(str(count)+'\n')
            f_w.close()

    def boxinitget(self):
        f=open('ui/boxcount.txt','r')
        history=f.readline()
        self.boxChild.lcdNumber.setProperty('value',history)
        f.close()

    def boxerrget(self):
        f=open('ui/boxerrcount.txt','r')
        history=f.readline()
        self.boxChild.lcdNumber_3.setProperty('value',history)
        f.close()

    def boxserautoget(self):
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list) <= 0:
            QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("端口号数量为零，请先连接串口"))
        else:
            pattern_serial='COM.+'
            for line in port_list:
                Match=re.search(pattern_serial,str(line))
                if Match:
                    new_line=str(line).split(' - ')
                    self.boxChild.sernum.addItem(new_line[0])

    def boxopen(self):
        global boxdevice
        try:
            boxdevice.close()
        except:
            pass
        try:
            Ygcboardev.close()
        except:
            pass
        sernum=str(self.boxChild.sernum.currentText())
        rate=int(self.boxChild.boundrate.currentText())

        try:
            boxdevice=serial.Serial(sernum,rate,timeout=5)
            status=u'盒子老化测试-'+str.upper(sernum)+':'+str(rate)+':READ'
            self.Dialog.setWindowTitle(status)
            self.boxChild.titostart.setEnabled(True)
            self.boxChild.titopause.setEnabled(True)
        except:
            QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("串口打开失败，请检查设置"))

    def boxserclose(self):
        try:
            boxdevice.close()
        except:
            pass
        self.boxChild.titostart.setEnabled(False)
        self.boxChild.titopause.setEnabled(False)
        status=u'盒子测试-串口已关闭'
        self.Dialog.setWindowTitle(status)

    def boxdebugstart(self):
        boxdevice.flushInput()
        self.boxChild.leftmotorvalue.setValue(0)
        self.boxChild.rightmotorvalue.setValue(0)
        self.boxChild.comboBox.setCurrentIndex(0)
        self.boxChild.comboBox_2.setCurrentIndex(0)
        self.boxChild.leftmotorcontrol.setCurrentIndex(0)
        self.boxChild.rightmotorcontrol.setCurrentIndex(0)
        self.boxChild.lcdNumber_2.setProperty('value',0)
        self.boxChild.runstat.setText(u'测试中')
        boxstopexist=os.path.exists('ui/boxstop.txt')
        if boxstopexist:
            os.remove('ui/boxstop.txt')
        boxerrexist=os.path.exists('ui/boxerrflag.txt')
        if boxerrexist:
            os.remove('ui/boxerrflag.txt')
        self.boxtest=boxdebug()
        self.boxtest.listSingnal.connect(self.boxany)
        #self.boxtest.ultraSingal.connect(self.)
        self.boxtest.start()

    def boxloop(self):
        boxstopexist=os.path.exists('ui/boxstop.txt')
        if boxstopexist:
            os.remove('ui/boxstop.txt')
        self.ultradis.start(1000)
        self.looper=boxloopthread()
        self.looper.boxcountSingnal.connect(self.boxcount)
        self.looper.leftmotorSingal.connect(self.updateleftmotor)
        self.looper.rightmotorSingal.connect(self.updaterightmotor)
        self.looper.leftmotordirSingal.connect(self.updateleftmotordir)
        self.looper.rightmotordirSingal.connect(self.updaterightmotordir)
        self.looper.leftmotorconSingal.connect(self.updateleftmotorcon)
        self.looper.rightmotorconSingal.connect(self.updaterightmotorcon)
        self.looper.boxSingal.connect(self.updatebox)
        self.looper.doorSingal.connect(self.updatedoor)
        self.looper.start()

    def updatebox(self,boxopen,boxnon,boxclose):
        if boxopen==1:
            self.boxChild.upboxopen.setChecked(True)
        else:
            self.boxChild.upboxopen.setChecked(False)
        if boxnon==1:
            self.boxChild.upboxnon.setChecked(True)
        else:
            self.boxChild.upboxnon.setChecked(False)
        if boxclose==1:
            self.boxChild.upboxclose.setChecked(True)
        else:
            self.boxChild.upboxclose.setChecked(False)

    def updatedoor(self,dooropen,doornon,doorclose):
        if dooropen==1:
            self.boxChild.updooropen.setChecked(True)
        else:
            self.boxChild.updooropen.setChecked(False)
        if doornon==1:
            self.boxChild.updoornon.setChecked(True)
        else:
            self.boxChild.updoornon.setChecked(False)
        if doorclose==1:
            self.boxChild.updoorclose.setChecked(True)
        else:
            self.boxChild.updoorclose.setChecked(False)

    def updateleftmotor(self,mlist):
        self.boxChild.leftmotorvalue.setProperty('value',mlist)

    def updaterightmotor(self,mlist):
        self.boxChild.rightmotorvalue.setProperty('value',mlist)

    def updateleftmotordir(self,mlist):
        self.boxChild.comboBox.setCurrentIndex(mlist)

    def updaterightmotordir(self,mlist):
        self.boxChild.comboBox_2.setCurrentIndex(mlist)

    def updateleftmotorcon(self,mlist):
        self.boxChild.leftmotorcontrol.setCurrentIndex(mlist)

    def updaterightmotorcon(self,mlist):
        self.boxChild.rightmotorcontrol.setCurrentIndex(mlist)

    def boxstop(self):
        self.boxChild.runstat.setText(u'已暂停')
        f=open('ui/boxstop.txt','w')
        f.write('boxstoped')
        f.close()

    def boxany(self,messlist):
        self.boxChild.chargestat.setText(str(messlist[0]).decode('utf-8'))
        self.boxChild.soc.setProperty('value',messlist[1])
        if messlist[2]=='61':
            if messlist[3]=='01':
                self.boxChild.leftswitch1.setText(u'到位')
            else:
                self.boxChild.leftswitch1.setText(u'未到位')
        elif messlist[2]=='62':
            if messlist[3]=='01':
                self.boxChild.leftswitch2.setText(u'到位')
            else:
                self.boxChild.leftswitch2.setText(u'未到位')

    def boxanywww(self,messlist):
        #print(messlist)
        self.boxChild.chargestat.setText(str(messlist[0]).decode('utf-8'))
        self.boxChild.soc.setProperty('value',messlist[1])
        if messlist[2]=='61':
            if messlist[3]=='01':
                self.boxChild.leftswitch1.setText(u'到位')
            else:
                self.boxChild.leftswitch1.setText(u'未到位')
        elif messlist[2]=='62':
            if messlist[3]=='01':
                self.boxChild.leftswitch2.setText(u'到位')
            else:
                self.boxChild.leftswitch2.setText(u'未到位')

    def boxcount(self,count):
        f=open('ui/boxcount.txt','w')
        self.boxChild.lcdNumber.setProperty('value',count)
        f.write(str(count)+'\n')
        f.close()

    def udpboxwindow(self):
        global udpboxwin,commandstat

        self.udpboxChild = Udpbox_Ui_Dialog()
        self.Dialog = QtGui.QDialog(self)
        self.udpboxChild.setupUi(self.Dialog)

        udpboxwin=self.udpboxChild

        self.udpboxChild.loop.clicked.connect(self.udpboxloop)
        self.udpboxChild.return_2.clicked.connect(self.udpboxreturn)
        self.udpboxChild.pause.clicked.connect(self.udpboxpause)

        self.Dialog.exec_()

    def udpboxloop(self):
        self.udpboxChild.return_2.setEnabled(True)
        boxstopexist=os.path.exists('ui/udpboxstop.txt')
        if boxstopexist:
            os.remove('ui/udpboxstop.txt')
        self.udpboxer=udpboxthread()
        self.udpboxer.listSingnal.connect(self.udpboxany)
        self.udpboxer.start()

    def udpboxreturn(self):
        boxstopexist=os.path.exists('ui/udpboxstop.txt')
        if boxstopexist:
            os.remove('ui/udpboxstop.txt')
        self.udplooper=udpboxloop()
        self.udplooper.countSingnal.connect(self.udpboxcount)
        self.udplooper.start()

    def udpboxpause(self):
        f=open('ui/udpboxstop.txt','w')
        f.write('udpboxstoped')
        f.close()

    def udpboxany(self,messlist):
        self.udpboxChild.charge.setText(str(messlist[0]).decode('utf-8'))
        self.udpboxChild.battery.setText(str(messlist[1]))

    def udpboxcount(self,mess):
        f_w=open('ui/udpbox.txt','w')
        f_w.write(str(mess))
        f_w.close()
        self.udpboxChild.count.setText(str(mess).decode('utf-8'))

    def messmarge(self,data,model):
        modbus_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
        messcrc=hex(modbus_crc_func(str(data).decode('hex')))
        if model ==1:
            sendcrc=messcrc
        else:
            sendcrc=hex(int(messcrc,16)+1)
        margecrc=sendcrc.lstrip('0x')
        if len(margecrc)==1:
            tempcrc='000'+margecrc
        elif len(margecrc)==2:
            tempcrc='00'+margecrc
        elif len(margecrc)==3:
            tempcrc='0'+margecrc
        else:
            tempcrc=margecrc
        finalcrc=tempcrc[2]+tempcrc[3]+tempcrc[0]+tempcrc[1]
        sendmess=(str(data)+finalcrc+'47').decode('hex')
        return sendmess

    def cutmess(self,mess):
        if unicode(mess)==u'C板已进入转发模式':
            self.cboardChild.workmodel.setText(u'转发')
        self.cboardChild.testmessage.append(mess)

    def getcurrentime(self):
        currentime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return currentime

    def boardidset(self,boardtype):
        if boardtype==u'Board-C':
            BID='EE'
        elif boardtype==u'IMU':
            BID='E1'
        elif boardtype==u'2.4G':
            BID='71'
        elif boardtype==u'左轮毂电机':
            BID='11'#调出测试窗口
        elif boardtype==u'右轮毂电机':
            BID='12'#调出测试窗口
        elif boardtype==u'直流电机1':
            BID='25'#调出测试窗口
        elif boardtype==u'直流电机2':
            BID='26'
        elif boardtype==u'直流电机3':
            BID='27'
        elif boardtype==u'直流电机4':
            BID='28'
        elif boardtype==u'超1':
            BID='D8'
        elif boardtype==u'超2':
            BID='E8'
        elif boardtype==u'超3':
            BID='F8'
        elif boardtype==u'超4':
            BID='FA'
        elif boardtype==u'超5':
            BID='FC'
        elif boardtype==u'超6':
            BID='FE'
        elif boardtype==u'左箱体控制板':
            BID='61'#调出测试窗口
        elif boardtype==u'右箱体控制板':
            BID='62'
        elif boardtype==u'BMS':
            BID='E3'
        elif boardtype==u'红外1':
            BID='51'
        elif boardtype==u'红外2':
            BID='52'
        elif boardtype==u'红外3':
            BID='53'
        elif boardtype==u'红外4':
            BID='54'
        elif boardtype==u'红外5':
            BID='55'
        elif boardtype==u'红外6':
            BID='56'
        elif boardtype==u'红外7':
            BID='57'
        elif boardtype==u'红外8':
            BID='58'
        elif boardtype==u'红外9':
            BID='59'
        elif boardtype==u'红外10':
            BID='5A'
        elif boardtype==u'超声1':
            BID='41'
        elif boardtype==u'超声2':
            BID='42'
        elif boardtype==u'超声3':
            BID='43'
        elif boardtype==u'超声4':
            BID='44'
        elif boardtype==u'超声5':
            BID='45'
        elif boardtype==u'超声6':
            BID='46'
        else:
            BID='31'
        return BID

    def tickmess(self,mess):
        self.cboardChild.testmessage.append(mess)

    def tickstart(self,flag,tickseq):
        if flag==1:#tick接收完成
            currentobject=(unicode(self.cboardChild.boardlist.currentItem().text()))
            currensubtitem=(unicode(self.cboardChild.subitem.currentItem().text()))
            boardid=self.boardidset(currentobject)
            if currensubtitem==u'读取0byte':
                self.readgeralreginfo(boardid,tickseq,0)
            elif currentitem == u'写入SN':
                self.cboardChild.SN.clear()
                self.cboardChild.SN.setEnabled(True)
                self.writesn(boardid,tickseq)
            elif currentitem == u'写入BID':
                self.writebid(boardid,tickseq)
            elif currentitem == u'写入硬件版本号':
                self.writehardver(boardid,tickseq)
            elif currentitem == u'写入软件版本号':
                self.writesoftver(boardid,tickseq)
            elif currentitem == u'写入协议版本号':
                self.writesoftver(boardid,tickseq)
            else:
                pass
        else:
            pass

    def readgeralreginfo(self,bid,seq,length):
        self.cboardChild.testmessage.append(u'开始发送读取通用寄存器请求')
        messdata='59'+str(bid)+'00'+'02'+'00'+'40'+str(seq)
        messcrc=hex(CRC16().calculate(messdata.decode('hex')))
        margecrc=messcrc.lstrip('0x')
        if len(margecrc)==1:
            tempcrc='000'+margecrc
        elif len(margecrc)==2:
            tempcrc='00'+margecrc
        elif len(margecrc)==3:
            tempcrc='0'+margecrc
        else:
            tempcrc=margecrc
        sendmess=(messdata+tempcrc+'47').decode('hex')
        self.cboardChild.testmessage.append('tock:'+sendmess.encode('hex'))
        Ygcboardev.write(sendmess)

    def geralregclear(self):
        self.cboardChild.reginfonon.clear()

    def otaupdate(self):
        self.otaChild = Update_Ui_Dialog()
        self.Dialog = QtGui.QDialog(self)
        self.otaChild.setupUi(self.Dialog)

        currentboard=unicode(self.cboardChild.otalist.currentItem().text())
        self.Dialog.setWindowTitle(u'OTA升级界面_'+currentboard)
        self.otaChild.otamessage.append(u'已选择'+currentboard+u'升级')
        self.cboardChild.testitem.clear()
        self.cboardChild.subtest.clear()
        if currentboard==u'轮毂电机':
            self.otaChild.sublist.setEnabled(True)
            self.otaChild.sublist.addItem(u'左电机')
            self.otaChild.sublist.addItem(u'右电机')
        elif currentboard==u'开门电机':
            self.otaChild.sublist.setEnabled(True)
            self.otaChild.sublist.addItem(u'直流电机1')
            self.otaChild.sublist.addItem(u'直流电机2')
        elif currentboard==u'左右箱体控制板':
            self.otaChild.sublist.setEnabled(True)
            self.otaChild.sublist.addItem(u'左上箱体')
            self.otaChild.sublist.addItem(u'右上箱体')
            self.otaChild.sublist.addItem(u'左下箱体')
            self.otaChild.sublist.addItem(u'右下箱体')
        elif currentboard==u'红外传感器':
            self.otaChild.sublist.setEnabled(True)
            self.otaChild.sublist.addItem(u'红外1')
            self.otaChild.sublist.addItem(u'红外2')
            self.otaChild.sublist.addItem(u'红外3')
            self.otaChild.sublist.addItem(u'红外4')
            self.otaChild.sublist.addItem(u'红外5')
            self.otaChild.sublist.addItem(u'红外6')
            self.otaChild.sublist.addItem(u'红外7')
            self.otaChild.sublist.addItem(u'红外8')
            self.otaChild.sublist.addItem(u'红外9')
            self.otaChild.sublist.addItem(u'红外10')
        elif currentboard==u'IMU':
            self.otaChild.sublist.setEnabled(True)
            self.otaChild.sublist.addItem(u'IMU')
        elif currentboard=='2.4G':
            self.otaChild.sublist.setEnabled(True)
            self.otaChild.sublist.addItem(u'2.4G')
        elif currentboard=='Board-C':
            self.otaChild.sublist.addItem(u'Board-C')
            self.otaChild.sublist.setEnabled(True)

        else:
            self.otaChild.verlist.setEnabled(True)

        self.softimer=QtCore.QTimer(self)
        self.softimer.setSingleShot(True)
        self.softimer.timeout.connect(self.firmreload)
        self.softimer.start(10)

        self.otaChild.firwareselect.clicked.connect(self.firwareadd)
        self.otaChild.sublist.clicked.connect(self.upenable)
        self.otaChild.verlist.itemDoubleClicked.connect(self.firmupdate)
        self.otaChild.pause.clicked.connect(self.upstop)
        self.otaChild.open.clicked.connect(self.reopenser)
        self.otaChild.clear.clicked.connect(self.clearmess)
        self.Dialog.exec_()

    def upenable(self):
        self.otaChild.verlist.setEnabled(True)

    def clearmess(self):
        self.otaChild.otamessage.clear()

    def upstop(self):
        try:
            Ygcboardev.close()
            status=u'OTA升级界面-串口已关闭'
            self.Dialog.setWindowTitle(status)
            self.otaChild.open.setEnabled(True)
        except:
            pass

    def firmreload(self):
        totalpatt='total.+'
        successpatt='sucess.+'
        f=open('ui/upcount.txt','r')
        for line in f:
            totalmatch=re.search(totalpatt,line)
            sumatch=re.search(successpatt,line)
            if totalmatch:
                templist=line.split(' ')
                self.otaChild.total.setText(templist[1].rstrip('\n'))
            if sumatch:
                templist=line.split(' ')
                self.otaChild.successcount.setText(templist[1].rstrip('\n'))
        f.close()
        dirs=os.listdir('firmwares/')
        for line in dirs:
            temp=line.split('/')
            version=temp[-1].rstrip('.bin')
            self.otaChild.verlist.addItem(version)

    def firwareadd(self):
        self.otaChild.textBrowser_3.clear()
        firmwarepath =unicode(QtGui.QFileDialog.getOpenFileName(self, 'Open file'))
        if len(firmwarepath):
            temp=firmwarepath.split('/')
            firmwarename=temp[-1]
            firmpattern='.+\.bin'
            firmmatch=re.search(firmpattern,firmwarename)
            if firmmatch:
                self.otaChild.textBrowser_3.append(firmwarepath)
                self.otaChild.verlist.addItem(firmwarename.rstrip('.bin'))
                shutil.copy(firmwarepath,'firmwares/')
            else:
                self.otaChild.otamessage.append(u'选择的文件不是bin文件类型')
                QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("选择的文件不是bin文件类型"))
        else:
            pass

    def firmupdate(self):
        global errindexflag,errcrcflag
        errindexflag=int(self.otaChild.errindex.isChecked())
        errcrcflag=int(self.otaChild.errcrc.isChecked())
        upflagexist=os.path.exists('log/stopflag.txt')
        if upflagexist:
            os.remove('log/stopflag.txt')
        self.otaChild.upstat.setText(u'开始升级')
        currentfirmware=unicode(self.otaChild.verlist.currentItem().text())
        fullfirmware='firmwares/'+currentfirmware+'.bin'
        self.mdvaluehash(fullfirmware)
        devicebid=self.otabidget()
        self.otauper=otaupdater(devicebid,fullfirmware)
        self.otauper.bootSingnal.connect(self.bootmessage)
        self.otauper.barSingnal.connect(self.updateprogess)
        self.otauper.start()

    def bootmessage(self,mess):
        self.otaChild.otamessage.append(unicode(mess))

    def updateprogess(self,value):
        self.otaChild.upbar.setProperty('value',value)
        if value==100:
            self.otaChild.upstat.setText(u'升级完成')

    def otabidget(self):
        currentstation=unicode(self.otaChild.sublist.currentItem().text())
        if currentstation == 'Board-C':
            bid='EE'
        elif currentstation == 'IMU':
            bid='E1'
        elif currentstation == '2.4G':
            bid='71'
        elif currentstation == u'左电机':
            bid='11'
        elif currentstation == u'右电机':
            bid='12'
        elif currentstation == u'轮毂广播升级':
            bid='10'
        elif currentstation == u'左上箱体':
            bid='26'
        elif currentstation == u'右上箱体':
            bid='25'
        elif currentstation == u'左下箱体':
            bid='28'
        elif currentstation == u'右下箱体':
            bid='27'
        elif currentstation == u'BMS':
            bid='E3'
        elif currentstation == u'红外1':
            bid='51'
        elif currentstation == u'红外2':
            bid='52'
        elif currentstation == u'红外3':
            bid='53'
        elif currentstation == u'红外4':
            bid='54'
        elif currentstation == u'红外5':
            bid='55'
        elif currentstation == u'红外6':
            bid='56'
        elif currentstation == u'红外7':
            bid='57'
        elif currentstation == u'红外8':
            bid='58'
        elif currentstation == u'红外9':
            bid='59'
        elif currentstation == u'红外10':
            bid='5A'
        elif currentstation == u'红外广播升级':
            bid='50'
        else:
            bid='31'
        return bid

    def mdvaluehash(self,firmware):
        global MdValue
        data=''
        MdValue=[]
        m=hashlib.md5()
        f=open(firmware,'rb')
        for line in f:
            data+=line
        m.update(data)
        MStr=m.hexdigest()
        for j in xrange(0,32,2):
            Ndata=MStr[j:j+2]
            MdValue.append(Ndata)
        if self.otaChild.errmd5.isChecked():
            temp=int(MdValue[-1],16)+1
            hextemp=hex(temp).lstrip('0x')
            MdValue[-1]=hextemp
        f.close()

    def loginselect(self):
        global sshCilent,rebootflag
        rebootflag=0
        sshCilent = paramiko.SSHClient()
        sshCilent.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        rebootexist=os.path.exists('ui/reboot.txt')
        if self.ui.manual.isEnabled():
            self.ui.textBrowser.append(u'正在按字典查找登录配置文件，请稍后.....')
            self.loginer=autologiner(1,'None')
            self.loginer.autologinSingnal.connect(self.loginWindow)
            self.loginer.netstatSingnal.connect(self.netinfo)
            self.loginer.start()
        else:
            self.ui.textBrowser.append(u'请等待系统完成重启后再登录')

    def netinfo(self,autologin):
        if autologin ==2:
            QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("未知的wifi连接"))
        if autologin ==3:
            QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("PC未连接wifi"))
        if autologin ==4:
            QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("已连接wifi但是ping不通远端"))
        if autologin ==5:
            QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("已连接wifi,ping成功，但是SSH登录失败，检查字典或者远端SSH设置"))
        self.manuallogin()

    def loginWindow(self,autologin,host,port,use,passwd):
        if autologin == 1:
            self.manualWindow(str(host),str(port),str(use),str(passwd))
        else:
            pass

    def manuallogin(self):
        self.conset()
        global configname,stateditflag
        stateditflag=0
        self.LoginChild = Login_Ui_Dialog()
        self.Dialog = QtGui.QDialog(self)
        self.LoginChild.setupUi(self.Dialog)
        configname='ui\Station.txt'
        configsize=os.path.getsize(configname)
        if configsize:
            configer=open(configname,'r')
            for line in configer:
                lineList=line.split(' ')
                statfull=lineList[2]+'@'+lineList[0]
                self.LoginChild.stationlist.addItem(statfull)
            configer.close()
        self.LoginChild.cancel.setHidden(True)
        self.LoginChild.stationlist.setCurrentRow(0)
        self.LoginChild.stationlist.itemClicked.connect(self.statmonitor)
        self.LoginChild.stationlist.itemDoubleClicked.connect(self.login)
        self.LoginChild.stationedit.clicked.connect(self.currentstatedit)
        self.LoginChild.login.clicked.connect(self.login)
        self.LoginChild.close.clicked.connect(self.close)
        self.LoginChild.deletestation.clicked.connect(self.delestat)
        self.LoginChild.cancel.clicked.connect(self.cancelstat)
        self.Dialog.exec_()

    def netssidget(self):
        netstat=(os.popen('netsh WLAN show interfaces').readlines())
        netpattern='    SSID.+'
        for line in netstat:
            netmatch=re.search(netpattern,line)
            if netmatch:
                temp=line.split(': ')
                netssid=temp[1].rstrip('\n')
                break
            else:
                netssid=''
        return netssid

    def autologindump(self,ssid):
        autologinflag=0
        Host=''
        Port=''
        Use=''
        Passwd=''
        if len(ssid):
            ssidhander=open('ui/netdirct.txt','r')
            sshCilent = paramiko.SSHClient()
            sshCilent.set_missing_host_key_policy(paramiko.AutoAddPolicy())#第一次登录的认证信息
            for line in ssidhander:
                ssidlist=line.split(' ')
                ssidpattern=ssidlist[0]+'.+'
                ssiduper=str.upper(ssidlist[0][0])
                ssiduperpattern=ssiduper+ssidlist[0][1:]+'.+'
                ssidmatch=re.search(ssidpattern,ssid)
                ssidupermatch=re.search(ssiduperpattern,ssid)
                if ssidmatch or ssidupermatch:
                    try:
                        sshCilent.connect(hostname=ssidlist[1], port=ssidlist[2], username=ssidlist[3], password=ssidlist[4].rstrip('\n'))
                        autologinflag=1
                        Host=ssidlist[1]
                        Port=ssidlist[2]
                        Use=ssidlist[3]
                        Passwd=ssidlist[4].rstrip('\n')
                        break
                    except:
                        autologinflag=0
                else:
                    pass
            #sshCilent.close()
            if autologinflag==0:
                QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("未知的wifi连接"))
        else:
            autologinflag=0
            QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("PC没有连上wifi"))
        return autologinflag,Host,Port,Use,Passwd

    def autologinerdump(self):
        result=self.netssidget()
        loginflag,host,port,use,passwd=self.autologin(result)
        return loginflag,host,port,use,passwd

    def close(self):
        self.Dialog.close()

    def delestat(self):
        currenstat=unicode(self.LoginChild.stationlist.currentItem().text())
        if currenstat == u'新建站点':
            pass
        else:
            currentrow=self.LoginChild.stationlist.currentRow()
            self.LoginChild.stationlist.takeItem(currentrow)
            with open("ui\Station.txt","r") as f:
                lines = f.readlines()
            with open("ui\Station.txt","w") as f_w:
                 for line in lines:
                     linelist=line.split(' ')
                     if linelist[2]+'@'+linelist[0] == currenstat:
                         continue
                     f_w.write(line)

    def cancelstat(self):
        statname=unicode(self.LoginChild.stationlist.currentItem().text())
        f=open(configname,'a+')
        for line in f:
            linelist=line.split(' ')
            if linelist[2]+'@'+linelist[0] == statname:
                self.LoginChild.hostname.clear()
                self.LoginChild.port.clear()
                self.LoginChild.username.clear()
                self.LoginChild.password.clear()
                self.LoginChild.hostname.setText(linelist[0])
                self.LoginChild.port.setText(linelist[1])
                self.LoginChild.username.setText(linelist[2])
                self.LoginChild.password.setText(linelist[3].rstrip('\n'))
        f.close()

    def deviceSetWindow(self):
        self.WChild = Ui_Dialog()
        self.Dialog = QtGui.QDialog(self)#不加self不在父窗体中,有两个任务栏,加self 表示在父子在窗体中在一个任务栏
        self.WChild.setupUi(self.Dialog)
        self.WChild.deviceSetbutton.clicked.connect(self.openSerial)
        self.Dialog.exec_()

    def statmonitor(self):
        f=open(configname,'a+')
        currenstat=unicode(self.LoginChild.stationlist.currentItem().text())
        if currenstat == u'新建站点':
            self.LoginChild.stationedit.setText(u'保存')
            self.LoginChild.hostname.clear()
            self.LoginChild.port.clear()
            self.LoginChild.username.clear()
            self.LoginChild.password.clear()
            self.LoginChild.hostname.setEnabled(True)
            self.LoginChild.port.setEnabled(True)
            self.LoginChild.username.setEnabled(True)
            self.LoginChild.password.setEnabled(True)
            self.LoginChild.cancel.setHidden(True)
        else:
            self.LoginChild.stationedit.setText(u'编辑')
            for line in f:
                linelist=line.split(' ')
                if linelist[2]+'@'+linelist[0] == currenstat:
                    self.LoginChild.hostname.clear()
                    self.LoginChild.port.clear()
                    self.LoginChild.username.clear()
                    self.LoginChild.password.clear()
                    self.LoginChild.hostname.setText(linelist[0])
                    self.LoginChild.port.setText(linelist[1])
                    self.LoginChild.username.setText(linelist[2])
                    self.LoginChild.password.setText(linelist[3].rstrip('\n'))
                self.LoginChild.hostname.setDisabled(True)
                self.LoginChild.port.setDisabled(True)
                self.LoginChild.username.setDisabled(True)
                self.LoginChild.password.setDisabled(True)
        f.close()

    def currentstatedit(self):
        if unicode(self.LoginChild.stationedit.text()) == u'编辑':
            self.LoginChild.hostname.setEnabled(True)
            self.LoginChild.port.setEnabled(True)
            self.LoginChild.password.setEnabled(True)
            self.LoginChild.username.setEnabled(True)
            self.LoginChild.stationedit.setText(u'保存')
        else:
            currentHost=str(self.LoginChild.hostname.toPlainText())
            currentPort=str(self.LoginChild.port.toPlainText())
            currentPasswd=str(self.LoginChild.password.text())
            currentUse=str(self.LoginChild.username.toPlainText())
            currentlistItem=unicode(self.LoginChild.stationlist.currentItem().text())
            self.LoginChild.hostname.setDisabled(True)
            self.LoginChild.port.setDisabled(True)
            self.LoginChild.password.setDisabled(True)
            self.LoginChild.username.setDisabled(True)
            self.LoginChild.stationedit.setText(u'编辑')
            if currentlistItem != u'新建站点':#更改原有站点信息时
                currentrow=self.LoginChild.stationlist.currentRow()
                self.LoginChild.stationlist.takeItem(currentrow)#删除原有的站点
                self.LoginChild.stationlist.insertItem(1,currentUse+'@'+currentHost)
                self.LoginChild.stationlist.setCurrentRow(1)#新增编辑的站点，并且设置为选中状态
                self.updater(1,currentUse,currentHost,currentPasswd,currentPort,currentlistItem)
                self.updater(2,currentUse,currentHost,currentPasswd,currentPort,currentlistItem)
            else:
                self.LoginChild.stationlist.insertItem(1,currentUse+'@'+currentHost)
                self.LoginChild.stationlist.setCurrentRow(1)
                self.updater(2,currentUse,currentHost,currentPasswd,currentPort,currentlistItem)
        if unicode(self.LoginChild.stationlist.currentItem().text())==u'新建站点':
            self.LoginChild.cancel.setHidden(True)
        else:
            self.LoginChild.cancel.setHidden(False)

    def updater(self,model,Use,Host,Passwd,Port,listItem):
        if model==1:
            with open("ui\Station.txt","r") as f:
                lines = f.readlines()
            with open("ui\Station.txt","w") as f_w:
                for line in lines:
                    linelist=line.split(' ')
                    if linelist[2]+'@'+linelist[0] == listItem:
                        continue
                    f_w.write(line)
            f_w.close()
        else:
            with open("ui\Station.txt","r") as f:
                lines = f.readlines()
            with open("ui\Station.txt","w") as f_w:
                for line in lines:
                    f_w.write(line)
                f_w.write(Host+' '+Port+' '+Use+' '+Passwd+'\n')
            f_w.close()
            self.conset()

    def conset(self):
        templist=[]
        f=open('ui\Station.txt','r')
        for line in f:
            templist.append(line)
        f.close()
        f_w=open('ui\Station.txt','w')
        finaltemp=list(set(templist))
        for sublist in finaltemp:
            f_w.write(sublist)
        f_w.close()

    def login(self):
        global newHost,newPort,newPasswd,newUse
        newHost=str(self.LoginChild.hostname.toPlainText())
        newPort=str(self.LoginChild.port.toPlainText())
        newPasswd=str(self.LoginChild.password.text())
        newUse=str(self.LoginChild.username.toPlainText())
        if len(newHost) and len(newPasswd) and len(newPort) and len(newUse):
            hostlist=newHost.split('.')
            try:
                ipseg=int(hostlist[3])
                try:
                    ipseg_tw=int(hostlist[4])
                    QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("输入的IP地址大于4段，地址格式错误"))
                except:
                    if ipseg>0 and ipseg<=254:
                        self.LoginChild.messinfo.append(u'正在检查网络连接，请等待2s')
                        self.LoginChild.stationlist.setDisabled(True)
                        self.LoginChild.login.setDisabled(True)
                        self.network=networker()
                        self.network.netSingnal.connect(self.netstat)
                        self.network.start()
                    else:
                        QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("输入的IP地址必须大于0小于255"))
            except:
                QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("输入的IP地址小于4段，地址格式错误"))
        else:
            QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("输入不能为空，请检查"))

    def netstat(self,result):
        if result==1:
            self.sshClient()
        else:
            self.LoginChild.messinfo.append(u'无法PING通主机IP地址，检查wifi连接')
            self.LoginChild.stationlist.setEnabled(True)
            self.LoginChild.login.setEnabled(True)
            QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("无法PING通主机IP地址，检查wifi连接"))

    def sshClient(self):
        self.shClient=sshCilenthread()
        self.shClient.loginSingnal.connect(self.loginmessage)
        self.shClient.start()

    def loginmessage(self,mess,flag):
        self.netssidget()
        self.LoginChild.messinfo.append(mess)
        if flag==1:
            loginhost=str(self.LoginChild.hostname.toPlainText())
            loginport=str(self.LoginChild.port.toPlainText())
            loginuse=str(self.LoginChild.username.toPlainText())
            loginpasswd=str(self.LoginChild.password.text())
            self.Dialog.close()
            self.ui.textBrowser.clear()
            self.manualWindow(loginhost,loginport,loginuse,loginpasswd)
        else:
            pass

    def manualWindow(self,host,port,use,passwd):
        global manualhost,manualport,manualuse,manualpasswd,currentplacenum
        manualhost=host
        manualport=int(port)
        manualuse=use
        manualpasswd=passwd

        self.manualChild = Manual_Ui_Dialog()
        self.Dialog = QtGui.QDialog(self)#不加self不在父窗体中,有两个任务栏,加self 表示在父子在窗体中在一个任务栏
        self.manualChild.setupUi(self.Dialog)

        self.createContextMenuRemote()
        self.createContextMenuLocal()
        self.createContextMenuMap()

        self.firtimer=QtCore.QTimer(self)
        self.platimer=QtCore.QTimer(self)

        self.conchecktimer=QtCore.QTimer(self)
        self.ssidchecktimer=QtCore.QTimer(self)
        path=QtGui.QPixmap(r'ui/icons/green.png')
        self.manualChild.constat.setPixmap(path)
        self.manualChild.constat.resize(path.width(),path.height())
        self.connect(self.manualChild.updateini, QtCore.SIGNAL("clicked()"),self.configup)
        self.manualChild.resetcore.clicked.connect(self.corereset)
        self.manualChild.maplist.itemDoubleClicked.connect(self.testmapinit)
        self.manualChild.localist.itemDoubleClicked.connect(self.testmapinit)
        self.manualChild.remotelist.itemDoubleClicked.connect(self.testmapinit)
        self.manualChild.softreset.clicked.connect(self.softreset)
        self.manualChild.review.clicked.connect(self.reviewfile)
        self.manualChild.clear.clicked.connect(self.clearmessage)
        self.manualChild.coreselect.clicked.connect(self.yogoCCselect)
        self.manualChild.iniselet.clicked.connect(self.iniselect)
        self.manualChild.coreupload.clicked.connect(self.yogoccup)
        self.manualChild.mapreflush.clicked.connect(self.mapreflush)#获取远端地图清单
        self.manualChild.inidown.clicked.connect(self.inidownlocad)
        self.manualChild.yogostat.clicked.connect(self.getstat)
        self.manualChild.kill.clicked.connect(self.killthread)
        self.manualChild.logenable.clicked.connect(self.enablecorelog)
        self.manualChild.mapselect.clicked.connect(self.localmap)
        self.firtimer.timeout.connect(self.firupdate)
        self.platimer.timeout.connect(self.comboxplacenable)
        self.conchecktimer.timeout.connect(self.netcheck)
        self.ssidchecktimer.timeout.connect(self.ssidcheck)

        self.manualEnable=QtCore.QTimer(self)
        self.manualEnable.setSingleShot(True)
        self.manualEnable.timeout.connect(self.manualcontrol)

        self.firtimer.setSingleShot(True)

        self.firtimer.start(10)
        self.platimer.start(10)
        self.ssidchecktimer.start(1000)
        self.conchecktimer.start(3000)

        self.Dialog.exec_()

    def remotemap(self,remotelist):
        self.manualChild.maplist.clear()
        remotemap=remotelist
        if len(remotemap):
            for mlist in remotemap:
                self.manualChild.maplist.addItem(mlist)
        else:
            self.manualChild.textBrowser.append(u'远端无地图配置，请检查yogoCC.ini文件')

    def initmapget(self):
        self.localgetmap()
        self.getmap()

    def mapreflush(self):
        currentindex=int(self.manualChild.maptablewidget.currentIndex())
        if currentindex ==0:
            self.manualChild.remotelist.clear()
            self.sftper('maplist',1,'yogoCore/maps/')
        elif currentindex==1:
            self.localgetmap()
        else:
            shutil.copy('coretemp/yogoCC.ini','coretemp/yogoCCdump.ini')
            self.remotemapflush()

    def ssidcheck(self):
        newssid=self.netssidget()
        try:
            currentSSID=str(self.manualChild.APSSID.text())
            if currentSSID=='':
                self.manualChild.APSSID.setText(newssid)
            else:
                if currentSSID == newssid:
                    pass
                else:
                    self.ssidchecktimer.stop()
                    if newssid == '':
                        pass
                    else:
                        QtGui.QMessageBox.information(self,u"通知!",self.trUtf8('已更换wifi连接'))
                        self.netcutupdate()
                        self.manualChild.APSSID.setText(newssid)
        except:
            self.ssidchecktimer.stop()

    def netcutupdate(self):
        #self.Dialog.close()
        self.ui.textBrowser.append(u'网络已切换，请重新登录')

    def netcutupdatedump(self):
        self.Dialog.close()
        self.conset()
        global configname,stateditflag
        stateditflag=0
        self.LoginChild = Login_Ui_Dialog()
        self.Dialog = QtGui.QDialog(self)
        self.LoginChild.setupUi(self.Dialog)
        configname='ui\Station.txt'
        configsize=os.path.getsize(configname)
        if configsize:
            configer=open(configname,'r')
            for line in configer:
                lineList=line.split(' ')
                statfull=lineList[2]+'@'+lineList[0]
                self.LoginChild.stationlist.addItem(statfull)
            configer.close()
        self.LoginChild.cancel.setHidden(True)
        self.LoginChild.stationlist.setCurrentRow(0)
        self.LoginChild.stationlist.itemClicked.connect(self.statmonitor)
        self.LoginChild.stationedit.clicked.connect(self.currentstatedit)
        self.LoginChild.login.clicked.connect(self.login)
        self.LoginChild.close.clicked.connect(self.close)
        self.LoginChild.deletestation.clicked.connect(self.delestat)
        self.LoginChild.cancel.clicked.connect(self.cancelstat)
        self.Dialog.exec_()

    def maplistclear(self):
        self.manualChild.maplist.clear()

    def remotemapflush(self):
        self.mapflush=maprefulsh()
        self.mapflush.mapSingnal.connect(self.remotemapadd)
        self.mapflush.start()

    def mapconnect(self):
        mapselet=unicode(self.manualChild.maplist.currentItem().text())
        self.manualChild.mapname.setText(mapselet)

    def localmap(self):
        seletflag=0
        self.manualChild.mappatch.clear()
        fullmapath =unicode(QtGui.QFileDialog.getOpenFileName(self, 'Open file'))
        if len(fullmapath):
            self.manualChild.mappatch.setText(fullmapath)
            temp=fullmapath[-4:]
            if temp == '.dat':
                seletflag=1
            elif temp == '.emt':
                seletflag=1
            elif temp == 'path':
                seletflag=1
            else:
                seletflag=0
            if seletflag:
                templist=fullmapath.split('/')
                mapath=templist[-1].split('.')

                if temp == 'path':
                    datpath=fullmapath[0:-5]+'.dat'
                    patpath=fullmapath[0:-5]+'.path'
                    emtpath=fullmapath[0:-5]+'.emt'
                else:
                    datpath=fullmapath[0:-4]+'.dat'
                    patpath=fullmapath[0:-4]+'.path'
                    emtpath=fullmapath[0:-4]+'.emt'
                try:
                    shutil.copy(datpath,'maps/')
                    datcopyflag=1
                except:
                    datcopyflag=0
                    QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("dat文件无法复制,原因1.地图文件在maps下2.原文件丢失"))
                try:
                    shutil.copy(patpath,'maps/')
                    patcopyflag=1
                except:
                    patcopyflag=0
                    QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("path文件无法复制原因1.地图文件在maps下2.原文件丢失"))
                try:
                    shutil.copy(emtpath,'maps/')
                    emtcopyflag=1
                except:
                    emtcopyflag=0
                    QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("emt文件无法复制原因1.地图文件在maps下2.原文件丢失"))
                if datcopyflag and emtcopyflag and patcopyflag:
                    itemCount=int(self.manualChild.localist.count())
                    for itemindex in range(0,itemCount):
                        currentitem=str(self.manualChild.localist.item(itemindex).text())
                        if currentitem == u'无地图文件':
                            self.manualChild.localist.takeItem(itemindex)
                    self.manualChild.localist.addItem(mapath[0])
                else:
                    datexist=os.path.exists('maps/'+mapath[0]+'.dat')
                    pathexist=os.path.exists('maps/'+mapath[0]+'.path')
                    emtexist=os.path.exists('maps/'+mapath[0]+'.emt')
                    if datexist:
                        pass
                        #os.remove('maps/'+mapath[0]+'.dat')
                    if pathexist:
                        pass
                        #os.remove('maps/'+mapath[0]+'.path')
                    if emtexist:
                        pass
                        #os.remove('maps/'+mapath[0]+'.emt')
            else:
                QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("选择的地图文件格式错误"))
        else:
            pass

    def netcheck(self):
        self.checker=netchecker()
        self.checker.checkSingnal.connect(self.checkmem)
        self.checker.start()

    def localgetmap(self):
        self.manualChild.localist.clear()
        templist=[]
        dirs=os.listdir('maps/')
        if dirs == []:
            self.manualChild.localist.addItem(u'无地图文件')
        else:
            for temap in dirs:
                line=temap.split('.')
                templist.append(line[0])
            localmaplist=list(set(templist))
            for mapline in localmaplist:
                datmap=mapline+'.dat'
                patmap=mapline+'.path'
                emtmap=mapline+'.emt'
                datexist=os.path.exists('maps/'+datmap)
                pathexist=os.path.exists('maps/'+patmap)
                emtexist=os.path.exists('maps/'+emtmap)
                if datexist:
                    datflag=1
                else:
                     datflag=0
                if pathexist:
                    patflag=1
                else:
                    patflag=0
                if emtexist:
                    emtflag=1
                else:
                    emtflag=0
                if datflag and patflag and emtflag:
                    self.manualChild.localist.addItem(mapline)
                else:
                    pass

    def checkmem(self,flag):
        if flag==1:
            try:
                self.manualChild.netloger.setText('0')
                #self.manualChild.constat.setText(u'网络连接畅通')
                path=QtGui.QPixmap(r'ui/icons/green.png')
                self.manualChild.constat.setPixmap(path)
                self.manualChild.constat.resize(path.width(),path.height())
            except:
                pass
        else:
            try:
                currentnet=int(self.manualChild.netloger.text())
                netcount=currentnet+1
                self.manualChild.netloger.setText(str(netcount))
                #self.manualChild.constat.setText(u'网络连接失败')
                path=QtGui.QPixmap(r'ui/icons/red.png')
                self.manualChild.constat.setPixmap(path)
                self.manualChild.constat.resize(path.width(),path.height())
            except:
                pass
                #self.conchecktimer.stop()
        try:
            if int(self.manualChild.netloger.text()) == 5:
                self.Dialog.close()
                self.conchecktimer.stop()
                self.firtimer.stop()
                self.platimer.stop()
                self.ssidchecktimer.stop()
                self.ui.textBrowser.append(u'网络连接中断，已自动退出维护界面')
        except:
            self.conchecktimer.stop()

    def manualcontrol(self):
        #os.remove('ui/reboot.txt')
        self.ui.manual.setEnabled(True)

    def enablecorelog(self):
        if unicode(self.manualChild.logenable.text()) == u'输出log':
            self.manualChild.logenable.setText(u'关闭log')
        else:
            self.manualChild.logenable.setText(u'输出log')

    def corereset(self):
        rebootexist=os.path.exists('ui/reboot.txt')
        if rebootexist:
            os.remove('ui/reboot.txt')
        self.sheller=gitbashshell(1)
        self.sheller.shellSingnal.connect(self.shellmessage)
        self.sheller.corelogSingal.connect(self.corelog)
        self.sheller.start()

    def softreset(self):
        self.firtimer.stop()
        self.platimer.stop()
        self.conchecktimer.stop()
        self.ssidchecktimer.stop()
        self.ui.manual.setDisabled(True)
        self.manualEnable.start(40000)
        self.softsheller=gitbashshell(2)
        self.softsheller.shellSingnal.connect(self.shellmessage)
        self.softsheller.start()

    def reviewfile(self):
        self.sheller=gitbashshell(3)
        self.sheller.shellSingnal.connect(self.shellmessage)
        self.sheller.start()

    def getstat(self):
        self.sheller=gitbashshell(4)
        self.sheller.shellSingnal.connect(self.shellmessage)
        self.sheller.start()

    def killthread(self):
        self.sheller=gitbashshell(5)
        self.sheller.shellSingnal.connect(self.shellmessage)
        self.sheller.start()

    def clearmessage(self):
        self.manualChild.textBrowser.clear()

    def shellmessage(self,mess):
        self.rebootimer=QtCore.QTimer(self)
        self.rebootimer.timeout.connect(self.diaclose)
        self.rebootimer.setSingleShot(True)
        if mess=='out':
            shellresult=u'SSH登录失败'
            self.manualChild.textBrowser.append(shellresult)
        else:
            if str(mess) == u'已发送指令，请等待设备完成重启':
                self.manualChild.textBrowser.append(u'本窗口将于3S后关闭，请至少等待20s后再次登录')
                self.rebootimer.start(3000)
                self.ui.textBrowser.append(u'设备重启中，请等待20s后再次登录')
            elif str(mess)[0:5] == 'total':
                linelist=str(mess).split('\n')
                count=0
                for line in linelist:
                    if count==0:
                        pass
                    else:
                        if len(line)>2:
                            linelist=line.split(' ')
                            newmess=linelist[-1].decode('utf-8')+'  '+linelist[-3]+'  '+linelist[-2]+'  '+linelist[0]
                            self.manualChild.textBrowser.append(newmess)
                        else:
                            pass
                    count+=1
            else:
                self.manualChild.textBrowser.append(unicode(mess))

    def corelog(self,mess):
        enableswitch=unicode(self.manualChild.logenable.text())
        if enableswitch == u'输出log':
            self.manualChild.textBrowser.append(mess)
        else:
            pass

    def diaclose(self):
        self.Dialog.close()

    def firupdate(self):
        self.localgetmap()
        self.getmap()
        self.shClient=sshCilenthreaddump()
        self.shClient.yogoSingnal.connect(self.yogomessage)
        self.shClient.connectSingnal.connect(self.updateconstat)
        self.shClient.yogoSingnalmiss.connect(self.yogomiss)
        self.shClient.yogoiniSingal.connect(self.yogoinianaly)
        self.shClient.start()

    def iniselect(self):
        inipath =unicode(QtGui.QFileDialog.getOpenFileName(self, 'Open file'))
        self.manualChild.inipath.setText(inipath)

    def inidownlocad(self):
        path=unicode(self.manualChild.inipath.toPlainText())
        pathpattern='yogoCC.ini'
        if len(path):
            pathmath=re.search(pathpattern,path)
            if not pathmath:
                QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("选择的文件不是yogoCC.ini"))
            else:
                pathlist=path.split('/')
                if pathlist[-1] == 'yogoCC.ini':
                    self.sftper('yogoCC.ini',3,path)
                    shutil.copy(path,'coretemp/yogoCCdump.ini')
                    self.getconfiger()
                    self.remotemapflush()
                else:
                    self.manualChild.textBrowser.append(u'yogoCC.ini文件带有其他说明')
                    shutil.copy(path,'coretemp/yogoCC.ini')
                    self.sftper('yogoCC.ini',2,'coretemp/yogoCC.ini')
                    shutil.copy(path,'coretemp/yogoCCdump.ini')
                    self.getconfiger()
                    self.remotemapflush()
                    #self.manualChild.textBrowser.append(u'yogoCC.ini文件已下载')
        else:
            pass

    def getconfiger(self):
        self.manualChild.updatebar.setProperty('value',0)
        self.getClient=sshCilenthreaddump()
        self.getClient.yogoSingnal.connect(self.yogomessage)
        self.getClient.yogoSingnalmiss.connect(self.yogomiss)
        self.getClient.yogoiniSingal.connect(self.yogoinianaly)
        self.getClient.start()

    def yogoCCselect(self):
        global yogopath
        yogopath =unicode(QtGui.QFileDialog.getOpenFileName(self, 'Open file'))
        self.manualChild.corepath.setText(yogopath)
        path=QtGui.QPixmap(r'ui/icons/green.png')
        self.manualChild.constat.setPixmap(path)
        self.manualChild.constat.resize(path.width(),path.height())

    def yogoccup(self):
        sourcesize=self.getsourcesize()
        result=self.sftper('yogoCC','None','None')
        self.manualChild.updatebar_2.setProperty('value',0)
        self.manualChild.coreupload.setDisabled(True)
        self.copyer=yogocoreuper()
        self.copyer.coreupSingnal.connect(self.coreupbar)
        self.copyer.upterSingal.connect(self.mapinfo)
        self.copyer.transtatSingal.connect(self.tanscheck)
        self.copyer.start()

    def tanscheck(self,mess):
        if mess == u'你选的文件不是yogoCC':
            self.manualChild.coreupload.setEnabled(True)
            QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("你选的文件不是yogoCC"))
        elif mess == u"无法复制"+yogopath:
            self.manualChild.textBrowser.append(unicode(mess))
        elif mess == u"你选择的yogoCC带有尾缀说明":
            self.manualChild.textBrowser.append(mess+u',已自动去除尾缀')
        else:
            pass
            #self.processtimer.start(2000)

    def startput(self,copyflag):
        if copyflag:
            self.uphander=yogocoreuper()
            self.uphander.coreupSingnal.connect(self.coreupbar)
            self.uphander.upterSingal.connect(self.mapinfo)
            #self.uphander.transSingal.connect(self.removeyogoCC)
            #self.processtimer.start(2000)
            self.uphander.start()
        else:
            pass

    def removeyogoCC(self,removeflag):
        if removeflag:
            os.remove('coretemp/backup/yogoCC')
        else:
            pass

    def getsourcesize(self):
        size=os.path.getsize(yogopath)
        return size

    def sizerestore(self):
        self.manualChild.updatebar_2.setProperty('value',50)
        #self.processtimer.stop()

    def sizerestoredup(self):
        stdin, stdout, stderr = sshCilent.exec_command('cd yogoCore/;wc -c yogoCC')
        res,err = stdout.read(),stderr.read()
        result = res if res else err
        if result >= sourcesize:
            pass
                #self.processtimer.stop()
                #self.manualChild.updatebar_2.setProperty('value',50)
        else:
            bar=int(result/sourcesize)*100
            self.manualChild.updatebar_2.setProperty('value',bar)

    def getmap(self):
        self.manualChild.remotelist.clear()
        self.sftper('maplist',1,'yogoCore/maps/')

    def sftper(self,cmd,model,path):
        global sftpCilenter
        removeflag=0
        templist=[]
        maplist=[]
        transport = paramiko.Transport((manualhost, manualport))
        transport.connect(username=manualuse, password=manualpasswd)
        sftpCilenter = paramiko.SFTPClient.from_transport(transport)
        if cmd == 'yogoCC':
            pass
        elif cmd == 'maplist':
            remotepath='/home/'+manualuse+'/yogoCore'
            sftpCilenter.chdir(remotepath)
            result=sftpCilenter.listdir('maps')
            if result == []:
                self.manualChild.remotelist.addItem(u'无地图文件')
                QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("远端无地图文件"))
            else:
                for line in result:
                    temp=line.split('.')
                    try:
                        templist.append(temp[0])
                    except:
                        self.manualChild.textBrowser.append(u'maps文件夹下存在格式非法文件:'+line)
                maplist=list(set(templist))
                for lst in maplist:
                    self.manualChild.remotelist.addItem(lst)
        elif cmd == 'yogoCC.ini':
            remotepath='/home/'+manualuse+'/yogoCore/yogoCC.ini'
            if model==1:#get
                file_handler=open(path,'wb')
                sftpCilenter.get(remotepath, path)
                file_handler.close()
            elif model ==2:
                self.manualChild.updatebar.setProperty('value',0)
                sftpCilenter.put(path,remotepath)
                sftpCilenter.chmod('/home/yogo/yogoCore/yogoCC.ini',0777)
                self.manualChild.textBrowser.append(u'yogoCC.ini已下载')
                self.manualChild.updatebar.setProperty('value',100)
            else:#put
                sftpCilenter.put(path,remotepath)
                sftpCilenter.chmod('/home/yogo/yogoCore/yogoCC.ini',0777)
                QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("已自动替换ini模板"))
        else:
            pass
        removeflag=1
        return removeflag

    def coreupbar(self,bar):
        self.manualChild.updatebar_2.setProperty('value',bar)
        if bar == 100:
            self.manualChild.coreupload.setEnabled(True)

    def yogoinianaly(self,result):
        if result==1:
            self.yoinianaly=yogoinalay()
            self.yoinianaly.yogoconfig.connect(self.yogoupdate)
            self.yoinianaly.maplist.connect(self.remotelist)
            self.yoinianaly.start()

    def remotelist(self,maplist):
        global yogoremotelist
        yogoremotelist=maplist
        self.remotemap(yogoremotelist)

    def placenable(self,placeindex):
        if placeindex==1:
            self.manualChild.place1.setEnabled(True)
            self.manualChild.place2.setDisabled(True)
            self.manualChild.place3.setDisabled(True)
            self.manualChild.place4.setDisabled(True)
            self.manualChild.place5.setDisabled(True)
            self.manualChild.place6.setDisabled(True)
        elif placeindex==2:
            self.manualChild.place1.setEnabled(True)
            self.manualChild.place2.setEnabled(True)
            self.manualChild.place3.setDisabled(True)
            self.manualChild.place4.setDisabled(True)
            self.manualChild.place5.setDisabled(True)
            self.manualChild.place6.setDisabled(True)
        elif placeindex==3:
            self.manualChild.place1.setEnabled(True)
            self.manualChild.place2.setEnabled(True)
            self.manualChild.place3.setEnabled(True)
            self.manualChild.place4.setDisabled(True)
            self.manualChild.place5.setDisabled(True)
            self.manualChild.place6.setDisabled(True)
        elif placeindex==4:
            self.manualChild.place1.setEnabled(True)
            self.manualChild.place2.setEnabled(True)
            self.manualChild.place3.setEnabled(True)
            self.manualChild.place4.setEnabled(True)
            self.manualChild.place5.setDisabled(True)
            self.manualChild.place6.setDisabled(True)
        elif placeindex==5:
            self.manualChild.place1.setEnabled(True)
            self.manualChild.place2.setEnabled(True)
            self.manualChild.place3.setEnabled(True)
            self.manualChild.place4.setEnabled(True)
            self.manualChild.place5.setEnabled(True)
            self.manualChild.place6.setDisabled(True)
        elif placeindex==6:
            self.manualChild.place1.setEnabled(True)
            self.manualChild.place2.setEnabled(True)
            self.manualChild.place3.setEnabled(True)
            self.manualChild.place4.setEnabled(True)
            self.manualChild.place5.setEnabled(True)
            self.manualChild.place6.setEnabled(True)
        else:
            pass

    def configup(self):
        global editmapnum,editmapname,editestpla,editpla1,editpla2,editpla3,editpla4,editpla5,editpla6
        editmapnum=str(self.manualChild.mapnum.toPlainText()).lstrip(' ').rstrip(' ')
        editmapname=str(self.manualChild.mapname.toPlainText()).lstrip(' ').rstrip(' ')
        editestpla=str(self.manualChild.testplace.toPlainText()).lstrip(' ').rstrip(' ')
        editpla1=str(self.manualChild.place1.toPlainText()).lstrip(' ').rstrip(' ')
        editpla2=str(self.manualChild.place2.toPlainText()).lstrip(' ').rstrip(' ')
        editpla3=str(self.manualChild.place3.toPlainText()).lstrip(' ').rstrip(' ')
        self.manualChild.updatebar.setProperty('value',20)
        editpla4=str(self.manualChild.place4.toPlainText()).lstrip(' ').rstrip(' ')
        editpla5=str(self.manualChild.place5.toPlainText()).lstrip(' ').rstrip(' ')
        editpla6=str(self.manualChild.place6.toPlainText()).lstrip(' ').rstrip(' ')
        self.manualChild.updatebar.setProperty('value',40)
        self.coreiniuper=yogocoreiniuper()
        self.coreiniuper.coreupSingnal.connect(self.corebar)
        self.coreiniuper.mapSingnal.connect(self.mapinfo)
        self.coreiniuper.start()

    def corebar(self,bar):
        self.manualChild.updatebar.setProperty('value',bar)
        if bar == 100:
            shutil.copy('coretemp/yogoCC.ini','coretemp/yogoCCdump.ini')
            self.mapter=maprefulsh()
            self.mapter.mapSingnal.connect(self.remotemapadd)
            self.mapter.start()

    def remotemapadd(self,map0,map1,map2,map3,map4,map5,map6):
        self.manualChild.maplist.clear()
        self.manualChild.maplist.addItem(map0)
        self.manualChild.maplist.addItem(map1)
        self.manualChild.maplist.addItem(map2)
        self.manualChild.maplist.addItem(map3)
        self.manualChild.maplist.addItem(map4)
        self.manualChild.maplist.addItem(map5)
        self.manualChild.maplist.addItem(map6)

    def mapinfo(self,mess):
        self.manualChild.textBrowser.append(unicode(mess))
        if mess == u'请先拷贝地图文件至maps文件夹下':
            QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("请先拷贝地图文件至maps文件夹下"))

    def updateconstat(self,upflag):
        if upflag==0:
            self.manualChild.textBrowser.append(u'网络连接失败，请检查连接')

    def yogomiss(self,mess):
        self.manualChild.textBrowser.append(unicode(mess))
        if mess == u'yogoCC.ini丢失':
            QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("yogoCC.ini丢失"))
            localinipath='coretemp/yogoCC.ini'
            self.sftper('yogoCC.ini',2,localinipath)
            self.manualChild.textBrowser.append(u'已自动替换yogoCC.ini模板')
        if mess == u'yogoCC丢失':
            QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("yogoCC丢失"))

    def yogomessage(self,mess):
        linelist=str(mess).split('\n')
        count=0
        for line in linelist:
            if count==0:
                pass
            else:
                if len(line)>2:
                    linelist=line.split(' ')
                    newmess=linelist[-1].decode('utf-8')+'  '+linelist[-3]+'  '+linelist[-2]+'  '+linelist[0]
                    self.manualChild.textBrowser.append(newmess)
                else:
                    pass
            count+=1

    def yogoerr(self,mess):
        self.manualChild.textBrowser_2.append(unicode(mess))

    def yogoupdate(self,initmap,mapname,placenum,first,sec,thr,four,fiv,six):
        self.manualChild.mapname.setText(str(mapname).lstrip(' ').rstrip(' '))
        self.manualChild.mapnum.setText(str(initmap).lstrip(' ').rstrip(' '))
        self.manualChild.testplace.setText(str(placenum).lstrip(' ').rstrip(' '))
        self.manualChild.place1.setText(str(first).lstrip(' ').rstrip(' '))
        self.manualChild.place2.setText(str(sec).lstrip(' ').rstrip(' '))
        self.manualChild.place3.setText(str(thr).lstrip(' ').rstrip(' '))
        self.manualChild.place4.setText(str(four).lstrip(' ').rstrip(' '))
        self.manualChild.place5.setText(str(fiv).lstrip(' ').rstrip(' '))
        self.manualChild.place6.setText(str(six).lstrip(' ').rstrip(' '))
        self.placenable(int(placenum))

    def comboxplacenable(self):
        placeindex=0
        try:
            if len(str(self.manualChild.testplace.toPlainText())):
                placeindex=int(self.manualChild.testplace.toPlainText())
            if placeindex==1:
                self.manualChild.place1.setEnabled(True)
                self.manualChild.place2.setDisabled(True)
                self.manualChild.place3.setDisabled(True)
                self.manualChild.place4.setDisabled(True)
                self.manualChild.place5.setDisabled(True)
                self.manualChild.place6.setDisabled(True)
            elif placeindex==2:
                self.manualChild.place1.setEnabled(True)
                self.manualChild.place2.setEnabled(True)
                self.manualChild.place3.setDisabled(True)
                self.manualChild.place4.setDisabled(True)
                self.manualChild.place5.setDisabled(True)
                self.manualChild.place6.setDisabled(True)
            elif placeindex==3:
                self.manualChild.place1.setEnabled(True)
                self.manualChild.place2.setEnabled(True)
                self.manualChild.place3.setEnabled(True)
                self.manualChild.place4.setDisabled(True)
                self.manualChild.place5.setDisabled(True)
                self.manualChild.place6.setDisabled(True)
            elif placeindex==4:
                self.manualChild.place1.setEnabled(True)
                self.manualChild.place2.setEnabled(True)
                self.manualChild.place3.setEnabled(True)
                self.manualChild.place4.setEnabled(True)
                self.manualChild.place5.setDisabled(True)
                self.manualChild.place6.setDisabled(True)
            elif placeindex==5:
                self.manualChild.place1.setEnabled(True)
                self.manualChild.place2.setEnabled(True)
                self.manualChild.place3.setEnabled(True)
                self.manualChild.place4.setEnabled(True)
                self.manualChild.place5.setEnabled(True)
                self.manualChild.place6.setDisabled(True)
            elif placeindex==6:
                self.manualChild.place1.setEnabled(True)
                self.manualChild.place2.setEnabled(True)
                self.manualChild.place3.setEnabled(True)
                self.manualChild.place4.setEnabled(True)
                self.manualChild.place5.setEnabled(True)
                self.manualChild.place6.setEnabled(True)
            else:
                pass
        except:
            self.platimer.stop()

    def initmapconnect(self):
        try:
            initmaplist=yogoremotelist
            try:
                if len(str(self.manualChild.mapnum.toPlainText())):
                    placeindex=int(self.manualChild.mapnum.toPlainText())
                    if placeindex==0:
                        temp=initmaplist[0].split(' = ')
                        self.manualChild.mapname.setText(temp[1])
                    elif placeindex==1:
                        temp=initmaplist[1].split(' = ')
                        self.manualChild.mapname.setText(temp[1])
                    elif placeindex==2:
                        temp=initmaplist[2].split(' = ')
                        self.manualChild.mapname.setText(temp[1])
                    elif placeindex==3:
                        temp=initmaplist[3].split(' = ')
                        self.manualChild.mapname.setText(temp[1])
                    elif placeindex==4:
                        temp=initmaplist[4].split(' = ')
                        self.manualChild.mapname.setText(temp[1])
                    elif placeindex==5:
                        temp=initmaplist[5].split(' = ')
                        self.manualChild.mapname.setText(temp[1])
                    elif placeindex==6:
                        temp=initmaplist[6].split(' = ')
                        self.manualChild.mapname.setText(temp[1])
                    else:
                        pass
                else:
                    pass
            except:
                self.initimer.stop()
        except:
              pass

    def openSerial(self):
        global devcieSerial
        runFlag=0
        deviceType=str(self.WChild.deviceType.currentText())
        deviceSerialNum=str(self.WChild.portSelect.currentText())
        self.ticktimer=QtCore.QTimer(self)
        self.ticktimer.timeout.connect(self.startick)
        try:
            devcieSerial=serial.Serial(deviceSerialNum,1000000,timeout=5)
            runFlag=1
        except:
            QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("端口打开失败，请检查设置"))

        if runFlag:
            status=str.upper(deviceType)+':'+deviceSerialNum+':Ready'
            self.statusBar().showMessage(status)
            self.ticktimer.start(10)

    def startick(self):
        self.monitor=statusMonitor()
        self.monitor.deviceSingal.connect(self.deviceStateupdate)
        self.monitor.controlSingnal.connect(self.deviceconupdate)
        self.monitor.batterystateSingal.connect(self.batstateupdate)
        self.monitor.luggageSingal.connect(self.lugstateupdate)
        self.monitor.framcheckSingal.connect(self.framcheck)
        self.monitor.framissSingal.connect(self.framiss)
        self.monitor.start()
        self.Dialog.close()

    def deviceconupdate(self,boardstate,motorstate):
        self.ui.boardStatus.setText(boardstate)
        self.ui.motorStatus.setText(motorstate)

    def deviceStateupdate(self,datalist):
        self.ui.batteryVolage.setProperty('value',datalist[0])
        self.ui.insideGate.setText(datalist[1])
        self.ui.motorleft.setProperty('value',int(datalist[2],16))
        self.ui.motoright.setProperty('value',int(datalist[3],16))
        self.ui.motorspeedl.setProperty('value',int(datalist[4],16))
        self.ui.motorspeedr.setProperty('value',int(datalist[5],16))
        self.ui.zitaijiao.setText(datalist[6])
        self.ui.sanzhoucichang.setText(datalist[7])
        self.ui.siluspeed.setText(datalist[8])
        self.ui.downDelte.setText(datalist[9])
        self.ui.dianti.setText(datalist[10])
        self.ui.zhongliang.setText(datalist[11])
        self.ui.sanzhoujiasudu.setText(datalist[12])
        self.ui.catchDele.setText(datalist[13])
        self.ui.touchHead.setText(datalist[14])

    def batstateupdate(self,batstate):
        self.ui.chargeStatus.setText(batstate)

    def lugstateupdate(self,lugstate):
        self.ui.gateControl.setText(lugstate)

    def framcheck(self,modle,framerr,recvframe):
        if modle==1:
            self.ui.textBrowser.append(framerr+':'+recvframe)
        else:
            self.ticktimer.stop()

    def framiss(self,modle,errtype,idlist,recvframe):
        if modle==1:#不打断定时器，继续tick/tock
            self.ui.textBrowser.append(idlist+errtype+':'+recvframe)
        else:
            self.ticktimer.stop()

class statusMonitor(QtCore.QThread):

    controlSingnal=QtCore.pyqtSignal(str,str)
    deviceSingal=QtCore.pyqtSignal(list)
    batterystateSingal=QtCore.pyqtSignal(str)
    luggageSingal=QtCore.pyqtSignal(str)
    framcheckSingal=QtCore.pyqtSignal(int,str,str)
    framissSingal=QtCore.pyqtSignal(int,str,str,str)
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        result=self.framerecv()
        if result == '':
            pass
        else:
            print(result)
            checkFlag=self.frameCRCheck(result)
            if checkFlag ==1 :
                self.framcheckSingal.emit(1,u'错误帧',result)
            frameMissResult,missIdlist=self.frameMisscheck(result)
            if frameMissResult == 1:
                misslist=missIdlist[0]+' '+missIdlist[1]
                self.framissSingal.emit(1,u'丢包',misslist,result)
            if checkFlag==0 and frameMissResult==0:
                self.frameMessgeanaly(result)

    def framerecv(self):
        result = ''
        recvHead=devcieSerial.read()
        hexHead = ord(recvHead)
        frameHead = '%02x'%hexHead
        if frameHead == '68':
            result+=frameHead
            for i in range(0,63):
                message=devcieSerial.read()
                hvol = ord(message)
                hhex = '%02x'%hvol
                result += hhex
        return result

    def frameCRCheck(self,result):
        CrcheckFlag=0
        checksum=0
        for i in range(0,128,2):
            checksum+=int(result[i:i+2],16)
        checkValue=(hex(checksum))[-2:]
        recvCheck=result[-4:-2]
        if checkValue != recvCheck:
            CrcheckFlag=1
        return CrcheckFlag

    def frameMisscheck(self,framelist):
        frameId=[]
        frameMissFlag=0
        frameId.append(framelist[16:18])
        if len(frameId)==2:
            if int(frameId[1],16)-int(frameId[0],16) == 1:
                pass
            else:
                if frameId[1] == '00' and frameId[0] == '62':
                    pass
                else:
                    frameMissFlag=1
        return frameMissFlag,frameId

    def frameMessgeanaly(self,frame):
        devicelist=[]
        self.controlstate(frame[18:20])
        self.batterystate(frame[20:22])
        batval=self.batteryval(frame[22:24])
        devicelist.append(batval)
        self.luggagestate(frame[24:26])
        cabinetval=self.cabinetstate(frame[26:28])
        devicelist.append(cabinetval)
        motorposl=self.motor_pos_left(frame[28:32])
        devicelist.append(motorposl)
        motorposr=self.motor_pos_right(frame[32:36])
        devicelist.append(motorposr)
        motorspeedl=self.motor_speed_left(frame[36:40])
        devicelist.append(motorspeedl)
        motorspeedr=self.motor_speed_right(frame[40:44])
        devicelist.append(motorspeedr)
        pitchresult=self.pitch(frame[44:48])
        devicelist.append(pitchresult)
        rollresult=self.roll(frame[48:52])
        devicelist.append(rollresult)
        yawresult=self.yaw(frame[52:56])
        devicelist.append(yawresult)
        iCMPxresult=self.iCMPx(frame[56:60])
        devicelist.append(iCMPxresult)
        iCMPyresult=self.iCMPy(frame[60:64])
        devicelist.append(iCMPyresult)
        iCMPzresult=self.iCMPz(frame[64:68])
        devicelist.append(iCMPzresult)
        ultresult=self.ultra(frame[68:70])
        devicelist.append(ultresult)
        fallingresult=self.falling_delete(frame[70:72])
        devicelist.append(fallingresult)
        gapresult=self.gap(frame[72:74])
        devicelist.append(gapresult)
        wightresult=self.wight(frame[76:80])
        devicelist.append(wightresult)
        iAXresult=self.iAX(frame[80:84])
        devicelist.append(iAXresult)
        iAyresult=self.iAY(frame[84:88])
        devicelist.append(iAyresult)
        iAzresult=self.iAZ(frame[88:92])
        devicelist.append(iAzresult)
        limiteresult=self.limite(frame[94:96])
        devicelist.append(limiteresult)
        touchval=self.touchval(frame[96:100])
        devicelist.append(touchval)
        self.deviceSingal.emit(devicelist)

    def controlstate(self,data):
        controlbit=bin(int(data,10)).lstrip('0b')
        for i in range(0,8-len(controlbit)):
            controlbit='0'+controlbit
        if controlbit[-2:]=='00':
            controlResult=u'正常'
        elif controlbit[-2:]=='01':
            controlResult=u'正在重启'
        elif controlbit[-2:]=='10':
            controlResult=u'正在关机'
        else:
            controlResult=u'请求关机'

        if controlbit[4:6]=='00':
            motorResult=u'无动作'
        elif controlbit[4:6]=='01':
            motorResult=u'使能'
        elif controlbit[4:6]=='10':
            motorResult=u'释放'
        else:
            motorResult=u'非法值:'+controlbit[4:6]
        self.controlSingnal.emit(controlResult,motorResult)

    def batterystate(self,data):
        if data=='00':
            statecode=u'无充电桩'
        elif data=='01':
            statecode=u'充满'
        elif data=='10':
            statecode=u'充电器错误'
        elif data=='11':
            statecode=u'充电中'
        else:
            statecode=u'非法值'+data
        self.batterystateSingal.emit(statecode)

    def batteryval(self,data):
        battery_state=int(data,16)
        return battery_state

    def luggagestate(self,data):
        if data=='00':
            state=u'状态位置'
        elif data=='01':
            state=u'已关闭'
        elif data=='02':
            state=u'已打开'
        elif data=='03':
            state=u'关闭中'
        elif data=='04':
            state=u'打开中'
        elif data=='05':
            state=u'暂停'
        elif data=='06':
            state=u'夹手'
        elif data=='07':
            state=u'开门出错'
        else:
            state=u'非法值'+data
        self.luggageSingal.emit(state)

    def cabinetstate(self,data):
        return data

    def motor_pos_left(self,data):
        return data

    def motor_pos_right(self,data):
        return data

    def motor_speed_left(self,data):
        return data

    def motor_speed_right(self,data):
        return data

    def pitch(self,data):
        return data

    def roll(self,data):
        return data

    def yaw(self,data):
        return data

    def iCMPx(self,data):
        return data

    def iCMPy(self,data):
        return data

    def iCMPz(self,data):
        return data

    def ultra(self,data):
        return data

    def falling_delete(self,data):
        return data

    def gap(self,data):
        return data

    def wight(self,data):
        return data

    def iAX(self,data):
        return data

    def iAY(self,data):
        return data

    def iAZ(self,data):
        return data

    def limite(self,data):
        return data

    def touchval(self,data):
        return data

class sshCilenthread(QtCore.QThread):
    loginSingnal=QtCore.pyqtSignal(str,int)
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        self.loginSingnal.emit(u'开始SSH登陆',2)
        try:
            sshCilent.connect(hostname=newHost, port=newPort, username=newUse, password=newPasswd)

            self.loginSingnal.emit(u'SSH登陆成功',1)
        except:
            self.loginSingnal.emit(u'ssh登录失败',0)

class sshCilenthreaddump(QtCore.QThread):
    connectSingnal=QtCore.pyqtSignal(int)
    yogoSingnalmiss=QtCore.pyqtSignal(str)
    yogoSingnal=QtCore.pyqtSignal(str)
    yogoiniSingal=QtCore.pyqtSignal(int)
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        self.trunyogoCore()

    def trunyogoCore(self):
        result=self.shellcmd('cd yogoCore/;ls -l --time-style=long-iso')
        if result:
            newresult=result.decode('utf-8')
            self.yogoSingnal.emit(newresult)
            #print(result.decode('utf-8'))
            patterncore='yogoCC'+'\n'
            patternini='yogoCC.ini'+'\n'
            result=self.shellcmd('cd yogoCore/;ls')
            matchini=re.search(patternini,result)
            if matchini :
                matiniflag=1
            else:
                matiniflag=0
            if matiniflag==1:
                self.sfpget('yogoCC.ini')
            else:
                self.yogoSingnalmiss.emit(u'yogoCC.ini丢失')
            matchcore=re.search(patterncore,result)
            if matchcore:
                matcoreflag=1
            else:
                matcoreflag=0
            if not matcoreflag:
                self.yogoSingnalmiss.emit(u'yogoCC丢失')
            else:
                pass
        else:
            self.yogoSingnalmiss.emit(result)

    def shellcmd(self,cmd):
        stdin, stdout, stderr = sshCilent.exec_command(cmd)
        res,err = stdout.read(),stderr.read()
        result = res if res else err
        return result

    def sfpget(self,typecore):
        yoinitransport=0
        if typecore=='yogoCC':
            remotepath='/home/'+manualuse+'/yogoCore/yogoCC'
            file_handler=open('coretemp/yogoCC','wb')
            #sftpCilenterdump.get('/home/yogo/yogoCore/yogoCC', 'coretemp/yogoCC')
            sftpCilenter.get(remotepath, 'coretemp/yogoCC')
            file_handler.close()
        else:
            remotepath='/home/'+manualuse+'/yogoCore/yogoCC.ini'
            file_handler=open('coretemp/yogoCC.ini','wb')
            sftpCilenter.get(remotepath, 'coretemp/yogoCC.ini')
            file_handler.close()
            yoinitransport=1
            self.yogoiniSingal.emit(yoinitransport)

class yogoinalay(QtCore.QThread):
    yogoconfig=QtCore.pyqtSignal(str,str,str,str,str,str,str,str,str)
    yogoerr=QtCore.pyqtSignal(str)
    maplist=QtCore.pyqtSignal(list)
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        self.fullmap()
        posflag=0
        pospattern='initMap.+'
        yogoiniHander=open('coretemp/yogoCC.ini','r')
        for hander in yogoiniHander:
            posmatch=re.search(pospattern,hander)
            if posmatch:
                posflag=0
                handerlist=hander.split('=')
                initmap=(handerlist[1].lstrip(' '))[0]
                #print(initmap)
                mapname,mapflag=self.mapinfo(initmap)
                if mapflag==1:
                    placenum=self.yogoplace('Place0')
                    firplace=self.yogoplace('Place1')
                    secplace=self.yogoplace('Place2')
                    thrplace=self.yogoplace('Place3')
                    forplace=self.yogoplace('Place4')
                    fivplace=self.yogoplace('Place5')
                    sixplace=self.yogoplace('Place6')
                    self.yogoconfig.emit(initmap,mapname,placenum,firplace,secplace,thrplace,forplace,fivplace,sixplace)
                break
            else:
                posflag=1
        yogoiniHander.close()
        if posflag:
            self.yogoerr.emit(u'yogoCC.ini 找不到initMAP段')

    def mapinfo(self,initmap):
        mapmatchflag=0
        mapflag=0
        mapname='Null'
        mapattern='MAP'+initmap+'.+'
        yogoinimapHander=open('coretemp/yogoCC.ini','r')
        for maphander in yogoinimapHander:
            mapmatch=re.search(mapattern,maphander)
            if mapmatch:
                mapmatchflag=0
                maplist=maphander.split('=')
                mapname=(maplist[1].rstrip('\n')).lstrip(' ')
                mapflag=1
                break
            else:
                mapmatchflag=1
                mapflag=0
                mapname='Null'
        if mapmatchflag:
            self.yogoerr.emit(u'yogoCC.ini 找不到MAP段')
        yogoinimapHander.close()
        return mapname,mapflag

    def yogoplace(self,placelocation):
        placeflag=0
        placepattern=placelocation+'.+'
        yogoplaceHander=open('coretemp/yogoCC.ini','r')
        for placehander in yogoplaceHander:
            placematch=re.search(placepattern,placehander)
            if placematch:
                placeflag=0
                placelist=placehander.split('=')
                if placelocation=='Place0' or placelocation=='Place1':
                    placetemp=placelist[1].split(';')
                    placenum=placetemp[0].rstrip('\n')
                else:
                    placenum=(placelist[1]).rstrip('\n')
                break
            else:
                placeflag=1
                placenum='Null'
        if placeflag:
            self.yogoerr.emit(u'yogoCC.ini 找不到'+placelocation+u'段')
        yogoplaceHander.close()
        return placenum

    def fullmap(self):
        remaplist=[]
        Hander=open('coretemp/yogoCC.ini','r')
        map0pat='MAP0.+'
        map1pat='MAP1.+'
        map2pat='MAP2.+'
        map3pat='MAP3.+'
        map4pat='MAP4.+'
        map5pat='MAP5.+'
        map6pat='MAP6.+'
        for line in Hander:
            map0match=re.search(map0pat,line)
            map1match=re.search(map1pat,line)
            map2match=re.search(map2pat,line)
            map3match=re.search(map3pat,line)
            map4match=re.search(map4pat,line)
            map5match=re.search(map5pat,line)
            map6match=re.search(map6pat,line)
            if map0match:
                remaplist.append(line.rstrip('\n'))
            if map1match:
                remaplist.append(line.rstrip('\n'))
            if map2match:
                remaplist.append(line.rstrip('\n'))
            if map3match:
                remaplist.append(line.rstrip('\n'))
            if map4match:
                remaplist.append(line.rstrip('\n'))
            if map5match:
                remaplist.append(line.rstrip('\n'))
            if map6match:
                remaplist.append(line.rstrip('\n'))
        self.maplist.emit(remaplist)

class networker(QtCore.QThread):
    netSingnal=QtCore.pyqtSignal(int)
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        ret = os.popen("ping -n 2 -w 1 %s " %newHost)
        result=ret.read()
        pattern=u'100%'
        backinfo=re.search(pattern,result)
        #backinfo=os.system('ping -w 1 %s'%newHost)
        if backinfo:
            self.netSingnal.emit(0)
        else:
            self.netSingnal.emit(1)

class yogocoreiniuper(QtCore.QThread):
    coreupSingnal=QtCore.pyqtSignal(int)
    mapSingnal=QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        pospattern='initMap.+'
        mapnamepattern='MAP'+editmapnum+'.+'
        testplanumpat='Place0.+'
        place1pat='Place1.+'
        place2pat='Place2.+'
        place3pat='Place3.+'
        place4pat='Place4.+'
        place5pat='Place5.+'
        place6pat='Place6.+'
        poipat='POI.+'
        with open("coretemp/yogoCC.ini","r") as f:
            lines = f.readlines()
        f.close()
        with open("coretemp/yogoCC.ini","w") as f_w:
            for line in lines:
                posmatch=re.search(pospattern,line)
                mapmatch=re.search(mapnamepattern,line)
                testplamatch=re.search(testplanumpat,line)
                pla1match=re.search(place1pat,line)
                pla2match=re.search(place2pat,line)
                pla3match=re.search(place3pat,line)
                pla4match=re.search(place4pat,line)
                pla5match=re.search(place5pat,line)
                pla6match=re.search(place6pat,line)
                poimatch=re.search(poipat,line)
                if posmatch:
                    f_w.write('initMap='+editmapnum+' ;start from which floor'+'\n')
                elif mapmatch:
                    f_w.write('MAP'+editmapnum+'='+editmapname+'\n')
                elif testplamatch:
                    f_w.write('Place0='+editestpla+' ; this is number of patrol places. others should be set these numbers such as: 30011;'+'\n')
                elif pla1match:
                    linelist=line.split('=')
                    temp=linelist[0].rstrip(' ').rstrip('\t')
                    if temp=='Place1':
                        f_w.write('Place1='+editpla1+' ; the first place stay double time'+'\n')
                    else:
                        f_w.write(line)
                elif pla2match:
                    linelist=line.split('=')
                    temp=linelist[0].rstrip(' ').rstrip('\t')
                    if temp=='Place2':
                        f_w.write('Place2='+editpla2+'\n')
                    else:
                        f_w.write(line)
                elif pla3match:
                    linelist=line.split('=')
                    temp=linelist[0].rstrip(' ').rstrip('\t')
                    if temp=='Place3':
                        f_w.write('Place3='+editpla3+'\n')
                    else:
                        f_w.write(line)
                elif pla4match:
                    linelist=line.split('=')
                    temp=linelist[0].rstrip(' ').rstrip('\t')
                    if temp=='Place4':
                        f_w.write('Place4='+editpla4+'\n')
                    else:
                        f_w.write(line)
                elif pla5match:
                    linelist=line.split('=')
                    temp=linelist[0].rstrip(' ').rstrip('\t')
                    if temp=='Place5':
                        f_w.write('Place5='+editpla5+'\n')
                    else:
                        f_w.write(line)
                elif pla6match:
                    linelist=line.split('=')
                    temp=linelist[0].rstrip(' ').rstrip('\t')
                    if temp=='Place6':
                        f_w.write('Place6='+editpla6+'\n')
                    else:
                        f_w.write(line)
                elif poimatch:
                    f_w.write('POI=./maps/'+editmapname+'.poi'+'\n')
                else:
                    f_w.write(line)
            updateflag=1
        f_w.close()
        if updateflag==1:
            mapflag,macopy=self.mapasser()
            if mapflag and macopy:
                self.coreiniput('yogoCC.ini')
            else:
                self.coreupSingnal.emit(0)

    def coreiniput(self,path):
        if path == 'yogoCC.ini':
            remotepath='/home/'+manualuse+'/yogoCore/yogoCC.ini'
            sftpCilenter.remove(remotepath)
            self.mapSingnal.emit(u'正在传输yogoCC.ini')
            sftpCilenter.put('coretemp/yogoCC.ini',remotepath)
            sftpCilenter.chmod('/home/'+manualuse+'/yogoCore/yogoCC.ini',0777)
            self.mapSingnal.emit(u'yogoCC.ini done')
            self.coreupSingnal.emit(100)
        else:
            remotemap='/home/'+manualuse+'/yogoCore/maps'
            sftpCilenter.chdir(remotemap)
            transmess=u'正在传输:'+path
            self.mapSingnal.emit(transmess)
            sftpCilenter.put('maps/'+path,path)
            sftpCilenter.chmod(path,0777)

    def mapasser(self):
        patflag=0
        datflag=0
        emtflag=0
        mapcopyflag=0
        stdin, stdout, stderr = sshCilent.exec_command('cd yogoCore/maps/;ls')
        res,err = stdout.read(),stderr.read()
        result = res if res else err
        namepat=editmapname+'.path'
        namedat=editmapname+'.dat'
        nameemt=editmapname+'.emt'
        mathdat=re.search(namedat,result)
        mathpat=re.search(namepat,result)
        mathemt=re.search(nameemt,result)
        if mathdat and mathpat and mathemt:
            mapflag=1
            mapcopyflag=1
        else:
            mapflag=0
        if not mapflag:
            self.mapSingnal.emit(u'机器人无测试地图')
            dirs = os.listdir('maps/')
            namepat=editmapname+'.path'
            namedat=editmapname+'.dat'
            nameemt=editmapname+'.emt'
            for dirc in dirs:
                if dirc == namepat:
                    patflag=1
                elif dirc == namedat:
                    datflag=1
                elif dirc == nameemt:
                    emtflag=1
                else:
                    pass
            if patflag and datflag and emtflag:
                #os.system('cd maps/')
                self.coreiniput(namepat)
                self.coreupSingnal.emit(50)
                self.coreiniput(namedat)
                self.coreupSingnal.emit(70)
                self.coreiniput(nameemt)
                self.coreupSingnal.emit(80)
                mapflag=1
                mapcopyflag=1
            else:
                self.mapSingnal.emit(u'请先拷贝地图文件至maps文件夹下')
        else:
            self.mapSingnal.emit(u'远端已有initMap地图文件')
        return mapflag,mapcopyflag

class yogocoreuper(QtCore.QThread):
    coreupSingnal=QtCore.pyqtSignal(int)
    upterSingal=QtCore.pyqtSignal(str)
    transtatSingal=QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        yogoCCpattern='.+yogoCC'
        yogomatch=re.search(yogoCCpattern,yogopath)
        if yogomatch:
            self.transtatSingal.emit(u"开始检测yogoCC")
            remotepath='/home/'+manualuse+'/yogoCore'
            sftpCilenter.chdir(remotepath)
            pathlist=yogopath.split('/')
            if pathlist[-1] == 'yogoCC':
                try:
                    sftpCilenter.remove('yogoCC')
                except:
                    pass
                self.copycore(sftpCilenter)
            else:
                self.transtatSingal.emit(u"你选择的yogoCC带有尾缀说明")
                shutil.copy(yogopath,'coretemp/backup/yogoCC')
                yogoexist=os.path.exists('coretemp/backup/yogoCC')
                if yogoexist:
                    try:
                        sftpCilenter.remove('yogoCC')
                    except:
                        pass
                    self.copycore(sftpCilenter)
                else:
                    self.transtatSingal.emit(u"无法复制"+yogopath)
        else:
            self.transtatSingal.emit(u"你选的文件不是yogoCC")

    def copycore(self,sftp):
        #remotepath='/home/yogo/yogoCore'
        #sftp.chdir(remotepath)
        self.upterSingal.emit(u'开始传输yogoCC')
        sftp.put(yogopath,'yogoCC')
        self.coreupSingnal.emit(100)
        sftp.chmod('yogoCC',0777)
        self.upterSingal.emit(u'yogoCC传输已完成')

    def timerask(self):
        stdin, stdout, stderr = sshCilent.exec_command('cd yogoCore/;wc -c yogoCC')
        res,err = stdout.read(),stderr.read()
        result = res if res else err
        return result

class gitbashshell(QtCore.QThread):
    shellSingnal=QtCore.pyqtSignal(str)
    resultSignal=QtCore.pyqtSignal(str)
    corelogSingal=QtCore.pyqtSignal(str)
    def __init__(self, Model):
        super(self.__class__, self).__init__()
        self.shcmd=Model

    def __del__(self):
        self.wait()

    def run(self):
        if self.shcmd==1:
            self.shellSingnal.emit(u'正在获取yogoCC PID')
            self.shecmd(1)
        elif self.shcmd == 2:
            #self.shellSingnal.emit(u'已发送指令，请等待设备完成重启')
            self.shecmd(2)
        elif self.shcmd == 3:
            self.shecmd(3)
        elif self.shcmd == 4:
            self.shecmd(4)
        elif self.shcmd == 5:
            self.shecmd(5)
        else:
            pass

    def shecmd(self,cmd):
        if cmd == 1 or cmd == 5:
            stdin, stdout, stderr = sshCilent.exec_command('ps -A|grep yogoCC')
            res,err = stdout.read(),stderr.read()
            result = res if res else err
            if result=='':

                if cmd==1:
                    self.shellSingnal.emit(u'yogoCC进程未启动')
                    newcmd='cd yogoCore/;./yogoCC -platform offscreen'
                    ssh_shell = sshCilent.invoke_shell()
                    ssh_shell.settimeout(1000)
                    ssh_shell.send(newcmd+'\n')
                    while True:
                        line = ssh_shell.recv(1024)
                        self.corelogSingal.emit(line)
                        if line and line.endswith('>'):
                            break
                elif cmd ==5:
                    self.shellSingnal.emit(u'yogoCC进程未启动,无需结束')
            else:
                self.shellSingnal.emit(result)
                subresult=str(result).split(' ?')
                firesult=subresult[0].lstrip(' ')
                self.shellSingnal.emit(u'正在kill yogoCC PID')
                sshCilent.exec_command('sudo kill '+firesult)
                self.shellSingnal.emit(u'yogoCC进程已结束')
                if cmd == 1:
                    newcmd='cd yogoCore/;./yogoCC -platform offscreen'
                    ssh_shell = sshCilent.invoke_shell()
                    ssh_shell.settimeout(1000)
                    ssh_shell.send(newcmd+'\n')
                    while True:
                        line = ssh_shell.recv(1024)
                        self.corelogSingal.emit(line)
                        rebootexist=os.path.exists('ui/reboot.txt')
                        if rebootexist:
                            os.remove('ui/reboot.txt')
                            sshCilent.close()
                            break;
        elif cmd == 2:
            f=open('ui/reboot.txt','a')
            f.write('reboot'+'\n')
            f.close()
            sftpCilenter.close()
            self.shellSingnal.emit(u'已发送指令，请等待设备完成重启')
            sshCilent.exec_command('sudo reboot')
            #sshCilent.close()

        elif cmd == 3:
            stdin, stdout, stderr = sshCilent.exec_command('cd yogoCore/;ls -l --time-style=long-iso')
            res,err = stdout.read(),stderr.read()
            result = res if res else err
            self.shellSingnal.emit(result.decode('utf-8'))
        elif cmd == 4:
            stdin, stdout, stderr = sshCilent.exec_command('ps -A|grep yogoCC')
            res,err = stdout.read(),stderr.read()
            result = res if res else err
            if result=='':
                self.shellSingnal.emit(u'yogoCC进程未启动')
            else:
                self.shellSingnal.emit(u'yogoCC已启动')
                self.shellSingnal.emit(result)
        else:
            pass

class yogoCCopy(QtCore.QThread):
    copySingnal=QtCore.pyqtSignal(int)
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        copyflag=0
        while True:
            shutil.copy(yogopath,'coretemp/backup')
            yogoexist=os.path.exists('coretemp/backup/yogoCC')
            if yogoexist:
                copyflag=1
                break
            else:
                copyflag=0
        self.copySingnal.emit(copyflag)

class netchecker(QtCore.QThread):
    checkSingnal=QtCore.pyqtSignal(int)
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        ret = os.popen("ping -n 1 -w 1 %s " %manualhost)
        result=ret.read()
        pattern=u'100%'
        backinfo=re.search(pattern,result)
        if backinfo:
            self.checkSingnal.emit(0)
        else:
            self.checkSingnal.emit(1)

class initwriter(QtCore.QThread):
    mapwriteSingnal=QtCore.pyqtSignal(str)
    def __init__(self, datatype,placeindex,initnum):
        super(self.__class__, self).__init__()
        self.datawrite=datatype
        self.placewrite=placeindex
        self.initwrite=initnum

    def __del__(self):
        self.wait()

    def run(self):
        try:
            with open("coretemp/yogoCC.ini","r") as f:
                lines = f.readlines()
            f.close()
            with open("coretemp/yogoCC.ini","w") as f_w:
                for line in lines:
                    mapattern=self.datawrite+'.+'
                    match=re.search(mapattern,line)
                    if match:
                        if self.datawrite == 'MAP0':
                            f_w.write('MAP0='+self.placewrite+'\n')
                        elif self.datawrite == 'MAP1':
                            f_w.write('MAP1='+self.placewrite+'\n')
                        elif self.datawrite == 'MAP2':
                            f_w.write('MAP2='+self.placewrite+'\n')
                        elif self.datawrite=='MAP3':
                            f_w.write('MAP3='+self.placewrite+'\n')
                        elif self.datawrite == 'MAP4':
                            f_w.write('MAP4='+self.placewrite+'\n')
                        elif self.datawrite == 'MAP5':
                            f_w.write('MAP5='+self.placewrite+'\n')
                        elif self.datawrite == 'MAP6':
                            f_w.write('MAP6='+self.placewrite+'\n')
                        else:#更改initmap
                            f_w.write('initMap='+self.initwrite+' ;start from which floor'+'\n')
                    else:
                        f_w.write(line)
            updateflag=1
            self.mapwriteSingnal.emit(self.datawrite)
            f_w.close()
        except:
            QtGui.QMessageBox.information(self,u"警告!",self.trUtf8("coretemp下yogoCC.ini文件丢失"))

class autologiner(QtCore.QThread):
    autologinSingnal=QtCore.pyqtSignal(int,str,str,str,str)
    netstatSingnal=QtCore.pyqtSignal(int)
    def __init__(self, Model,ssid):
        super(self.__class__, self).__init__()
        self.entry=Model
        self.cutssid=ssid

    def __del__(self):
        self.wait()

    def run(self):
        result=self.netssidget()
        self.autologin(result)

    def netssidget(self):
        netstat=(os.popen('netsh WLAN show interfaces').readlines())
        netpattern='    SSID.+'
        for line in netstat:
            netmatch=re.search(netpattern,line)
            if netmatch:
                temp=line.split(': ')
                netssid=temp[1].rstrip('\n')
                break
            else:
                netssid=''
        return netssid

    def autologin(self,ssid):
        autologinflag=0
        Host=''
        Port=''
        Use=''
        Passwd=''
        if len(ssid):
            ssidhander=open('ui/netdirct.txt','r')
            for line in ssidhander:
                ssidlist=line.split(' ')
                ssidpattern=ssidlist[0]+'.+'
                ssiduper=str.upper(ssidlist[0][0])
                ssiduperpattern=ssiduper+ssidlist[0][1:]+'.+'
                ssidmatch=re.search(ssidpattern,ssid)
                ssidupermatch=re.search(ssiduperpattern,ssid)
                Hostname=ssidlist[1]
                if ssidmatch or ssidupermatch:
                    p = subprocess.Popen(["ping.exe", Hostname], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
                    out = p.stdout.read().decode('gbk')
                    reg_receive = u'丢失 = 0 (0% 丢失)'#ping成功
                    match_receive = re.search(reg_receive, out)
                    if not match_receive:
                        try:
                            sshCilent.connect(hostname=Hostname, port=ssidlist[2], username=ssidlist[3], password=ssidlist[4].rstrip('\n'))
                            autologinflag=1
                            Host=ssidlist[1]
                            Port=ssidlist[2]
                            Use=ssidlist[3]
                            Passwd=ssidlist[4].rstrip('\n')
                            self.autologinSingnal.emit(autologinflag,Host,Port,Use,Passwd)
                            break
                        except:
                            self.netstatSingnal.emit(5)
                            break
                    else:#热点已连接，但是ping失败
                        self.netstatSingnal.emit(4)
                        break
                else:
                    self.netstatSingnal.emit(2)
                    break
        else:
            self.netstatSingnal.emit(3)

class maprefulsh(QtCore.QThread):
    mapSingnal=QtCore.pyqtSignal(str,str,str,str,str,str,str)
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        posresult=''
        map0result=''
        map1result=''
        map2result=''
        map3result=''
        map4result=''
        map5result=''
        map6result=''
        pospattern='initMap.+'
        mapzpattern='MAP0.+'
        mapfpattern='MAP1.+'
        mapsepattern='MAP2.+'
        maptpattern='MAP3.+'
        mapfopattern='MAP4.+'
        mapfvpattern='MAP5.+'
        mapsxpattern='MAP6.+'
        with open("coretemp/yogoCCdump.ini","r") as f_w:
            lines = f_w.readlines()
            for line in lines:
                posmatch=re.search(pospattern,line)
                mapzmatch=re.search(mapzpattern,line)
                mapfmatch=re.search(mapfpattern,line)
                mapsematch=re.search(mapsepattern,line)
                maptmatch=re.search(maptpattern,line)
                mapfomatch=re.search(mapfopattern,line)
                mapfvmatch=re.search(mapfvpattern,line)
                mapsxmatch=re.search(mapsxpattern,line)
                if posmatch:
                    linelist=line.split('=')
                    posresult=(linelist[1].lstrip(' ').rstrip('\n'))[0]
                elif mapzmatch:
                    map0result=line.rstrip('\n')
                elif mapfmatch:
                    map1result=line.rstrip('\n')
                elif mapsematch:
                    map2result=line.rstrip('\n')
                elif maptmatch:
                    map3result=line.rstrip('\n')
                elif mapfomatch:
                    map4result=line.rstrip('\n')
                elif mapfvmatch:
                    map5result=line.rstrip('\n')
                elif mapsxmatch:
                    map6result=line.rstrip('\n')
                else:
                    pass
        f_w.close()
        for i in range(0,7):
            if i ==0:
                map0indexlist=map0result.split('=')
                map0index=map0indexlist[0][3]
                if map0index == posresult:
                    map0result=map0result+'    initMap'
                    break
            elif i ==1:
                map1indexlist=map0result.split('=')
                map1index=map1indexlist[0][3]
                if map1index == posresult:
                    map1result=map1result+'    initMap'
                    break
            elif i ==2:
                map2indexlist=map2result.split('=')
                map2index=map2indexlist[0][3]
                if map2index == posresult:
                    map2result=map2result+'    initMap'
                    break
            elif i ==3:
                map3indexlist=map3result.split('=')
                map3index=map3indexlist[0][3]
                if map3index == posresult:
                    map3result=map3result+'    initMap'
                    break
            elif i ==4:
                map4indexlist=map4result.split('=')
                map4index=map4indexlist[0][3]
                if map4index == posresult:
                    map4result=map4result+'    initMap'
                    break
            elif i ==5:
                map5indexlist=map5result.split('=')
                map5index=map5indexlist[0][3]
                if map5index == posresult:
                    map5result=map5result+'    initMap'
                    break
            elif i ==6:
                map6indexlist=map6result.split('=')
                map6index=map6indexlist[0][3]
                if map6index == posresult:
                    map6result=map6result+'    initMap'
                    break
            else:
                pass
        self.mapSingnal.emit(map0result,map1result,map2result,map3result,map4result,map5result,map6result)

class titodebug(QtCore.QThread):

    messSingnal=QtCore.pyqtSignal(str)
    listSingnal=QtCore.pyqtSignal(list)
    titocountSingnal=QtCore.pyqtSignal(int)
    errSingnal=QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        count=0
        while True:
            result=self.framerecv('ee','6e')
            if result == '':
                pass
            else:
                checkFlag=self.frameCRCheck(result)
                if checkFlag ==1 :
                    self.messSingnal.emit(u'CRC16校验错误')
                else:
                    seq=result[-8:-6]
                    self.tocksend(seq)
                    #print(result)
                    messlist=self.frameMessgeanaly(result)
                    self.listSingnal.emit(messlist)
            count+=1
            if count>=2:
                count=0
            titostopexist=os.path.exists('ui/titostop.txt')
            if titostopexist:
                break

    def framerecv(self,bid,cmd):
        result = ''
        soflag=0
        while True:
            recvHead=titodevice.read()
            try:
                hexHead = ord(recvHead)
                frameHead = '%02x'%hexHead
                if frameHead == '59':
                    soflag=1
                    result+=frameHead
                    break
            except:
                self.messSingnal.emit(u'SOF段接收超时')
                break
        if soflag==1:
            recvbinbid=titodevice.read()
            hexbid = ord(recvbinbid)
            recvbid = '%02x'%hexbid
            result+=recvbid
            if str.upper(recvbid) != bid:
                self.messSingnal.emit(u'tito BID对不上')
            recvbincmd=titodevice.read()
            hexcmd = ord(recvbincmd)
            recvcmd = '%02x'%hexcmd
            result+=recvcmd
            if str.upper(recvcmd) != cmd:
                self.messSingnal.emit(u'tito cmd对不上')
            recvbinlen=titodevice.read()
            hexlen = ord(recvbinlen)
            recvlen = '%02x'%hexlen
            result+=recvlen
            length=int(recvlen,16)
            for i in range(0,length+4):
                message=titodevice.read()
                hvol = ord(message)
                hhex = '%02x'%hvol
                result += hhex
            self.messSingnal.emit(result)
        return result

    def frameCRCheck(self,result):
        modbus_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
        CrcheckFlag=0
        checksum=''
        for i in range(0,len(result)-6,2):
            checksum+=result[i:i+2]
        temp=checksum.decode('hex')
        checkValue=hex(modbus_crc_func(temp)).lstrip('0x')
        for i in range(0,4-len(checkValue)):
            checkValue='0'+checkValue
        recvCheck=result[-4:-2]+result[-6:-4]
        if checkValue != recvCheck:
            CrcheckFlag=1
        return CrcheckFlag

    def tocksend(self,seq):
        leftspeed=titowin.leftmotorvalue.value()
        rightspeed=titowin.rightmotorvalue.value()
        if unicode(titowin.comboBox.currentText())== u'反向':
            if leftspeed==0:
                hexleft='0000'
            else:
                temp=65536-leftspeed
                hextemp=hex(temp).lstrip('0x').rstrip('L')
                for i in range(0,4-len(hextemp)):
                    hextemp='0'+hextemp
                hexleft=hextemp
        else:
            hexleftspeed=hex(leftspeed).lstrip('0x')
            for i in range(0,4-len(hexleftspeed)):
                hexleftspeed='0'+hexleftspeed
            hexleft=hexleftspeed

        if unicode(titowin.comboBox_2.currentText())== u'反向':
            if rightspeed==0:
                hexright='0000'
            else:
                temp=65536-rightspeed
                hexrightemp=hex(temp).lstrip('0x').rstrip('L')
                for i in range(0,4-len(hexrightemp)):
                    hexrightemp='0'+hexrightemp
                hexright=hexrightemp
        else:
            hexrightspeed=hex(rightspeed).lstrip('0x')
            for i in range(0,4-len(hexrightspeed)):
                hexrightspeed='0'+hexrightspeed
            hexright=hexrightspeed

        if unicode(titowin.leftmotorcontrol.currentText())==u'使能' and unicode(titowin.rightmotorcontrol.currentText())==u'使能':
            motorcontrol='11'
        elif unicode(titowin.leftmotorcontrol.currentText())==u'使能' and unicode(titowin.rightmotorcontrol.currentText())==u'释放':
            motorcontrol='01'
        elif unicode(titowin.leftmotorcontrol.currentText())==u'释放' and unicode(titowin.rightmotorcontrol.currentText())==u'使能':
            motorcontrol='10'
        else:
            motorcontrol='00'

        doorcmd=self.getdoorcmd()
        motorcmd=hexleft[2]+hexleft[3]+hexleft[0]+hexleft[1]+hexright[2]+hexright[3]+hexright[0]+hexright[1]

        duojicmd=self.duojicmdinfoget()
        lightcmd=self.lightinfoget()

        tockmessage=motorcmd+motorcontrol+'0000'+doorcmd+duojicmd+lightcmd+'000000000000'
        mess='59'+'ee'+'ee'+'11'+'10'+tockmessage+seq
        tocksendmess=self.messmarge(mess,1)
        titodevice.flushInput()
        titodevice.write(tocksendmess)
        #print(tocksendmess.encode('hex'))

    def lightinfoget(self):
        action='00'
        if titowin.groupBox_11.isEnabled():
            if titowin.leftlight1open.isChecked():
                leftlightfirvol=1
            else:
                leftlightfirvol=0

            if titowin.leftlight2open.isChecked():
                leftlightsecvol=4
            else:
                leftlightsecvol=0

            if titowin.rightlight1open.isChecked():
                rightlightfirvol=2
            else:
                rightlightfirvol=0

            if titowin.rightlight2open.isChecked():
                rightlightsecvol=8
            else:
                rightlightsecvol=0
            temp=hex(leftlightfirvol+rightlightfirvol+leftlightsecvol+rightlightsecvol).lstrip('0x')
            if temp=='':
                temp='00'
            if len(temp)==1:
                action='0'+temp
            else:
                action=temp
        return action

    def duojicmdinfoget(self):
        action='00'
        if titowin.groupBox_11.isEnabled():
            if titowin.leftduoji1open.isChecked():
                leftduojifirvol=1
            else:
                leftduojifirvol=0

            if titowin.leftduoji2open.isChecked():
                leftduojisecvol=4
            else:
                leftduojisecvol=0

            if titowin.rightduoji1open.isChecked():
                rightduojifirvol=2
            else:
                rightduojifirvol=0

            if titowin.rightduoji2open.isChecked():
                rightduojisecvol=8
            else:
                rightduojisecvol=0
            temp=hex(leftduojifirvol+rightduojifirvol+leftduojisecvol+rightduojisecvol).lstrip('0x')
            if temp=='':
                temp='00'
            if len(temp)==1:
                action='0'+temp
            else:
                action=temp
        return action

    def getdoorcmd(self):
        action='00'
        if titowin.groupBox_12.isEnabled():
            if titowin.openrightdoorup.isChecked():
                rightupaction=2
            else:
                rightupaction=0

            if titowin.openleftdoorup.isChecked():
                leftupaction=1
            else:
                leftupaction=0

            if titowin.openrightdoordown.isChecked():
                rightdownaction=8
            else:
                rightdownaction=0

            if titowin.openleftdoordown.isChecked():
                leftdownaction=4
            else:
                leftdownaction=0

            temp=hex(leftupaction+rightupaction+leftdownaction+rightdownaction).lstrip('0x')
            if temp=='':
                temp='00'
            if len(temp)==1:
                action='0'+temp
            else:
                action=temp

        return action

    def messmarge(self,data,model):
        modbus_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
        messcrc=hex(modbus_crc_func(str(data).decode('hex')))
        if model ==1:
            sendcrc=messcrc
        else:
            sendcrc=hex(int(messcrc,16)+1)
        margecrc=sendcrc.lstrip('0x')
        if len(margecrc)==1:
            tempcrc='000'+margecrc
        elif len(margecrc)==2:
            tempcrc='00'+margecrc
        elif len(margecrc)==3:
            tempcrc='0'+margecrc
        else:
            tempcrc=margecrc

        finalcrc=tempcrc[2]+tempcrc[3]+tempcrc[0]+tempcrc[1]
        sendmess=(str(data)+finalcrc+'47').decode('hex')
        self.messSingnal.emit('tock:'+sendmess.encode('hex'))
        return sendmess

    def frameMessgeanaly(self,frame):
        #print(frame)
        devicelist=[]
        warrcode=self.warringcode(frame[10:12])
        devicelist.append(warrcode)
        errcode=self.errcodeany(frame[12:14])
        devicelist.append(errcode)

        Inchingstat=self.Inchingstatget(frame[14:16])
        devicelist.append(Inchingstat)
        leftmotorstat,rightmotorstat=self.motorstatget(frame[16:18])
        devicelist.append(leftmotorstat)
        devicelist.append(rightmotorstat)
        motorposl=self.motor_pos_left(frame[18:22],frame)
        devicelist.append(motorposl)
        motorspeedl=self.motor_speed_left(frame[22:26],frame)
        devicelist.append(motorspeedl)
        motorposr=self.motor_pos_right(frame[26:30],frame)
        devicelist.append(motorposr)
        motorspeedr=self.motor_speed_right(frame[30:34],frame)
        devicelist.append(motorspeedr)

        IMUaccX=self.IMUaccXget(frame[38:42],frame)
        devicelist.append(IMUaccX)
        IMUaccY=self.IMUaccYget(frame[42:46],frame)
        devicelist.append(IMUaccY)
        IMUaccZ=self.IMUaccZget(frame[46:50],frame)
        devicelist.append(IMUaccZ)
        IMUcmpX=self.IMUcmpXget(frame[50:54],frame)
        devicelist.append(IMUcmpX)
        IMUcmpY=self.IMUcmpYget(frame[54:58],frame)
        devicelist.append(IMUcmpY)
        IMUcmpZ=self.IMUcmpZget(frame[58:62],frame)
        devicelist.append(IMUcmpZ)
        IMUpitch=self.IMUpitchget(frame[62:66],frame)
        devicelist.append(IMUpitch)
        IMURoll=self.IMURollget(frame[66:70],frame)
        devicelist.append(IMURoll)
        IMUYaw=self.IMUYawget(frame[70:74],frame)
        devicelist.append(IMUYaw)

        fallingresult=self.falling_dete(frame[74:76])
        devicelist.append(fallingresult)
        leftupdoor,leftdowndoor,rightupdoor,rightdowndoor=self.cabinedoorstat(frame[78:80])
        devicelist.append(leftupdoor)
        devicelist.append(leftdowndoor)
        devicelist.append(rightupdoor)
        devicelist.append(rightdowndoor)
        luplock,ldownlock,ruplock,rdownlock,upbox,downbox=self.cabinelockstat(frame[80:82])
        devicelist.append(luplock)
        devicelist.append(ldownlock)
        devicelist.append(ruplock)
        devicelist.append(rdownlock)
        devicelist.append(upbox)
        devicelist.append(downbox)
        batstat=self.batterystate(frame[82:84])
        devicelist.append(batstat)
        batval=self.batteryval(frame[84:86],frame)
        #print(batval)
        devicelist.append(batval)

        ultrasoundfir=self.ultrasoundget(frame[90:92],frame)
        devicelist.append(ultrasoundfir)
        ultrasoundsec=self.ultrasoundget(frame[92:94],frame)
        devicelist.append(ultrasoundsec)
        ultrasoundthr=self.ultrasoundget(frame[94:96],frame)
        devicelist.append(ultrasoundthr)
        ultrasoundfou=self.ultrasoundget(frame[96:98],frame)
        devicelist.append(ultrasoundfou)
        ultrasoundfiv=self.ultrasoundget(frame[98:100],frame)
        devicelist.append(ultrasoundfiv)
        ultrasoundsix=self.ultrasoundget(frame[100:102],frame)
        devicelist.append(ultrasoundsix)

        infraredfir=self.infraredget(frame[102:104],frame)
        devicelist.append(infraredfir)
        infraredsec=self.infraredget(frame[104:106],frame)
        devicelist.append(infraredsec)
        infraredthr=self.infraredget(frame[106:108],frame)
        devicelist.append(infraredthr)
        infraredfou=self.infraredget(frame[108:110],frame)
        devicelist.append(infraredfou)
        infraredfiv=self.infraredget(frame[110:112],frame)
        devicelist.append(infraredfiv)
        infraredsix=self.infraredget(frame[112:114],frame)
        devicelist.append(infraredsix)
        infraredsev=self.infraredget(frame[114:116],frame)
        devicelist.append(infraredsev)
        infraredeig=self.infraredget(frame[116:118],frame)
        devicelist.append(infraredeig)
        infrarednig=self.infraredget(frame[118:120],frame)
        devicelist.append(infrarednig)
        infraredten=self.infraredget(frame[120:122],frame)
        devicelist.append(infraredten)
        leftup,rightup,leftdown,rightdown,totalup,totaldown=self.weiany(frame)
        devicelist.append(leftup)
        devicelist.append(rightup)
        devicelist.append(leftdown)
        devicelist.append(rightdown)
        devicelist.append(totalup)
        devicelist.append(totaldown)

        return devicelist

    def warringcode(self,code):
        if code == '01':
            warrtype=u'丢包过多'
        elif code == '02':
            warrtype=u'重启过'
        elif code =='04':
            warrtype=u'CPU温度过高'
        elif code == '03':
            warrtype=u'丢包过多,重启过'
        elif code == '05':
            warrtype=u'丢包过多,CPU温度过高'
        elif code == '06':
            warrtype=u'CPU温度过高,重启过'
        elif code == '07':
            warrtype=u'丢包过多,CPU温度过高,重启过'
        else:
            warrtype=u'正常'
        return warrtype

    def errcodeany(self,code):
        if code != '00':
            errtype=u'设备故障'
        else:
            errtype=u'正常'
        return errtype

    def motor_pos_left(self,data,frame):
        try:
            tempdata=int(data[2]+data[3]+data[0]+data[1],16)
        except:
            self.errSingnal.emit(frame)
            tempdata='0000'
        return tempdata

    def motor_pos_right(self,data,frame):
        try:
            tempdata=int(data[2]+data[3]+data[0]+data[1],16)
        except:
            self.errSingnal.emit(frame)
            tempdata='0000'
        return tempdata

    def motor_speed_left(self,data,frame):
        finaldata=0
        try:
            temp=data[2]+data[3]+data[0]+data[1]
            speed=int(temp,16)
            if speed>32768:
                speed=65536-speed
                finaldata='-'+str(speed)
            else:
                finaldata=speed
        except:
            self.errSingnal.emit(frame)
        return finaldata

    def motor_speed_right(self,data,frame):
        finaldata=0
        try:
            temp=data[2]+data[3]+data[0]+data[1]
            speed=int(temp,16)
            if speed>32768:
                speed=65536-speed
                finaldata='-'+str(speed)
            else:
                finaldata=speed
        except:
            self.errSingnal.emit(frame)
        return finaldata

    def IMUaccXget(self,data,frame):
        finaldata=0
        try:
            temp=data[2]+data[3]+data[0]+data[1]
            tempdata=int(temp,16)
            if tempdata>32768:
                tempdata=float((65536-tempdata)*0.01)
                finaldata='-'+str(tempdata)
            else:
                finaldata=float(tempdata*0.01)
        except:
            self.errSingnal.emit(frame)
        return finaldata

    def IMUaccYget(self,data,frame):
        finaldata=0
        try:
            temp=data[2]+data[3]+data[0]+data[1]
            tempdata=int(temp,16)
            if tempdata>32768:
                tempdata=float((65536-tempdata)*0.01)
                finaldata='-'+str(tempdata)
            else:
                finaldata=float(tempdata*0.01)
        except:
            self.errSingnal.emit(frame)
        return finaldata

    def IMUaccZget(self,data,frame):
        finaldata=0
        try:
            temp=data[2]+data[3]+data[0]+data[1]
            tempdata=int(temp,16)
            if tempdata>32768:
                tempdata=float((65536-tempdata)*0.01)
                finaldata='-'+str(tempdata)
            else:
                finaldata=float(tempdata*0.01)
        except:
            self.errSingnal.emit(frame)
        return finaldata

    def IMUgropXget(self,data,frame):
        finaldata=0
        try:
            temp=data[2]+data[3]+data[0]+data[1]
            tempdata=int(temp,16)
            if tempdata>32768:
                tempdata=65536-tempdata
                finaldata='-'+str(tempdata)
            else:
                finaldata=tempdata
        except:
            self.errSingnal.emit(frame)
        return finaldata

    def IMUgropYget(self,data,frame):
        finaldata=0
        try:
            temp=data[2]+data[3]+data[0]+data[1]
            tempdata=int(temp,16)
            if tempdata>32768:
                tempdata=65536-tempdata
                finaldata='-'+str(tempdata)
            else:
                finaldata=tempdata
        except:
            self.errSingnal.emit(frame)
        return finaldata

    def IMUgropZget(self,data,frame):
        finaldata=0
        try:
            temp=data[2]+data[3]+data[0]+data[1]
            tempdata=int(temp,16)
            if tempdata>32768:
                tempdata=65536-tempdata
                finaldata='-'+str(tempdata)
            else:
                finaldata=tempdata
        except:
            self.errSingnal.emit(frame)
        return finaldata

    def IMUcmpXget(self,data,frame):
        finaldata=0
        try:
            temp=data[2]+data[3]+data[0]+data[1]
            tempdata=int(temp,16)
            if tempdata>32768:
                tempdata=65536-tempdata
                finaldata='-'+str(tempdata)
            else:
                finaldata=tempdata
        except:
            self.errSingnal.emit(frame)
        return finaldata

    def IMUcmpYget(self,data,frame):
        finaldata=0
        try:
            temp=data[2]+data[3]+data[0]+data[1]
            tempdata=int(temp,16)
            if tempdata>32768:
                tempdata=65536-tempdata
                finaldata='-'+str(tempdata)
            else:
                finaldata=tempdata
        except:
            self.errSingnal.emit(frame)
        return finaldata

    def IMUcmpZget(self,data,frame):
        finaldata=0
        try:
            temp=data[2]+data[3]+data[0]+data[1]
            tempdata=int(temp,16)
            if tempdata>32768:
                tempdata=65536-tempdata
                finaldata='-'+str(tempdata)
            else:
                finaldata=tempdata
        except:
            self.errSingnal.emit(frame)
        return finaldata

    def IMUpitchget(self,data,frame):
        finaldata=0
        try:
            temp=data[2]+data[3]+data[0]+data[1]
            tempdata=int(temp,16)
            if tempdata>32768:
                tempdata=float((65536-tempdata)*0.01)
                finaldata='-'+str(tempdata)
            else:
                finaldata=str(float(tempdata*0.01))
        except:
            self.errSingnal.emit(frame)
        return finaldata

    def IMURollget(self,data,frame):
        finaldata=0
        try:
            temp=data[2]+data[3]+data[0]+data[1]
            tempdata=int(temp,16)
            if tempdata>32768:
                tempdata=float((65536-tempdata)*0.01)
                finaldata='-'+str(tempdata)
            else:
                finaldata=str(float(tempdata*0.01))
        except:
            self.errSingnal.emit(frame)
        return finaldata

    def IMUYawget(self,data,frame):
        finaldata=0
        try:
            temp=data[2]+data[3]+data[0]+data[1]
            tempdata=int(temp,16)
            if tempdata>32768:
                tempdata=float((65536-tempdata)*0.01)
                finaldata='-'+str(tempdata)
            else:
                finaldata=str(float(tempdata*0.01))
        except:
            self.errSingnal.emit(frame)
        return finaldata

    def ultrasoundget(self,data,frame):
        dis=0
        try:
            dis=int(data,16)
        except:
            self.errSingnal.emit(frame)
        return str(dis)

    def infraredget(self,data,frame):
        dis=0
        try:
            dis=int(data,16)
        except:
            self.errSingnal.emit(frame)
        return str(dis)

    def batterystate(self,data):
        if data=='00':
            statecode=u'未知状态'
        elif data=='01':
            statecode=u'正常放电'
        elif data=='02':
            statecode=u'正在充电'
        elif data=='03':
            statecode=u'充满电'
        elif data=='ff':
            statecode=u'异常状态'
        else:
            statecode=u'非法值'+data
        return statecode

    def batteryval(self,data,frame):
        battery=0
        try:
            battery=int(data,16)
        except:
            self.errSingnal.emit(frame)
        return battery

    def Inchingstatget(self,data):
        if data=='01':
            inchstat=u'右侧'
        elif data=='02':
            inchstat=u'中间'
        elif data=='03':
            inchstat=u'右侧,中间'
        elif data=='04':
            inchstat=u'左侧'
        elif data=='05':
            inchstat=u'左,右'
        elif data=='06':
            inchstat=u'左侧,中间'
        elif data=='07':
            inchstat=u'左中右'
        else:
            inchstat=u'无碰撞'
        return inchstat

    def falling_dete(self,data):
        if data=='00' or data=='01':
            fallstat=u'正常'
        elif data=='02':
            fallstat=u'异常'
        elif data=='04':
            fallstat=u'失重'
        else:
            fallstat=u'电梯'
        return fallstat

    def outdoorstat(self,data):
        if data=='00':
            doorstat=u'未知'
        elif data=='01':
            doorstat=u'关闭'
        elif data=='02':
            doorstat=u'已开'
        elif data=='03':
            doorstat=u'正在关'
        elif data=='04':
            doorstat=u'正在开'
        elif data=='f0':
            doorstat=u'异常'
        else:
            doorstat=u'非法值'
        return doorstat

    def cabinedoorstat(self,data):
        try:
            temp=int(data,16)
        except:
            temp=0
        if temp==0:
            leftup=u'打开'
            leftdown=u'打开'
            rightup=u'打开'
            rightdown=u'打开'
        else:
            if temp&1==1:
                leftup=u'中间'
            if temp&2==2:
                leftup=u'关闭'
            if temp&1!=1 and temp&2!=2:
                leftup=u'打开'
            if temp&3 == 3:
                leftup=u'未知'

            if temp&4==4:
                rightup=u'中间'
            if temp&8==8:
                rightup=u'关闭'
            if temp&4!=4 and temp&8!=8:
                rightup=u'打开'
            if temp&12==12:
                rightup=u'未知'

            if temp&16==16:
                leftdown=u'中间'
            if temp&32==32:
                leftdown=u'关闭'
            if temp&4!=16 and temp&32!=32:
                leftdown=u'打开'
            if temp&48==48:
                leftdown=u'未知'

            if temp&64==64:
                rightdown=u'中间'
            if temp&128==128:
                rightdown=u'关闭'
            if temp&64!=64 and temp&128!=128:
                rightdown=u'打开'
            if temp&192==192:
                rightdown=u'未知'

        return leftup,leftdown,rightup,rightdown

    def cabinelockstat(self,data):
        try:
            temp=int(data,16)
        except:
            temp=0
        if temp&64==64:
            upbox=u'到位'
        else:
            upbox=u'未到位'
        if temp&128==128:
            downbox=u'到位'
        else:
            downbox=u'未到位'
        if temp&1==1:
            leftup=u'锁定'
        else:
            leftup=u'未锁'
        if temp&4==4:
            leftdown=u'锁定'
        else:
            leftdown=u'未锁'
        if temp&2==2:
            rightup=u'锁定'
        else:
            rightup=u'未锁'
        if temp&8==8:
            rightdown=u'锁定'
        else:
            rightdown=u'未锁'

        return leftup,leftdown,rightup,rightdown,upbox,downbox

    def workmode(self,data):
        return data

    def motorstatget(self,data):
        if data=='00':
            leftmotor=u'释放'
            rightmotor=u'释放'
        elif data=='01':
            leftmotor=u'使能'
            rightmotor=u'释放'
        elif data=='10':
            leftmotor=u'释放'
            rightmotor=u'使能'
        else:
            leftmotor=u'使能'
            rightmotor=u'使能'
        return leftmotor,rightmotor

    def dboardstatget(self,data):
        return data

    def weiany(self,frame):
        temp1=int((frame[132]+frame[133]+frame[130]+frame[131]),16)
        temp2=int((frame[136]+frame[137]+frame[134]+frame[135]),16)
        temp3=int((frame[140]+frame[141]+frame[138]+frame[139]),16)
        #print((frame[140]+frame[141]+frame[138]+frame[139]))
        temp4=int((frame[144]+frame[145]+frame[142]+frame[143]),16)
        #print((frame[144]+frame[145]+frame[142]+frame[143]))
        if temp1>32767:
            tempdata=65536-temp1
            leftup='-'+str(tempdata)
        else:
            leftup=str(temp1)

        if temp2>32767:
            tempdata=65536-temp2
            rightup='-'+str(tempdata)
        else:
            rightup=str(temp2)

        if temp1>32767 and temp2>32767:
            totaltemp=(65536-temp1)+(65536-temp2)
            totalup='-'+str(totaltemp)
        elif temp1>32767 and temp2<32767:
            if (65536-temp1)>temp2:
                totaltemp=65536-temp1-temp2
                totalup='-'+str(totaltemp)
            else:
                totaltemp=temp2-(65536-temp1)
                totalup=str(totaltemp)
        elif temp1<32767 and temp2>32767:
            if (65536-temp2)>temp1:
                totaltemp=(65536-temp2)-temp1
                totalup='-'+str(totaltemp)
            else:
                totaltemp=temp1-(65536-temp2)
                totalup=str(totaltemp)
        else:
            totaltemp=temp1+temp2
            totalup=str(totaltemp)

        if temp3>32767:
            tempdata=65536-temp3
            leftdown='-'+str(tempdata)
        else:
            leftdown=str(temp3)

        if temp4>32767:
            tempdata=65536-temp4
            rightdown='-'+str(tempdata)
        else:
            rightdown=str(temp4)

        if temp3>32767 and temp4>32767:
            totaltemp=(65536-temp3)+(65536-temp4)
            totaldown='-'+str(totaltemp)
        elif temp3>32767 and temp4<32767:
            if (65536-temp3)>temp4:
                totaltemp=65536-temp3-temp4
                totaldown='-'+str(totaltemp)
            else:
                totaltemp=temp4-(65536-temp3)
                totaldown=str(totaltemp)
        elif temp3<32767 and temp4>32767:
            if (65536-temp4)>temp3:
                totaltemp=(65536-temp4)-temp3
                totaldown='-'+str(totaltemp)
            else:
                totaltemp=temp3-(65536-temp4)
                totaldown=str(totaltemp)
        else:
            totaltemp=temp3+temp4
            totaldown=str(totaltemp)

        #totalup=int(leftup.lstrip('-'))+int(rightup.lstrip('-'))
        #totaldown=int(leftdown.lstrip('-'))+int(rightdown.lstrip('-'))

        if totalup[0]=='-':
            total=str((int(str(totalup).lstrip('-')))*0.38)
        else:
            total='-'+str((int(str(totalup).lstrip('-')))*0.38)

        if totaldown[0]=='-':
            downtotal=str((int(str(totaldown).lstrip('-')))*0.38)
        else:
            downtotal='-'+str((int(str(totaldown).lstrip('-')))*0.38)

        return leftup,rightup,leftdown,rightdown,total,downtotal

class titothread(QtCore.QThread):

    seqSingnal=QtCore.pyqtSignal(str)
    messSingnal=QtCore.pyqtSignal(str)
    def __init__(self, bid,cmd):
        super(self.__class__, self).__init__()
        self.devid=bid
        self.cmd=cmd

    def __del__(self):
        self.wait()

    def run(self):
        checkFlag=0
        result=self.framerecv(self.devid,self.cmd)
        if result == '':
            pass
        else:
            checkFlag=self.frameCRCheck(result)
            if checkFlag ==1 :
                self.messSingnal.emit(u'CRC16校验错误')
            else:
                seq=result[-8:-6]
                self.seqSingnal.emit(seq)

    def framerecv(self,bid,cmd):
        result = ''
        soflag=0
        while True:
            recvHead=Ygcboardev.read()
            try:
                hexHead = ord(recvHead)
                frameHead = '%02x'%hexHead
                if frameHead == '59':
                    soflag=1
                    result+=frameHead
                    break
            except:
                self.messSingnal.emit(u'SOF段接收超时')
                break
        if soflag==1:
            recvbinbid=Ygcboardev.read()
            try:
                hexbid = ord(recvbinbid)
                recvbid = '%02x'%hexbid
                result+=recvbid
                if str.upper(recvbid) == bid:
                    pass
                else:
                    self.messSingnal.emit(u'tito BID对不上')
                recvbincmd=Ygcboardev.read()
                try:
                    hexcmd = ord(recvbincmd)
                    recvcmd = '%02x'%hexcmd
                    result+=recvcmd
                    if str.upper(recvcmd) == cmd:
                        pass
                    else:
                        self.messSingnal.emit(u'tito cmd对不上')
                    recvbinlen=Ygcboardev.read()
                    try:
                        hexlen = ord(recvbinlen)
                        recvlen = '%02x'%hexlen
                        result+=recvlen
                        length=int(recvlen,16)
                        for i in range(0,length+4):
                            message=Ygcboardev.read()
                            try:
                                hvol = ord(message)
                                hhex = '%02x'%hvol
                                result += hhex
                            except:
                                self.messSingnal.emit(u'数据接收超时')
                                break
                    except:
                        self.messSingnal.emit(u'LEN接收超时')
                except:
                    self.messSingnal.emit(u'cmd接收超时')
            except:
                self.messSingnal.emit(u'bid接收超时')
        self.messSingnal.emit(result)
        return result

    def frameCRCheck(self,result):
        modbus_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
        CrcheckFlag=0
        checksum=''
        for i in range(0,len(result)-6,2):
            checksum+=result[i:i+2]
        temp=checksum.decode('hex')
        checkValue=hex(modbus_crc_func(temp)).lstrip('0x')
        for i in range(0,4-len(checkValue)):
            checkValue='0'+checkValue
        recvCheck=result[-4:-2]+result[-6:-4]
        if checkValue != recvCheck:
            CrcheckFlag=1
        return CrcheckFlag

class otaupdater(QtCore.QThread):

    bootSingnal=QtCore.pyqtSignal(str)
    barSingnal=QtCore.pyqtSignal(int)
    def __init__(self, bid,fullpath):
        super(self.__class__, self).__init__()
        self.devicebid=bid
        self.firmpath=fullpath

    def __del__(self):
        self.wait()

    def run(self):
        Ygcboardev.flushInput()
        upflagexist=os.path.exists('ui/stopflag.txt')
        if upflagexist:
            os.remove('ui/stopflag.txt')
        size,mainloop,loopmu,datalist=self.TransportBinToHex(self.firmpath)
        bootready=self.bootready(self.devicebid)
        if bootready:#boot模式已经准备就绪，可以开始升级
            #self.bootSingnal.emit(u'等待系统重启1s')
            #time.sleep(1)
            time1=(int(round((time.time()) * 1000)))
            writeresult=self.writefirminfo(self.devicebid,self.firmpath)
            if writeresult:#固件信息写入成功，可开始传输固件
                self.bootSingnal.emit(u'开始升级固件')
                transflag=self.transfirmware(mainloop,loopmu,datalist,self.devicebid,size)
                if transflag:
                    self.bootSingnal.emit(u'固件传输完成，开始校验固件')
                    checkresult=self.firmwarevalidation(self.devicebid)
                    if checkresult:
                        self.rebootToApp(self.devicebid)
                        time2=(int(round((time.time()) * 1000)))
                        TotleTime=str(int((time2-time1)/1000))
                        self.bootSingnal.emit(u'传输耗时：'+TotleTime+u'秒')
                    else:
                        pass
                else:
                    pass
            else:
                self.bootSingnal.emit(u'重复10次无法写入固件信息和版本号，本次升级失败')
        else:
            self.bootSingnal.emit(u'重复10次无法进入boot模式，本次升级失败')

    def framerecv(self):
        result = ''
        recvHead=Ygcboardev.read()
        try:
            hexHead = ord(recvHead)
            frameHead = '%02x'%hexHead
            if frameHead == '59':
                result+=frameHead
                recvbinbid=Ygcboardev.read()
                hexbid = ord(recvbinbid)
                recvbid = '%02x'%hexbid
                result+=recvbid
                recvbincmd=Ygcboardev.read()
                hexcmd = ord(recvbincmd)
                recvcmd = '%02x'%hexcmd
                result+=recvcmd
                recvbinlen=Ygcboardev.read()
                hexlen = ord(recvbinlen)
                recvlen = '%02x'%hexlen
                result+=recvlen
                length=int(recvlen,16)
                for i in range(0,length+4):
                    message=Ygcboardev.read()
                    hvol = ord(message)
                    hhex = '%02x'%hvol
                    result += hhex
                self.bootSingnal.emit(result)
            return result
        except:
            self.bootSingnal.emit(u'SOF接收超时')
            return result

    def frameCRCheck(self,framelen,result):
        modbus_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
        CrcheckFlag=0
        checksum=''
        for i in range(0,framelen-6,2):
            checksum+=result[i:i+2]
        temp=checksum.decode('hex')
        checkValue=hex(modbus_crc_func(temp)).lstrip('0x')
        for i in range(0,4-len(checkValue)):
            checkValue='0'+checkValue
        recvCheck=result[-4:-2]+result[-6:-4]
        if checkValue != recvCheck:
            CrcheckFlag=1
        return CrcheckFlag

    def bootready(self,bid):
        readyflag=0
        bootcount=0
        #if not bid == ' ':#C板升级，无需使C板进入转发模式
        self.bootSingnal.emit(u'正在发送进入boot命令')
        messdata='59'+str(bid)+'51'+'01'+'00'+'00'
        framedata=self.messmarge(messdata)
        while True:
            Ygcboardev.write(framedata)
            result=self.framerecv()
            #print(result)
            framelen=len(result)
            if framelen == 0:
                self.bootSingnal.emit(u'重新发送进入boot模式指令')
            else:
                crcheckresult=self.frameCRCheck(framelen,result)
                if crcheckresult==1:
                    self.bootSingnal.emit(u'进入boot模式帧校验错误')
                else:
                    if result[8:10]=='00':
                        self.bootSingnal.emit(u'已进入boot模式')
                        readyflag=1
                        break
                    else:
                        self.bootSingnal.emit(u'进入boot模式失败,重新发送进入boot模式')
            upflagexist=os.path.exists('log/stopflag.txt')
            if upflagexist:
                readyflag=0
                break
            #bootcount+=1
            #if bootcount>=10:
                #readyflag=0
                #break
        #else:
            #pass
        return readyflag

    def entrycboard(self):
        self.bootSingnal.emit(u'正在发送C板进入转发模式命令')
        messdata='59'+'EE'+'62'+'00'+'00'
        framedata=self.messmarge(messdata)
        Ygcboardev.write(framedata)

    def messmarge(self,data):
        modbus_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
        messcrc=hex(modbus_crc_func(data.decode('hex')))
        margecrc=messcrc.lstrip('0x')
        if len(margecrc)==0:
            tempcrc='0000'
        elif len(margecrc)==1:
            tempcrc='000'+margecrc
        elif len(margecrc)==2:
            tempcrc='00'+margecrc
        elif len(margecrc)==3:
            tempcrc='0'+margecrc
        else:
            tempcrc=margecrc
        finalcrc=tempcrc[2]+tempcrc[3]+tempcrc[0]+tempcrc[1]
        sendmess=(data+finalcrc+'47').decode('hex')
        self.bootSingnal.emit(sendmess.encode('hex'))
        return sendmess

    def writefirminfo(self,bid,filename):
        writeflag=0
        #writecount=0
        self.bootSingnal.emit(u'开始写入固件大小和版本')
        Size = os.path.getsize(filename)
        self.bootSingnal.emit(u'固件大小:'+str(Size)+'Bytes')
        hexsize=hex(Size).lstrip('0x').rstrip('L')
        for i in range(0,8-len(hexsize)):
            hexsize='0'+hexsize
        messdata='59'+str(bid)+'52'+'06'+hexsize[6:8]+hexsize[4:6]+hexsize[2:4]+hexsize[0:2]+'0000'+'00'#缺少版本号格式
        framedata=self.messmarge(messdata)
        while True:
            Ygcboardev.write(framedata)
            result=self.framerecv()
            framelen=len(result)
            crcheckresult=self.frameCRCheck(framelen,result)
            if crcheckresult != 1:
                if result[8:10]=='00':
                    self.bootSingnal.emit(u'已写入固件大小和版本号')
                    writeflag=1
                    break
                else:
                    self.bootSingnal.emit(u'写入固件大小和版本号失败,重新写入固件信息')
            else:
                self.bootSingnal.emit(u'帧校验失败，重新写入固件和版本号信息')
            upflagexist=os.path.exists('log/stopflag.txt')
            if upflagexist:
                writeflag=0
                break
            #writecount+=1
            #if writecount>=10:
                #writeflag=0
                #break
        return writeflag

    def TransportBinToHex(self,filename):
        data=''
        datalist=[]
        f=open(filename,'rb')
        Size = os.path.getsize(filename)
        for i in f:
            data+=binascii.b2a_hex(i)
        f.close()
        length=len(data)
        for j in xrange(0,length,2):
            Ndata=data[j:j+2]
            datalist.append(Ndata)
        mainloop=int(Size/64)
        loopmu=Size%64#不够整除部分
        return Size,mainloop,loopmu,datalist

    def transfirmware(self,mainloop,loopmu,datalist,bid,size):
        upflag=0
        if loopmu == 0:#升级包大小正好是64byte整数倍
            result=self.transmain(mainloop,datalist,bid)
            if result:
                upflag=1
            else:
                upflag=0
        else:#不是64字节整数倍
            result=self.transmain(mainloop,datalist,bid)#先将整数部分传输完
            if result:
                subresult=self.transub(mainloop,datalist[size-loopmu:size],bid)
                if subresult:
                    upflag=1
                    self.barSingnal.emit(100)
        return upflag

    def transmain(self,mainloop,datalist,bid):
        transresult=1
        for loop in range(0,mainloop):
            index=hex(loop).lstrip('0x')
            for j in range(0,8-len(index)):
                index='0'+index
            result=self.dataSplit(datalist[loop*64:loop*64+64],index,loop,bid)
            bar=(loop/mainloop)*100
            self.barSingnal.emit(bar)
            if result==0:
                transresult=0
                self.bootSingnal.emit(u'数据重复发送超过10次失败,本次升级失败')
                break
        return transresult

    def dataSplit(self,data,index,loop,bid):
        #transcount=0
        transflag=0
        newdata=''
        if loop>255:
            temploop=loop%256
            if temploop==0:
                seqloop='00'
            else:
                if temploop<16:
                    seqloop='0'+hex(temploop).lstrip('0x')
                else:
                    seqloop=hex(temploop).lstrip('0x')
        else:
            if loop==0:
                seqloop='00'
            else:
                if loop<16:
                    seqloop='0'+hex(loop).lstrip('0x')
                else:
                    seqloop=hex(loop).lstrip('0x')
        for line in data:
            newdata+=line
        if errindexflag:
            if index=='00000008':
                index='00000002'
        messdata='59'+str(bid)+'53'+'44'+index[6:8]+index[4:6]+index[2:4]+index[0:2]+newdata+seqloop
        framedata=self.messmarge(messdata)
        while True:
            Ygcboardev.write(framedata)
            result=self.framerecv()
            framelen=len(result)
            if framelen==0:
                self.bootSingnal.emit(u'数据发送失败,重新发送')
            else:
                crcheckresult=self.frameCRCheck(framelen,result)
                if crcheckresult != 1:
                    #if result[-8:-6]== seqloop:
                    if result[8:10] == '00':
                        transflag=1
                        break
                    else:
                        self.bootSingnal.emit(u'数据发送失败,重新发送')
                    #else:
                        #self.bootSingnal.emit(u'数据帧回复帧seq段错误,重新发送')
                else:
                    self.bootSingnal.emit(u'数据帧回复帧校验失败,重新发送')
            upflagexist=os.path.exists('log/stopflag.txt')
            if upflagexist:
                transflag=0
                break
            #transcount+=1
            #if transcount>=10:
                #transflag=0
                #break
        return transflag

    def transub(self,mainloop,data,bid):
        transflag=0
        transcount=0
        datas=''
        for line in data:
            datas+=line
        index=hex(mainloop).lstrip('0x').rstrip('L')
        for j in range(0,8-len(index)):
            index='0'+index
        datalen=hex(len(data)+4).lstrip('0x').rstrip('L')
        if len(datalen)==1:
            datalen='0'+datalen
        messdata='59'+str(bid)+'53'+datalen+index[6:8]+index[4:6]+index[2:4]+index[0:2]+datas+'00'
        framedata=self.messmarge(messdata)
        while True:
            Ygcboardev.write(framedata)
            result=self.framerecv()
            framelen=len(result)
            if framelen == 0:
                self.bootSingnal.emit(u'数据重新发送')
            else:
                crcheckresult=self.frameCRCheck(framelen,result)
                if crcheckresult != 1:
                    #if result[-8:-6]== '00':
                    if result[8:10] == '00':
                        transflag=1
                        self.bootSingnal.emit(u'数据传输已完成')
                        break
                    else:
                        self.bootSingnal.emit(u'result回复失败,数据重新发送')
                    #else:
                        #self.bootSingnal.emit(u'数据帧回复seq段错误,数据重新发送')
                else:
                    self.bootSingnal.emit(u'数据帧校验失败,数据重新发送')
            upflagexist=os.path.exists('log/stopflag.txt')
            if upflagexist:
                transflag=0
                break
            #transcount+=1
            #if transcount>=10:
                #transflag=0
                #self.bootSingnal.emit(u'数据重复发送超过10次失败,本次升级失败')
                #break
        return transflag

    def firmwarevalidation(self,bid):
        validationflag=0
        newmd=''
        for line in MdValue:
            newmd=newmd+line
        messdata='59'+str(bid)+'54'+'10'+newmd+'00'
        framedata=self.messmarge(messdata)
        while True:
            Ygcboardev.write(framedata)
            result=self.framerecv()
            framelen=len(result)
            if framelen == 0:
                self.bootSingnal.emit(u'无响应，固件校验失败')
            else:
                crcheckresult=self.frameCRCheck(framelen,result)
                if crcheckresult !=1 :
                    #if result[-8:-6]== '00':
                    if result[8:10] == '00':
                        self.bootSingnal.emit(u'固件校验成功')
                        validationflag=1
                        break
                    else:
                        self.bootSingnal.emit(u'固件校验失败')
                    #else:
                        #self.bootSingnal.emit(u'固件校验失败')
                else:
                    self.bootSingnal.emit(u'响应帧CRC校验失败')
            upflagexist=os.path.exists('log/stopflag.txt')
            if upflagexist:
                break
        return validationflag

    def rebootToApp(self,bid):
        rebootcount=0
        messdata='59'+str(bid)+'55'+'00'+'00'
        framedata=self.messmarge(messdata)
        while True:
            Ygcboardev.write(framedata)
            result=self.framerecv()
            framelen=len(result)
            if framelen == 0:
                 self.bootSingnal.emit(u'重新发送重启进入App指令')
            else:
                crcheckresult=self.frameCRCheck(framelen,result)
                if crcheckresult != 1:
                    #if result[-8:-6]== '00':
                    if result[8:10] == '00':
                        self.bootSingnal.emit(u'重启进入App成功')
                        break
                    else:
                        self.bootSingnal.emit(u'重启进入App失败,重新发送重启进入App指令')
                    #else:
                        #self.bootSingnal.emit(u'回复帧seq段错误,重新发送重启进入App指令')
                else:
                    self.bootSingnal.emit(u'帧校验失败，重新发送重启进入App指令')
            upflagexist=os.path.exists('log/stopflag.txt')
            if upflagexist:
                break
            #rebootcount+=1
            #if rebootcount>=10:
                #self.bootSingnal.emit(u'发送重启进入App指令连续超过10次，本次升级失败')
                #break

class uotaupdater(QtCore.QThread):
    bootSingnal=QtCore.pyqtSignal(str)
    barSingnal=QtCore.pyqtSignal(int)
    def __init__(self, bid,fullpath):
        super(self.__class__, self).__init__()
        self.devicebid=bid
        self.firmpath=fullpath

    def __del__(self):
        self.wait()

    def run(self):
        upflagexist=os.path.exists('ui/stopflag.txt')
        if upflagexist:
            os.remove('ui/stopflag.txt')
        size,mainloop,loopmu,datalist=self.TransportBinToHex(self.firmpath)
        bootready=self.bootready(self.devicebid)
        if bootready:#boot模式已经准备就绪，可以开始升级
            self.bootSingnal.emit(u'等待系统重启1s')
            time.sleep(1)
            time1=(int(round((time.time()) * 1000)))
            writeresult=self.writefirminfo(self.devicebid,self.firmpath)
            if writeresult:#固件信息写入成功，可开始传输固件
                self.bootSingnal.emit(u'开始升级固件')
                transflag=self.transfirmware(mainloop,loopmu,datalist,self.devicebid,size)
                if transflag:
                    self.bootSingnal.emit(u'固件传输完成，开始校验固件')
                    checkresult=self.firmwarevalidation(self.devicebid)
                    if checkresult:
                        self.rebootToApp(self.devicebid)
                        time2=(int(round((time.time()) * 1000)))
                        TotleTime=str(int((time2-time1)/1000))
                        self.bootSingnal.emit(u'传输耗时：'+TotleTime+u'秒')
                    else:
                        pass
                else:
                    pass
            else:
                self.bootSingnal.emit(u'重复10次无法写入固件信息和版本号，本次升级失败')
        else:
            self.bootSingnal.emit(u'重复10次无法进入boot模式，本次升级失败')

    def framerecv(self):
        result = ''
        recvHead=Ygcboardev.read()
        try:
            hexHead = ord(recvHead)
            frameHead = '%02x'%hexHead
            if frameHead == '59':
                result+=frameHead
                recvbinbid=Ygcboardev.read()
                hexbid = ord(recvbinbid)
                recvbid = '%02x'%hexbid
                result+=recvbid
                recvbincmd=Ygcboardev.read()
                hexcmd = ord(recvbincmd)
                recvcmd = '%02x'%hexcmd
                result+=recvcmd
                recvbinlen=Ygcboardev.read()
                hexlen = ord(recvbinlen)
                recvlen = '%02x'%hexlen
                result+=recvlen
                length=int(recvlen,16)
                for i in range(0,length+4):
                    message=Ygcboardev.read()
                    hvol = ord(message)
                    hhex = '%02x'%hvol
                    result += hhex
                self.bootSingnal.emit(result)
            return result
        except:
            self.bootSingnal.emit(u'SOF接收超时')
            return result

    def frameCRCheck(self,framelen,result):
        modbus_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
        CrcheckFlag=0
        checksum=''
        for i in range(0,framelen-6,2):
            checksum+=result[i:i+2]
        temp=checksum.decode('hex')
        checkValue=hex(modbus_crc_func(temp)).lstrip('0x')
        for i in range(0,4-len(checkValue)):
            checkValue='0'+checkValue
        recvCheck=result[-4:-2]+result[-6:-4]
        if checkValue != recvCheck:
            CrcheckFlag=1
        return CrcheckFlag

    def bootready(self,bid):
        readyflag=0
        bootcount=0
        self.bootSingnal.emit(u'正在发送进入boot命令')
        messdata='59'+str(bid)+'51'+'01'+'00'+'00'
        framedata=self.messmarge(messdata)
        print(framedata.encode('hex'))
        while True:
            cboardudp.sendto(framedata,('192.168.80.201',6650))
            try:
                print('..')
                result=cboardudp.recv(1024)
                recvflag=1
            except:
                recvflag=0
                self.bootSingnal.emit(u'重新发送进入boot模式指令')
            if recvflag==1:
                print(result.encode('hex'))
                framelen=len(result)
                if framelen == 0:
                    self.bootSingnal.emit(u'重新发送进入boot模式指令')
                else:
                    #crcheckresult=self.frameCRCheck(framelen,result)
                    crcheckresult=1
                    if crcheckresult==1:
                        self.bootSingnal.emit(u'进入boot模式帧校验错误')
                    else:
                        if result[8:10]=='00':
                            self.bootSingnal.emit(u'已进入boot模式')
                            readyflag=1
                            break
                        else:
                            self.bootSingnal.emit(u'进入boot模式失败,重新发送进入boot模式')
            upflagexist=os.path.exists('log/stopflag.txt')
            if upflagexist:
                readyflag=0
                break
            bootcount+=1
            if bootcount>=100:
                readyflag=0
                break
        return readyflag

    def entrycboard(self):
        self.bootSingnal.emit(u'正在发送C板进入转发模式命令')
        messdata='59'+'EE'+'62'+'00'+'00'
        framedata=self.messmarge(messdata)
        Ygcboardev.write(framedata)

    def messmarge(self,data):
        modbus_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
        messcrc=hex(modbus_crc_func(data.decode('hex')))
        margecrc=messcrc.lstrip('0x')
        if len(margecrc)==0:
            tempcrc='0000'
        elif len(margecrc)==1:
            tempcrc='000'+margecrc
        elif len(margecrc)==2:
            tempcrc='00'+margecrc
        elif len(margecrc)==3:
            tempcrc='0'+margecrc
        else:
            tempcrc=margecrc
        finalcrc=tempcrc[2]+tempcrc[3]+tempcrc[0]+tempcrc[1]
        sendmess=(data+finalcrc+'47').decode('hex')
        self.bootSingnal.emit(sendmess.encode('hex'))
        return sendmess

    def writefirminfo(self,bid,filename):
        writeflag=0
        writecount=0
        self.bootSingnal.emit(u'开始写入固件大小和版本')
        Size = os.path.getsize(filename)
        self.bootSingnal.emit(u'固件大小:'+str(Size)+'Bytes')
        hexsize=hex(Size).lstrip('0x').rstrip('L')
        for i in range(0,8-len(hexsize)):
            hexsize='0'+hexsize
        messdata='59'+str(bid)+'52'+'06'+hexsize[6:8]+hexsize[4:6]+hexsize[2:4]+hexsize[0:2]+'0000'+'00'#缺少版本号格式
        framedata=self.messmarge(messdata)
        while True:
            cboardudp.sendto(framedata,('192.168.80.201',6650))
            try:
                result=cboardudp.recv(1024)
                recvflag=1
            except:
                self.bootSingnal.emit(u'写入固件大小和版本号失败,重新写入固件信息')
                recvflag=0
            if recvflag==1:
                framelen=len(result)
                crcheckresult=self.frameCRCheck(framelen,result)
                if crcheckresult != 1:
                    if result[8:10]=='00':
                        self.bootSingnal.emit(u'已写入固件大小和版本号')
                        writeflag=1
                        break
                    else:
                        self.bootSingnal.emit(u'写入固件大小和版本号失败,重新写入固件信息')
                else:
                    self.bootSingnal.emit(u'帧校验失败，重新写入固件和版本号信息')
            upflagexist=os.path.exists('log/stopflag.txt')
            if upflagexist:
                writeflag=0
                break
            writecount+=1
            if writecount>=10:
                writeflag=0
                break
        return writeflag

    def TransportBinToHex(self,filename):
        data=''
        datalist=[]
        f=open(filename,'rb')
        Size = os.path.getsize(filename)
        for i in f:
            data+=binascii.b2a_hex(i)
        f.close()
        length=len(data)
        for j in xrange(0,length,2):
            Ndata=data[j:j+2]
            datalist.append(Ndata)
        mainloop=int(Size/64)
        loopmu=Size%64#不够整除部分
        return Size,mainloop,loopmu,datalist

    def transfirmware(self,mainloop,loopmu,datalist,bid,size):
        upflag=0
        if loopmu == 0:#升级包大小正好是64byte整数倍
            result=self.transmain(mainloop,datalist,bid)
            if result:
                upflag=1
            else:
                upflag=0
        else:#不是64字节整数倍
            result=self.transmain(mainloop,datalist,bid)#先将整数部分传输完
            if result:
                subresult=self.transub(mainloop,datalist[size-loopmu:size],bid)
                if subresult:
                    upflag=1
                    self.barSingnal.emit(100)
        return upflag

    def transmain(self,mainloop,datalist,bid):
        transresult=1
        for loop in range(0,mainloop):
            index=hex(loop).lstrip('0x')
            for j in range(0,8-len(index)):
                index='0'+index
            result=self.dataSplit(datalist[loop*64:loop*64+64],index,loop,bid)
            bar=(loop/mainloop)*100
            self.barSingnal.emit(bar)
            if result==0:
                transresult=0
                self.bootSingnal.emit(u'数据重复发送超过10次失败,本次升级失败')
                break
        return transresult

    def dataSplit(self,data,index,loop,bid):
        transcount=0
        transflag=0
        newdata=''
        if loop>255:
            temploop=loop%256
            if temploop==0:
                seqloop='00'
            else:
                if temploop<16:
                    seqloop='0'+hex(temploop).lstrip('0x')
                else:
                    seqloop=hex(temploop).lstrip('0x')
        else:
            if loop==0:
                seqloop='00'
            else:
                if loop<16:
                    seqloop='0'+hex(loop).lstrip('0x')
                else:
                    seqloop=hex(loop).lstrip('0x')
        for line in data:
            newdata+=line
        if errindexflag:
            if index=='00000008':
                index='00000002'
        messdata='59'+str(bid)+'53'+'44'+index[6:8]+index[4:6]+index[2:4]+index[0:2]+newdata+seqloop
        framedata=self.messmarge(messdata)
        while True:
            cboardudp.sendto(framedata,('192.168.80.201',6650))
            try:
                result=cboardudp.recv(1024)
                recvflag=1
            except:
                self.bootSingnal.emit(u'数据发送失败,重新发送')
                recvflag=0
            if recvflag==1:
                framelen=len(result)
                if framelen==0:
                    self.bootSingnal.emit(u'数据发送失败,重新发送')
                else:
                    crcheckresult=self.frameCRCheck(framelen,result)
                    if crcheckresult != 1:
                        if result[-8:-6]== seqloop:
                            if result[8:10] == '00':
                                transflag=1
                                break
                            else:
                                self.bootSingnal.emit(u'数据发送失败,重新发送')
                        else:
                            self.bootSingnal.emit(u'数据帧回复帧seq段错误,重新发送')
                    else:
                        self.bootSingnal.emit(u'数据帧回复帧校验失败,重新发送')
            upflagexist=os.path.exists('log/stopflag.txt')
            if upflagexist:
                transflag=0
                break
            transcount+=1
            if transcount>=10:
                transflag=0
                break
        return transflag

    def transub(self,mainloop,data,bid):
        transflag=0
        transcount=0
        datas=''
        for line in data:
            datas+=line
        index=hex(mainloop).lstrip('0x').rstrip('L')
        for j in range(0,8-len(index)):
            index='0'+index
        datalen=hex(len(data)+4).lstrip('0x').rstrip('L')
        if len(datalen)==1:
            datalen='0'+datalen
        messdata='59'+str(bid)+'53'+datalen+index[6:8]+index[4:6]+index[2:4]+index[0:2]+datas+'00'
        framedata=self.messmarge(messdata)
        while True:
            cboardudp.sendto(framedata,('192.168.80.201',6650))
            try:
                result=cboardudp.recv(1024)
                recvflag=1
            except:
                self.bootSingnal.emit(u'数据重新发送')
                recvflag=0
            if recvflag==1:
                framelen=len(result)
                if framelen == 0:
                    self.bootSingnal.emit(u'数据重新发送')
                else:
                    crcheckresult=self.frameCRCheck(framelen,result)
                    if crcheckresult != 1:
                        if result[-8:-6]== '00':
                            if result[8:10] == '00':
                                transflag=1
                                self.bootSingnal.emit(u'数据传输已完成')
                                break
                            else:
                                self.bootSingnal.emit(u'result回复失败,数据重新发送')
                        else:
                            self.bootSingnal.emit(u'数据帧回复seq段错误,数据重新发送')
                    else:
                        self.bootSingnal.emit(u'数据帧校验失败,数据重新发送')
            upflagexist=os.path.exists('log/stopflag.txt')
            if upflagexist:
                transflag=0
                break
            transcount+=1
            if transcount>=10:
                transflag=0
                self.bootSingnal.emit(u'数据重复发送超过10次失败,本次升级失败')
                break
        return transflag

    def firmwarevalidation(self,bid):
        validationflag=0
        newmd=''
        for line in MdValue:
            newmd=newmd+line
        messdata='59'+str(bid)+'54'+'10'+newmd+'00'
        framedata=self.messmarge(messdata)
        cboardudp.sendto(framedata,('192.168.80.201',6650))
        try:
            result=cboardudp.recv(1024)
            recvflag=1
        except:
            self.bootSingnal.emit(u'固件校验失败')
            recvflag=0
        if recvflag==1:
            framelen=len(result)
            if framelen == 0:
                self.bootSingnal.emit(u'固件校验失败')
            else:
                crcheckresult=self.frameCRCheck(framelen,result)
                if crcheckresult !=1 :
                    if result[-8:-6]== '00':
                        if result[8:10] == '00':
                            self.bootSingnal.emit(u'固件校验成功')
                            validationflag=1
                        else:
                            self.bootSingnal.emit(u'固件校验失败')
                    else:
                        self.bootSingnal.emit(u'固件校验失败')
                else:
                    self.bootSingnal.emit(u'固件校验失败')
        return validationflag

    def rebootToApp(self,bid):
        rebootcount=0
        messdata='59'+str(bid)+'55'+'00'+'00'
        framedata=self.messmarge(messdata)
        while True:
            Ygcboardev.write(framedata)
            result=self.framerecv()
            framelen=len(result)
            if framelen == 0:
                 self.bootSingnal.emit(u'重新发送重启进入App指令')
            else:
                crcheckresult=self.frameCRCheck(framelen,result)
                if crcheckresult != 1:
                    if result[-8:-6]== '00':
                        if result[8:10] == '00':
                            self.bootSingnal.emit(u'重启进入App成功')
                            break
                        else:
                            self.bootSingnal.emit(u'重启进入App失败,重新发送重启进入App指令')
                    else:
                        self.bootSingnal.emit(u'回复帧seq段错误,重新发送重启进入App指令')
                else:
                    self.bootSingnal.emit(u'帧校验失败，重新发送重启进入App指令')
            upflagexist=os.path.exists('log/stopflag.txt')
            if upflagexist:
                break
            rebootcount+=1
            if rebootcount>=10:
                self.bootSingnal.emit(u'发送重启进入App指令连续超过10次，本次升级失败')
                break

class tickrecvthread(QtCore.QThread):
    startSingnal=QtCore.pyqtSignal(str)
    messSingnal=QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        result=self.framerecv()
        if result == '':
            pass
        else:
            checkFlag=self.frameCRCheck(result)
            if checkFlag ==1 :
                self.messSingnal.emit(u'tick CRC16校验错误')
            else:
                seq=result[-8:-6]
                self.startSingnal.emit(seq)

    def framerecv(self):
        result = ''
        soflag=0
        while True:
            recvHead=Ygcboardev.read()
            try:
                hexHead = ord(recvHead)
                frameHead = '%02x'%hexHead
                if frameHead == '59':
                    soflag=1
                    result+=frameHead
                    break
            except:
                self.messSingnal.emit(u'SOF段接收超时')
                break
        if soflag==1:
            recvbinbid=Ygcboardev.read()
            try:
                hexbid = ord(recvbinbid)
                recvbid = '%02x'%hexbid
                result+=recvbid
                recvbincmd=Ygcboardev.read()
                try:
                    hexcmd = ord(recvbincmd)
                    recvcmd = '%02x'%hexcmd
                    result+=recvcmd
                    recvbinlen=Ygcboardev.read()
                    try:
                        hexlen = ord(recvbinlen)
                        recvlen = '%02x'%hexlen
                        result+=recvlen
                        length=int(recvlen,16)
                        for i in range(0,length+4):
                            message=Ygcboardev.read()
                            try:
                                hvol = ord(message)
                                hhex = '%02x'%hvol
                                result += hhex
                            except:
                                self.messSingnal.emit(u'数据接收超时')
                                break
                    except:
                        self.messSingnal.emit(u'LEN接收超时')
                except:
                    self.messSingnal.emit(u'cmd接收超时')
            except:
                self.messSingnal.emit(u'bid接收超时')
        self.messSingnal.emit(result)
        return result

    def frameCRCheck(self,result):
        modbus_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
        CrcheckFlag=0
        checksum=''
        for i in range(0,len(result)-6,2):
            checksum+=result[i:i+2]
        temp=checksum.decode('hex')
        checkValue=hex(modbus_crc_func(temp)).lstrip('0x')
        for i in range(0,4-len(checkValue)):
            checkValue='0'+checkValue
        recvCheck=result[-4:-2]+result[-6:-4]
        if checkValue != recvCheck:
            CrcheckFlag=1
        return CrcheckFlag

class cutmodelthread(QtCore.QThread):
    messSingnal=QtCore.pyqtSignal(str)
    seqSingnal=QtCore.pyqtSignal(str)
    def __init__(self,Model):
        super(self.__class__, self).__init__()
        self.model=Model

    def __del__(self):
        self.wait()

    def run(self):
        self.framerecv()

    def framerecv(self):
        time.sleep(1)
        Ygcboardev.flushInput()
        while True:
            recvHead=Ygcboardev.read()
            try:
                hexHead = ord(recvHead)
                if self.model==0:
                    self.messSingnal.emit(u'系统进入转发模式失败')
                else:
                    self.messSingnal.emit(u'系统进入正常模式')
                break
            except:
                if self.model==0:
                    self.messSingnal.emit(u'系统已进入转发模式')
                else:
                    self.messSingnal.emit(u'系统进入正常模式失败')
                break

class dboardcmdthread(QtCore.QThread):
    startSingnal=QtCore.pyqtSignal(int,str)
    messSingnal=QtCore.pyqtSignal(str)
    def __init__(self, bid):
        super(self.__class__, self).__init__()
        self.device=bid

    def __del__(self):
        self.wait()

    def run(self):
        checkFlag=0
        result=self.framerecv(self.devid,self.cmd)
        if result == '':
            pass
        else:
            checkFlag=self.frameCRCheck(result)
            if checkFlag ==1 :
                self.messSingnal.emit(u'CRC16校验错误')
            else:
                seq=result[-8:-6]
                self.seqSingnal.emit(seq)

    def framerecv(self,bid,cmd):
        Ygcboardev.flushInput()
        result = ''
        soflag=0
        while True:
            recvHead=Ygcboardev.read()
            try:
                hexHead = ord(recvHead)
                frameHead = '%02x'%hexHead
                if frameHead == '59':
                    soflag=1
                    result+=frameHead
                    break
            except:
                self.messSingnal.emit(u'SOF段接收超时')
                break
        if soflag==1:
            recvbinbid=Ygcboardev.read()
            try:
                hexbid = ord(recvbinbid)
                recvbid = '%02x'%hexbid
                result+=recvbid
                if str.upper(recvbid) == bid:
                    pass
                else:
                    self.messSingnal.emit(u'tito BID对不上')
                recvbincmd=Ygcboardev.read()
                try:
                    hexcmd = ord(recvbincmd)
                    recvcmd = '%02x'%hexcmd
                    result+=recvcmd
                    if str.upper(recvcmd) == cmd:
                        pass
                    else:
                        self.messSingnal.emit(u'tito cmd对不上')
                    recvbinlen=Ygcboardev.read()
                    try:
                        hexlen = ord(recvbinlen)
                        recvlen = '%02x'%hexlen
                        result+=recvlen
                        length=int(recvlen,16)
                        for i in range(0,length+4):
                            message=Ygcboardev.read()
                            try:
                                hvol = ord(message)
                                hhex = '%02x'%hvol
                                result += hhex
                            except:
                                self.messSingnal.emit(u'数据接收超时')
                                break
                    except:
                        self.messSingnal.emit(u'LEN接收超时')
                except:
                    self.messSingnal.emit(u'cmd接收超时')
            except:
                self.messSingnal.emit(u'bid接收超时')
        self.messSingnal.emit(result)
        return result

    def frameCRCheck(self,result):
        modbus_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
        CrcheckFlag=0
        checksum=''
        for i in range(0,len(result)-6,2):
            checksum+=result[i:i+2]
        temp=checksum.decode('hex')
        checkValue=hex(modbus_crc_func(temp)).lstrip('0x')
        for i in range(0,4-len(checkValue)):
            checkValue='0'+checkValue
        recvCheck=result[-4:-2]+result[-6:-4]
        if checkValue != recvCheck:
            CrcheckFlag=1
        return CrcheckFlag

class motorthread(QtCore.QThread):
    frameSingnal=QtCore.pyqtSignal(str,int)
    messSingnal=QtCore.pyqtSignal(str)
    countSingnal=QtCore.pyqtSignal(int)
    def __init__(self,parent=None):
        super(self.__class__, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        titocount=0
        while True:
            bid,cmd,motype=self.tocksend()
            result=self.framerecv(bid,cmd)
            if result == '':
                pass
            else:
                checkFlag=self.frameCRCheck(result)
                if checkFlag ==1 :
                    self.messSingnal.emit(u'CRC16校验错误')
                else:
                    self.frameSingnal.emit(result,motype)
            titocount+=1
            if titocount>=30:
                self.countSingnal.emit(titocount)
                titocount=1
            upflagexist=os.path.exists('log/motorstop.txt')
            if upflagexist:
                break

    def tocksend(self):
        if motorwin.leftmotordial.isEnabled():
            bid='11'
            cmd='91'
            leftspeed=motorwin.leftmotorvalue.value()
            if unicode(motorwin.comboBox.currentText())== u'反向':
                temp=65535-leftspeed
                hextemp=hex(temp).lstrip('0x').rstrip('L')
                for i in range(0,4-len(hextemp)):
                    hextemp='0'+hextemp
                hexleftspeed=hextemp[0]+hextemp[1]+hextemp[2]+hextemp[3]
            else:
                hexleft=hex(leftspeed).lstrip('0x')
                for i in range(0,4-len(hexleft)):
                    hexleft='0'+hexleft
                hexleftspeed=hexleft
            if unicode(motorwin.leftstat.currentText())== u'使能':
                enable='01'
            else:
                enable='00'
            mess='59'+bid+'11'+'03'+enable+hexleftspeed[2]+hexleftspeed[3]+hexleftspeed[0]+hexleftspeed[1]+'01'
            motortype=1
        elif motorwin.rightmotordial.isEnabled():
            bid='12'
            cmd='91'
            rightspeed=motorwin.rightmotorvalue.value()

            if unicode(motorwin.comboBox_2.currentText())== u'反向':
                temp=65535-rightspeed
                hextemp=hex(temp).lstrip('0x').rstrip('L')
                for i in range(0,4-len(hextemp)):
                    hextemp='0'+hextemp
                hexrightspeed=hextemp[0]+hextemp[1]+hextemp[2]+hextemp[3]
            else:
                hexright=hex(rightspeed).lstrip('0x')
                for i in range(0,4-len(hexright)):
                    hexright='0'+hexright
                hexrightspeed=hexright
            if unicode(motorwin.rightstat.currentText())== u'使能':
                enable='01'
            else:
                enable='00'
            mess='59'+bid+'11'+'03'+enable+hexrightspeed[2]+hexrightspeed[3]+hexrightspeed[0]+hexrightspeed[1]+'01'
            motortype=2
        else:
            bid='10'
            cmd='99'
            leftspeed=motorwin.leftmotorvalue.value()
            rightspeed=motorwin.rightmotorvalue.value()

            if unicode(motorwin.comboBox.currentText())== u'反向':
                leftemp=65535-leftspeed
                hexleftemp=hex(leftemp).lstrip('0x').rstrip('L')
                for i in range(0,4-len(hexleftemp)):
                    hexleftemp='0'+hexleftemp
                hexleftspeed=hexleftemp[0]+hexleftemp[1]+hexleftemp[2]+hexleftemp[3]
            else:
                hexleft=hex(leftspeed).lstrip('0x')
                for i in range(0,4-len(hexleft)):
                    hexleft='0'+hexleft
                hexleftspeed=hexleft

            if unicode(motorwin.comboBox_2.currentText())== u'反向':
                rightemp=65535-rightspeed
                hexrightemp=hex(rightemp).lstrip('0x').rstrip('L')
                for i in range(0,4-len(hexrightemp)):
                    hexrightemp='0'+hexrightemp
                hexrightspeed=hexrightemp[0]+hexrightemp[1]+hexrightemp[2]+hexrightemp[3]
            else:
                hexright=hex(rightspeed).lstrip('0x')
                for i in range(0,4-len(hexright)):
                    hexright='0'+hexright
                hexrightspeed=hexright

            if unicode(motorwin.rightstat.currentText())== u'使能' and unicode(motorwin.leftstat.currentText())== u'使能':
                enable='11'
            elif unicode(motorwin.rightstat.currentText())== u'使能' and not unicode(motorwin.leftstat.currentText())== u'使能':
                enable='01'
            elif not unicode(motorwin.rightstat.currentText())== u'使能' and unicode(motorwin.leftstat.currentText())== u'使能':
                enable='10'
            elif not unicode(motorwin.rightstat.currentText())== u'使能' and not unicode(motorwin.leftstat.currentText())== u'使能':
                enable='00'
            else:
                enable='11'
            mess='59'+bid+'19'+enable+hexleftspeed[2]+hexleftspeed[3]+hexleftspeed[0]+hexleftspeed[1]+hexrightspeed[2]+hexrightspeed[3]+hexrightspeed[0]+hexrightspeed[1]+'01'
            motortype=3
        tocksendmess=self.messmarge(mess,1)
        Ygcboardev.write(tocksendmess)
        return bid,cmd,motortype

    def framerecv(self,bid,cmd):
        result = ''
        soflag=0
        recvflag=0
        while True:
            recvHead=Ygcboardev.read()
            try:
                hexHead = ord(recvHead)
                frameHead = '%02x'%hexHead
                if frameHead == '59':
                    soflag=1
                    result+=frameHead
                    break
            except:
                self.messSingnal.emit(u'SOF段接收超时')
                break
        if soflag==1:
            recvbinbid=Ygcboardev.read()
            try:
                hexbid = ord(recvbinbid)
                recvbid = '%02x'%hexbid
                result+=recvbid
                if str.upper(recvbid) == bid:
                    pass
                else:
                    self.messSingnal.emit(u'tito BID对不上')
                recvbincmd=Ygcboardev.read()
                try:
                    hexcmd = ord(recvbincmd)
                    recvcmd = '%02x'%hexcmd
                    result+=recvcmd
                    if str.upper(recvcmd) == cmd:
                        pass
                    else:
                        self.messSingnal.emit(u'tito cmd对不上')
                    recvbinlen=Ygcboardev.read()
                    try:
                        hexlen = ord(recvbinlen)
                        recvlen = '%02x'%hexlen
                        result+=recvlen
                        length=int(recvlen,16)
                        for i in range(0,length+4):
                            message=Ygcboardev.read()
                            try:
                                hvol = ord(message)
                                hhex = '%02x'%hvol
                                result += hhex
                            except:
                                self.messSingnal.emit(u'数据接收超时')
                                break
                    except:
                        self.messSingnal.emit(u'LEN接收超时')
                except:
                    self.messSingnal.emit(u'cmd接收超时')
            except:
                self.messSingnal.emit(u'bid接收超时')
        self.messSingnal.emit(result)
        return result

    def frameCRCheck(self,result):
        modbus_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
        CrcheckFlag=0
        checksum=''
        for i in range(0,len(result)-6,2):
            checksum+=result[i:i+2]
        temp=checksum.decode('hex')
        checkValue=hex(modbus_crc_func(temp)).lstrip('0x')
        for i in range(0,4-len(checkValue)):
            checkValue='0'+checkValue
        recvCheck=result[-4:-2]+result[-6:-4]
        if checkValue != recvCheck:
            CrcheckFlag=1
        return CrcheckFlag

    def messmarge(self,data,model):
        modbus_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
        messcrc=hex(modbus_crc_func(str(data).decode('hex')))
        if model ==1:
            sendcrc=messcrc
        else:
            sendcrc=hex(int(messcrc,16)+1)
        margecrc=sendcrc.lstrip('0x')
        if len(margecrc)==1:
            tempcrc='000'+margecrc
        elif len(margecrc)==2:
            tempcrc='00'+margecrc
        elif len(margecrc)==3:
            tempcrc='0'+margecrc
        else:
            tempcrc=margecrc

        finalcrc=tempcrc[2]+tempcrc[3]+tempcrc[0]+tempcrc[1]
        sendmess=(str(data)+finalcrc+'47').decode('hex')
        self.messSingnal.emit('command:'+sendmess.encode('hex'))
        return sendmess

class dboardthread(QtCore.QThread):
    messSingnal=QtCore.pyqtSignal(str)
    frameSingnal=QtCore.pyqtSignal(str,str)
    def __init__(self, bid,cmd):
        super(self.__class__, self).__init__()
        self.devid=bid
        self.cmd=cmd

    def __del__(self):
        self.wait()

    def run(self):
        checkFlag=0
        result=self.framerecv(self.devid,self.cmd)
        if result == '':
            pass
        else:
            checkFlag=self.frameCRCheck(result)
            if checkFlag ==1 :
                self.messSingnal.emit(u'CRC16校验错误')
            else:
                self.frameSingnal.emit(result,self.devid)

    def framerecv(self,bid,cmd):
        result = ''
        soflag=0
        while True:
            recvHead=Ygcboardev.read()
            try:
                hexHead = ord(recvHead)
                frameHead = '%02x'%hexHead
                if frameHead == '59':
                    soflag=1
                    result+=frameHead
                    break
            except:
                self.messSingnal.emit(u'SOF段接收超时')
                break
        if soflag==1:
            recvbinbid=Ygcboardev.read()
            try:
                hexbid = ord(recvbinbid)
                recvbid = '%02x'%hexbid
                result+=recvbid
                if str.upper(recvbid) == bid:
                    pass
                else:
                    self.messSingnal.emit(u'tito BID对不上')
                recvbincmd=Ygcboardev.read()
                try:
                    hexcmd = ord(recvbincmd)
                    recvcmd = '%02x'%hexcmd
                    result+=recvcmd
                    if str.upper(recvcmd) == cmd:
                        pass
                    else:
                        self.messSingnal.emit(u'tito cmd对不上')
                    recvbinlen=Ygcboardev.read()
                    try:
                        hexlen = ord(recvbinlen)
                        recvlen = '%02x'%hexlen
                        result+=recvlen
                        length=int(recvlen,16)
                        for i in range(0,length+4):
                            message=Ygcboardev.read()
                            try:
                                hvol = ord(message)
                                hhex = '%02x'%hvol
                                result += hhex
                            except:
                                self.messSingnal.emit(u'数据接收超时')
                                break
                    except:
                        self.messSingnal.emit(u'LEN接收超时')
                except:
                    self.messSingnal.emit(u'cmd接收超时')
            except:
                self.messSingnal.emit(u'bid接收超时')
        self.messSingnal.emit(result)
        return result

    def frameCRCheck(self,result):
        modbus_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
        CrcheckFlag=0
        checksum=''
        for i in range(0,len(result)-6,2):
            checksum+=result[i:i+2]
        temp=checksum.decode('hex')
        checkValue=hex(modbus_crc_func(temp)).lstrip('0x')
        for i in range(0,4-len(checkValue)):
            checkValue='0'+checkValue
        recvCheck=result[-4:-2]+result[-6:-4]
        if checkValue != recvCheck:
            CrcheckFlag=1
        return CrcheckFlag

class loopthread(QtCore.QThread):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        titowin.leftmotorvalue.setValue(20)
        titowin.rightmotorvalue.setValue(20)
        while True:
            titowin.comboBox.setCurrentIndex(0)
            titowin.comboBox_2.setCurrentIndex(0)
            if unicode(titowin.chargestat.toPlainText())==u'开启':
                titowin.comboBox.setCurrentIndex(1)
                titowin.comboBox_2.setCurrentIndex(1)
                time.sleep(5)
            titostopexist=os.path.exists('ui/titostop.txt')
            if titostopexist:
                break

class uloopthread(QtCore.QThread):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        udpwin.leftmotorvalue.setValue(100)
        udpwin.rightmotorvalue.setValue(100)
        while True:
            udpwin.comboBox.setCurrentIndex(0)
            udpwin.comboBox_2.setCurrentIndex(0)
            time.sleep(3)
            udpwin.comboBox.setCurrentIndex(1)
            udpwin.comboBox_2.setCurrentIndex(1)
            time.sleep(3)
            titostopexist=os.path.exists('ui/titostop.txt')
            if titostopexist:
                break

class boxloopthread(QtCore.QThread):
    leftmotorSingal=QtCore.pyqtSignal(int)
    rightmotorSingal=QtCore.pyqtSignal(int)
    leftmotordirSingal=QtCore.pyqtSignal(int)
    rightmotordirSingal=QtCore.pyqtSignal(int)
    leftmotorconSingal=QtCore.pyqtSignal(int)
    rightmotorconSingal=QtCore.pyqtSignal(int)
    boxcountSingnal=QtCore.pyqtSignal(int)
    boxSingal=QtCore.pyqtSignal(int,int,int)
    doorSingal=QtCore.pyqtSignal(int,int,int)
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        boxcount=int(boxwin.lcdNumber.value())
        self.leftmotorSingal.emit(100)
        self.rightmotorSingal.emit(100)
        while True:
            boxerrexist=os.path.exists('ui/boxerrflag.txt')
            if boxerrexist:
                time.sleep(2)
                os.remove('ui/boxerrflag.txt')
            #self.leftmotorconSingal.emit(0)
            #self.rightmotorconSingal.emit(0)
            self.leftmotordirSingal.emit(0)
            self.rightmotordirSingal.emit(0)
            #if unicode(boxwin.chargestat.toPlainText())==u'开启':
            if unicode(boxwin.leftswitch1.toPlainText())==u'到位':
            #if commandstat[0]==1:
                self.leftmotorSingal.emit(0)
                self.rightmotorSingal.emit(0)

                self.boxSingal.emit(1,0,0)
                time.sleep(3)

                self.doorSingal.emit(1,0,0)
                time.sleep(3)

                self.doorSingal.emit(0,0,1)
                time.sleep(3)

                self.boxSingal.emit(0,0,1)
                time.sleep(3)

                self.leftmotordirSingal.emit(1)
                self.rightmotordirSingal.emit(1)
                self.leftmotorSingal.emit(100)
                self.rightmotorSingal.emit(100)
                time.sleep(2)
                boxcount+=1
                self.boxcountSingnal.emit(boxcount)
            time.sleep(1)
            boxstopexist=os.path.exists('ui/boxstop.txt')
            if boxstopexist:
                break

class boxdebug(QtCore.QThread):
    messSingnal=QtCore.pyqtSignal(str)
    listSingnal=QtCore.pyqtSignal(list)
    errSingnal=QtCore.pyqtSignal(str)
    ultraSingal=QtCore.pyqtSignal(int)
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        #titolist=['EE','6E']
        count=0
        doorflag=0
        while True:
            result=self.framerecv()
            #print(result)
            if result == '':
                pass
            else:
                checkFlag=self.frameCRCheck(result)
                if checkFlag ==1 :
                    self.messSingnal.emit(u'CRC16校验错误')
                else:
                    seq=result[-8:-6]
                    newbid,newcmd=self.tocksend(seq,count,doorflag)
                    #titolist[0]=newbid
                    #titolist[1]=newcmd
                    messlist=self.frameMessgeanaly(result)
                    if messlist[2]!='ee':
                        self.listSingnal.emit(messlist)
            boxstopexist=os.path.exists('ui/boxstop.txt')
            if boxstopexist:
                break
            count+=1
            if count>1:
                count=0
            doorflag+=1
            if doorflag>1:
                doorflag=0

    def framerecv(self):
        result = ''
        soflag=0
        recvflag=0
        while True:
            recvHead=boxdevice.read()
            try:
                hexHead = ord(recvHead)
                frameHead = '%02x'%hexHead
                if frameHead == '59':
                    soflag=1
                    result+=frameHead
                    break
            except:
                self.messSingnal.emit(u'SOF段接收超时')
                break
        if soflag==1:
            recvbinbid=boxdevice.read()
            hexbid = ord(recvbinbid)
            recvbid = '%02x'%hexbid
            result+=recvbid
            #if str.upper(recvbid) != bid:
                #self.messSingnal.emit(u'tito BID对不上')
            recvbincmd=boxdevice.read()
            hexcmd = ord(recvbincmd)
            recvcmd = '%02x'%hexcmd
            result+=recvcmd
            #if str.upper(recvcmd) != cmd:
                #self.messSingnal.emit(u'tito cmd对不上')
            recvbinlen=boxdevice.read()
            hexlen = ord(recvbinlen)
            recvlen = '%02x'%hexlen
            result+=recvlen
            length=int(recvlen,16)
            for i in range(0,length+4):
                message=boxdevice.read()
                hvol = ord(message)
                hhex = '%02x'%hvol
                result += hhex
            self.messSingnal.emit(result)
        return result

    def frameCRCheck(self,result):
        modbus_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
        CrcheckFlag=0
        checksum=''
        for i in range(0,len(result)-6,2):
            checksum+=result[i:i+2]
        temp=checksum.decode('hex')
        checkValue=hex(modbus_crc_func(temp)).lstrip('0x')
        for i in range(0,4-len(checkValue)):
            checkValue='0'+checkValue
        recvCheck=result[-4:-2]+result[-6:-4]
        if checkValue != recvCheck:
            CrcheckFlag=1
        return CrcheckFlag

    def tocksend(self,seq,count,doorcount):
        leftspeed=boxwin.leftmotorvalue.value()
        rightspeed=boxwin.rightmotorvalue.value()
        if unicode(boxwin.comboBox.currentText())== u'反向':
            if leftspeed==0:
                hexleft='0000'
            else:
                temp=65536-leftspeed
                hextemp=hex(temp).lstrip('0x').rstrip('L')
                for i in range(0,4-len(hextemp)):
                    hextemp='0'+hextemp
                hexleft=hextemp
        else:
            hexleftspeed=hex(leftspeed).lstrip('0x')
            for i in range(0,4-len(hexleftspeed)):
                hexleftspeed='0'+hexleftspeed
            hexleft=hexleftspeed

        if unicode(boxwin.comboBox_2.currentText())== u'反向':
            if rightspeed==0:
                hexright='0000'
            else:
                temp=65536-rightspeed
                hexrightemp=hex(temp).lstrip('0x').rstrip('L')
                for i in range(0,4-len(hexrightemp)):
                    hexrightemp='0'+hexrightemp
                hexright=hexrightemp
        else:
            hexrightspeed=hex(rightspeed).lstrip('0x')
            for i in range(0,4-len(hexrightspeed)):
                hexrightspeed='0'+hexrightspeed
            hexright=hexrightspeed

        if unicode(boxwin.leftmotorcontrol.currentText())==u'使能':
            leftmotorcontrol='01'
        else:
            leftmotorcontrol='02'

        if unicode(boxwin.rightmotorcontrol.currentText())==u'使能':
            rightmotorcontrol='01'
        else:
            rightmotorcontrol='02'

        #action=self.getdoorcmd(doorcount)
        if boxwin.updooropen.isChecked():
            action='04'
        elif boxwin.updoornon.isChecked():
            action='00'
        else:
            action='01'
        doorcmd=action+'0101000000'

        tockmessage=hexleft[2]+hexleft[3]+hexleft[0]+hexleft[1]+hexright[2]+hexright[3]+hexright[0]+hexright[1]+'00'+leftmotorcontrol+rightmotorcontrol+'000000000000'+doorcmd+'00'
        leftsec,rightsec=self.duojicmdinfoget()
        leftlight='0A'
        rightlight='0A'
        if count==0:
            bid='61'
            cmd='16'
            cmdata=leftlight+leftsec
            mess='59'+bid+'96'+'17'+'14'+tockmessage+cmdata+seq
            tocksendmess=self.messmarge(mess,1)
            boxdevice.write(tocksendmess)
        #elif count==1:
        else:
            bid='62'
            cmd='16'
            cmdata=rightlight+rightsec
            mess='59'+bid+'96'+'17'+'14'+tockmessage+cmdata+seq
            tocksendmess=self.messmarge(mess,1)
            boxdevice.write(tocksendmess)
        return bid,cmd

    def duojicmdinfoget(self):
        if boxwin.groupBox_11.isEnabled():
            if boxwin.upboxnon.isChecked():
                leftduojifirvol=0
                leftduojisecvol=0
                rightduojifirvol=0
                rightduojisecvol=0
            elif boxwin.upboxopen.isChecked():
                leftduojifirvol=2
                leftduojisecvol=8
                rightduojifirvol=2
                rightduojisecvol=8
            else:
                rightduojifirvol=1
                rightduojisecvol=4
                leftduojifirvol=1
                leftduojisecvol=4
            leftsecvol=leftduojifirvol+leftduojisecvol
            if leftsecvol==0:
                hexleftsecvol='00'
            else:
                hexleftsecvol='0'+hex(leftsecvol).lstrip('0x')

            rightsecvol=rightduojifirvol+rightduojisecvol
            if rightsecvol==0:
                hexrightsecvol='00'
            else:
                hexrightsecvol='0'+hex(rightsecvol).lstrip('0x')
            return hexleftsecvol,hexrightsecvol

    def getdoorcmd(self,door):
        action='00'
        if boxwin.groupBox_12.isEnabled():
            if door==0:
                if boxwin.updoornon.isChecked():
                    action='00'
                if boxwin.updooropen.isChecked():
                    action='04'
                if boxwin.updoorclose.isChecked():
                    action='01'
            elif door==1:
                if boxwin.downdoornon.isChecked():
                    action='00'
                if boxwin.downdooropen.isChecked():
                    action='04'
                if boxwin.downdoorclose.isChecked():
                    action='01'
            else:
                pass
        return action

    def messmarge(self,data,model):
        modbus_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
        messcrc=hex(modbus_crc_func(str(data).decode('hex')))
        if model ==1:
            sendcrc=messcrc
        else:
            sendcrc=hex(int(messcrc,16)+1)
        margecrc=sendcrc.lstrip('0x')
        if len(margecrc)==0:
            tempcrc='0000'
        elif len(margecrc)==1:
            tempcrc='000'+margecrc
        elif len(margecrc)==2:
            tempcrc='00'+margecrc
        elif len(margecrc)==3:
            tempcrc='0'+margecrc
        else:
            tempcrc=margecrc

        finalcrc=tempcrc[2]+tempcrc[3]+tempcrc[0]+tempcrc[1]
        sendmess=(str(data)+finalcrc+'47').decode('hex')
        self.messSingnal.emit('tock:'+sendmess.encode('hex'))
        return sendmess

    def frameMisscheck(self,frame):
        frameId=[]
        frameMissFlag=0
        frameId.append(frame[-7:-5])
        if len(frameId)==2:
            if int(frameId[1],16)-int(frameId[0],16) == 1:
                pass
            else:
                if frameId[1] == '00' and frameId[0] == 'ff':
                    pass
                else:
                    frameMissFlag=1
        return frameMissFlag,frameId

    def frameMessgeanaly(self,frame):
        #print(frame)
        devicelist=[]
        batstat=self.batterystate(frame[118:120])
        devicelist.append(batstat)
        batval=self.batteryval(frame[120:122],frame)
        devicelist.append(batval)

        deviceid=frame[2:4]
        devicelist.append(deviceid)
        if deviceid=='61' or deviceid=='62':
            xianwei1=frame[154:156]
            devicelist.append(xianwei1)
            xianwei2=frame[156:158]
            devicelist.append(xianwei2)
        if deviceid=='25' or deviceid=='26' or deviceid=='27' or deviceid=='28':
            pass
        self.ultraSingal.emit(int(frame[90:92],16))
        return devicelist

    def batterystate(self,data):
        if data=='00':
            statecode=u'关闭'
        elif data=='01':
            statecode=u'开启'
        elif data=='02':
            statecode=u'过压保护'
        elif data=='03':
            statecode=u'过流保护'
        elif data=='04':
            statecode=u'电池充满'
        elif data=='05':
            statecode=u'总压过压'
        elif data=='05':
            statecode=u'总压过压'
        elif data=='06':
            statecode=u'电池过温'
        elif data=='07':
            statecode=u'功率过温'
        elif data=='08':
            statecode=u'电池异常'
        elif data=='09':
            statecode=u'均衡线掉串'
        elif data=='0A':
            statecode=u'主板过温'
        elif data=='0D':
            statecode=u'放电管异常'
        elif data=='0F':
            statecode=u'手动关闭'
        else:
            statecode=u'非法值'+data
        return statecode

    def batteryval(self,data,frame):
        battery=0
        try:
            battery=int(data,16)
        except:
            self.errSingnal.emit(frame)
        return battery

class udpthread(QtCore.QThread):

    messSingnal=QtCore.pyqtSignal(str)
    listSingnal=QtCore.pyqtSignal(list)
    titocountSingnal=QtCore.pyqtSignal(int)
    errSingnal=QtCore.pyqtSignal(str)
    def __init__(self, model):
        super(self.__class__, self).__init__()
        self.runflag=model

    def __del__(self):
        self.wait()

    def run(self):
        udpclient=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpclient.settimeout(1)
        while True:
            if self.runflag==0:
                data='hello'
                #print(data)
            else:
                data=self.tocksend()
                #print(data.encode('hex'))
            udpclient.sendto(data,('192.168.80.201',6650))
            #udpclient.sendto(data,('10.42.5.9',6650))
            try:
                message=udpclient.recv(1024)
                flag=1
            except:
                self.messSingnal.emit(u'网络连接中断')
                flag=0
            if flag==1:
                if message=='':
                    pass
                else:
                    result=''
                    for data in message:
                        hexHead = ord(data)
                        frameHead = '%02x'%hexHead
                        result+=frameHead
                    #print(result)
                    checkFlag=self.frameCRCheck(result)
                    if checkFlag ==1 :
                        self.messSingnal.emit(u'CRC16校验错误')
                    else:
                        messlist=self.frameMessgeanaly(result)
                        self.listSingnal.emit(messlist)
            else:
                pass
            udptitostopexist=os.path.exists('ui/udpstop.txt')
            if udptitostopexist:
                break

    def frameCRCheck(self,result):
        modbus_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
        CrcheckFlag=0
        checksum=''
        for i in range(0,len(result)-6,2):
            checksum+=result[i:i+2]
        temp=checksum.decode('hex')
        checkValue=hex(modbus_crc_func(temp)).lstrip('0x')
        for i in range(0,4-len(checkValue)):
            checkValue='0'+checkValue
        recvCheck=result[-4:-2]+result[-6:-4]
        if checkValue != recvCheck:
            CrcheckFlag=1
        return CrcheckFlag

    def tocksend(self):
        leftspeed=udpwin.leftmotorvalue.value()
        rightspeed=udpwin.rightmotorvalue.value()
        if unicode(udpwin.comboBox.currentText())== u'反向':
            if leftspeed==0:
                hexleft='0000'
            else:
                temp=65536-leftspeed
                hextemp=hex(temp).lstrip('0x').rstrip('L')
                for i in range(0,4-len(hextemp)):
                    hextemp='0'+hextemp
                hexleft=hextemp
        else:
            hexleftspeed=hex(leftspeed).lstrip('0x')
            for i in range(0,4-len(hexleftspeed)):
                hexleftspeed='0'+hexleftspeed
            hexleft=hexleftspeed

        if unicode(udpwin.comboBox_2.currentText())== u'反向':
            if rightspeed==0:
                hexright='0000'
            else:
                temp=65536-rightspeed
                hexrightemp=hex(temp).lstrip('0x').rstrip('L')
                for i in range(0,4-len(hexrightemp)):
                    hexrightemp='0'+hexrightemp
                hexright=hexrightemp
        else:
            hexrightspeed=hex(rightspeed).lstrip('0x')
            for i in range(0,4-len(hexrightspeed)):
                hexrightspeed='0'+hexrightspeed
            hexright=hexrightspeed

        if unicode(udpwin.leftmotorcontrol.currentText())==u'使能' and unicode(udpwin.rightmotorcontrol.currentText())==u'使能':
            motorcontrol='11'
        elif unicode(udpwin.leftmotorcontrol.currentText())==u'使能' and unicode(udpwin.rightmotorcontrol.currentText())==u'释放':
            motorcontrol='01'
        elif unicode(udpwin.leftmotorcontrol.currentText())==u'释放' and unicode(udpwin.rightmotorcontrol.currentText())==u'使能':
            motorcontrol='10'
        else:
            motorcontrol='00'

        doorcmd=self.getdoorcmd()
        motorcmd=hexleft[2]+hexleft[3]+hexleft[0]+hexleft[1]+hexright[2]+hexright[3]+hexright[0]+hexright[1]

        duojicmd=self.duojicmdinfoget()
        lightcmd=self.lightinfoget()

        tockmessage=motorcmd+motorcontrol+'0000'+doorcmd+duojicmd+lightcmd+'000000000000'
        mess='59'+'ee'+'ee'+'11'+'10'+tockmessage+'00'
        tocksendmess=self.messmarge(mess,1)
        #print(tocksendmess.encode('hex'))
        return tocksendmess

    def lightinfoget(self):
        action='00'
        if udpwin.groupBox_11.isEnabled():
            if udpwin.leftlight1open.isChecked():
                leftlightfirvol=1
            else:
                leftlightfirvol=0

            if udpwin.leftlight2open.isChecked():
                leftlightsecvol=4
            else:
                leftlightsecvol=0

            if udpwin.rightlight1open.isChecked():
                rightlightfirvol=2
            else:
                rightlightfirvol=0

            if udpwin.rightlight2open.isChecked():
                rightlightsecvol=8
            else:
                rightlightsecvol=0
            temp=hex(leftlightfirvol+rightlightfirvol+leftlightsecvol+rightlightsecvol).lstrip('0x')
            if temp=='':
                temp='00'
            if len(temp)==1:
                action='0'+temp
            else:
                action=temp
        return action

    def duojicmdinfoget(self):
        action='00'
        if udpwin.groupBox_11.isEnabled():
            if udpwin.leftduoji1open.isChecked():
                leftduojifirvol=1
            else:
                leftduojifirvol=0

            if udpwin.leftduoji2open.isChecked():
                leftduojisecvol=4
            else:
                leftduojisecvol=0

            if udpwin.rightduoji1open.isChecked():
                rightduojifirvol=2
            else:
                rightduojifirvol=0

            if udpwin.rightduoji2open.isChecked():
                rightduojisecvol=8
            else:
                rightduojisecvol=0
            temp=hex(leftduojifirvol+rightduojifirvol+leftduojisecvol+rightduojisecvol).lstrip('0x')
            if temp=='':
                temp='00'
            if len(temp)==1:
                action='0'+temp
            else:
                action=temp
        return action

    def getdoorcmd(self):
        action='00'
        if udpwin.groupBox_12.isEnabled():
            if udpwin.leftdupdooropen.isChecked():
                leftupaction=1
            else:
                leftupaction=0

            if udpwin.rightupdooropen.isChecked():
                rightupaction=2
            else:
                rightupaction=0

            if udpwin.leftdowndooropen.isChecked():
                leftdownaction=4
            else:
                leftdownaction=0

            if udpwin.rightdowndooropen.isChecked():
                rightdownaction=8
            else:
                rightdownaction=0
            temp=hex(leftupaction+rightupaction+leftdownaction+rightdownaction).lstrip('0x')
            if temp=='':
                temp='00'
            if len(temp)==1:
                action='0'+temp
            else:
                action=temp
        return action

    def messmarge(self,data,model):
        modbus_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
        messcrc=hex(modbus_crc_func(str(data).decode('hex')))
        if model ==1:
            sendcrc=messcrc
        else:
            sendcrc=hex(int(messcrc,16)+1)
        margecrc=sendcrc.lstrip('0x')
        if len(margecrc)==1:
            tempcrc='000'+margecrc
        elif len(margecrc)==2:
            tempcrc='00'+margecrc
        elif len(margecrc)==3:
            tempcrc='0'+margecrc
        else:
            tempcrc=margecrc

        finalcrc=tempcrc[2]+tempcrc[3]+tempcrc[0]+tempcrc[1]
        sendmess=(str(data)+finalcrc+'47').decode('hex')
        #self.messSingnal.emit('tock:'+sendmess.encode('hex'))
        return sendmess

    def frameMessgeanaly(self,frame):
        devicelist=[]
        warrcode=self.warringcode(frame[10:12])
        devicelist.append(warrcode)
        errcode=self.errcodeany(frame[12:14])
        devicelist.append(errcode)

        Inchingstat=self.Inchingstatget(frame[14:16])
        devicelist.append(Inchingstat)
        leftmotorstat,rightmotorstat=self.motorstatget(frame[16:18])
        devicelist.append(leftmotorstat)
        devicelist.append(rightmotorstat)
        motorposl=self.motor_pos_left(frame[18:22],frame)
        devicelist.append(motorposl)
        motorspeedl=self.motor_speed_left(frame[22:26],frame)
        devicelist.append(motorspeedl)
        motorposr=self.motor_pos_right(frame[26:30],frame)
        devicelist.append(motorposr)
        motorspeedr=self.motor_speed_right(frame[30:34],frame)
        devicelist.append(motorspeedr)

        IMUaccX=self.IMUaccXget(frame[38:42],frame)
        devicelist.append(IMUaccX)
        IMUaccY=self.IMUaccYget(frame[42:46],frame)
        devicelist.append(IMUaccY)
        IMUaccZ=self.IMUaccZget(frame[46:50],frame)
        devicelist.append(IMUaccZ)
        IMUcmpX=self.IMUcmpXget(frame[50:54],frame)
        devicelist.append(IMUcmpX)
        IMUcmpY=self.IMUcmpYget(frame[54:58],frame)
        devicelist.append(IMUcmpY)
        IMUcmpZ=self.IMUcmpZget(frame[58:62],frame)
        devicelist.append(IMUcmpZ)
        IMUpitch=self.IMUpitchget(frame[62:66],frame)
        devicelist.append(IMUpitch)
        IMURoll=self.IMURollget(frame[66:70],frame)
        devicelist.append(IMURoll)
        IMUYaw=self.IMUYawget(frame[70:74],frame)
        devicelist.append(IMUYaw)

        fallingresult=self.falling_dete(frame[74:76])
        devicelist.append(fallingresult)
        #self.outdoorstat(frame[76:78])
        leftupdoor,leftdowndoor,rightupdoor,rightdowndoor=self.cabinedoorstat(frame[78:80])
        devicelist.append(leftupdoor)
        devicelist.append(leftdowndoor)
        devicelist.append(rightupdoor)
        devicelist.append(rightdowndoor)
        luplock,ldownlock,ruplock,rdownlock,upbox,downbox=self.cabinelockstat(frame[80:82])
        devicelist.append(luplock)
        devicelist.append(ldownlock)
        devicelist.append(ruplock)
        devicelist.append(rdownlock)
        devicelist.append(upbox)
        devicelist.append(downbox)
        batstat=self.batterystate(frame[82:84])
        devicelist.append(batstat)
        batval=self.batteryval(frame[84:86],frame)
        devicelist.append(batval)

        ultrasoundfir=self.ultrasoundget(frame[90:92],frame)
        devicelist.append(ultrasoundfir)
        ultrasoundsec=self.ultrasoundget(frame[92:94],frame)
        devicelist.append(ultrasoundsec)
        ultrasoundthr=self.ultrasoundget(frame[94:96],frame)
        devicelist.append(ultrasoundthr)
        ultrasoundfou=self.ultrasoundget(frame[96:98],frame)
        devicelist.append(ultrasoundfou)
        ultrasoundfiv=self.ultrasoundget(frame[98:100],frame)
        devicelist.append(ultrasoundfiv)
        ultrasoundsix=self.ultrasoundget(frame[100:102],frame)
        devicelist.append(ultrasoundsix)

        infraredfir=self.infraredget(frame[102:104],frame)
        devicelist.append(infraredfir)
        infraredsec=self.infraredget(frame[104:106],frame)
        devicelist.append(infraredsec)
        infraredthr=self.infraredget(frame[106:108],frame)
        devicelist.append(infraredthr)
        infraredfou=self.infraredget(frame[108:110],frame)
        devicelist.append(infraredfou)
        infraredfiv=self.infraredget(frame[110:112],frame)
        devicelist.append(infraredfiv)
        infraredsix=self.infraredget(frame[112:114],frame)
        devicelist.append(infraredsix)
        infraredsev=self.infraredget(frame[114:116],frame)
        devicelist.append(infraredsev)
        infraredeig=self.infraredget(frame[116:118],frame)
        devicelist.append(infraredeig)
        infrarednig=self.infraredget(frame[118:120],frame)
        devicelist.append(infrarednig)
        infraredten=self.infraredget(frame[120:122],frame)
        devicelist.append(infraredten)

        leftup,rightup,leftdown,rightdown,totalup,totaldown=self.weiany(frame)
        devicelist.append(leftup)
        devicelist.append(rightup)
        devicelist.append(leftdown)
        devicelist.append(rightdown)
        devicelist.append(totalup)
        devicelist.append(totaldown)

        return devicelist

    def warringcode(self,code):
        if code == '01':
            warrtype=u'丢包过多'
        elif code == '02':
            warrtype=u'重启过'
        elif code =='04':
            warrtype=u'CPU温度过高'
        elif code == '03':
            warrtype=u'丢包过多,重启过'
        elif code == '05':
            warrtype=u'丢包过多,CPU温度过高'
        elif code == '06':
            warrtype=u'CPU温度过高,重启过'
        elif code == '07':
            warrtype=u'丢包过多,CPU温度过高,重启过'
        else:
            warrtype=u'正常'
        return warrtype

    def errcodeany(self,code):
        if code != '00':
            errtype=u'设备故障'
        else:
            errtype=u'正常'
        return errtype

    def motor_pos_left(self,data,frame):
        try:
            tempdata=int(data[2]+data[3]+data[0]+data[1],16)
        except:
            self.errSingnal.emit(frame)
            tempdata='0000'
        return tempdata

    def motor_pos_right(self,data,frame):
        try:
            tempdata=int(data[2]+data[3]+data[0]+data[1],16)
        except:
            self.errSingnal.emit(frame)
            tempdata='0000'
        return tempdata

    def motor_speed_left(self,data,frame):
        finaldata=0
        try:
            temp=data[2]+data[3]+data[0]+data[1]
            speed=int(temp,16)
            if speed>32768:
                speed=65536-speed
                finaldata='-'+str(speed)
            else:
                finaldata=speed
        except:
            self.errSingnal.emit(frame)
        return finaldata

    def motor_speed_right(self,data,frame):
        finaldata=0
        try:
            temp=data[2]+data[3]+data[0]+data[1]
            speed=int(temp,16)
            if speed>32768:
                speed=65536-speed
                finaldata='-'+str(speed)
            else:
                finaldata=speed
        except:
            self.errSingnal.emit(frame)
        return finaldata

    def IMUaccXget(self,data,frame):
        finaldata=0
        try:
            temp=data[2]+data[3]+data[0]+data[1]
            tempdata=int(temp,16)
            if tempdata>32768:
                tempdata=65536-tempdata
                finaldata='-'+str(tempdata)
            else:
                finaldata=tempdata
        except:
            self.errSingnal.emit(frame)
        return finaldata

    def IMUaccYget(self,data,frame):
        finaldata=0
        try:
            temp=data[2]+data[3]+data[0]+data[1]
            tempdata=int(temp,16)
            if tempdata>32768:
                tempdata=65536-tempdata
                finaldata='-'+str(tempdata)
            else:
                finaldata=tempdata
        except:
            self.errSingnal.emit(frame)
        return finaldata

    def IMUaccZget(self,data,frame):
        finaldata=0
        try:
            temp=data[2]+data[3]+data[0]+data[1]
            tempdata=int(temp,16)
            if tempdata>32768:
                tempdata=65536-tempdata
                finaldata='-'+str(tempdata)
            else:
                finaldata=tempdata
        except:
            self.errSingnal.emit(frame)
        return finaldata

    def IMUgropXget(self,data,frame):
        finaldata=0
        try:
            temp=data[2]+data[3]+data[0]+data[1]
            tempdata=int(temp,16)
            if tempdata>32768:
                tempdata=65536-tempdata
                finaldata='-'+str(tempdata)
            else:
                finaldata=tempdata
        except:
            self.errSingnal.emit(frame)
        return finaldata

    def IMUgropYget(self,data,frame):
        finaldata=0
        try:
            temp=data[2]+data[3]+data[0]+data[1]
            tempdata=int(temp,16)
            if tempdata>32768:
                tempdata=65536-tempdata
                finaldata='-'+str(tempdata)
            else:
                finaldata=tempdata
        except:
            self.errSingnal.emit(frame)
        return finaldata

    def IMUgropZget(self,data,frame):
        finaldata=0
        try:
            temp=data[2]+data[3]+data[0]+data[1]
            tempdata=int(temp,16)
            if tempdata>32768:
                tempdata=65536-tempdata
                finaldata='-'+str(tempdata)
            else:
                finaldata=tempdata
        except:
            self.errSingnal.emit(frame)
        return finaldata

    def IMUcmpXget(self,data,frame):
        finaldata=0
        try:
            temp=data[2]+data[3]+data[0]+data[1]
            tempdata=int(temp,16)
            if tempdata>32768:
                tempdata=65536-tempdata
                finaldata='-'+str(tempdata)
            else:
                finaldata=tempdata
        except:
            self.errSingnal.emit(frame)
        return finaldata

    def IMUcmpYget(self,data,frame):
        finaldata=0
        try:
            temp=data[2]+data[3]+data[0]+data[1]
            tempdata=int(temp,16)
            if tempdata>32768:
                tempdata=65536-tempdata
                finaldata='-'+str(tempdata)
            else:
                finaldata=tempdata
        except:
            self.errSingnal.emit(frame)
        return finaldata

    def IMUcmpZget(self,data,frame):
        finaldata=0
        try:
            temp=data[2]+data[3]+data[0]+data[1]
            tempdata=int(temp,16)
            if tempdata>32768:
                tempdata=65536-tempdata
                finaldata='-'+str(tempdata)
            else:
                finaldata=tempdata
        except:
            self.errSingnal.emit(frame)
        return finaldata

    def IMUpitchget(self,data,frame):
        finaldata=0
        try:
            temp=data[2]+data[3]+data[0]+data[1]
            tempdata=int(temp,16)
            if tempdata>32768:
                tempdata=float((65536-tempdata)*0.01)
                finaldata='-'+str(tempdata)
            else:
                finaldata=str(float(tempdata*0.01))
        except:
            self.errSingnal.emit(frame)
        return finaldata

    def IMURollget(self,data,frame):
        finaldata=0
        try:
            temp=data[2]+data[3]+data[0]+data[1]
            tempdata=int(temp,16)
            if tempdata>32768:
                tempdata=float((65536-tempdata)*0.01)
                finaldata='-'+str(tempdata)
            else:
                finaldata=str(float(tempdata*0.01))
        except:
            self.errSingnal.emit(frame)
        return finaldata

    def IMUYawget(self,data,frame):
        finaldata=0
        try:
            temp=data[2]+data[3]+data[0]+data[1]
            tempdata=int(temp,16)
            if tempdata>32768:
                tempdata=float((65536-tempdata)*0.01)
                finaldata='-'+str(tempdata)
            else:
                finaldata=str(float(tempdata*0.01))
        except:
            self.errSingnal.emit(frame)
        return finaldata

    def ultrasoundget(self,data,frame):
        dis=0
        try:
            dis=int(data,16)
        except:
            self.errSingnal.emit(frame)
        return str(dis)

    def infraredget(self,data,frame):
        dis=0
        try:
            dis=int(data,16)
        except:
            self.errSingnal.emit(frame)
        return str(dis)

    def batterystate(self,data):
        if data=='00':
            statecode=u'未知状态'
        elif data=='01':
            statecode=u'正常放电'
        elif data=='02':
            statecode=u'正在充电'
        elif data=='03':
            statecode=u'充满电'
        elif data=='ff':
            statecode=u'异常状态'
        else:
            statecode=u'非法值'+data
        return statecode

    def batteryval(self,data,frame):
        battery=0
        try:
            battery=int(data,16)
        except:
            self.errSingnal.emit(frame)
        return battery

    def Inchingstatget(self,data):
        if data=='01':
            inchstat=u'右侧'
        elif data=='02':
            inchstat=u'中间'
        elif data=='03':
            inchstat=u'右侧,中间'
        elif data=='04':
            inchstat=u'左侧'
        elif data=='05':
            inchstat=u'左,右'
        elif data=='06':
            inchstat=u'左侧,中间'
        elif data=='07':
            inchstat=u'左中右'
        else:
            inchstat=u'无碰撞'
        return inchstat

    def falling_dete(self,data):
        if data=='01' or data=='00':
            fallstat=u'正常'
        else:
            fallstat=u'跌落'
        return fallstat

    def outdoorstat(self,data):
        if data=='00':
            doorstat=u'未知'
        elif data=='01':
            doorstat=u'关闭'
        elif data=='02':
            doorstat=u'已开'
        elif data=='03':
            doorstat=u'正在关'
        elif data=='04':
            doorstat=u'正在开'
        elif data=='f0':
            doorstat=u'异常'
        else:
            doorstat=u'非法值'
        return doorstat

    def cabinedoorstat(self,data):
        try:
            temp=int(data,16)
        except:
            temp=0
        if temp==0:
            leftup=u'打开'
            leftdown=u'打开'
            rightup=u'打开'
            rightdown=u'打开'
        else:
            if temp&1==1:
                leftup=u'中间'
            if temp&2==2:
                leftup=u'关闭'
            if temp&1!=1 and temp&2!=2:
                leftup=u'打开'

            if temp&4==4:
                rightup=u'中间'
            if temp&8==8:
                rightup=u'关闭'
            if temp&4!=4 and temp&8!=8:
                rightup=u'打开'

            if temp&16==16:
                leftdown=u'中间'
            if temp&32==32:
                leftdown=u'关闭'
            if temp&16!=16 and temp&32!=32:
                leftdown=u'打开'

            if temp&64==64:
                rightdown=u'中间'
            if temp&128==128:
                rightdown=u'关闭'
            if temp&64!=64 and temp&128!=128:
                rightdown=u'打开'

        return leftup,leftdown,rightup,rightdown

    def cabinelockstat(self,data):
        temp=int(data,16)
        if temp&64==64:
            upbox=u'到位'
        else:
            upbox=u'未到位'
        if temp&128==128:
            downbox=u'到位'
        else:
            downbox=u'未到位'
        if temp&1==1:
            leftup=u'锁定'
        else:
            leftup=u'未锁'
        if temp&4==4:
            leftdown=u'锁定'
        else:
            leftdown=u'未锁'
        if temp&2==2:
            rightup=u'锁定'
        else:
            rightup=u'未锁'
        if temp&8==8:
            rightdown=u'锁定'
        else:
            rightdown=u'未锁'

        return leftup,leftdown,rightup,rightdown,upbox,downbox

    def workmode(self,data):
        return data

    def motorstatget(self,data):
        if data=='00':
            leftmotor=u'释放'
            rightmotor=u'释放'
        elif data=='01':
            leftmotor=u'使能'
            rightmotor=u'释放'
        elif data=='10':
            leftmotor=u'释放'
            rightmotor=u'使能'
        else:
            leftmotor=u'使能'
            rightmotor=u'使能'
        return leftmotor,rightmotor

    def dboardstatget(self,data):
        return data

    def weiany(self,frame):
        temp1=int((frame[132]+frame[133]+frame[130]+frame[131]),16)
        temp2=int((frame[136]+frame[137]+frame[134]+frame[135]),16)
        temp3=int((frame[140]+frame[141]+frame[138]+frame[139]),16)
        temp4=int((frame[144]+frame[145]+frame[142]+frame[143]),16)
        if temp1>32767:
            tempdata=65536-temp1
            leftup='-'+str(tempdata)
        else:
            leftup=str(temp1)

        if temp2>32767:
            tempdata=65536-temp2
            rightup='-'+str(tempdata)
        else:
            rightup=str(temp2)

        if temp1>32767 and temp2>32767:
            totaltemp=(65536-temp1)+(65536-temp2)
            totalup='-'+str(totaltemp)
        elif temp1>32767 and temp2<32767:
            if (65536-temp1)>temp2:
                totaltemp=65536-temp1-temp2
                totalup='-'+str(totaltemp)
            else:
                totaltemp=temp2-(65536-temp1)
                totalup=str(totaltemp)
        elif temp1<32767 and temp2>32767:
            if (65536-temp2)>temp1:
                totaltemp=(65536-temp2)-temp1
                totalup='-'+str(totaltemp)
            else:
                totaltemp=temp1-(65536-temp2)
                totalup=str(totaltemp)
        else:
            totaltemp=temp1+temp2
            totalup=str(totaltemp)

        if temp3>32767:
            tempdata=65536-temp3
            leftdown='-'+str(tempdata)
        else:
            leftdown=str(temp3)

        if temp4>32767:
            tempdata=65536-temp4
            rightdown='-'+str(tempdata)
        else:
            rightdown=str(temp4)

        if temp3>32767 and temp4>32767:
            totaltemp=(65536-temp1)+(65536-temp2)
            totaldown='-'+str(totaltemp)
        elif temp3>32767 and temp4<32767:
            if (65536-temp3)>temp4:
                totaltemp=65536-temp3-temp4
                totaldown='-'+str(totaltemp)
            else:
                totaltemp=temp4-(65536-temp3)
                totaldown=str(totaltemp)
        elif temp3<32767 and temp4>32767:
            if (65536-temp4)>temp3:
                totaltemp=(65536-temp4)-temp3
                totaldown='-'+str(totaltemp)
            else:
                totaltemp=temp3-(65536-temp4)
                totaldown=str(totaltemp)
        else:
            totaltemp=temp3+temp4
            totaldown=str(totaltemp)

        #totalup=int(leftup.lstrip('-'))+int(rightup.lstrip('-'))
        #totaldown=int(leftdown.lstrip('-'))+int(rightdown.lstrip('-'))

        if totalup[0]=='-':
            total=str((int(str(totalup).lstrip('-')))*0.38)
        else:
            total='-'+str((int(str(totalup).lstrip('-')))*0.38)

        if totaldown[0]=='-':
            downtotal=str((int(str(totaldown).lstrip('-')))*0.38)
        else:
            downtotal='-'+str((int(str(totaldown).lstrip('-')))*0.38)

        return leftup,rightup,leftdown,rightdown,total,downtotal

class ultrathread(QtCore.QThread):
    messSingnal=QtCore.pyqtSignal(str)
    listSingnal=QtCore.pyqtSignal(list)
    titocountSingnal=QtCore.pyqtSignal(int)
    errSingnal=QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        dis1=titowin.urat1.toPlainText()
        dis2=titowin.urat2.toPlainText()
        dis3=titowin.urat3.toPlainText()
        dis4=titowin.urat4.toPlainText()

        dis5=titowin.urat5.toPlainText()
        dis6=titowin.urat6.toPlainText()

        inf1=titowin.irf1.toPlainText()
        inf2=titowin.irf2.toPlainText()
        inf3=titowin.irf3.toPlainText()
        inf4=titowin.irf4.toPlainText()
        inf5=titowin.irf5.toPlainText()
        inf6=titowin.irf6.toPlainText()
        inf7=titowin.irf7.toPlainText()
        inf8=titowin.irf8.toPlainText()
        inf9=titowin.irf9.toPlainText()
        infa=titowin.irfA.toPlainText()

        temp=str(titowin.pianhang.toPlainText())
        try:
            if temp[0]=='-':
                currentraw=360-float(temp.lstrip('-'))
            else:
                currentraw=float(temp)
            if currentraw>initraw:
                chazhi=currentraw-initraw
            else:
                chazhi=initraw-currentraw
            fontmargeline=dis1+' '+dis2+' '+dis3+' '+dis4
            backline=dis5+' '+dis6
            infline=inf1+' '+inf2+' '+inf3+' '+inf4+' '+inf5+' '+inf6+' '+inf7+' '+inf8+' '+inf9+' '+infa

            f_w=open('ui/fultra.txt','a')
            f_w.write(fontmargeline+' YAW:'+str(chazhi)+'\n')
            f_w.close()

            f_w=open('ui/bultra.txt','a')
            f_w.write(backline+' YAW:'+str(chazhi)+'\n')
            f_w.close()

            f_w=open('ui/inf.txt','a')
            f_w.write(infline+' YAW:'+str(chazhi)+'\n')
            f_w.close()
        except:
            pass

class speedthread(QtCore.QThread):
    messSingnal=QtCore.pyqtSignal(int)
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        currentspeed=titowin.leftmotorvalue.value()
        #currentrightspeed=titowin.rightmotorvalue.value()
        currentspeed+=5
        if currentspeed>=25:
            currentspeed=0
        #else:
            #speed=currentspeed
        self.messSingnal.emit(currentspeed)

class Udsthread(QtCore.QThread):

    messSingnal=QtCore.pyqtSignal(str)
    listSingnal=QtCore.pyqtSignal(list)
    def __init__(self, ip):
        super(self.__class__, self).__init__()
        self.address=ip

    def __del__(self):
        self.wait()

    def run(self):
        udpclient=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpclient.settimeout(1)
        bidflag=0
        seq=0
        while True:
            if seq==0:
                hexseq='00'
            else:
                if seq<=15:
                    hexseq='0'+hex(seq).lstrip('0x')
                else:
                    hexseq=hex(seq).lstrip('0x')
            self.tocksend(hexseq,bidflag,udpclient)
            tempresult=self.framerecv(udpclient)
            result=tempresult.encode('hex')
            if result == '':
                pass
            else:
                checkFlag=self.frameCRCheck(result)
                if checkFlag ==1 :
                    self.messSingnal.emit(u'CRC16校验错误')
                else:
                    messlist=self.frameMessgeanaly(result)
                    self.listSingnal.emit(messlist)
            bidflag+=1
            if bidflag>19:
                bidflag=0
            seq+=1
            if seq>=256:
                seq=0
            #titostopexist=os.path.exists('ui/titostop.txt')
            #if titostopexist:
                #break

    def framerecv(self,client):
        try:
            result=client.recv(1024)
        except:
            result=''
        return result

    def frameCRCheck(self,result):
        modbus_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
        CrcheckFlag=0
        checksum=''
        for i in range(0,len(result)-6,2):
            checksum+=result[i:i+2]
        temp=checksum.decode('hex')
        checkValue=hex(modbus_crc_func(temp)).lstrip('0x')
        for i in range(0,4-len(checkValue)):
            checkValue='0'+checkValue
        recvCheck=result[-4:-2]+result[-6:-4]
        if checkValue != recvCheck:
            CrcheckFlag=1
        return CrcheckFlag

    def tocksend(self,seq,flag,udpclient):
        tockmessage='00000000'+'11'+'0000'+'00'+'0F'+'0F'+'000000000000'
        if flag==0:
            bid='ee'
        elif flag==1:
            bid='11'
        elif flag==2:
            bid='12'
        elif flag==3:
            bid='61'
        elif flag==4:
            bid='62'
        elif flag==5:
            bid='51'
        elif flag==6:
            bid='52'
        elif flag==7:
            bid='53'
        elif flag==8:
            bid='54'
        elif flag==9:
            bid='55'
        elif flag==10:
            bid='56'
        elif flag==11:
            bid='57'
        elif flag==12:
            bid='58'
        elif flag==13:
            bid='59'
        elif flag==14:
            bid='5A'
        elif flag==15:
            bid='25'
        elif flag==16:
            bid='26'
        elif flag==17:
            bid='27'
        elif flag==18:
            bid='28'
        elif flag==19:
            bid='e1'
        else:
            bid='ee'
        mess='59'+bid+'80'+'13'+'10'+tockmessage+'3D01'+seq
        #print(mess)
        tocksendmess=self.messmarge(mess,1)
        #udpclient.sendto(tocksendmess,(self.address,6650))
        udpclient.sendto(tocksendmess,('192.168.80.201',6650))

    def messmarge(self,data,model):
        modbus_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
        messcrc=hex(modbus_crc_func(str(data).decode('hex')))
        if model ==1:
            sendcrc=messcrc
        else:
            sendcrc=hex(int(messcrc,16)+1)
        margecrc=sendcrc.lstrip('0x')
        if len(margecrc)==1:
            tempcrc='000'+margecrc
        elif len(margecrc)==2:
            tempcrc='00'+margecrc
        elif len(margecrc)==3:
            tempcrc='0'+margecrc
        else:
            tempcrc=margecrc

        finalcrc=tempcrc[2]+tempcrc[3]+tempcrc[0]+tempcrc[1]
        sendmess=(str(data)+finalcrc+'47').decode('hex')
        self.messSingnal.emit('tock:'+sendmess.encode('hex'))
        return sendmess

    def frameMessgeanaly(self,frame):
        #print(frame)
        devicelist=[]
        Inchingstat=self.Inchingstatget(frame[14:16])
        devicelist.append(Inchingstat)
        fallingresult=self.falling_dete(frame[74:76])
        devicelist.append(fallingresult)
        batstat=self.batterystate(frame[82:84])
        devicelist.append(batstat)
        batval=self.batteryval(frame[84:86],frame)
        devicelist.append(batval)

        bid=frame[2:4]
        devicelist.append(bid)

        errcode=self.errcodeany(frame[-10:-8],frame[2:4])
        devicelist.append(errcode)
        return devicelist

    def errcodeany(self,code,bid):
        if bid=='ee':
            if code=='00':
                errcode=u'正常'
            elif code=='01':
                errcode=u'左轮毂电机连接不上'
            elif code=='02':
                errcode=u'右轮毂电机连接不上'
            elif code=='03':
                errcode=u'直流电机1连接不'
            elif code=='04':
                errcode=u'直流电机2连接不上'
            elif code=='05':
                errcode=u'直流电机3连接不上'
            elif code=='06':
                errcode=u'直流电机4连接不上'
            elif code=='07':
                errcode=u'超声波1连接不上'
            elif code=='08':
                errcode=u'超声波2连接不上'
            elif code=='09':
                errcode=u'超声波3连接不上'
            elif code=='0a':
                errcode=u'超声波4连接不上'
            elif code=='0b':
                errcode=u'超声波5连接不上'
            elif code=='0c':
                errcode=u'超声波6连接不上'
            elif code=='0d':
                errcode=u'左箱体板连接不上'
            elif code=='0e':
                errcode=u'右箱体板连接不上'
            elif code=='0f':
                errcode=u'BMS连接不上'
            elif code=='10':
                errcode=u'IMU连接不上'
            elif code=='11':
                errcode=u'红外1连接不上'
            elif code=='12':
                errcode=u'红外2连接不上'
            elif code=='13':
                errcode=u'红外3连接不上'
            elif code=='14':
                errcode=u'红外4连接不上'
            elif code=='15':
                errcode=u'红外5连接不上'
            elif code=='16':
                errcode=u'红外6连接不上'
            elif code=='17':
                errcode=u'红外7连接不上'
            elif code=='18':
                errcode=u'红外8连接不上'
            elif code=='19':
                errcode=u'红外9连接不上'
            elif code=='1a':
                errcode=u'红外10连接不上'
            elif code=='1b':
                errcode=u'ARM连接不上'
            else:
                errcode=u'非法值'
        elif bid=='11' or bid=='12':
            if code=='00':
                errcode=u'正常'
            elif code=='01':
                errcode=u'速度偏差故障'
            elif code=='02':
                errcode=u'霍尔故障'
            elif code=='04':
                errcode=u'编码器故障'
            elif code=='08':
                errcode=u'静态电流故障'
            elif code=='10':
                errcode=u'欠压故障'
            elif code=='20':
                errcode=u'过压故障'
            elif code=='40':
                errcode=u'堵转故障'
            elif code=='80':
                errcode=u'上下桥故障'
            else:
                errcode=u'非法值'
        elif bid=='61' or bid=='62':
            if code=='00':
                errcode=u'正常'
            elif code=='01':
                errcode=u'上盒子舵机关不到位'
            elif code=='02':
                errcode=u'下盒子舵机关不到位'
            elif code=='03':
                errcode=u'上盒子舵机开不到位'
            elif code=='04':
                errcode=u'下盒子舵机开不到位'
            elif code=='05':
                errcode=u'上盒子称重数值异常'
            elif code=='06':
                errcode=u'下盒子称重数值异常'
            elif code=='07':
                errcode=u'上盒子开门电机过流'
            elif code=='08':
                errcode=u'下盒子开门电机过流'
            elif code=='09':
                errcode=u'上盒子开门电机堵转'
            elif code=='0a':
                errcode=u'下盒子开门电机堵转'
            elif code=='0b':
                errcode=u'上盒子开门电机门开不到位'
            elif code=='0c':
                errcode=u'下盒子开门电机门开不到位'
            elif code=='0d':
                errcode=u'上盒子开门电机门关不到位'
            elif code=='0e':
                errcode=u'下盒子开门电机门关不到位'
            elif code=='0f':
                errcode=u'上盒子电机供电欠压'
            elif code=='10':
                errcode=u'下盒子电机供电欠压'
            elif code=='11':
                errcode=u'上盒子电机供电过压'
            elif code=='12':
                errcode=u'下盒子电机供电过压'
            elif code=='13':
                errcode=u'上盒子电机失位置'
            elif code=='14':
                errcode=u'下盒子电机失位置'
            else:
                errcode=u'非法值'
        elif bid=='51' or bid=='52' or bid=='53' or bid=='54' or bid=='55' or bid=='56' or bid=='57' or bid=='58' or bid=='59' or bid=='5a':
            if code=='00':
                errcode=u'正常'
            elif code=='01':
                errcode=u'红外传感器异常'
            else:
                errcode=u'非法值'

        elif bid=='25' or bid=='27' or bid=='26' or bid=='28':
            if code=='00':
                errcode=u'无故障'
            elif code=='01':
                errcode=u'程序初始化错误'
            elif code=='02':
                errcode=u'电机停止错误'
            elif code=='03':
                errcode=u'电机启动错误'
            elif code=='04':
                errcode=u'PWM波丢失'
            elif code=='05':
                errcode=u'PWM脉冲过宽'
            elif code=='06':
                errcode=u'PWM脉冲过窄'
            elif code=='07':
                errcode=u'电机A相开路'
            elif code=='08':
                errcode=u'电机B相开路'
            elif code=='09':
                errcode=u'电机C相开路'
            elif code=='0a':
                errcode=u'电机A相与GND短路'
            elif code=='0b':
                errcode=u'电机B相与GND短路'
            elif code=='0c':
                errcode=u'电机C相与GND短路'
            elif code=='0d':
                errcode=u'电机A相与电池正极短路'
            elif code=='0e':
                errcode=u'电机B相与电池正极短路'
            elif code=='0f':
                errcode=u'电机C相与电池正极短路'
            elif code=='10':
                errcode=u'电机A相过流'
            elif code=='11':
                errcode=u'电机B相过流'
            elif code=='12':
                errcode=u'电机C相过流'
            elif code=='13':
                errcode=u'硬件错误'
            elif code=='14':
                errcode=u'硬件错误'
            elif code=='15':
                errcode=u'硬件错误'
            elif code=='16':
                errcode=u'硬件错误'
            elif code=='17':
                errcode=u'硬件错误'
            elif code=='18':
                errcode=u'硬件错误'
            elif code=='19':
                errcode=u'硬件错误'
            elif code=='1a':
                errcode=u'硬件错误'
            elif code=='1b':
                errcode=u'电池电压过低'
            elif code=='1c':
                errcode=u'电池电压过高'
            elif code=='1d':
                errcode=u'电机1关门位置严重错误'
            elif code=='1e':
                errcode=u'电机1关门角度太小'
            elif code=='1f':
                errcode=u'电机1关门角度太大'
            elif code=='20':
                errcode=u'电机2关门位置严重错误'
            elif code=='21':
                errcode=u'电机2关门角度太小'
            elif code=='22':
                errcode=u'电机2关门角度太大'
            else:
                errcode=u'非法值'

        elif bid=='e1':
            if code=='00':
                errcode=u'正常'
            elif code=='01':
                errcode=u'无法获取数据'
            else:
                errcode=u'非法值'
        else:
            pass

        return errcode

    def batterystate(self,data):
        if data=='00':
            statecode=u'未知状态'
        elif data=='01':
            statecode=u'正常放电'
        elif data=='02':
            statecode=u'正在充电'
        elif data=='03':
            statecode=u'充满电'
        elif data=='ff':
            statecode=u'异常状态'
        else:
            statecode=u'非法值'+data
        return statecode

    def batteryval(self,data,frame):
        battery=0
        try:
            battery=int(data,16)
        except:
            self.errSingnal.emit(frame)
        return battery

    def Inchingstatget(self,data):
        if data=='01':
            inchstat=u'右侧'
        elif data=='02':
            inchstat=u'中间'
        elif data=='03':
            inchstat=u'右侧,中间'
        elif data=='04':
            inchstat=u'左侧'
        elif data=='05':
            inchstat=u'左,右'
        elif data=='06':
            inchstat=u'左侧,中间'
        elif data=='07':
            inchstat=u'左中右'
        else:
            inchstat=u'无碰撞'
        return inchstat

    def falling_dete(self,data):
        if data=='00':
            fallstat=u'正常'
        else:
            fallstat=u'跌落'
        return fallstat

class burnthread(QtCore.QThread):
    barSingnal=QtCore.pyqtSignal(int)
    testSingnal=QtCore.pyqtSignal(int)
    def __init__(self,count):
        super(self.__class__, self).__init__()
        self.test=count

    def __del__(self):
        self.wait()

    def run(self):
        for current in range(1,self.test+1):
            burnstopexist=os.path.exists('ui/burn.txt')
            if burnstopexist:
                break
            udpwin.leftdoormotoropen1.setChecked(True)
            udpwin.leftdoormotorclose1.setChecked(False)
            udpwin.leftdoormotoropen2.setChecked(True)
            udpwin.leftdoormotorclose2.setChecked(False)
            udpwin.leftlight1open.setChecked(True)
            udpwin.leftlight1close.setChecked(False)
            udpwin.rightlight1open.setChecked(True)
            udpwin.rightlight1close.setChecked(False)

            udpwin.rightdoormotoropen1.setChecked(True)
            udpwin.rightdoormotorclose1.setChecked(False)
            udpwin.rightdoormotoropen2.setChecked(True)
            udpwin.rightdoormotorclose2.setChecked(False)
            udpwin.leftlight2open.setChecked(True)
            udpwin.leftlight2close.setChecked(False)
            udpwin.rightlight2open.setChecked(True)
            udpwin.rightlight2close.setChecked(False)
            time.sleep(3)

            udpwin.leftdoormotoropen1.setChecked(False)
            udpwin.leftdoormotorclose1.setChecked(True)
            udpwin.leftdoormotoropen2.setChecked(False)
            udpwin.leftdoormotorclose2.setChecked(True)
            udpwin.leftlight1open.setChecked(False)
            udpwin.leftlight1close.setChecked(True)
            udpwin.rightlight1open.setChecked(False)
            udpwin.rightlight1close.setChecked(True)

            udpwin.rightdoormotoropen1.setChecked(False)
            udpwin.rightdoormotorclose1.setChecked(True)
            udpwin.rightdoormotoropen2.setChecked(False)
            udpwin.rightdoormotorclose2.setChecked(True)
            udpwin.leftlight2open.setChecked(False)
            udpwin.leftlight2close.setChecked(True)
            udpwin.rightlight2open.setChecked(False)
            udpwin.rightlight2close.setChecked(True)
            time.sleep(3)

            self.testSingnal.emit(current)
            bar=(current/self.test)*100
            self.barSingnal.emit(bar)

class titoburnthread(QtCore.QThread):
    barSingnal=QtCore.pyqtSignal(int)
    testSingnal=QtCore.pyqtSignal(int)
    def __init__(self,parent=None):
        super(self.__class__, self).__init__(parent)
        #self.test=count

    def __del__(self):
        self.wait()

    def run(self):
        close=0
        openflag=0
        f=open('ui/burn.txt','r')
        current=int(f.readline())
        f.close()
        while True:
            leftup=unicode(titowin.leftupdoor.toPlainText())
            leftdown=unicode(titowin.leftdowndoor.toPlainText())
            rightup=unicode(titowin.rightupdoor.toPlainText())
            rightdown=unicode(titowin.rightdowndoor.toPlainText())
            if leftup==u'关闭' and rightup==u'关闭' and leftdown==u'关闭' and rightdown==u'关闭':
                titowin.openrightdoorup.setChecked(True)
                titowin.closerightdoorup.setChecked(False)
                titowin.openleftdoorup.setChecked(True)
                titowin.closeleftdoorup.setChecked(False)
                titowin.leftlight1open.setChecked(True)
                titowin.leftlight1close.setChecked(False)
                titowin.rightlight1open.setChecked(True)
                titowin.rightlight1close.setChecked(False)

                titowin.openrightdoordown.setChecked(True)
                titowin.closerightdoordown.setChecked(False)
                titowin.openleftdoordown.setChecked(True)
                titowin.closeleftdoordown.setChecked(False)
                titowin.leftlight2open.setChecked(True)
                titowin.leftlight2close.setChecked(False)
                titowin.rightlight2open.setChecked(True)
                titowin.rightlight2close.setChecked(False)
                close=1
            if leftup==u'打开' and leftdown==u'打开' and rightup==u'打开' and rightdown==u'打开':
                titowin.openrightdoorup.setChecked(False)
                titowin.closerightdoorup.setChecked(True)
                titowin.openleftdoorup.setChecked(False)
                titowin.closeleftdoorup.setChecked(True)
                titowin.leftlight1open.setChecked(False)
                titowin.leftlight1close.setChecked(True)
                titowin.rightlight1open.setChecked(False)
                titowin.rightlight1close.setChecked(True)

                titowin.openrightdoordown.setChecked(False)
                titowin.closerightdoordown.setChecked(True)
                titowin.openleftdoordown.setChecked(False)
                titowin.closeleftdoordown.setChecked(True)
                titowin.leftlight2open.setChecked(False)
                titowin.leftlight2close.setChecked(True)
                titowin.rightlight2open.setChecked(False)
                titowin.rightlight2close.setChecked(True)
                openflag=1

            if close==1 and openflag==1:
                current+=1
                self.testSingnal.emit(current)
                close=0
                openflag=0
                f=open('ui/burn.txt','w')
                f.write(str(current)+'\n')
                f.close()
                #bar=(current/self.test)*100
                #self.barSingnal.emit(bar)
            burnstopexist=os.path.exists('ui/titoburn.txt')
            if burnstopexist:
                break

class nonYGprothread(QtCore.QThread):
    shellSingnal=QtCore.pyqtSignal(str)
    resultSignal=QtCore.pyqtSignal(str)
    corelogSingal=QtCore.pyqtSignal(str)
    def __init__(self, BID):
        super(self.__class__, self).__init__()
        self.device=BID

    def __del__(self):
        self.wait()

    def run(self):
        if self.device==1:
            send='88 99 AA BB CC DD'
            Ygcboardev.write(send.decode('hex'))
            result = ''
            soflag=0
            while True:
                recvHead=titodevice.readline()
                print(recvHead.encode('hex'))
                try:
                    hexHead = ord(recvHead)
                    frameHead = '%02x'%hexHead
                    if frameHead == '03':
                        soflag=1
                        result+=frameHead
                        break
                except:
                    self.messSingnal.emit(u'接收超时')
                    break
            if soflag==1:
                recvbinbid=titodevice.read()
                hexbid = ord(recvbinbid)
                recvbid = '%02x'%hexbid
                result+=recvbid
                recvbincmd=titodevice.read()
                hexcmd = ord(recvbincmd)
                recvcmd = '%02x'%hexcmd
                result+=recvcmd
                recvbinlen=titodevice.read()
                hexlen = ord(recvbinlen)
                recvlen = '%02x'%hexlen
                result+=recvlen
                length=int(recvlen,16)
                for i in range(0,length+4):
                    message=titodevice.read()
                    hvol = ord(message)
                    hhex = '%02x'%hvol
                    result += hhex
                return result
        elif self.device==2:
            pass
        elif self.device==3:
            pass
        elif self.device==4:
            pass
        elif self.device==5:
            pass
        elif self.device==6:
            pass
        else:
            pass

class xthread(QtCore.QThread):

    messSingnal=QtCore.pyqtSignal(str)
    listSingnal=QtCore.pyqtSignal(list)
    titocountSingnal=QtCore.pyqtSignal(int)
    errSingnal=QtCore.pyqtSignal(str)
    def __init__(self, MODEL):
        super(self.__class__, self).__init__()
        self.model=MODEL

    def __del__(self):
        self.wait()

    def run(self):
        count=0
        while True:
            self.commandsend(0,count)
            time.sleep(1)
            count+=1
            if count==2:
                count=0
            result=self.framerecv()
            if result=='':
                pass
            else:
                relist=self.frameMessgeanaly(result)
                self.listSingnal.emit(relist)
            xtstopexist=os.path.exists('ui/xtstop.txt')
            if xtstopexist:
                break


    def framerecv(self):
        result = ''
        soflag=0
        while True:
            recvHead=Ygcboardev.read()
            try:
                hexHead = ord(recvHead)
                frameHead = '%02x'%hexHead
                if frameHead == '59':
                    soflag=1
                    result+=frameHead
                    break
            except:
                pass
        if soflag==1:
            recvbinbid=Ygcboardev.read()
            hexbid = ord(recvbinbid)
            recvbid = '%02x'%hexbid
            result+=recvbid
            recvbincmd=Ygcboardev.read()
            hexcmd = ord(recvbincmd)
            recvcmd = '%02x'%hexcmd
            result+=recvcmd
            recvbinlen=Ygcboardev.read()
            hexlen = ord(recvbinlen)
            recvlen = '%02x'%hexlen
            result+=recvlen
            length=int(recvlen,16)
            for i in range(0,length+4):
                message=Ygcboardev.read()
                hvol = ord(message)
                hhex = '%02x'%hvol
                result += hhex
        return result

    def frameCRCheck(self,result):
        modbus_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
        CrcheckFlag=0
        checksum=''
        for i in range(0,len(result)-6,2):
            checksum+=result[i:i+2]
        temp=checksum.decode('hex')
        checkValue=hex(modbus_crc_func(temp)).lstrip('0x')
        for i in range(0,4-len(checkValue)):
            checkValue='0'+checkValue
        recvCheck=result[-4:-2]+result[-6:-4]
        if checkValue != recvCheck:
            CrcheckFlag=1
        return CrcheckFlag

    def commandsend(self,chanel,count):
        if self.model==0:
            bid='61'
            cmd='16'
            if count==0:
                data='0505'
            else:
                data='0A0A'
        else:
            bid='62'
            cmd='16'
            if count==0:
                data='0505'
            else:
                data='0A0A'
        if chanel==0:
            pass
        elif chanel==1:
            pass
        elif chanel==2:
            pass
        else:
            pass

        mess='59'+bid+cmd+'02'+data+'00'
        tocksendmess=self.messmarge(mess,1)
        Ygcboardev.flushInput()
        Ygcboardev.write(tocksendmess)
        #print(tocksendmess.encode('hex'))

    def messmarge(self,data,model):
        modbus_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
        messcrc=hex(modbus_crc_func(str(data).decode('hex')))
        if model ==1:
            sendcrc=messcrc
        else:
            sendcrc=hex(int(messcrc,16)+1)
        margecrc=sendcrc.lstrip('0x')
        if len(margecrc)==1:
            tempcrc='000'+margecrc
        elif len(margecrc)==2:
            tempcrc='00'+margecrc
        elif len(margecrc)==3:
            tempcrc='0'+margecrc
        else:
            tempcrc=margecrc

        finalcrc=tempcrc[2]+tempcrc[3]+tempcrc[0]+tempcrc[1]
        sendmess=(str(data)+finalcrc+'47').decode('hex')
        self.messSingnal.emit('tock:'+sendmess.encode('hex'))
        return sendmess

    def frameMessgeanaly(self,frame):
        #print(frame)
        devicelist=[]
        warrcode=self.warringcode(frame[10:12])
        devicelist.append(warrcode)
        errcode=self.errcodeany(frame[12:14])
        devicelist.append(errcode)

        up,down=self.weiany(frame)
        devicelist.append(up)
        devicelist.append(down)

        upswitch,downswitch=self.switch(frame[24:28])
        devicelist.append(upswitch)
        devicelist.append(downswitch)

        return devicelist

    def warringcode(self,code):
        if code == '01':
            warrtype=u'丢包过多'
        elif code == '02':
            warrtype=u'重启过'
        elif code =='04':
            warrtype=u'CPU温度过高'
        elif code == '03':
            warrtype=u'丢包过多,重启过'
        elif code == '05':
            warrtype=u'丢包过多,CPU温度过高'
        elif code == '06':
            warrtype=u'CPU温度过高,重启过'
        elif code == '07':
            warrtype=u'丢包过多,CPU温度过高,重启过'
        else:
            warrtype=u'正常'
        return warrtype

    def errcodeany(self,code):
        if code != '00':
            errtype=u'设备故障'
        else:
            errtype=u'正常'
        return errtype

    def cabinedoorstat(self,data):
        try:
            temp=int(data,16)
        except:
            temp=0
        if temp==0:
            leftup=u'打开'
            leftdown=u'打开'
            rightup=u'打开'
            rightdown=u'打开'
        else:
            if temp&1==1:
                rightup=u'中间'
            if temp&2==2:
                rightup=u'关闭'
            if temp&1!=1 and temp&2!=2:
                rightup=u'打开'

            if temp&4==4:
                leftup=u'中间'
            if temp&8==8:
                leftup=u'关闭'
            if temp&4!=4 and temp&8!=8:
                leftup=u'打开'

            if temp&16==16:
                rightdown=u'中间'
            if temp&32==32:
                rightdown=u'关闭'
            if temp&16!=16 and temp&32!=32:
                rightdown=u'打开'

            if temp&64==64:
                leftdown=u'中间'
            if temp&128==128:
                leftdown=u'关闭'
            if temp&64!=64 and temp&128!=128:
                leftdown=u'打开'

        return leftup,leftdown,rightup,rightdown

    def switch(self,data):

        if data[0:2]=='01':
            up=u'到位'
        else:
            up=u'未到位'
        if data[2:4]=='01':
            down=u'到位'
        else:
            down=u'未到位'

        return up,down

    def weiany(self,frame):
        temp1=int((frame[14]+frame[15]+frame[12]+frame[13]),16)
        temp2=int((frame[18]+frame[19]+frame[16]+frame[17]),16)
        if temp1>32767:
            tempdata=65536-temp1
            up='-'+str(tempdata)
        else:
            up=str(temp1)

        if temp2>32767:
            tempdata=65536-temp2
            down='-'+str(tempdata)
        else:
            down=str(temp2)

        return up,down

class manualxthread(QtCore.QThread):

    messSingnal=QtCore.pyqtSignal(str)
    listSingnal=QtCore.pyqtSignal(list)
    titocountSingnal=QtCore.pyqtSignal(int)
    errSingnal=QtCore.pyqtSignal(str)
    def __init__(self,MODEL):
        super(self.__class__, self).__init__()
        self.model=MODEL


    def __del__(self):
        self.wait()

    def run(self):
        if self.model==0:
            bid='61'
        else:
            bid='62'
        while True:
            self.commandsend(bid)
            result=self.framerecv()
            if result=='':
                pass
            else:
                relist=self.frameMessgeanaly(result)
                self.listSingnal.emit(relist)
            xtstopexist=os.path.exists('ui/xtmanualstop.txt')
            if xtstopexist:
                break


    def framerecv(self):
        result = ''
        soflag=0
        while True:
            recvHead=Ygcboardev.read()
            try:
                hexHead = ord(recvHead)
                frameHead = '%02x'%hexHead
                if frameHead == '59':
                    soflag=1
                    result+=frameHead
                    break
            except:
                pass
        if soflag==1:
            recvbinbid=Ygcboardev.read()
            hexbid = ord(recvbinbid)
            recvbid = '%02x'%hexbid
            result+=recvbid
            recvbincmd=Ygcboardev.read()
            hexcmd = ord(recvbincmd)
            recvcmd = '%02x'%hexcmd
            result+=recvcmd
            recvbinlen=Ygcboardev.read()
            hexlen = ord(recvbinlen)
            recvlen = '%02x'%hexlen
            result+=recvlen
            length=int(recvlen,16)
            for i in range(0,length+4):
                message=Ygcboardev.read()
                hvol = ord(message)
                hhex = '%02x'%hvol
                result += hhex
        return result

    def frameCRCheck(self,result):
        modbus_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
        CrcheckFlag=0
        checksum=''
        for i in range(0,len(result)-6,2):
            checksum+=result[i:i+2]
        temp=checksum.decode('hex')
        checkValue=hex(modbus_crc_func(temp)).lstrip('0x')
        for i in range(0,4-len(checkValue)):
            checkValue='0'+checkValue
        recvCheck=result[-4:-2]+result[-6:-4]
        if checkValue != recvCheck:
            CrcheckFlag=1
        return CrcheckFlag

    def commandsend(self,bid):
        data=0
        lightdata=0
        if xtwin.uplock.isChecked():
            data=data|2
        if xtwin.upunlock.isChecked():
            data=data&253
            data=data|1
        if xtwin.downlock.isChecked():
            data=data|8
        if xtwin.downunlock.isChecked():
            data=data&247
            data=data|4

        hexdata=hex(data).lstrip('0x')
        if len(hexdata)==0:
            hexdata='00'
        elif len(hexdata)==1:
            hexdata='0'+hexdata
        else:
            pass

        if xtwin.uplighton.isChecked():
            lightdata=lightdata|2
        if xtwin.uplightoff.isChecked():
            lightdata=lightdata&253
            lightdata=lightdata|1
        if xtwin.downlighton.isChecked():
            lightdata=lightdata|8
        if xtwin.downlightoff.isChecked():
            lightdata=lightdata&247
            lightdata=lightdata|4

        hexlight=hex(lightdata).lstrip('0x')
        if len(hexlight)==0:
            hexlight='00'
        elif len(hexlight)==1:
            hexlight='0'+hexlight
        else:
            pass

        mess='59'+bid+'16'+'02'+hexlight+hexdata+'00'
        tocksendmess=self.messmarge(mess,1)
        Ygcboardev.flushInput()
        Ygcboardev.write(tocksendmess)
        #print(tocksendmess.encode('hex'))

    def messmarge(self,data,model):
        modbus_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
        messcrc=hex(modbus_crc_func(str(data).decode('hex')))
        if model ==1:
            sendcrc=messcrc
        else:
            sendcrc=hex(int(messcrc,16)+1)
        margecrc=sendcrc.lstrip('0x')
        if len(margecrc)==1:
            tempcrc='000'+margecrc
        elif len(margecrc)==2:
            tempcrc='00'+margecrc
        elif len(margecrc)==3:
            tempcrc='0'+margecrc
        else:
            tempcrc=margecrc

        finalcrc=tempcrc[2]+tempcrc[3]+tempcrc[0]+tempcrc[1]
        sendmess=(str(data)+finalcrc+'47').decode('hex')
        self.messSingnal.emit('tock:'+sendmess.encode('hex'))
        return sendmess

    def frameMessgeanaly(self,frame):
        #print(frame)
        devicelist=[]
        warrcode=self.warringcode(frame[10:12])
        devicelist.append(warrcode)
        errcode=self.errcodeany(frame[12:14])
        devicelist.append(errcode)

        up,down=self.weiany(frame)
        devicelist.append(up)
        devicelist.append(down)

        upswitch,downswitch=self.switch(frame[24:28])
        devicelist.append(upswitch)
        devicelist.append(downswitch)

        return devicelist

    def warringcode(self,code):
        if code == '01':
            warrtype=u'丢包过多'
        elif code == '02':
            warrtype=u'重启过'
        elif code =='04':
            warrtype=u'CPU温度过高'
        elif code == '03':
            warrtype=u'丢包过多,重启过'
        elif code == '05':
            warrtype=u'丢包过多,CPU温度过高'
        elif code == '06':
            warrtype=u'CPU温度过高,重启过'
        elif code == '07':
            warrtype=u'丢包过多,CPU温度过高,重启过'
        else:
            warrtype=u'正常'
        return warrtype

    def errcodeany(self,code):
        if code != '00':
            errtype=u'设备故障'
        else:
            errtype=u'正常'
        return errtype

    def switch(self,data):
        if data[0:2]=='01':
            up=u'到位'
        else:
            up=u'未到位'
        if data[2:4]=='01':
            down=u'到位'
        else:
            down=u'未到位'

        return up,down

    def cabinelockstat(self,data):
        try:
            temp=int(data,16)
        except:
            temp=0
        if temp&64==64:
            upbox=u'到位'
        else:
            upbox=u'未到位'
        if temp&128==128:
            downbox=u'到位'
        else:
            downbox=u'未到位'
        if temp&1==1:
            leftup=u'锁定'
        else:
            leftup=u'未锁'
        if temp&4==4:
            leftdown=u'锁定'
        else:
            leftdown=u'未锁'
        if temp&2==2:
            rightup=u'锁定'
        else:
            rightup=u'未锁'
        if temp&8==8:
            rightdown=u'锁定'
        else:
            rightdown=u'未锁'

        return leftup,leftdown,rightup,rightdown,upbox,downbox

    def weiany(self,frame):
        temp1=int((frame[14]+frame[15]+frame[12]+frame[13]),16)
        temp2=int((frame[18]+frame[19]+frame[16]+frame[17]),16)
        if temp1>32767:
            tempdata=65536-temp1
            up='-'+str(tempdata)
        else:
            up=str(temp1)

        if temp2>32767:
            tempdata=65536-temp2
            down='-'+str(tempdata)
        else:
            down=str(temp2)

        return up,down

class udpboxthread(QtCore.QThread):

    messSingnal=QtCore.pyqtSignal(str)
    listSingnal=QtCore.pyqtSignal(list)
    titocountSingnal=QtCore.pyqtSignal(int)
    errSingnal=QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        udpclient=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpclient.settimeout(1)
        while True:
            self.tocksend(udpclient)
            message=self.framerecv(udpclient)
            if not message:
                pass
            else:
                result=''
                for data in message:
                    hexHead = ord(data)
                    frameHead = '%02x'%hexHead
                    result+=frameHead
                messlist=self.frameMessgeanaly(result)
                self.listSingnal.emit(messlist)
            titostopexist=os.path.exists('ui/udpboxstop.txt')
            if titostopexist:
                break

    def framerecv(self,udpclient):
        try:
            result=udpclient.recv(1024)
        except:
            result=''
        return result

    def frameCRCheck(self,result):
        modbus_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
        CrcheckFlag=0
        checksum=''
        for i in range(0,len(result)-6,2):
            checksum+=result[i:i+2]
        temp=checksum.decode('hex')
        checkValue=hex(modbus_crc_func(temp)).lstrip('0x')
        for i in range(0,4-len(checkValue)):
            checkValue='0'+checkValue
        recvCheck=result[-4:-2]+result[-6:-4]
        if checkValue != recvCheck:
            CrcheckFlag=1
        return CrcheckFlag

    def tocksend(self,udpclient):
        leftspeed=udpboxwin.leftmotorvalue.value()
        rightspeed=udpboxwin.rightmotorvalue.value()
        if unicode(udpboxwin.comboBox.currentText())== u'反向':
            if leftspeed==0:
                hexleft='0000'
            else:
                temp=65536-leftspeed
                hextemp=hex(temp).lstrip('0x').rstrip('L')
                for i in range(0,4-len(hextemp)):
                    hextemp='0'+hextemp
                hexleft=hextemp
        else:
            hexleftspeed=hex(leftspeed).lstrip('0x')
            for i in range(0,4-len(hexleftspeed)):
                hexleftspeed='0'+hexleftspeed
            hexleft=hexleftspeed

        if unicode(udpboxwin.comboBox_2.currentText())== u'反向':
            if rightspeed==0:
                hexright='0000'
            else:
                temp=65536-rightspeed
                hexrightemp=hex(temp).lstrip('0x').rstrip('L')
                for i in range(0,4-len(hexrightemp)):
                    hexrightemp='0'+hexrightemp
                hexright=hexrightemp
        else:
            hexrightspeed=hex(rightspeed).lstrip('0x')
            for i in range(0,4-len(hexrightspeed)):
                hexrightspeed='0'+hexrightspeed
            hexright=hexrightspeed

        if unicode(udpboxwin.leftmotorcontrol.currentText())==u'使能' and unicode(udpboxwin.rightmotorcontrol.currentText())==u'使能':
            motorcontrol='11'
        elif unicode(udpboxwin.leftmotorcontrol.currentText())==u'使能' and unicode(udpboxwin.rightmotorcontrol.currentText())==u'释放':
            motorcontrol='01'
        elif unicode(udpboxwin.leftmotorcontrol.currentText())==u'释放' and unicode(udpboxwin.rightmotorcontrol.currentText())==u'使能':
            motorcontrol='10'
        else:
            motorcontrol='00'

        motorcmd=hexleft[2]+hexleft[3]+hexleft[0]+hexleft[1]+hexright[2]+hexright[3]+hexright[0]+hexright[1]

        tockmessage=motorcmd+motorcontrol+'0000000000000000000000'
        mess='59'+'ee'+'ee'+'11'+'10'+tockmessage+'00'
        tocksendmess=self.messmarge(mess,1)
        udpclient.sendto(tocksendmess,('192.168.80.201',6650))
        #print(tocksendmess.encode('hex'))

    def messmarge(self,data,model):
        modbus_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
        messcrc=hex(modbus_crc_func(str(data).decode('hex')))
        if model ==1:
            sendcrc=messcrc
        else:
            sendcrc=hex(int(messcrc,16)+1)
        margecrc=sendcrc.lstrip('0x')
        if len(margecrc)==1:
            tempcrc='000'+margecrc
        elif len(margecrc)==2:
            tempcrc='00'+margecrc
        elif len(margecrc)==3:
            tempcrc='0'+margecrc
        else:
            tempcrc=margecrc

        finalcrc=tempcrc[2]+tempcrc[3]+tempcrc[0]+tempcrc[1]
        sendmess=(str(data)+finalcrc+'47').decode('hex')
        self.messSingnal.emit('tock:'+sendmess.encode('hex'))
        return sendmess

    def frameMessgeanaly(self,frame):
        devicelist=[]
        batstat=self.batterystate(frame[82:84])
        devicelist.append(batstat)
        batval=self.batteryval(frame[84:86],frame)
        devicelist.append(batval)
        return devicelist

    def batterystate(self,data):
        #print(data)
        if data=='00':
            statecode=u'未知状态'
        elif data=='01':
            statecode=u'正常放电'
        elif data=='02':
            statecode=u'正在充电'
        elif data=='03':
            statecode=u'充满电'
        elif data=='ff':
            statecode=u'异常状态'
        else:
            statecode=u'非法值'+unicode(data)
        return statecode

    def batteryval(self,data,frame):
        battery=0
        try:
            battery=int(data,16)
        except:
            self.errSingnal.emit(frame)
        return battery

class udpboxloop(QtCore.QThread):
    countSingnal=QtCore.pyqtSignal(int)
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        f=open('ui/udpbox.txt','r')
        count=int(f.readline())
        f.close()
        udpboxwin.leftmotorvalue.setValue(10)
        udpboxwin.rightmotorvalue.setValue(10)
        while True:
            delay=udpboxwin.delaytime.value()
            udpboxwin.comboBox.setCurrentIndex(0)
            udpboxwin.comboBox_2.setCurrentIndex(0)
            time.sleep(1)
            if unicode(udpboxwin.charge.toPlainText())==u'正在充电':
                udpboxwin.comboBox.setCurrentIndex(1)
                udpboxwin.comboBox_2.setCurrentIndex(1)
                time.sleep(delay-1)
                count+=1
                self.countSingnal.emit(count)
            titostopexist=os.path.exists('ui/udpboxstop.txt')
            if titostopexist:
                break

class mselecthread(QtCore.QThread):

    messSingnal=QtCore.pyqtSignal(str)
    listSingnal=QtCore.pyqtSignal(list)
    def __init__(self, bid,mastercmd,savlecmd):
        super(self.__class__, self).__init__()
        self.devid=bid
        self.mascmd=mastercmd
        self.savlecmd=savlecmd

    def __del__(self):
        self.wait()

    def run(self):
        tockdata='00000000000000000000000000000000'
        mess='59'+self.devid+self.savlecmd+'13'+'10'+tockdata+'25'+'02'+'00'
        tocksend=self.messmarge(mess,1)
        #self.cboardChild.testmessage.append('tock:'+tocksend.encode('hex'))
        Ygcboardev.write(tocksend)
        Ygcboardev.flushInput()
        while True:
            result=self.framerecv(self.devid,self.mascmd)
            if result == '':
                pass
            else:
                checkFlag=self.frameCRCheck(result)
                if checkFlag ==1 :
                    self.messSingnal.emit(u'CRC16校验错误')
                else:
                    if result[2:4]=='11' or result[2:4]=='12':
                        if result[4:6]=='19' or result[4:6]=='20':
                            messlist=self.frameMessgeanaly(result)
                            self.listSingnal.emit(messlist)
                            break
                        else:
                            pass
                    else:
                        pass

    def framerecv(self,bid,cmd):
        result = ''
        soflag=0
        while True:
            recvHead=Ygcboardev.read()
            try:
                hexHead = ord(recvHead)
                frameHead = '%02x'%hexHead
                if frameHead == '59':
                    soflag=1
                    result+=frameHead
                    break
            except:
                self.messSingnal.emit(u'SOF段接收超时')
                break
        if soflag==1:
            recvbinbid=Ygcboardev.read()
            try:
                hexbid = ord(recvbinbid)
                recvbid = '%02x'%hexbid
                result+=recvbid
                if str.upper(recvbid) == bid:
                    pass
                else:
                    self.messSingnal.emit(u'tito BID对不上')
                recvbincmd=Ygcboardev.read()
                try:
                    hexcmd = ord(recvbincmd)
                    recvcmd = '%02x'%hexcmd
                    result+=recvcmd
                    if str.upper(recvcmd) == cmd:
                        pass
                    else:
                        self.messSingnal.emit(u'tito cmd对不上')
                    recvbinlen=Ygcboardev.read()
                    try:
                        hexlen = ord(recvbinlen)
                        recvlen = '%02x'%hexlen
                        result+=recvlen
                        length=int(recvlen,16)
                        for i in range(0,length+4):
                            message=Ygcboardev.read()
                            try:
                                hvol = ord(message)
                                hhex = '%02x'%hvol
                                result += hhex
                            except:
                                self.messSingnal.emit(u'数据接收超时')
                                break
                    except:
                        self.messSingnal.emit(u'LEN接收超时')
                except:
                    self.messSingnal.emit(u'cmd接收超时')
            except:
                self.messSingnal.emit(u'bid接收超时')
        self.messSingnal.emit(result)
        return result

    def frameCRCheck(self,result):
        modbus_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
        CrcheckFlag=0
        checksum=''
        for i in range(0,len(result)-6,2):
            checksum+=result[i:i+2]
        temp=checksum.decode('hex')
        checkValue=hex(modbus_crc_func(temp)).lstrip('0x')
        for i in range(0,4-len(checkValue)):
            checkValue='0'+checkValue
        recvCheck=result[-4:-2]+result[-6:-4]
        if checkValue != recvCheck:
            CrcheckFlag=1
        return CrcheckFlag

    def frameMessgeanaly(self,frame):
        devicelist=[]
        devicelist.append(frame[2:4])
        devicelist.append(frame[4:6])
        if frame[4:6]=='20':
            devicelist.append(frame[146:148])
            errcode=self.errany(frame[148:150],frame[4:6])
            devicelist.append(errcode)
            part1=self.datany(frame[150:154])
            devicelist.append(part1)
            part2=self.datany(frame[154:158])
            devicelist.append(part2)
            part3=self.datany(frame[158:162])
            devicelist.append(part3)
            part4=self.datany(frame[162:166])
            devicelist.append(part4)
        elif frame[4:6]=='19':
            current=self.datany(frame[146:150])
            devicelist.append(current)
            postion=self.datany(frame[150:154])
            devicelist.append(postion)
            voltage=self.datany(frame[154:158])
            devicelist.append(voltage)
            setspeed=self.datany(frame[158:162])
            devicelist.append(setspeed)
            feedbackspeed=self.datany(frame[162:166])
            devicelist.append(feedbackspeed)
        else:
            pass
        return devicelist

    def errany(self,data,cmd):
        if cmd=='20':
            if data=='08':
                errcode=u'静态电流故障'
            elif data=='10':
                errcode=u'过压'
            elif data=='20':
                errcode=u'欠压'
            elif data=='40':
                errcode=u'堵转'
            elif data=='80':
                errcode=u'上下桥故障'
            elif data=='00':
                errcode=u'正常'
            else:
                errcode=u'非法值'+data
        else:
            pass
        return errcode

    def datany(self,data):
        temp=data[2]+data[3]+data[0]+data[1]
        value=int(temp,16)
        return value

    def messmarge(self,data,model):
        modbus_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
        messcrc=hex(modbus_crc_func(str(data).decode('hex')))
        if model ==1:
            sendcrc=messcrc
        else:
            sendcrc=hex(int(messcrc,16)+1)
        margecrc=sendcrc.lstrip('0x')
        if len(margecrc)==1:
            tempcrc='000'+margecrc
        elif len(margecrc)==2:
            tempcrc='00'+margecrc
        elif len(margecrc)==3:
            tempcrc='0'+margecrc
        else:
            tempcrc=margecrc

        finalcrc=tempcrc[2]+tempcrc[3]+tempcrc[0]+tempcrc[1]
        sendmess=(str(data)+finalcrc+'47').decode('hex')
        self.messSingnal.emit('tock:'+sendmess.encode('hex'))
        return sendmess

class udpmselecthread(QtCore.QThread):

    messSingnal=QtCore.pyqtSignal(str)
    listSingnal=QtCore.pyqtSignal(list)
    def __init__(self, bid,mastercmd,savlecmd):
        super(self.__class__, self).__init__()
        self.devid=bid
        self.mascmd=mastercmd
        self.savlecmd=savlecmd

    def __del__(self):
        self.wait()

    def run(self):
        tockdata='00000000000000000000000000000000'
        mess='59'+self.devid+self.savlecmd+'13'+'10'+tockdata+'25'+'02'+'00'
        tocksend=self.messmarge(mess,1)
        udpclient=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpclient.settimeout(1)
        while True:
            udpclient.sendto(tocksend,('192.168.80.201',6650))
            try:
                frame=udpclient.recv(1024)
            except:
                frame=''
                self.messSingnal.emit(u'接收超时')
            if frame == '':
                pass
            else:
                result=''
                for data in frame:
                    hexHead = ord(data)
                    frameHead = '%02x'%hexHead
                    result+=frameHead
                #print(result)
                if result[2:4]=='11' or result[2:4]=='12':
                    if result[4:6]=='19' or result[4:6]=='20':
                        messlist=self.frameMessgeanaly(result)
                        self.listSingnal.emit(messlist)
                        break
                    else:
                        pass
                else:
                    pass

    def frameCRCheck(self,result):
        modbus_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
        CrcheckFlag=0
        checksum=''
        for i in range(0,len(result)-6,2):
            checksum+=result[i:i+2]
        temp=checksum.decode('hex')
        checkValue=hex(modbus_crc_func(temp)).lstrip('0x')
        for i in range(0,4-len(checkValue)):
            checkValue='0'+checkValue
        recvCheck=result[-4:-2]+result[-6:-4]
        if checkValue != recvCheck:
            CrcheckFlag=1
        return CrcheckFlag

    def frameMessgeanaly(self,frame):
        devicelist=[]
        devicelist.append(frame[2:4])
        devicelist.append(frame[4:6])
        if frame[4:6]=='20':
            devicelist.append(frame[146:148])
            errcode=self.errany(frame[148:150])
            devicelist.append(errcode)
            part1=self.datany(frame[150:154])
            devicelist.append(part1)
            part2=self.datany(frame[154:158])
            devicelist.append(part2)
            part3=self.datany(frame[158:162])
            devicelist.append(part3)
            part4=self.datany(frame[162:166])
            devicelist.append(part4)
        elif frame[4:6]=='19':
            current=self.currentdatany(frame[146:150])
            devicelist.append(current)
            postion=self.datany(frame[150:154])
            devicelist.append(postion)
            voltage=self.datany(frame[154:158])
            devicelist.append(voltage)
            fdspeed=self.speeddatany(frame[158:162])
            devicelist.append(fdspeed)
            refspeed=self.speeddatany(frame[162:166])
            devicelist.append(refspeed)
        else:
            pass
        return devicelist

    def errany(self,data):
        errcode=''
        val=int(data,16)
        if val & 1==1:
            errcode=errcode+u'速度偏差故障 '
        if val & 2==2:
            errcode=errcode+u'霍尔故障 '
        if val & 4==4:
            errcode=errcode+u'编码器故障 '
        if val & 8==8:
            errcode=errcode+u'静态电流故障 '
        if val & 16==16:
            errcode=errcode+u'过压'
        if val & 32==32:
            errcode=errcode+u'欠压'
        if val & 64==64:
            errcode=u'堵转'
        if val & 128==128:
            errcode=u'上下桥故障'
        if data=='00':
            errcode=u'正常'
        return errcode

    def currentdatany(self,data):

        temp=data[2]+data[3]+data[0]+data[1]
        tempvalue=int(temp,16)
        if tempvalue>32767:
            value=65536-tempvalue
            temp=value*3.3/4096
            final='-'+str(temp)
        else:
            value=int(temp,16)
            final=value*3.3/4096
        return final

    def datany(self,data):
        temp=data[2]+data[3]+data[0]+data[1]
        value=int(temp,16)
        return value

    def speeddatany(self,data):
        temp=data[2]+data[3]+data[0]+data[1]
        tempvalue=int(temp,16)
        if tempvalue>32767:
            value='-'+str(65536-tempvalue)
        else:
            value=tempvalue
        return value

    def messmarge(self,data,model):
        modbus_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
        messcrc=hex(modbus_crc_func(str(data).decode('hex')))
        if model ==1:
            sendcrc=messcrc
        else:
            sendcrc=hex(int(messcrc,16)+1)
        margecrc=sendcrc.lstrip('0x')
        if len(margecrc)==1:
            tempcrc='000'+margecrc
        elif len(margecrc)==2:
            tempcrc='00'+margecrc
        elif len(margecrc)==3:
            tempcrc='0'+margecrc
        else:
            tempcrc=margecrc

        finalcrc=tempcrc[2]+tempcrc[3]+tempcrc[0]+tempcrc[1]
        sendmess=(str(data)+finalcrc+'47').decode('hex')
        self.messSingnal.emit('tock:'+sendmess.encode('hex'))
        return sendmess

def main():
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    app = QtGui.QApplication(sys.argv)
    mycode = locale.getpreferredencoding()
    code = QtCore.QTextCodec.codecForName(mycode)
    QtCore.QTextCodec.setCodecForLocale(code)
    QtCore.QTextCodec.setCodecForTr(code)
    QtCore.QTextCodec.setCodecForCStrings(code)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
