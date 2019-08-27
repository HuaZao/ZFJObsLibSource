import sys, os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QLabel, QMessageBox, QCheckBox, QTextEdit, QFileDialog, QMenuBar
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QTextCursor, QIcon
import main_codeObf as codeObf, ignoreFiles, webbrowser, subprocess
from singletonModel import ZFJPersoninfo
from mapListView import mapListView
import datetime, pytz, zfjTools, requests
logIn_wid = 1360
logIn_hei = 751
margin_size = 10
_translate = QtCore.QCoreApplication.translate
_funMap = {}
_checkBoxList = []
_downBtnList = []
 
class rootView(QWidget):
 
    def __init__(self):
        super().__init__()
        self.defaultView()
        self.initUI()
        self.reloadUI()
 
    def defaultView(self):
        self.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        self.resize(logIn_wid, logIn_hei)
        self.setFixedSize(logIn_wid, logIn_hei)
        self.setStyleSheet('background-color:#fff')
        self.center()
        self.setWindowTitle(zfjTools.baseTitle)
        personinfo = ZFJPersoninfo()
        personinfo.prefixMap = zfjTools.readPrefixMap()
 
    def initUI(self):
        font = QtGui.QFont()
        font.setPointSize(14)
        margin_top = margin_size
        titleLab = QLabel('iOS混淆工具', self)
        titleLab.setStyleSheet('color:#d4237a;')
        titleLab.setAlignment(Qt.AlignCenter)
        titleLab.setGeometry(QtCore.QRect(margin_size, margin_top, logIn_wid / 2 - margin_size * 2, 40))
        font.setPointSize(18)
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
        pathLab = QLabel('请选择文件夹所在路径:', self)
        pathLab.setStyleSheet('color:#000000')
        pathLab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        pathLab.setGeometry(QtCore.QRect(margin_size, margin_top, 150, 30))
        font.setPointSize(14)
        pathLab.setFont(font)
        self.pathEdit = QtWidgets.QLineEdit(self)
        self.pathEdit.setGeometry(QtCore.QRect(150 + margin_size * 2, margin_top, 350, 30))
        self.pathEdit.setFont(font)
        self.pathEdit.setText('......')
        choicePathBtn = QtWidgets.QPushButton(self)
        choicePathBtn.setGeometry(QtCore.QRect(margin_size * 3 + 150 + 350, margin_top, 100, 30))
        choicePathBtn.setObjectName('logInBtn')
        choicePathBtn.setText(_translate('MainWindow', '选择文件夹'))
        choicePathBtn.setStyleSheet('color:#000000;background-color:#efeff3;border:1px solid #efeff3;')
        choicePathBtn.clicked.connect(self.choicePathBtnClick)
        choicePathBtn.setFont(font)
        margin_top += margin_size + 30
        ignoreLab = QLabel('请输入要忽略的文件&文件夹:', self)
        ignoreLab.setStyleSheet('color:#000')
        ignoreLab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        ignoreLab.setGeometry(QtCore.QRect(margin_size, margin_top, 150, 30))
        ignoreLab.setFont(font)
        self.ignoreEdit = QtWidgets.QLineEdit(self)
        self.ignoreEdit.setGeometry(QtCore.QRect(150 + margin_size * 2, margin_top, 350, 30))
        self.ignoreEdit.setFont(font)
        self.ignoreEdit.setText('Pods,Vendor,LIB,Util,Lib,lib')
        font.setPointSize(12)
        ignoreTips = QLabel('*多个文件&文件夹请用,号分割', self)
        ignoreTips.setStyleSheet('color:#cc0066')
        ignoreTips.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        ignoreTips.setGeometry(QtCore.QRect(margin_size * 3 + 150 + 350, margin_top, 140, 30))
        ignoreTips.setFont(font)
        margin_top += margin_size * 2 + 30
        left_part_wid = margin_size * 4 + 150 + 350 + 140
        line_lab = QLabel(self)
        line_lab.setStyleSheet('background-color:#dcdcdc')
        line_lab.setGeometry(QtCore.QRect(0, margin_top, left_part_wid, 1))
        line_vertical = QLabel(self)
        line_vertical.setStyleSheet('background-color:#dcdcdc')
        line_vertical.setGeometry(QtCore.QRect(left_part_wid, 0, 1, logIn_hei))
        margin_top += margin_size * 1
        font.setPointSize(14)
        choiceFunLab = QLabel('请选择需要开启的功能:', self)
        choiceFunLab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        choiceFunLab.setGeometry(QtCore.QRect(margin_size, margin_top, 150, 30))
        choiceFunLab.setFont(font)
        tipsBtn = QtWidgets.QPushButton(self)
        tipsBtn.setGeometry(QtCore.QRect(left_part_wid - 60 - margin_size, margin_top, 60, 30))
        tipsBtn.setText(_translate('MainWindow', '*特别说明'))
        tipsBtn.setStyleSheet('background-color:#fff;color:#cc0066;border:1px solid #fff;')
        tipsBtn.clicked.connect(self.tipsBtnClick)
        font.setPointSize(13)
        tipsBtn.setFont(font)
        margin_top += margin_size + 30
        checkBox_wid = (left_part_wid - margin_size * 6) / 2
        checkBox_hei = 30
        fun_list = [
         '属性混淆',
         '类名混淆',
         '方法混淆',
         '修改资源Hash值',
         '翻新资源名',
         '添加垃圾代码和垃圾类(垃圾类为0不创建)',
         '加密字符串',
         '-添加次数',
         '删除注释',
         '修改项目工程名',
         '混淆文件目录',
         '-手动设置项目名']
        self.fun_key_list = [
         'property',
         'objName',
         'funName',
         'souHashKey',
         'upSouName',
         'rubbishCode',
         'encryStr',
         'rubbishLine',
         'deleteNotes',
         'misProjectName',
         'missFolder',
         'setProjectName'
         ]
        this_margin_top = margin_top
        for index in range(0, len(fun_list)):
            part_checkBox_wid = checkBox_wid
            checkBox = QCheckBox(fun_list[index].replace('-', ''), self)
            checkBox_x = margin_size * 2 + (checkBox_wid + margin_size * 2) * (index % 2)
            checkBox_y = (checkBox_hei + margin_size * 2) * (index // 2) + this_margin_top
            checkBox.stateChanged.connect(self.checkBoxClick)
            if fun_list[index].startswith('-'):
                checkBox_x += margin_size * 2
                part_checkBox_wid -= margin_size * 3
            if index == 7:
                checkBox.setGeometry(QtCore.QRect(checkBox_x, checkBox_y, 77, checkBox_hei))
                checkBox_x += 77 + margin_size
                self.amountEdit = QtWidgets.QLineEdit(self)
                self.amountEdit.setGeometry(QtCore.QRect(checkBox_x, checkBox_y, 46, checkBox_hei))
                self.amountEdit.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
                self.amountEdit.setFont(font)
                self.amountEdit.setText('5')
                self.amountEdit.setStyleSheet('color:#cc0066')
                checkBox_x += 46 + margin_size
                self.rubClsTieBox = QCheckBox('垃圾类数量', self)
                self.rubClsTieBox.setStyleSheet('background-color:#ebeaeb')
                self.rubClsTieBox.setGeometry(QtCore.QRect(checkBox_x, checkBox_y, 91, checkBox_hei))
                self.rubClsTieBox.setFont(font)
                self.rubClsTieBox.stateChanged.connect(self.checkBoxClick)
                checkBox_x += 91 + margin_size
                self.rubClsEdit = QtWidgets.QLineEdit(self)
                self.rubClsEdit.setGeometry(QtCore.QRect(checkBox_x, checkBox_y, 46, checkBox_hei))
                self.rubClsEdit.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
                self.rubClsEdit.setFont(font)
                self.rubClsEdit.setText('3')
                self.rubClsEdit.setStyleSheet('color:#cc0066')
            else:
                if index == 11:
                    checkBox.setGeometry(QtCore.QRect(checkBox_x, checkBox_y, 130, checkBox_hei))
                    self.projectNameEdit = QtWidgets.QLineEdit(self)
                    self.projectNameEdit.setGeometry(QtCore.QRect(130 + margin_size + checkBox_x, checkBox_y, 100, checkBox_hei))
                    self.projectNameEdit.setFont(font)
                    self.projectNameEdit.setStyleSheet('color:#cc0066')
                    #这里好像是原作者强制指定工程名,先注释了,需要再打开
                    # personinfo = ZFJPersoninfo()
                    # prefixMap = personinfo.prefixMap
                    # if 'projectNamePreFix' in prefixMap.keys():
                    self.projectNameEdit.setText("iOSProject")
                    # 
                else:
                    checkBox.setGeometry(QtCore.QRect(checkBox_x, checkBox_y, part_checkBox_wid, checkBox_hei))
                    checkBox.setStyleSheet('background-color:#ebeaeb')
                    checkBox.setFont(font)
            _checkBoxList.append(checkBox)       
            _funMap[self.fun_key_list[index]] = '0'
            margin_top = checkBox_y
 
        margin_top += margin_size * 7 + checkBox_hei
        startMissBtn = QtWidgets.QPushButton(self)
        startMissBtn.setGeometry(QtCore.QRect((left_part_wid - 160) / 2, margin_top, 160, 40))
        startMissBtn.setObjectName('startMissBtn')
        startMissBtn.setText(_translate('MainWindow', '开始混淆'))
        startMissBtn.setStyleSheet('background-color:#fff;color:#cc0066;border:1px solid #cc0066;')
        startMissBtn.clicked.connect(self.startMissBtnClick)
        font.setPointSize(18)
        startMissBtn.setFont(font)
        tipsLab = QLabel('为了方便修改产生的错误,建议功能一项一项使用,错误修改完成以后再进行其他操作!', self)
        tipsLab.setStyleSheet('color:#cc0066;')
        tipsLab.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        tipsLab.setGeometry(QtCore.QRect((left_part_wid - 500) / 2, margin_top + 40 + 8, 500, 20))
        font.setPointSize(12)
        tipsLab.setFont(font)
        margin_top += margin_size * 7 + 40
        detailBtn_wid = 130
        detailBtn_list = ['查看详细说明', '打开混淆日志', '查看映射列表', '清空右侧日志']
        detailBtn_space = (left_part_wid - detailBtn_wid * len(detailBtn_list)) / (len(detailBtn_list) + 1)
        for index in range(0, len(detailBtn_list)):
            detailBtn = QtWidgets.QPushButton(self)
            detailBtn.setGeometry(QtCore.QRect(detailBtn_space + (detailBtn_wid + detailBtn_space) * index, margin_top, detailBtn_wid, 30))
            detailBtn.setText(_translate('MainWindow', detailBtn_list[index]))
            detailBtn.setStyleSheet('background-color:#fff;color:#87b753;border:1px solid #87b753;')
            font.setPointSize(13)
            detailBtn.setFont(font)
            _downBtnList.append(detailBtn)
            if index == 0:
                detailBtn.clicked.connect(self.showDetailInfor)
            else:
                if index == 1:
                    detailBtn.clicked.connect(self.openConfusedLog)
                else:
                    if index == 2:
                        detailBtn.clicked.connect(self.showMapList)
                    else:
                        if index == 3:
                            detailBtn.clicked.connect(self.cleanTextEdit)
 
        margin_top += margin_size + 30
        line_lab_1 = QLabel(self)
        line_lab_1.setStyleSheet('background-color:#dcdcdc')
        line_lab_1.setGeometry(QtCore.QRect(0, margin_top, left_part_wid, 1))
        downLab_wid = (left_part_wid - margin_size * 3) / 2
        margin_top += margin_size + 1
        self.accountLab = QLabel('账号:', self)
        self.accountLab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.accountLab.setGeometry(QtCore.QRect(margin_size, margin_top, downLab_wid, 30))
        font.setPointSize(13)
        self.accountLab.setFont(font)
        self.timeLab = QLabel('到期时间:', self)
        self.timeLab.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.timeLab.setGeometry(QtCore.QRect(margin_size * 2 + downLab_wid, margin_top, downLab_wid, 30))
        font.setPointSize(13)
        self.timeLab.setFont(font)
        margin_top += margin_size + 30
        self.textEdit = QTextEdit(self)
        self.textEdit.setStyleSheet('background-color:#262626;color:#fff;')
        self.textEdit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.textEdit.setGeometry(QtCore.QRect(left_part_wid, 0, logIn_wid - left_part_wid, logIn_hei))
        font.setPointSize(14)
        self.textEdit.setFont(font)
 
    def backMainViewBtnClick(self):
        personinfo = ZFJPersoninfo()
        if personinfo.isMissing == True:
            self.megBoxInfor('正在混淆中')
            return
        if personinfo.mainRootView != None:
            personinfo.mainRootView.show()
            self.close()
        else:
            print('mainRootView')
 
    def tipsBtnClick(self):
        meg = '1.方法名相同，被多次混淆覆盖;\n'
        meg += '2.忽略的文件夹中包含了已被混淆的类或者方法;\n'
        meg += '3.图片如果不显示，可能原因是代码中图片名采用的是拼接的，手动替换一下就可以了;\n'
        meg += '4.如果出现项目路径修改了，但是本地实体路径没有修改，自己手动把本地路径修改一下;\n'
        meg += '5.utf-8编码错误和[Errno 13] Permission denied权限错误不用管;\n'
        self.megBoxInfor(meg)
 
    def reloadUI(self):
        self.accountLab.setText('账号:特别版')
        self.timeLab.setText('到期时间:永久')
 
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
 
    def megBoxInfor(self, infor):
        infor = infor.replace(':', '!')
        QMessageBox.information(self, '', infor, QMessageBox.Yes)
 
    def choicePathBtnClick(self):
        file_dir = ''
        try:
            file_dir = QFileDialog.getExistingDirectory(self, 'open file', '/Users/')
        except Exception as e:
            try:
                file_dir = '获取失败,请手动输入,或者复制路径'
            finally:
                e = None
                del e
 
        self.pathEdit.setText(file_dir)
 
    def checkBoxClick(self):
        for index in range(0, len(_checkBoxList)):
            fun_key = self.fun_key_list[index]
            checkBox = _checkBoxList[index]
            _funMap[fun_key] = str(checkBox.checkState())
            if index == 5:
                checkBox_7 = _checkBoxList[7]
                if checkBox.checkState() == 0:
                    checkBox_7.setCheckState(Qt.Unchecked)
                    self.rubClsTieBox.setCheckState(Qt.Unchecked)
                else:
                    checkBox_7.setCheckState(Qt.Checked)
                    self.rubClsTieBox.setCheckState(Qt.Checked)
            elif index == 9:
                checkBox_11 = _checkBoxList[11]
                if checkBox.checkState() == 0:
                    checkBox_11.setCheckState(Qt.Unchecked)
 
    def showDetailInfor(self):
        url = 'https://zfj1128.blog.csdn.net/article/details/95482006'
        webbrowser.open_new_tab(url)
 
    def openConfusedLog(self):
        subprocess.call(['open', 'ZFJ.log'])
 
    def showMapList(self):
        personinfo = ZFJPersoninfo()
        if personinfo.mapView == None:
            mapView = mapListView()
            mapView.reloadData()
            mapView.show()
            personinfo.mapView = mapView
        else:
            personinfo.mapView.reloadData()
            personinfo.mapView.show()
 
    def cleanTextEdit(self):
        self.textEdit.clear()
 
    def startMissBtnClick(self):
        personinfo = ZFJPersoninfo()
        if personinfo.isMissing == True:
            self.megBoxInfor('正在混淆中...')
            return
        file_dir = self.pathEdit.text()
        if len(file_dir) == 0:
            self.megBoxInfor('路径不能为空')
            return
        if os.path.exists(file_dir) == False:
            self.megBoxInfor('文件不存在')
            return
        ignoreFilesStr = self.ignoreEdit.text()
        ignoreFilesStr.replace(',', ',').replace('/', '')
        if len(ignoreFilesStr) > 0:
            for ignoreFile in ignoreFilesStr.split(','):
                ignoreFile_new = '/' + ignoreFile + '/'
                if '.' in ignoreFile:
                    ignoreFile_new = '/' + ignoreFile
                if ignoreFile_new not in ignoreFiles.ignore_Files:
                    ignoreFiles.ignore_Files.append(ignoreFile_new)
 
        isHaveFun = 0
        for item in _funMap:
            if _funMap[item] != '0':
                isHaveFun += 1
 
        if isHaveFun == 0:
            self.megBoxInfor('没有开启任何功能.....')
            return
        rubbishCode = int(_funMap['rubbishCode'])
        if rubbishCode > 0:
            rubbishLine = self.amountEdit.text()
            if zfjTools.is_number(rubbishLine) == False:
                self.megBoxInfor('添加次数值不对')
                return
            if int(rubbishLine) <= 0:
                self.megBoxInfor('添加次数值为负数')
                return
            _funMap['rubbishLine'] = str(rubbishLine)
            rubObjCount = self.rubClsEdit.text()
            if zfjTools.is_number(rubObjCount) == False:
                self.megBoxInfor('垃圾类数值不对')
                return
            if int(rubObjCount) < 0:
                self.megBoxInfor('垃圾类数值为负数')
                return
            _funMap['rubObjCount'] = str(rubObjCount)
        misProjectName = int(_funMap['misProjectName'])
        setProjectName = int(_funMap['setProjectName'])
        if misProjectName > 0:
            if setProjectName > 0:
                projectNamePreFix = self.projectNameEdit.text()
                if len(projectNamePreFix) <= 0:
                    self.megBoxInfor('自定义项目名为空')
                    return
                prefixMap = personinfo.prefixMap
                prefixMap['projectNamePreFix'] = projectNamePreFix
                personinfo.prefixMap = prefixMap
                zfjTools.savePrefixMap(prefixMap)
        codeObf.start_fun(file_dir, _funMap)
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    rootView = rootView()
    rootView.show()
    personinfo = ZFJPersoninfo()
    personinfo.rootView = rootView
    sys.exit(app.exec_())
 
def addTextEdit(log_str):
    personinfo = ZFJPersoninfo()
    rootView = personinfo.rootView
    if rootView != None:
        str_text = rootView.textEdit.toPlainText()
        str_text += log_str + '\n'
        rootView.textEdit.setPlainText(str_text)
        rootView.textEdit.moveCursor(QTextCursor.End)
        QApplication.processEvents()