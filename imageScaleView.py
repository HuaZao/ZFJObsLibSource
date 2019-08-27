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
import zfjTools, imageScaleObj, os
viewWid = 625
viewHei = 661
margin_size = 10
_translate = QtCore.QCoreApplication.translate

class ImgScaleView(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.defaultView()
        self.reloadUI()
        self.funType = -1

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
        titleLab = QLabel('图片压缩工具', self)
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
        oldImgLab = QLabel('请选择图片所在路径:', self)
        oldImgLab.setStyleSheet('color:#000000;')
        oldImgLab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        oldImgLab.setGeometry(QtCore.QRect(margin_size, margin_top, 135, 30))
        font.setPointSize(14)
        oldImgLab.setFont(font)
        self.oldImgEdit = QtWidgets.QLineEdit(self)
        self.oldImgEdit.setGeometry(QtCore.QRect(135 + margin_size * 2, margin_top, 350, 30))
        font.setPointSize(14)
        self.oldImgEdit.setFont(font)
        self.oldImgEdit.setText('/Users/zhangfujie/Desktop/Obfuscated')
        oldImgPathBtn = QtWidgets.QPushButton(self)
        oldImgPathBtn.setGeometry(QtCore.QRect(margin_size * 3 + 135 + 350, margin_top, 100, 30))
        oldImgPathBtn.setText(_translate('MainWindow', '选择文件夹'))
        oldImgPathBtn.setStyleSheet('color:#000000;background-color:#efeff3;border:1px solid #efeff3;')
        oldImgPathBtn.clicked.connect(self.oldImgPathBtnClick)
        oldImgPathBtn.setFont(font)
        margin_top += 30 + margin_size
        newImgLab = QLabel('请选择图片保存路径:', self)
        newImgLab.setStyleSheet('color:#000000;')
        newImgLab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        newImgLab.setGeometry(QtCore.QRect(margin_size, margin_top, 135, 30))
        font.setPointSize(14)
        newImgLab.setFont(font)
        self.newImgEdit = QtWidgets.QLineEdit(self)
        self.newImgEdit.setGeometry(QtCore.QRect(135 + margin_size * 2, margin_top, 350, 30))
        font.setPointSize(14)
        self.newImgEdit.setFont(font)
        self.newImgEdit.setText('/Users/zhangfujie/Desktop/Obfuscated/NewImgs')
        newImgPathBtn = QtWidgets.QPushButton(self)
        newImgPathBtn.setGeometry(QtCore.QRect(margin_size * 3 + 135 + 350, margin_top, 100, 30))
        newImgPathBtn.setText(_translate('MainWindow', '选择文件夹'))
        newImgPathBtn.setStyleSheet('color:#000000;background-color:#efeff3;border:1px solid #efeff3;')
        newImgPathBtn.clicked.connect(self.newImgPathBtnClick)
        newImgPathBtn.setFont(font)
        margin_top += 30 + margin_size
        line_lab = QLabel(self)
        line_lab.setStyleSheet('background-color:#dcdcdc')
        line_lab.setGeometry(QtCore.QRect(0, margin_top, viewWid, 1))
        margin_top += 1 + margin_size
        smlTitLab = QLabel('请选择图片压缩方式', self)
        smlTitLab.setStyleSheet('color:#d4237a;')
        smlTitLab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        smlTitLab.setGeometry(QtCore.QRect(margin_size, margin_top, 135, 30))
        smlTitLab.setFont(font)
        textEditWid = (viewWid - margin_size * 3) / 2
        self.textEdit = QTextEdit(self)
        self.textEdit.setStyleSheet('background-color:#262626;color:#fff;')
        self.textEdit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.textEdit.setGeometry(QtCore.QRect(textEditWid - margin_size * 5, margin_top, textEditWid + margin_size * 6, 411 - margin_top))
        font.setPointSize(12)
        self.textEdit.setFont(font)
        margin_top += 30 + margin_size
        self.sysBtn = QRadioButton('自动生成@1x,@2x,@3x', self)
        self.sysBtn.setStyleSheet('color:#000;')
        self.sysBtn.setGeometry(QtCore.QRect(margin_size * 2, margin_top, 200, 30))
        self.sysBtn.setChecked(False)
        self.sysBtn.toggled.connect(lambda : self.radioBtnClick(self.sysBtn))
        margin_top += 30 + margin_size
        self.userBtn = QRadioButton('手动设置图片尺寸(格式:宽x高)', self)
        self.userBtn.setStyleSheet('color:#000;')
        self.userBtn.setGeometry(QtCore.QRect(margin_size * 2, margin_top, 200, 30))
        self.userBtn.setChecked(False)
        self.userBtn.toggled.connect(lambda : self.radioBtnClick(self.userBtn))
        titleArr = [
         '@1x尺寸:', '@2x尺寸:', '@3x尺寸:']
        self.checkBoxList = []
        self.checkBoxEditList = []
        for index in range(0, 3):
            margin_top += 30 + margin_size
            checkBox = QCheckBox(titleArr[index], self)
            checkBox.setStyleSheet('color:#000;')
            checkBox.stateChanged.connect(self.checkBoxClick)
            checkBox.setGeometry(QtCore.QRect(margin_size * 4, margin_top, 80, 30))
            self.checkBoxList.append(checkBox)
            checkBoxEdit = QtWidgets.QLineEdit(self)
            checkBoxEdit.setText('0x0')
            checkBoxEdit.setGeometry(QtCore.QRect(margin_size * 4 + 80, margin_top, 200 - (margin_size * 4 + 80) + margin_size * 2, 30))
            checkBoxEdit.setFont(font)
            checkBoxEdit.setStyleSheet('color:#cc0066;background-color:#efeff3;')
            checkBoxEdit.textChanged.connect(lambda : self.checkBoxEditChanged(index))
            self.checkBoxEditList.append(checkBoxEdit)

        margin_top += 30 + margin_size
        self.alphaCheckBox = QCheckBox('移除PNG的alpha通道', self)
        self.alphaCheckBox.setStyleSheet('color:#000;')
        self.alphaCheckBox.stateChanged.connect(self.checkBoxClick)
        self.alphaCheckBox.setGeometry(QtCore.QRect(margin_size * 2, margin_top, 200, 30))
        margin_top += 30 + margin_size
        self.imgTypeBox = QCheckBox('webp', self)
        self.imgTypeBox.setStyleSheet('color:#000;')
        self.imgTypeBox.stateChanged.connect(self.checkBoxClick)
        self.imgTypeBox.setGeometry(QtCore.QRect(margin_size * 2, margin_top, 200, 30))
        margin_top += 30 + margin_size * 5
        startScaleBtn = QtWidgets.QPushButton(self)
        startScaleBtn.setGeometry(QtCore.QRect((viewWid - 160) / 2, margin_top, 160, 40))
        startScaleBtn.setText(_translate('MainWindow', '开始压缩'))
        startScaleBtn.setStyleSheet('background-color:#fff;color:#cc0066;border:1px solid #cc0066;')
        startScaleBtn.clicked.connect(self.startScaleBtnClick)
        font.setPointSize(18)
        startScaleBtn.setFont(font)
        margin_top += 40 + margin_size * 2
        tipsTitLab = QLabel('使用须知', self)
        tipsTitLab.setStyleSheet('color:#d4237a;')
        tipsTitLab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        tipsTitLab.setGeometry(QtCore.QRect(margin_size, margin_top, viewWid - margin_size * 2, 30))
        font.setPointSize(14)
        tipsTitLab.setFont(font)
        margin_top += 30
        tipsLabText = '1.选择自动生成@1x、@2x、@3x时,默认把原图作为@3x, @1x和@2x在此基础上向下压缩;\n2.选择手动设置图片尺寸时，为了保证图片的清晰质量，原图尺寸最好大于等于三倍尺寸;'
        tipsLab = QLabel(tipsLabText, self)
        tipsLab.setStyleSheet('color:#87b753;')
        tipsLab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        tipsLab.setGeometry(QtCore.QRect(margin_size, margin_top, viewWid - margin_size * 2, 50))
        font.setPointSize(12)
        tipsLab.setFont(font)
        margin_top += 50 + margin_size
        line_lab_1 = QLabel(self)
        line_lab_1.setStyleSheet('background-color:#dcdcdc')
        line_lab_1.setGeometry(QtCore.QRect(0, margin_top, viewWid, 1))
        margin_top += 1 + margin_size
        downLab_wid = (viewWid - margin_size * 3) / 2
        self.accountLab = QLabel(':', self)
        self.accountLab.setStyleSheet('color:#000;')
        self.accountLab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.accountLab.setGeometry(QtCore.QRect(margin_size, margin_top, downLab_wid, 30))
        font.setPointSize(13)
        self.accountLab.setFont(font)
        self.timeLab = QLabel(':', self)
        self.timeLab.setStyleSheet('color:#000;')
        self.timeLab.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.timeLab.setGeometry(QtCore.QRect(margin_size * 2 + downLab_wid, margin_top, downLab_wid, 30))
        font.setPointSize(13)
        self.timeLab.setFont(font)
        margin_top += 30 + margin_size

    def backMainViewBtnClick(self):
        personinfo = ZFJPersoninfo()
        if personinfo.mainRootView != None:
            personinfo.mainRootView.show()
            self.close()
        else:
            print('mainRootView')

    def oldImgPathBtnClick(self):
        file_dir = ''
        try:
            file_dir = QFileDialog.getExistingDirectory(self, 'open file', '/Users/')
        except Exception as e:
            try:
                file_dir = ','
            finally:
                e = None
                del e

        self.oldImgEdit.setText(file_dir)

    def newImgPathBtnClick(self):
        file_dir = ''
        try:
            file_dir = QFileDialog.getExistingDirectory(self, 'open file', '/Users/')
        except Exception as e:
            try:
                file_dir = ','
            finally:
                e = None
                del e

        self.newImgEdit.setText(file_dir)

    def radioBtnClick(self, btn):
        if self.sysBtn.isChecked() == True:
            self.funType = 0
            for checkBox in self.checkBoxList:
                checkBox.setCheckState(Qt.Unchecked)

            for checkBoxEdit in self.checkBoxEditList:
                checkBoxEdit.setText('')

        else:
            self.funType = 1
            for checkBox in self.checkBoxList:
                checkBox.setCheckState(Qt.Checked)

    def checkBoxClick(self):
        if self.sysBtn.isChecked() == True or self.funType == -1:
            for checkBox in self.checkBoxList:
                checkBox.setCheckState(Qt.Unchecked)

    def checkBoxEditChanged(self, index):
        if self.sysBtn.isChecked() == True or self.funType == -1:
            for checkBoxEdit in self.checkBoxEditList:
                checkBoxEdit.setText('0x0')

    def startScaleBtnClick(self):
        oldImgPath = self.oldImgEdit.text()
        if len(oldImgPath) == 0:
            self.megBoxInfor('')
            return
        if os.path.exists(oldImgPath) == False:
            self.megBoxInfor('')
            return
        newImgPath = self.newImgEdit.text()
        if len(newImgPath) == 0:
            self.megBoxInfor('')
            return
        if os.path.exists(newImgPath) == False:
            self.megBoxInfor('')
            return
        sizeTupList = None
        if self.funType == 1:
            checkCount = 0
            for checkBox in self.checkBoxList:
                if checkBox.checkState() == Qt.Checked:
                    checkCount += 1
                    continue

            if checkCount == 0:
                self.megBoxInfor('')
                return
            titleArr = [
             '@1x', '@2x', '@3x']
            for index in range(0, len(self.checkBoxEditList)):
                checkBox = self.checkBoxList[index]
                checkBoxEdit = self.checkBoxEditList[index]
                checkBoxEditText = checkBoxEdit.text().replace('X', 'x')
                if checkBox.checkState() == Qt.Checked:
                    if 'x' not in checkBoxEditText:
                        self.megBoxInfor('' + titleArr[index] + '(:100x100)')
                        return
                    if zfjTools.is_number(checkBoxEditText.replace('x', '')) == False:
                        self.megBoxInfor('' + titleArr[index] + '(:100x100)')
                        return
                    width = checkBoxEditText[:checkBoxEditText.find('x')]
                    if len(width) == 0:
                        width = '0'
                    height = checkBoxEditText[checkBoxEditText.find('x') + 1:]
                    if len(height) == 0:
                        height = '0'
                    if int(width) <= 0:
                        self.megBoxInfor(titleArr[index] + '<=0(:100x100)')
                        return
                    if int(height) <= 0:
                        self.megBoxInfor(titleArr[index] + '<=0(:100x100)')
                        return
                    sizeTup = (
                     width, height)
                    sizeTupList.append(sizeTup)
                else:
                    sizeTup = (0, 0)
                    sizeTupList.append(sizeTup)

        else:
            if self.funType == 0:
                sizeTupList = []
            else:
                sizeTupList = None
            isCloseAlpha = False
            if self.alphaCheckBox.checkState() == Qt.Checked:
                isCloseAlpha = True
            isUpDateImgType = False
            if self.imgTypeBox.checkState() == Qt.Checked:
                isUpDateImgType = True
            self.textEdit.clear()
            imageScaleObj.startScaleImg(oldImgPath, newImgPath, sizeTupList, isCloseAlpha, isUpDateImgType)

    def reloadUI(self):
        personinfo = ZFJPersoninfo()
        self.accountLab.setText(':' + str(personinfo.account))
        self.timeLab.setText(':' + personinfo.expireDate.replace('"', ''))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def megBoxInfor(self, infor):
        QMessageBox.information(self, '', infor, QMessageBox.Yes)


def addTextEdit(log_str):
    personinfo = ZFJPersoninfo()
    scaleView = personinfo.scaleView
    if scaleView != None:
        str_text = scaleView.textEdit.toPlainText()
        str_text += log_str + '\n'
        scaleView.textEdit.setPlainText(str_text)
        scaleView.textEdit.moveCursor(QTextCursor.End)
        QApplication.processEvents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    scaleView = ImgScaleView()
    personinfo = ZFJPersoninfo()
    personinfo.scaleView = scaleView
    scaleView.show()
    sys.exit(app.exec_())