#! /usr/bin/env python 3.7 (3394)
#coding=utf-8
# Compiled at: 1969-12-31 18:00:00
#Powered by BugScaner
#http://tools.bugscaner.com/
#如果觉得不错,请分享给你朋友使用吧!
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QTextEdit
from PyQt5 import QtCore, QtGui
from singletonModel import ZFJPersoninfo
logIn_wid = 1000
logIn_hei = 800

class mapListView(QWidget):

    def __init__(self):
        super().__init__()
        self.defaultView()
        self.initUI()

    def defaultView(self):
        self.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        self.resize(logIn_wid, logIn_hei)
        self.setFixedSize(logIn_wid, logIn_hei)
        self.setStyleSheet('background-color:#fff')
        self.center()
        self.setWindowTitle('-QQ:365152048')

    def initUI(self):
        font = QtGui.QFont()
        font.setPointSize(15)
        self.textEdit = QTextEdit(self)
        self.textEdit.setStyleSheet('background-color:#262626;color:#fff;')
        self.textEdit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, logIn_wid, logIn_hei))
        font.setPointSize(15)
        self.textEdit.setFont(font)

    def reloadData(self):
        textEditText = '\n'
        personinfo = ZFJPersoninfo()
        if personinfo.propertyMisMap != None:
            space_line = '----------------------------------------\n'
            textEditText += space_line
            textEditText += str(personinfo.propertyMisMap) + '\n\n'
        if personinfo.method_list_map != None:
            space_line = '----------------------------------------\n'
            textEditText += space_line
            textEditText += str(personinfo.method_list_map) + '\n\n'
        if personinfo.objectNamesMap != None:
            space_line = '----------------------------------------\n'
            textEditText += space_line
            textEditText += str(personinfo.objectNamesMap) + '\n\n'
        if personinfo.sourceMap != None:
            space_line = '----------------------------------------\n'
            textEditText += space_line
            textEditText += str(personinfo.sourceMap) + '\n\n'
            if personinfo.xcassetsMap != None:
                textEditText += str(personinfo.xcassetsMap) + '\n\n'
        if personinfo.PBXGroupMap != None:
            space_line = '----------------------------------------\n'
            textEditText += space_line
            textEditText += str(personinfo.PBXGroupMap) + '\n\n'
        self.textEdit.setPlainText(textEditText)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())