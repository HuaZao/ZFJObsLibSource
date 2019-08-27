#! /usr/bin/env python 3.7 (3394)
#coding=utf-8
# Compiled at: 1969-12-31 18:00:00
#Powered by BugScaner
#http://tools.bugscaner.com/
#如果觉得不错,请分享给你朋友使用吧!
"""
1.,;
2.
3.project.pbxproj,
"""
import os, ignoreFiles as igFil
from singletonModel import ZFJPersoninfo
import zfjTools, confusionLog as conLog
_projectNameTup = None

def getMyProjectName(file_dir):
    global _projectNameTup
    fs = os.listdir(file_dir)
    for dir in fs:
        tmp_path = os.path.join(file_dir, dir)
        if os.path.isdir(tmp_path):
            if not igFil.isIgnoreFiles(tmp_path):
                if tmp_path.endswith('.xcodeproj'):
                    _projectName = tmp_path.split('/')[-1].split('.')[0]
                    personinfo = ZFJPersoninfo()
                    projectNamePreFix = personinfo.prefixMap['projectNamePreFix']
                    if len(projectNamePreFix) == 0:
                        projectNamePreFix = zfjTools.getWordFromLexicon().capitalize() + zfjTools.getWordFromLexicon().capitalize()
                    _projectNameTup = (
                     _projectName, projectNamePreFix)
                    break
                else:
                    getMyProjectName(tmp_path)


def modifyFolderName(file_dir):
    if _projectNameTup == None:
        return
    fs = os.listdir(file_dir)
    for dir in fs:
        tmp_path = os.path.join(file_dir, dir)
        tmp_pathList = '/.git/' not in tmp_path and tmp_path.split('/')
        FolderName = tmp_pathList[-1]
        if _projectNameTup[0] in FolderName:
            FolderName = FolderName.replace(_projectNameTup[0], _projectNameTup[1])
            tmp_pathList[-1] = FolderName
            new_path = '/'.join(tmp_pathList)
            try:
                os.rename(tmp_path, new_path)
                conLog.info('[MissProName OK] ' + new_path)
                tmp_path = new_path
            except Exception as e:
                try:
                    conLog.error('[MissProName Fail] ' + str(e))
                finally:
                    e = None
                    del e

            if not os.path.isdir(tmp_path):
                pass
            else:
                modifyFolderName(tmp_path)


def findProjectPbxproj(file_dir):
    if _projectNameTup == None:
        return
    fs = os.listdir(file_dir)
    for dir in fs:
        tmp_path = os.path.join(file_dir, dir)
        if not os.path.isdir(tmp_path):
            try:
                if tmp_path.endswith('project.pbxproj'):
                    if not igFil.isIgnoreFiles(tmp_path):
                        modifyProjectPbxproj(tmp_path)
                    if '/Pods/' in tmp_path or tmp_path.endswith('contents.xcworkspacedata'):
                        modifyProjectPbxproj(tmp_path)
                    else:
                        if '/Pods/' not in tmp_path:
                            if tmp_path.endswith('Podfile'):
                                modifyProjectPbxproj(tmp_path)
                    conLog.info('[MissProName OK] ' + tmp_path)
            except Exception as e:
                try:
                    conLog.error('[MissProName Fail] ' + str(e))
                finally:
                    e = None
                    del e

        else:
            findProjectPbxproj(tmp_path)


def modifyProjectPbxproj(tmp_path):
    file_data = ''
    Ropen = open(tmp_path, 'r')
    for line in Ropen:
        file_data += line.replace(_projectNameTup[0], _projectNameTup[1])

    Ropen.close()
    Wopen = open(tmp_path, 'w')
    Wopen.write(file_data)
    Wopen.close()


def initData():
    global _projectNameTup
    _projectNameTup = None


def startModifyProjectName(file_dir):
    initData()
    conLog.info('----------------------------------------')
    getMyProjectName(file_dir)
    conLog.info(_projectNameTup)
    conLog.info('----------------------------------------')
    modifyFolderName(file_dir)
    findProjectPbxproj(file_dir)


if __name__ == '__main__':
    file_dir = '/Users/zhangfujie/Desktop/Obfuscated/'
    startModifyProjectName(file_dir)