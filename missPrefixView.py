#! /usr/bin/env python 3.7 (3394)
#coding=utf-8
# Compiled at: 1969-12-31 18:00:00
#Powered by BugScaner
#http://tools.bugscaner.com/
#如果觉得不错,请分享给你朋友使用吧!
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QLabel, QPushButton, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from singletonModel import ZFJPersoninfo
import zfjTools
viewWid = 625
viewHei = 565
margin_size = 10
_translate = QtCore.QCoreApplication.translate
_prefixMap = {'proPreFix':'', 
 'objPreFix':'',  'funPreFix':'',  'imgPreFix':'',  'rubPreFix':'',  'folderPreFix':'',  'projectNamePreFix':''}

class PrefixView(QWidget):

    def __init__(self):
        super().__init__()
        self.defaultView()
        self.initUI()
        self.setprefixEditValue()

    def defaultView(self):
        self.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        self.resize(viewWid, viewHei)
        self.setFixedSize(viewWid, viewHei)
        self.setStyleSheet('background-color:#fff')
        self.center()
        self.setWindowTitle(zfjTools.baseTitle)

    def initUI(self):
        font = QtGui.QFont()
        font.setPointSize(18)
        margin_top = margin_size
        titleLab = QLabel('设置混淆前缀', self)
        titleLab.setStyleSheet('color:#d4237a;')
        titleLab.setAlignment(Qt.AlignCenter)
        titleLab.setGeometry(QtCore.QRect(margin_size, margin_top, viewWid - margin_size * 2, 40))
        titleLab.setFont(font)
        backMainViewBtn = QtWidgets.QPushButton(self)
        backMainViewBtn.setGeometry(QtCore.QRect(margin_size, margin_top + 7.5, 50, 25))
        backMainViewBtn.setObjectName('logInBtn')
        backMainViewBtn.setText(_translate('MainWindow', '返回'))
        backMainViewBtn.setStyleSheet('color:#1667ea;background-color:#fff;border:1px solid #1667ea;')
        backMainViewBtn.clicked.connect(self.backMainViewBtnClick)
        font.setPointSize(14)
        backMainViewBtn.setFont(font)
        margin_top += 40 + margin_size
        self.preFixList = [
         '属性混淆前缀', '类名混淆前缀', '方法混淆前缀', '翻新资源前缀', '垃圾代码前缀', '混淆目录前缀', '混淆工程前缀']
        lineViewWid = (viewWid - margin_size * 8) / 2
        lineViewHei = 35
        self.prefixEditList = []
        for index in range(0, len(self.preFixList)):
            this_margin_top = margin_top + (lineViewHei + margin_size * 2) * index
            preFixTitLab = QLabel('  ' + self.preFixList[index] + ':', self)
            preFixTitLab.setStyleSheet('color:#000;background-color:#ebeaeb;')
            preFixTitLab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            preFixTitLab.setGeometry(QtCore.QRect(margin_size * 3, this_margin_top, lineViewWid, lineViewHei))
            preFixTitLab.setFont(font)
            prefixEdit = QtWidgets.QLineEdit(self)
            prefixEdit.setGeometry(QtCore.QRect(margin_size * 5 + lineViewWid, this_margin_top, lineViewWid, lineViewHei))
            prefixEdit.setFont(font)
            prefixEdit.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            prefixEdit.setStyleSheet('color:#cc0066')
            self.prefixEditList.append(prefixEdit)

        margin_top += (lineViewHei + margin_size * 2) * len(self.preFixList)
        tipsLab = QLabel('提示:混淆前缀不能包含数字和中文!', self)
        tipsLab.setStyleSheet('color:#cc0066;')
        tipsLab.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        tipsLab.setGeometry(QtCore.QRect(margin_size * 3, margin_top, viewWid - margin_size * 6, 20))
        font.setPointSize(14)
        tipsLab.setFont(font)
        margin_top += 20 + margin_size * 3
        saveBtn = QtWidgets.QPushButton(self)
        saveBtn.setGeometry(QtCore.QRect((viewWid - 160) / 2, margin_top, 160, 40))
        saveBtn.setObjectName('saveBtn')
        saveBtn.setText(_translate('MainWindow', '保存'))
        saveBtn.setStyleSheet('background-color:#fff;color:#cc0066;border:1px solid #cc0066;')
        saveBtn.clicked.connect(self.saveBtnClick)
        font.setPointSize(18)
        saveBtn.setFont(font)
        margin_top += margin_size * 3 + 40

    def backMainViewBtnClick(self):
        personinfo = ZFJPersoninfo()
        if personinfo.mainRootView != None:
            personinfo.mainRootView.show()
            self.close()
        else:
            print('mainRootView')

    def setprefixEditValue(self):
        global _prefixMap
        cacheMap = zfjTools.readPrefixMap()
        for index in range(0, len(self.prefixEditList)):
            prefixEdit = self.prefixEditList[index]
            key = list(_prefixMap.keys())[index]
            if key in cacheMap.keys():
                prefixEdit.setText(cacheMap[key])
                _prefixMap[key] = cacheMap[key]

    def saveBtnClick(self):
        for index in range(0, len(self.prefixEditList)):
            prefixEdit = self.prefixEditList[index]
            if zfjTools.is_number(prefixEdit.text()) == True:
                self.megBoxInfor(self.preFixList[index] + '')
                return
            if zfjTools.is_contain_chinese(prefixEdit.text()) == True:
                self.megBoxInfor(self.preFixList[index] + '')
                return
            value = ''.join(prefixEdit.text().split())
            key = list(_prefixMap.keys())[index]
            _prefixMap[key] = value

        zfjTools.savePrefixMap(_prefixMap)
        personinfo = ZFJPersoninfo()
        personinfo.prefixMap = _prefixMap
        self.megBoxInfor('保存成功')

    def megBoxInfor(self, infor):
        QMessageBox.information(self, '', infor, QMessageBox.Yes)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    prefixView = PrefixView()
    prefixView.show()
    sys.exit(app.exec_())