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
from PyQt5.QtGui import QPixmap
from singletonModel import ZFJPersoninfo
import zfjTools, confusionLog as conLog
from threading import Thread
import subprocess, requests, webbrowser
from rootViewUI import rootView
from imageScaleView import ImgScaleView
from reptileView import ReptileView
from DeveLexiconUI import DeveLexiconView
from missPrefixView import PrefixView
from cleanRubResView import CleanResView
viewWid = 625
viewHei = 565
margin_size = 10
_translate = QtCore.QCoreApplication.translate

class MainRootView(QWidget):

    def __init__(self):
        super().__init__()
        self.defaultView()
        self.initUI()

    def defaultView(self):
        self.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        self.resize(viewWid, viewHei)
        self.setFixedSize(viewWid, viewHei)
        self.setStyleSheet('background-color:#fff')
        self.center()
        self.setWindowTitle(zfjTools.baseTitle)

    def initUI(self):
        font = QtGui.QFont()
        font.setPointSize(20)
        margin_top = margin_size * 2
        picUrl = 'http://cdn.5151study.com/media_blog_27465911382665_2019_07_19_10_47_16_653_5051_wh754x186.jpg'
        req_Logo = requests.get(picUrl)
        pix = QPixmap()
        pix.loadFromData(req_Logo.content)
        titleLab = QLabel(self)
        titleLab.setStyleSheet('background-color:#dcdcdc;')
        titleLab.setGeometry(QtCore.QRect((viewWid - 210) / 2, margin_top, 210, 52))
        titleLab.setPixmap(pix)
        titleLab.setScaledContents(True)
        margin_top += 52 + margin_size
        funTitLab = QLabel('功能', self)
        funTitLab.setStyleSheet('color:#111a1b;')
        funTitLab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        funTitLab.setGeometry(QtCore.QRect(margin_size, margin_top, viewWid - margin_size * 2, 30))
        font.setPointSize(18)
        funTitLab.setFont(font)
        margin_top += 30
        line_lab_0 = QLabel(self)
        line_lab_0.setStyleSheet('background-color:#dcdcdc')
        line_lab_0.setGeometry(QtCore.QRect(margin_size, margin_top, viewWid - margin_size * 2, 1))
        margin_top += 1 + margin_size * 2
        line_count = 3
        funButton_hei = 45
        funButton_wid = (viewWid - margin_size * 2 * (line_count + 1)) // line_count
        funTitleArr = ['代码混淆', '图片压缩', '爬虫工具', '混淆词库', '混淆前缀', '资源清理']
        this_margin_top = margin_top
        for index in range(0, len(funTitleArr)):
            funButton_x = margin_size * 2 + (funButton_wid + margin_size * 2) * (index % line_count)
            funButton_y = (funButton_hei + margin_size * 2) * (index // line_count) + this_margin_top
            funButton = QtWidgets.QPushButton(self)
            funButton.setGeometry(QtCore.QRect(funButton_x, funButton_y, funButton_wid, funButton_hei))
            funButton.setText(_translate('MainWindow', funTitleArr[index]))
            funButton.setStyleSheet('color:#c13677;background-color:#efeff3;border:1px solid #efeff3;')
            font.setPointSize(16)
            funButton.setFont(font)
            if index == 0:
                funButton.clicked.connect(self.missBtnClick)
            else:
                if index == 1:
                    funButton.clicked.connect(self.imageScaleBtnClick)
                else:
                    if index == 2:
                        funButton.clicked.connect(self.reptileBtnClick)
                    else:
                        if index == 3:
                            funButton.clicked.connect(self.missWordBtnClick)
                        else:
                            if index == 4:
                                funButton.clicked.connect(self.missPrefixBtnClick)
                            else:
                                if index == 5:
                                    funButton.clicked.connect(self.cleanResBtnClick)
            margin_top = funButton_y + funButton_hei

        margin_top += margin_size * 2
        helpTitLab = QLabel('帮助', self)
        helpTitLab.setStyleSheet('color:#111a1b;')
        helpTitLab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        helpTitLab.setGeometry(QtCore.QRect(margin_size, margin_top, viewWid - margin_size * 2, 30))
        font.setPointSize(18)
        helpTitLab.setFont(font)
        margin_top += 30
        line_lab_1 = QLabel(self)
        line_lab_1.setStyleSheet('background-color:#dcdcdc')
        line_lab_1.setGeometry(QtCore.QRect(margin_size, margin_top, viewWid - margin_size * 2, 1))
        margin_top += 1 + margin_size * 2
        funTitleArr = ['详细介绍', '错误汇总', 'Git']
        this_margin_top = margin_top
        for index in range(0, len(funTitleArr)):
            funButton_x = margin_size * 2 + (funButton_wid + margin_size * 2) * (index % line_count)
            funButton_y = (funButton_hei + margin_size * 2) * (index // line_count) + this_margin_top
            funButton = QtWidgets.QPushButton(self)
            funButton.setGeometry(QtCore.QRect(funButton_x, funButton_y, funButton_wid, funButton_hei))
            funButton.setText(_translate('MainWindow', funTitleArr[index]))
            funButton.setStyleSheet('color:#c13677;background-color:#efeff3;border:1px solid #efeff3;')
            font.setPointSize(16)
            funButton.setFont(font)
            if index == 0:
                funButton.clicked.connect(self.detailBtnClick)
            else:
                if index == 1:
                    funButton.clicked.connect(self.errorBtnClick)
                else:
                    if index == 2:
                        funButton.clicked.connect(self.gitBtnClick)
            margin_top = funButton_y + funButton_hei

        margin_top += margin_size * 2
        helpTitLab = QLabel('说明', self)
        helpTitLab.setStyleSheet('color:#111a1b;')
        helpTitLab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        helpTitLab.setGeometry(QtCore.QRect(margin_size, margin_top, viewWid - margin_size * 2, 30))
        font.setPointSize(18)
        helpTitLab.setFont(font)
        margin_top += 30
        line_lab_1 = QLabel(self)
        line_lab_1.setStyleSheet('background-color:#dcdcdc')
        line_lab_1.setGeometry(QtCore.QRect(margin_size, margin_top, viewWid - margin_size * 2, 1))
        margin_top += 1 + margin_size * 2
        infor = '1.使用此软件可能会产生一些小问题,非专业iOS开发人员慎用;\n'
        infor += '2.项目混淆不承诺必过审核,因为人工审核无法控制;\n'
        infor += '3.元数据信息要和以前的项目不同,元数据包括但不限于APP名称、描述、关键词、LOGO、介绍图、网址等;\n'
        infor += '4.一个ZFJObsL ib账号只能在一台电脑上使用，即注册电脑(特别版除外😂);\n'
        infor += '5.混淆项目的时候请复制一份新的项目进行混淆，备份原有项目;'
        detailLab = QLabel(infor, self)
        detailLab.setWordWrap(True)
        detailLab.setStyleSheet('color:#c13677;')
        detailLab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        detailLab.setGeometry(QtCore.QRect(margin_size * 2, margin_top, viewWid - margin_size * 4, 115))
        font.setPointSize(14)
        detailLab.setFont(font)
        margin_top += 115 + margin_size * 2

    def missBtnClick(self):
        personinfo = ZFJPersoninfo()
        if personinfo.rootView != None:
            personinfo.rootView.show()
        else:
            root_View = rootView()
            root_View.show()
            personinfo.rootView = root_View
        self.close()

    def imageScaleBtnClick(self):
        personinfo = ZFJPersoninfo()
        if personinfo.scaleView == None:
            scaleView = ImgScaleView()
            scaleView.show()
            personinfo.scaleView = scaleView
        else:
            personinfo.scaleView.show()
        self.close()

    def reptileBtnClick(self):
        personinfo = ZFJPersoninfo()
        if personinfo.reptileView == None:
            reptileView = ReptileView()
            reptileView.show()
            personinfo.reptileView = reptileView
        else:
            personinfo.reptileView.show()
        self.close()

    def missWordBtnClick(self):
        personinfo = ZFJPersoninfo()
        if personinfo.lexiconView == None:
            lexiconView = DeveLexiconView()
            lexiconView.show()
            personinfo.lexiconView = lexiconView
        else:
            personinfo.lexiconView.show()
        self.close()

    def missPrefixBtnClick(self):
        personinfo = ZFJPersoninfo()
        if personinfo.missPrefixView == None:
            missPrefixView = PrefixView()
            missPrefixView.show()
            personinfo.missPrefixView = missPrefixView
        else:
            personinfo.missPrefixView.show()
        self.close()

    def cleanResBtnClick(self):
        personinfo = ZFJPersoninfo()
        if personinfo.cleanResView == None:
            cleanResView = CleanResView()
            cleanResView.show()
            personinfo.cleanResView = cleanResView
        else:
            personinfo.cleanResView.show()
        self.close()

    def detailBtnClick(self):
        url = 'https://zfj1128.blog.csdn.net/article/details/95482006'
        webbrowser.open_new_tab(url)

    def errorBtnClick(self):
        meg = '1.方法名相同，被多次混淆覆盖;\n'
        meg += '2.忽略的文件夹中包含了已被混淆的类或者方法;\n'
        meg += '3.图片如果不显示，可能原因是代码中图片名采用的是拼接的，手动替换一下就可以了;\n'
        meg += '4.如果出现项目路径修改了，但是本地实体路径没有修改，自己手动把本地路径修改一下;\n'
        meg += '5.utf-8编码错误和[Errno 13] Permission denied权限错误不用管;\n'
        self.megBoxInfor(meg)

    def gitBtnClick(self):
        url = 'https://gitee.com/zfj1128/ZFJObsLib_dmg'
        webbrowser.open_new_tab(url)

    def megBoxInfor(self, infor):
        QMessageBox.information(self, '', infor, QMessageBox.Yes)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainRootView = MainRootView()
    mainRootView.show()
    personinfo = ZFJPersoninfo()
    personinfo.mainRootView = mainRootView
    sys.exit(app.exec_())