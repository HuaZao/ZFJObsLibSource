#! /usr/bin/env python 3.7 (3394)
#coding=utf-8
# Compiled at: 1969-12-31 18:00:00
#Powered by BugScaner
#http://tools.bugscaner.com/
#如果觉得不错,请分享给你朋友使用吧!
import reptileService, sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QLabel, QMessageBox, QLineEdit, QRadioButton, QCheckBox, QTextEdit, QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QTextCursor
from singletonModel import ZFJPersoninfo
import zfjTools, imageScaleObj, os, re, userAgentList, requests, subprocess, random, base64
viewWid = 625
viewHei = 629
margin_size = 10
headers = {'User-Agent': userAgentList.getUserAgent()}
_translate = QtCore.QCoreApplication.translate

class ReptileView(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.defaultView()
        self.reloadUI()
        self.reptileType = -1
        self.errorPath = ''

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
        titleLab = QLabel('爬虫工具', self)
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
        addLab = QLabel('请输入爬取地址:', self)
        addLab.setStyleSheet('color:#000000;')
        addLab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        addLab.setGeometry(QtCore.QRect(margin_size, margin_top, 110, 30))
        font.setPointSize(14)
        addLab.setFont(font)
        self.addEdit = QtWidgets.QLineEdit(self)
        self.addEdit.setGeometry(QtCore.QRect(110 + margin_size * 2, margin_top, viewWid - 110 - margin_size * 3, 30))
        font.setPointSize(14)
        self.addEdit.setFont(font)
        self.addEdit.setText('https://m.mzitu.com/23463')
        margin_top += 30 + margin_size
        line_lab = QLabel(self)
        line_lab.setStyleSheet('background-color:#dcdcdc')
        line_lab.setGeometry(QtCore.QRect(0, margin_top, viewWid, 1))
        margin_top += 1 + margin_size
        smlTitLab = QLabel('爬取方式', self)
        smlTitLab.setStyleSheet('color:#d4237a;')
        smlTitLab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        smlTitLab.setGeometry(QtCore.QRect(margin_size, margin_top, 135, 30))
        smlTitLab.setFont(font)
        margin_top += 30 + margin_size
        self.sysBtn = QRadioButton('自动爬取资源文件', self)
        self.sysBtn.setStyleSheet('color:#000;')
        self.sysBtn.setGeometry(QtCore.QRect(margin_size * 2, margin_top, 200, 30))
        self.sysBtn.setChecked(False)
        self.sysBtn.toggled.connect(lambda : self.radioBtnClick())
        margin_top += 30 + margin_size
        self.checkBoxList = []
        titLabArr = ['图片资源', '音频资源', '视频资源']
        for index in range(0, len(titLabArr)):
            margin_x = margin_size * 4 + (90 + margin_size * 4) * index
            checkBox = QCheckBox(titLabArr[index], self)
            checkBox.setStyleSheet('color:#000;')
            checkBox.stateChanged.connect(self.checkBoxClick)
            checkBox.setGeometry(QtCore.QRect(margin_x, margin_top, 90, 30))
            self.checkBoxList.append(checkBox)

        margin_top += 30 + margin_size
        self.customBtn = QRadioButton('自定义爬取节点', self)
        self.customBtn.setStyleSheet('color:#000;')
        self.customBtn.setGeometry(QtCore.QRect(margin_size * 2, margin_top, 200, 30))
        self.customBtn.setChecked(False)
        self.customBtn.toggled.connect(lambda : self.radioBtnClick())
        margin_top += 30 + margin_size
        nodeTitLabWid = 48
        fatherLab = QLabel('父节点:', self)
        fatherLab.setStyleSheet('color:#000;')
        fatherLab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        fatherLab.setGeometry(QtCore.QRect(margin_size * 4, margin_top, nodeTitLabWid, 30))
        font.setPointSize(14)
        fatherLab.setFont(font)
        editWid = (viewWid - margin_size * 11 - nodeTitLabWid * 2) / 2
        self.fatherNodeEdit = QtWidgets.QLineEdit(self)
        self.fatherNodeEdit.setGeometry(QtCore.QRect(margin_size * 5 + nodeTitLabWid, margin_top, editWid, 30))
        font.setPointSize(14)
        self.fatherNodeEdit.setFont(font)
        self.fatherNodeEdit.setText('//div[@class="pMain"]/div')
        childLab = QLabel('子节点:', self)
        childLab.setStyleSheet('color:#000;')
        childLab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        childLab.setGeometry(QtCore.QRect(margin_size * 6 + 45 + editWid, margin_top, nodeTitLabWid, 30))
        font.setPointSize(14)
        childLab.setFont(font)
        self.childNodeEdit = QtWidgets.QLineEdit(self)
        self.childNodeEdit.setGeometry(QtCore.QRect(margin_size * 7 + nodeTitLabWid * 2 + editWid, margin_top, editWid, 30))
        font.setPointSize(14)
        self.childNodeEdit.setFont(font)
        self.childNodeEdit.setText('./a/img/@src')
        margin_top += 38
        tipsLab = QLabel('例如:父节点//div[@class="pMain"]/div,子节点./a/img/@src;使用此功能需知晓XPath规则!', self)
        tipsLab.setStyleSheet('color:#87b753;')
        tipsLab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        tipsLab.setGeometry(QtCore.QRect(margin_size * 4, margin_top, viewWid - margin_size * 8, 20))
        font.setPointSize(12)
        tipsLab.setFont(font)
        margin_top += 20 + margin_size
        smlTitLab = QLabel('储存路径', self)
        smlTitLab.setStyleSheet('color:#d4237a;')
        smlTitLab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        smlTitLab.setGeometry(QtCore.QRect(margin_size, margin_top, 135, 30))
        font.setPointSize(14)
        smlTitLab.setFont(font)
        margin_top += 30 + margin_size
        pathEditWid = viewWid - margin_size * 5 - 100
        self.pathEdit = QtWidgets.QLineEdit(self)
        self.pathEdit.setGeometry(QtCore.QRect(margin_size * 2, margin_top, pathEditWid, 30))
        font.setPointSize(14)
        self.pathEdit.setFont(font)
        self.pathEdit.setText('/Users/zhangfujie/Desktop/Obfuscated')
        pathBtn = QtWidgets.QPushButton(self)
        pathBtn.setGeometry(QtCore.QRect(margin_size * 3 + pathEditWid, margin_top, 100, 30))
        pathBtn.setText(_translate('MainWindow', '选择文件夹'))
        pathBtn.setStyleSheet('color:#000000;background-color:#efeff3;border:1px solid #efeff3;')
        pathBtn.clicked.connect(self.pathBtnClick)
        pathBtn.setFont(font)
        margin_top += 30 + margin_size
        stateTitLab = QLabel('爬取结果', self)
        stateTitLab.setStyleSheet('color:#d4237a;')
        stateTitLab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        stateTitLab.setGeometry(QtCore.QRect(margin_size, margin_top, 135, 30))
        font.setPointSize(14)
        stateTitLab.setFont(font)
        margin_top += 30 + margin_size
        self.resultLab = QLabel('暂无爬取数据', self)
        self.resultLab.setStyleSheet('color:#000;')
        self.resultLab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.resultLab.setGeometry(QtCore.QRect(margin_size * 2, margin_top, viewWid - margin_size * 4, 30))
        font.setPointSize(12)
        self.resultLab.setFont(font)
        margin_top += 30 + margin_size * 5
        startReptileBtn = QtWidgets.QPushButton(self)
        startReptileBtn.setGeometry(QtCore.QRect((viewWid - 160) / 2, margin_top, 160, 40))
        startReptileBtn.setText(_translate('MainWindow', '开始爬取'))
        startReptileBtn.setStyleSheet('background-color:#fff;color:#cc0066;border:1px solid #cc0066;')
        startReptileBtn.clicked.connect(self.startReptileBtnClick)
        font.setPointSize(18)
        startReptileBtn.setFont(font)
        margin_top += 30 + margin_size * 2
        self.showLab = QLabel('--', self)
        self.showLab.setStyleSheet('color:#87b753;')
        self.showLab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.showLab.setGeometry(QtCore.QRect(margin_size * 2, margin_top, pathEditWid, 30))
        font.setPointSize(12)
        self.showLab.setFont(font)
        errorBtn = QtWidgets.QPushButton(self)
        errorBtn.setGeometry(QtCore.QRect(margin_size * 3 + pathEditWid + margin_size + 5, margin_top, 100, 30))
        errorBtn.setText(_translate('MainWindow', '查看错误列表'))
        errorBtn.setStyleSheet('color:#87b753;border:1px solid #fff;')
        errorBtn.clicked.connect(self.errorBtnClick)
        errorBtn.setFont(font)
        margin_top += 30 + margin_size
        line_lab_1 = QLabel(self)
        line_lab_1.setStyleSheet('background-color:#dcdcdc')
        line_lab_1.setGeometry(QtCore.QRect(0, margin_top, viewWid, 1))
        margin_top += 1 + margin_size
        downLab_wid = (viewWid - margin_size * 3) / 2
        self.accountLab = QLabel('账号:', self)
        self.accountLab.setStyleSheet('color:#000;')
        self.accountLab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.accountLab.setGeometry(QtCore.QRect(margin_size, margin_top, downLab_wid, 30))
        font.setPointSize(13)
        self.accountLab.setFont(font)
        self.timeLab = QLabel('时间:', self)
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

    def startReptileBtnClick(self):
        url = self.addEdit.text().strip()
        if len(url) == 0:
            self.megBoxInfor('')
            return
        if self.reptileType == -1:
            self.megBoxInfor('')
            return
        savePath = self.pathEdit.text()
        if len(savePath) == 0:
            self.megBoxInfor('')
            return
        if os.path.exists(savePath) == False:
            self.megBoxInfor('')
            return
        if not savePath.endswith('/'):
            savePath += '/'
        self.errorPath = savePath + 'error.txt'
        if os.path.exists(self.errorPath) == False:
            open(self.errorPath, 'w').close()
        resultLabText = ''
        if self.reptileType == 0:
            checkCount = 0
            for checkBox in self.checkBoxList:
                if checkBox.checkState() == Qt.Checked:
                    checkCount += 1
                    continue

            if checkCount == 0:
                self.megBoxInfor('')
                return
            isImage = True if self.checkBoxList[0].checkState() == Qt.Checked else False
            isAudio = True if self.checkBoxList[1].checkState() == Qt.Checked else False
            isVideo = True if self.checkBoxList[2].checkState() == Qt.Checked else False
            self.showLab.setText('......')
            tub = reptileService.getResourceUrlList(url, isImage, isAudio, isVideo)
            if isImage == True:
                resultLabText += ' ' + str(len(tub[0])) + ''
                self.imagePath = savePath + './images'
                if os.path.exists(self.imagePath) == False:
                    os.mkdir(self.imagePath)
            if isAudio == True:
                resultLabText += ' ' + str(len(tub[1])) + ''
                self.audioPath = savePath + './audios'
                if os.path.exists(self.audioPath) == False:
                    os.mkdir(self.audioPath)
            if isVideo == True:
                resultLabText += ' ' + str(len(tub[2])) + ''
                self.videPath = savePath + './vides'
                if os.path.exists(self.videPath) == False:
                    os.mkdir(self.videPath)
            self.resultLab.setText(resultLabText)
            self.saveResourceTub(tub)
        else:
            if self.reptileType == 1:
                fatherNode = self.fatherNodeEdit.text().strip().replace(',', ',').strip(',').strip()
                if len(fatherNode) == 0:
                    self.megBoxInfor('')
                    return
                childNode = self.childNodeEdit.text().strip().replace(',', ',').strip(',').strip()
                if len(childNode) == 0:
                    self.megBoxInfor('')
                    return
                savePath = self.pathEdit.text()
                if len(savePath) == 0:
                    self.megBoxInfor('')
                    return
                if os.path.exists(savePath) == False:
                    self.megBoxInfor('')
                    return
                if not savePath.endswith('/'):
                    savePath += '/'
                self.errorPath = savePath + 'error.txt'
                if os.path.exists(self.errorPath) == False:
                    open(self.errorPath, 'w').close()
                self.showLab.setText('......')
                dataArray = reptileService.getNoteInfors(url, fatherNode, childNode)
                resultLabText += ' ' + str(len(dataArray)) + ''
                self.resultLab.setText(resultLabText)
                self.saveNodeData(dataArray, savePath)

    def saveResourceTub(self, tub):
        global headers
        errorStr = ''
        isImage = True if self.checkBoxList[0].checkState() == Qt.Checked else False
        isAudio = True if self.checkBoxList[1].checkState() == Qt.Checked else False
        isVideo = True if self.checkBoxList[2].checkState() == Qt.Checked else False
        if isImage == True:
            imageUrlList = tub[0]
            for index in range(0, len(imageUrlList)):
                imageObj = imageUrlList[index]
                if '$==$' in imageObj:
                    imageName = imageObj.split('$==$')[0]
                    imgUrl = imageObj.split('$==$')[-1]
                    img = base64.urlsafe_b64decode(imgUrl + '=' * (4 - len(imgUrl) % 4))
                    try:
                        open(self.imagePath + '/' + imageName, 'wb').write(img)
                    except Exception as e:
                        try:
                            errorStr += 'image:data:image;' + imageObj.split('$==$')[-1] + '\n'
                        finally:
                            e = None
                            del e

                else:
                    headers['Referer'] = imageObj
                    imageName = zfjTools.getTimestamp() + str(random.randint(100, 999)) + str(random.randint(10, 99)) + '.' + imageObj.split('.')[-1]
                    req = requests.get(imageObj, headers=headers, stream=True)
                    if req.status_code == 200:
                        try:
                            open(self.imagePath + '/' + imageName, 'wb').write(req.content)
                        except Exception as e:
                            try:
                                errorStr += 'image:' + imageObj + '\n'
                            finally:
                                e = None
                                del e

                    else:
                        errorStr += 'image:' + imageObj + '\n'
                    self.showLab.setText('' + str(index + 1) + '')
                    QApplication.processEvents()

        if isAudio == True:
            audioUrlList = tub[1]
            for index in range(0, len(audioUrlList)):
                audioUrl = audioUrlList[index]
                headers['Referer'] = audioUrl
                imageName = zfjTools.getTimestamp() + str(random.randint(100, 999)) + str(random.randint(10, 99)) + '.' + audioUrl.split('.')[-1]
                req = requests.get(audioUrl, headers=headers, stream=True)
                if req.status_code == 200:
                    try:
                        open(self.audioPath + '/' + imageName, 'wb').write(req.content)
                    except Exception as e:
                        try:
                            errorStr += 'audio:' + imageObj + '\n'
                        finally:
                            e = None
                            del e

                else:
                    errorStr += 'audio:' + imageObj + '\n'
                self.showLab.setText('' + str(index + 1) + '')
                QApplication.processEvents()

        if isVideo == True:
            videoUrlList = tub[2]
            for index in range(0, len(videoUrlList)):
                videoUr = videoUrlList[index]
                headers['Referer'] = videoUr
                imageName = zfjTools.getTimestamp() + str(random.randint(100, 999)) + str(random.randint(10, 99)) + '.' + videoUr.split('.')[-1]
                req = requests.get(videoUr, headers=headers, stream=True)
                if req.status_code == 200:
                    try:
                        open(self.videPath + '/' + imageName, 'wb').write(req.content)
                    except Exception as e:
                        try:
                            errorStr += 'video:' + imageObj + '\n'
                        finally:
                            e = None
                            del e

                else:
                    errorStr += 'video:' + imageObj + '\n'
                self.showLab.setText('' + str(index + 1) + '')
                QApplication.processEvents()

        self.showLab.setText('')
        QApplication.processEvents()
        if len(errorStr) > 0:
            if len(self.errorPath) > 0:
                open(self.errorPath, 'w').write(errorStr)

    def saveNodeData(self, dataArray, savePath):
        if len(dataArray) == 0:
            self.showLab.setText('')
            return
        self.showLab.setText('')
        nodesDataPath = savePath + 'nodes:' + zfjTools.getTimestamp() + '.txt'
        if os.path.exists(nodesDataPath) == False:
            open(nodesDataPath, 'w').close()
        dataStr = ''
        for item in dataArray:
            dataStr += str(item) + '\n'

        open(nodesDataPath, 'w').write(dataStr)
        self.showLab.setText('')
        subprocess.call(['open', nodesDataPath])

    def regularVerification(self, node):
        mail = re.compile('^([a-zA-z])+\\[@class="+[A-Z0-9a-z._+-]+"+\\]$')
        if re.search(mail, node):
            return True
        else:
            return False

    def pathBtnClick(self):
        file_dir = ''
        try:
            file_dir = QFileDialog.getExistingDirectory(self, 'open file', '/Users/')
        except Exception as e:
            try:
                file_dir = ','
            finally:
                e = None
                del e

        self.pathEdit.setText(file_dir)

    def errorBtnClick(self):
        if len(self.errorPath) == 0:
            self.megBoxInfor('')
        else:
            subprocess.call(['open', self.errorPath])

    def radioBtnClick(self):
        if self.sysBtn.isChecked() == True:
            self.reptileType = 0
        else:
            if self.customBtn.isChecked() == True:
                self.reptileType = 1
                for checkBox in self.checkBoxList:
                    checkBox.setCheckState(Qt.Unchecked)

    def checkBoxClick(self):
        if self.sysBtn.isChecked() != True:
            for checkBox in self.checkBoxList:
                checkBox.setCheckState(Qt.Unchecked)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    reptileView = ReptileView()
    personinfo = ZFJPersoninfo()
    personinfo.reptileView = reptileView
    reptileView.show()
    sys.exit(app.exec_())