#! /usr/bin/env python 3.7 (3394)
#coding=utf-8
# Compiled at: 1969-12-31 18:00:00
#Powered by BugScaner
#http://tools.bugscaner.com/
#如果觉得不错,请分享给你朋友使用吧!
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QTextEdit, QLabel, QPushButton, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from singletonModel import ZFJPersoninfo
import zfjTools, confusionLog as conLog
from threading import Thread
import subprocess
logIn_wid = 625
logIn_hei = 580
margin_size = 10
_translate = QtCore.QCoreApplication.translate

class DeveLexiconView(QWidget):

    def __init__(self):
        super().__init__()
        self.defaultView()
        self.initUI()
        self.reloadData()

    def defaultView(self):
        self.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        self.resize(logIn_wid, logIn_hei)
        self.setFixedSize(logIn_wid, logIn_hei)
        self.setStyleSheet('background-color:#fff')
        self.center()
        self.setWindowTitle(zfjTools.baseTitle)

    def initUI(self):
        font = QtGui.QFont()
        font.setPointSize(14)
        margin_top = margin_size
        titleTipLab = QLabel('混淆词库工具', self)
        titleTipLab.setStyleSheet('color:#cc0066;')
        titleTipLab.setAlignment(Qt.AlignCenter)
        titleTipLab.setGeometry(QtCore.QRect(margin_size, margin_top, logIn_wid - margin_size * 2, 30))
        font.setPointSize(18)
        titleTipLab.setFont(font)
        backMainViewBtn = QtWidgets.QPushButton(self)
        backMainViewBtn.setGeometry(QtCore.QRect(margin_size, margin_top + 7.5, 50, 25))
        backMainViewBtn.setObjectName('logInBtn')
        backMainViewBtn.setText(_translate('MainWindow', '返回'))
        backMainViewBtn.setStyleSheet('color:#1667ea;background-color:#fff;border:1px solid #1667ea;')
        backMainViewBtn.clicked.connect(self.backMainViewBtnClick)
        font.setPointSize(14)
        backMainViewBtn.setFont(font)
        showWordBtn = QtWidgets.QPushButton(self)
        showWordBtn.setGeometry(QtCore.QRect(logIn_wid - 80, margin_top + 5.0, 80, 30))
        showWordBtn.setText(_translate('MainWindow', ''))
        showWordBtn.setStyleSheet('color:#87b753;border:1px solid #fff;')
        showWordBtn.clicked.connect(self.showWordBtnClick)
        font.setPointSize(14)
        showWordBtn.setFont(font)
        margin_top += 30 + margin_size * 2
        self.addTextEdit = QTextEdit(self)
        self.addTextEdit.setStyleSheet('color:#000;background-color:#e1e3e6;')
        self.addTextEdit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.addTextEdit.setGeometry(QtCore.QRect(margin_size, margin_top, logIn_wid - margin_size * 2, 400))
        font.setPointSize(14)
        self.addTextEdit.setFont(font)
        margin_top += 400 + margin_size
        tipsLab = QLabel('', self)
        tipsLab.setStyleSheet('color:#000000;')
        tipsLab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        tipsLab.setGeometry(QtCore.QRect(margin_size, margin_top, logIn_wid - margin_size * 2, 30))
        font.setPointSize(14)
        tipsLab.setFont(font)
        margin_top += 30 + margin_size * 2
        addWordBtn = QtWidgets.QPushButton(self)
        addWordBtn.setGeometry(QtCore.QRect((logIn_wid - 160) / 2, margin_top, 160, 40))
        addWordBtn.setObjectName('addWordBtn')
        addWordBtn.setText(_translate('MainWindow', '打开词库'))
        addWordBtn.setStyleSheet('background-color:#fff;color:#cc0066;border:1px solid #cc0066;')
        addWordBtn.clicked.connect(self.addWordBtnClick)
        font.setPointSize(18)
        addWordBtn.setFont(font)
        margin_top += 40 + margin_size * 2
        lexiconTitleLab = QLabel('', self)
        lexiconTitleLab.setStyleSheet('color:#cc0066;')
        lexiconTitleLab.setAlignment(Qt.AlignVCenter)
        lexiconTitleLab.setGeometry(QtCore.QRect(margin_size, margin_top, logIn_wid - margin_size * 2, 30))
        lexiconTitleLab.setFont(font)
        margin_top += 30 + margin_size
        self.lexiconEdit = QTextEdit(self)
        self.lexiconEdit.setStyleSheet('background-color:#e1e3e6;color:#000;')
        self.lexiconEdit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.lexiconEdit.setGeometry(QtCore.QRect(margin_size, margin_top, logIn_wid - margin_size * 2, 400))
        font.setPointSize(14)
        self.lexiconEdit.setFont(font)

    def backMainViewBtnClick(self):
        personinfo = ZFJPersoninfo()
        if personinfo.mainRootView != None:
            personinfo.mainRootView.show()
            self.close()
        else:
            print('mainRootView')

    def showWordBtnClick(self):
        subprocess.call(['open', 'lexicon20.txt'])

    def addWordBtnClick(self):
        personinfo = ZFJPersoninfo()
        fail_list = []
        scu_list = []
        addText = self.addTextEdit.toPlainText()
        addText = ''.join(addText.split())
        addText.replace(',', ',')
        new_lexicon_list = addText.split(',')
        for word in new_lexicon_list:
            if len(word) > 0:
                if word not in personinfo.lexicon_list:
                    personinfo.lexicon_list.append(word)
                    scu_list.append(word)
                else:
                    fail_list.append(word)
            else:
                conLog.info('AddLexicon Fail ')

        if len(fail_list) > 0:
            self.megBoxInfor('添加成功:' + ','.join(fail_list))
            conLog.info('AddLexicon Fail ' + ','.join(fail_list))
        if len(scu_list) > 0:
            file_data = ','.join(personinfo.lexicon_list)
            Wopen = open('lexicon.txt', 'w')
            Wopen.write(file_data)
            Wopen.close()
            conLog.info('AddLexicon OK ' + ','.join(scu_list))
            self.lexiconEdit.setPlainText(','.join(personinfo.lexicon_list))

    def megBoxInfor(self, infor):
        QMessageBox.information(self, '', infor, QMessageBox.Yes)

    def reloadData(self):
        pass

    def reloadWordThread(self):
        lexicon_list = zfjTools.readLexiconList()
        self.lexiconEdit.setPlainText(','.join(lexicon_list))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    root_view = DeveLexiconView()
    root_view.show()
    sys.exit(app.exec_())