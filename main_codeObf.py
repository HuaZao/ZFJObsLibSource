#! /usr/bin/env python 3.7 (3394)
#coding=utf-8
# Compiled at: 1969-12-31 18:00:00
#Powered by BugScaner
#http://tools.bugscaner.com/
#如果觉得不错,请分享给你朋友使用吧!
import addRubbishFile as addFile
import cunfusionObjName as conObjN
import confusionFun as conFunc
import cunfusionProperty as conPro
import confusionLog as conLog
import deleteNotes as delNot
import updateSourceHash as updHash
import encryptString as encStr
import sourceName as soName
import modifyProjectName as modProName
import missFolder
import addRubbishCode as addCode 
from singletonModel import ZFJPersoninfo

def start_fun(file_dir, funMap={}):
    personinfo = ZFJPersoninfo()
    personinfo.isMissing = True
    if len(file_dir) == 0:
        return
    if int(funMap['property']) > 0:
        conLog.tips('******************************Fun:开始混淆方法******************************')
        conPro.startConfusionPro(file_dir, personinfo.prefixMap['proPreFix'])
    if int(funMap['funName']) > 0:
        conLog.tips('******************************Fun:开始混淆方法******************************')
        conFunc.startConfusionFun(file_dir, personinfo.prefixMap['funPreFix'])
    if int(funMap['objName']) > 0:
        conLog.tips('******************************Fun:开始混淆类名******************************')
        conObjN.startObfuscatedObjName(file_dir, personinfo.prefixMap['objPreFix'])
    if int(funMap['souHashKey']) > 0:
        conLog.tips('******************************Fun:修改资源HASH值******************************')
        updHash.startUpdateSourceHash(file_dir)
    if int(funMap['upSouName']) > 0:
        conLog.tips('******************************Fun:翻新资源文件名******************************')
        soName.startSourceName(file_dir, personinfo.prefixMap['imgPreFix'])
    if int(funMap['encryStr']) > 0:
        conLog.tips('******************************Fun:加密明文字符串******************************')
        encStr.startEncryptStr(file_dir)
    if int(funMap['rubbishCode']) > 0:
        amount = int(funMap['rubbishLine'])
        amount = 5 if amount <= 0 else amount
        rubObjCount = int(funMap['rubObjCount'])
        if rubObjCount > 0:
            conLog.tips('******************************Fun:添加垃圾文件******************************')
            addFile.startAddRubFileClass(file_dir, rubObjCount, amount, personinfo.prefixMap['rubPreFix'])
        conLog.tips('******************************Fun:添加垃圾代码******************************')
        addCode.startAddRubbishCode(file_dir, amount, personinfo.prefixMap['rubPreFix'])
    if int(funMap['deleteNotes']) > 0:
        conLog.tips('******************************Fun:开始删除注释******************************')
        delNot.startDeleteNotes(file_dir)
    if int(funMap['missFolder']) > 0:
        conLog.tips('******************************Fun:开始混淆文件夹名******************************')
        missFolder.startMissFolder(file_dir, personinfo.prefixMap['folderPreFix'])
    if int(funMap['misProjectName']) > 0:
        conLog.tips('******************************Fun:开始修改项目名******************************')
        modProName.startModifyProjectName(file_dir)
    conLog.tips('******************************End:混淆结束******************************')
    personinfo.isMissing = False