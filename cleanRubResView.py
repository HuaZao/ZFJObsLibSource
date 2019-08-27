#! /usr/bin/env python 3.7 (3394)
#coding=utf-8
# Compiled at: 1969-12-31 18:00:00
#Powered by BugScaner
#http://tools.bugscaner.com/
#如果觉得不错,请分享给你朋友使用吧!
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QLabel, QMessageBox, QLineEdit, QRadioButton, QCheckBox, QTextEdit, QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QTextCursor
from singletonModel import ZFJPersoninfo
import zfjTools, cleanRubResClass, os
viewWid = 625
viewHei = 675
margin_size = 10
_translate = QtCore.QCoreApplication.translate

class CleanResView(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.defaultView()

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
        titleLab = QLabel('无用资源清理工具', self)
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
        projectTitLab = QLabel('项目路径:', self)
        projectTitLab.setStyleSheet('color:#000000;')
        projectTitLab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        projectTitLab.setGeometry(QtCore.QRect(margin_size, margin_top, 65, 30))
        font.setPointSize(14)
        projectTitLab.setFont(font)
        self.projectPathEdit = QtWidgets.QLineEdit(self)
        self.projectPathEdit.setGeometry(QtCore.QRect(65 + margin_size * 2, margin_top, viewWid - margin_size * 4 - 65 - 90, 30))
        font.setPointSize(14)
        self.projectPathEdit.setFont(font)
        self.projectPathEdit.setText('/Users/zhangfujie/Desktop/Obfuscated')
        projectPathBtn = QtWidgets.QPushButton(self)
        projectPathBtn.setGeometry(QtCore.QRect(viewWid - margin_size - 90, margin_top, 90, 30))
        projectPathBtn.setText(_translate('MainWindow', '选择文件夹'))
        projectPathBtn.setStyleSheet('color:#000000;background-color:#efeff3;border:1px solid #efeff3;')
        projectPathBtn.clicked.connect(self.projectPathBtnClick)
        projectPathBtn.setFont(font)
        margin_top += 30 + margin_size * 2
        smlTitLab = QLabel('设置忽略清理的资源文件名', self)
        smlTitLab.setStyleSheet('color:#d4237a;')
        smlTitLab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        smlTitLab.setGeometry(QtCore.QRect(margin_size, margin_top, 200, 30))
        smlTitLab.setFont(font)
        margin_top += 30 + margin_size
        self.ignoreEdit = QtWidgets.QLineEdit(self)
        self.ignoreEdit.setGeometry(QtCore.QRect(margin_size * 2, margin_top, viewWid - margin_size * 4, 30))
        font.setPointSize(14)
        self.ignoreEdit.setFont(font)
        margin_top += 35
        tipsLab = QLabel('多个资源名使用,分割!', self)
        tipsLab.setStyleSheet('color:#87b753;')
        tipsLab.setGeometry(QtCore.QRect(margin_size * 2, margin_top, viewWid - margin_size * 4, 20))
        font.setPointSize(12)
        tipsLab.setFont(font)
        margin_top += 20 + margin_size * 2
        textEditWid = (viewWid - margin_size * 3) / 2
        self.textEdit = QTextEdit(self)
        self.textEdit.setStyleSheet('background-color:#262626;color:#fff;')
        self.textEdit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.textEdit.setGeometry(QtCore.QRect(margin_size * 2, margin_top, viewWid - margin_size * 4, 350))
        font.setPointSize(12)
        self.textEdit.setFont(font)
        margin_top += 350 + margin_size * 3
        startCleanBtn = QtWidgets.QPushButton(self)
        startCleanBtn.setGeometry(QtCore.QRect((viewWid - 160) / 2, margin_top, 160, 40))
        startCleanBtn.setText(_translate('MainWindow', '开始清理'))
        startCleanBtn.setStyleSheet('background-color:#fff;color:#cc0066;border:1px solid #cc0066;')
        startCleanBtn.clicked.connect(self.startCleanBtnClick)
        font.setPointSize(18)
        startCleanBtn.setFont(font)
        margin_top += 40 + margin_size * 3

    def backMainViewBtnClick(self):
        personinfo = ZFJPersoninfo()
        if personinfo.mainRootView != None:
            personinfo.mainRootView.show()
            self.close()
        else:
            print('mainRootView')

    def projectPathBtnClick(self):
        file_dir = ''
        try:
            file_dir = QFileDialog.getExistingDirectory(self, 'open file', '/Users/')
        except Exception as e:
            try:
                file_dir = ','
            finally:
                e = None
                del e

        self.projectPathEdit.setText(file_dir)

    def startCleanBtnClick(self):
        file_dir = self.projectPathEdit.text()
        if os.path.exists(file_dir) == False:
            self.megBoxInfor('目录不存在')
            return
        ignoreText = self.ignoreEdit.text()
        ignoreList = []
        if len(ignoreText) > 0:
            ignoreText = ignoreText.replace(',', ',')
            ignoreList = ignoreText.split(',')
        try:
            cleanRubResClass.startCleanRubRes(file_dir, ignoreList)
        except Exception as e:
            try:
                QMessageBox.information(self, '', str(e), QMessageBox.Yes)
            finally:
                e = None
                del e

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def megBoxInfor(self, infor):
        QMessageBox.information(self, '', infor, QMessageBox.Yes)


def addTextEdit(log_str):
    personinfo = ZFJPersoninfo()
    cleanResView = personinfo.cleanResView
    if cleanResView != None:
        str_text = cleanResView.textEdit.toPlainText()
        str_text += log_str + '\n'
        cleanResView.textEdit.setPlainText(str_text)
        cleanResView.textEdit.moveCursor(QTextCursor.End)
        QApplication.processEvents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cleanResView = CleanResView()
    personinfo = ZFJPersoninfo()
    personinfo.cleanResView = cleanResView
    cleanResView.show()
    sys.exit(app.exec_())