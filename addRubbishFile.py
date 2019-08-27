#! /usr/bin/env python 3.7 (3394)
#coding=utf-8
# Compiled at: 1969-12-31 18:00:00
#Powered by BugScaner
#http://tools.bugscaner.com/
#如果觉得不错,请分享给你朋友使用吧!
import random, os, zfjTools, addRandomCode
from singletonModel import ZFJPersoninfo
import confusionLog as conLog
_sportObjList = [
 'NSObject', 'UIView', 'UIViewController']
_importList = ['#import <Foundation/Foundation.h>\n#import <UIKit/UIKit.h>', '#import <UIKit/UIKit.h>', '#import <UIKit/UIKit.h>']
_createFilePath = None
_projectPbxprojPath = None
_createFileMap = {}
_createFolderName = None
_createFolderUDID = None
_createFolderCode = None
_createFolderChildrenCode = None
_createFolderchildrenList = []
_PBXFileReferenceCodeList = []
_PBXSourcesBuildPhaseList = []
_PBXBuildFileList = []

def createRubbishOCFile(fileCount=1, amount=5, rubPrefix=''):
    global _createFileMap
    global _createFilePath
    if _createFilePath == None:
        return
    for index in range(0, fileCount):
        createOCFile(_createFilePath, amount, rubPrefix)

    personinfo = ZFJPersoninfo()
    personinfo.rubbishFileMap = _createFileMap


def createOCFile(filePath, amount=5, rubPrefix=''):
    global _PBXBuildFileList
    global _PBXFileReferenceCodeList
    global _PBXSourcesBuildPhaseList
    global _createFolderchildrenList
    global _importList
    global _sportObjList
    rubCodeTuple = addRandomCode.addRandomClass(amount, rubPrefix)
    index = random.randint(0, 2)
    objClass = _sportObjList[index]
    importName = _importList[index]
    objectName = addRandomCode.getMissObjName(objClass)
    h_filePath = filePath + '/' + objectName + '.h'
    m_filePath = filePath + '/' + objectName + '.m'
    hFileCode = getHeadCode(objectName + '.h')
    hFileCode += importName + '\n\n'
    hFileCode += '@interface ' + objectName + ' : ' + objClass + '\n'
    hFileCode += '\n'
    hFileCode += rubCodeTuple[0]
    hFileCode += '\n'
    hFileCode += '@end\n'
    Wopen = open(h_filePath, 'w')
    Wopen.write(hFileCode)
    Wopen.close()
    conLog.info('[CreateRubFile OK] ' + h_filePath)
    h_file_udid = addRandomCode.getMyUIID()
    h_file_code = h_file_udid + ' /* ' + objectName + '.h' + ' */,'
    _createFolderchildrenList.append(h_file_code)
    h_PBXFileRef_code = h_file_udid + ' /* ' + objectName + '.h */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.c.h; path = ' + objectName + '.h; sourceTree = "<group>"; };' + '\n'
    _PBXFileReferenceCodeList.append(h_PBXFileRef_code)
    mFileCode = getHeadCode(objectName + '.m')
    mFileCode += '#import "' + objectName + '.h"\n'
    choseMap = {}
    if len(_createFileMap.keys()) > 3:
        random.seed(len(_createFileMap.keys()))
        keyList = random.sample(list(_createFileMap.keys()), 3)
        for key in keyList:
            choseMap[key] = _createFileMap[key]

    else:
        choseMap = _createFileMap
    createProMap = {}
    for objClassName in choseMap:
        mFileCode += '#import "' + objClassName + '.h"\n'
        createProMap[objClassName] = zfjTools.getWordFromLexicon() + zfjTools.getWordFromLexicon().capitalize() + objClassName[:3].capitalize()

    mFileCode += '\n'
    mFileCode += '@interface ' + objectName + ' ()\n\n'
    for proObjName in createProMap:
        mFileCode += '@property(nonatomic,strong) ' + proObjName + ' *' + createProMap[proObjName] + ';' + '\n'

    interfaceProFunName = ''
    if len(createProMap) > 0:
        mFileCode += '\n'
        interfaceProFunName = zfjTools.getWordFromLexicon() + zfjTools.getWordFromLexicon().capitalize() + 'Fun'
    mFileCode += '@end\n\n'
    mFileCode += '@implementation ' + objectName + '\n\n'
    if objClass == 'UIViewController':
        mFileCode += '- (void)viewDidLoad {\n'
        mFileCode += '    [super viewDidLoad];\n'
        mFileCode += '    // Do any additional setup after loading the view from its nib.\n'
        for key in rubCodeTuple[3]:
            mFileCode += '    [self ' + rubCodeTuple[3][key] + '];' + '\n'

        if len(interfaceProFunName) > 0:
            mFileCode += '    [self ' + interfaceProFunName + '];' + '\n'
        mFileCode += '}\n\n'
    else:
        mFileCode += createInitFun(rubCodeTuple[3], interfaceProFunName)
    if len(interfaceProFunName) > 0:
        mFileCode += realizePropertyRubClass(createProMap, interfaceProFunName)
    mFileCode += getNewRubbishCode(rubCodeTuple[1], choseMap)
    mFileCode += '@end\n'
    Wopen = open(m_filePath, 'w')
    Wopen.write(mFileCode)
    Wopen.close()
    conLog.info('[CreateRubFile OK] ' + m_filePath)
    m_file_udid = addRandomCode.getMyUIID()
    m_file_udid_1 = addRandomCode.getMyUIID()
    m_file_code = m_file_udid + ' /* ' + objectName + '.m' + ' */,'
    _createFolderchildrenList.append(m_file_code)
    m_PBXFileRef_code = m_file_udid + ' /* ' + objectName + '.m */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.c.objc; path = ' + objectName + '.m; sourceTree = "<group>"; };' + '\n'
    _PBXFileReferenceCodeList.append(m_PBXFileRef_code)
    m_PBXSources_code = m_file_udid_1 + ' /* ' + objectName + '.m in Sources */,' + '\n'
    _PBXSourcesBuildPhaseList.append(m_PBXSources_code)
    m_PBXBuildFile_code = m_file_udid_1 + ' /* ' + objectName + '.m in Sources */ = {isa = PBXBuildFile; fileRef = ' + m_file_udid + ' /* ' + objectName + '.m */; };' + '\n'
    _PBXBuildFileList.append(m_PBXBuildFile_code)
    _createFileMap[objectName] = rubCodeTuple[2]


def getNewRubbishCode(oldRubCode, choseMap):
    replaceCode = ''
    if len(choseMap) >= 1:
        index = random.randint(0, len(choseMap.keys()) - 1)
        objName = list(choseMap.keys())[index]
        newProName = zfjTools.getWordFromLexicon() + zfjTools.getWordFromLexicon().capitalize() + objName[:3].capitalize()
        replaceCode += objName + ' *' + newProName + ' = [[' + objName + ' alloc] init];' + '\n'
        replaceCode += '    [' + newProName + ' ' + choseMap[objName] + '];' + '\n'
        oldRubCode = oldRubCode.replace('//ZFJ_OTHER', replaceCode)
    else:
        replaceCode = oldRubCode
    return oldRubCode + '\n'


def realizePropertyRubClass(createProMap, interfaceProFunName):
    if len(createProMap) > 0:
        lazyLoadCode = '\n'
        proCode = '- (void)' + interfaceProFunName + '{' + '\n'
        for objClassName in createProMap:
            propertyName = createProMap[objClassName]
            lazyLoadCode += '- (' + objClassName + ' *)' + propertyName + '{' + '\n'
            lazyLoadCode += '    if(_' + propertyName + ' == nil){' + '\n'
            lazyLoadCode += '        _' + propertyName + ' = [[' + objClassName + ' alloc] init];' + '\n'
            lazyLoadCode += '    }\n'
            lazyLoadCode += '    return _' + propertyName + ';' + '\n'
            lazyLoadCode += '}\n\n'
            proCode += '    [self.' + propertyName + ' ' + _createFileMap[objClassName] + '];' + '\n'

        proCode += '}\n\n'
        return lazyLoadCode + proCode
    else:
        return '\n'


def createInitFun(rubFunMap, interfaceProFunName):
    initCode = ''
    initCode += '- (instancetype)init{\n'
    previousLine = '    if (self == [super init]){\n'
    initCode += previousLine
    for key in rubFunMap:
        initCode += '        [self ' + rubFunMap[key] + '];' + '\n'

    if len(interfaceProFunName) > 0:
        initCode += '        [self ' + interfaceProFunName + '];' + '\n'
    initCode += '    }\n'
    initCode += '    return self;\n'
    initCode += '}\n\n'
    return initCode


def getHeadCode(objectName):
    headCode = '//\n'
    headCode += '//  ' + objectName + '\n'
    headCode += '//  ' + zfjTools.getWordFromLexicon().upper() + '\n'
    headCode += '//\n'
    headCode += '//  Created by ' + zfjTools.getWordFromLexicon().upper() + ' on ' + zfjTools.getTimeStr() + '.\n'
    headCode += '//  Copyright  2019 ' + zfjTools.getWordFromLexicon().upper() + '. All rights reserved.\n'
    headCode += '//\n\n\n'
    return headCode


def searchXcodeprojPath(file_dir):
    global _createFilePath
    global _createFolderCode
    global _createFolderName
    global _createFolderUDID
    global _projectPbxprojPath
    fs = os.listdir(file_dir)
    for dir in fs:
        tmp_path = os.path.join(file_dir, dir)
        if tmp_path.endswith('.xcodeproj'):
            if '/Pods/' not in tmp_path:
                _createFolderName = zfjTools.getWordFromLexicon().capitalize() + zfjTools.getWordFromLexicon().capitalize()
                tmp_path_list = tmp_path.split('/')
                tmp_path_list[-1] = _createFolderName
                _createFilePath = '/'.join(tmp_path_list)
                if not os.path.exists(_createFilePath):
                    os.makedirs(_createFilePath)
                _createFolderUDID = addRandomCode.getMyUIID()
                _createFolderCode = _createFolderUDID + ' /* ' + _createFolderName + ' */,'
            if tmp_path.endswith('project.pbxproj'):
                if '/Pods/' not in tmp_path:
                    _projectPbxprojPath = tmp_path
        if _createFilePath != None:
            if _projectPbxprojPath != None:
                break
        if not os.path.isdir(tmp_path):
            continue
        searchXcodeprojPath(tmp_path)


def setCreateFolderChildrenCode():
    global _createFolderChildrenCode
    if _createFolderUDID == None:
        return
    if _createFolderName == None:
        return
    _createFolderChildrenCode = ''
    _createFolderChildrenCode += '\t\t' + _createFolderUDID + ' /* ' + _createFolderName + ' */ = {' + '\n'
    _createFolderChildrenCode += '\t\t\tisa = PBXGroup;\n'
    _createFolderChildrenCode += '\t\t\tchildren = (\n'
    for item in _createFolderchildrenList:
        _createFolderChildrenCode += '\t\t\t\t' + item + '\n'

    _createFolderChildrenCode += '\t\t\t);\n'
    _createFolderChildrenCode += '\t\t\tpath = ' + _createFolderName + ';' + '\n'
    _createFolderChildrenCode += '\t\t\tsourceTree = "<group>";\n'
    _createFolderChildrenCode += '\t\t};\n'


def addCodeInProjectPbxproj():
    if _projectPbxprojPath == None:
        return
    if _createFolderChildrenCode == None:
        return
    file_data = ''
    Ropen = open(_projectPbxprojPath, 'r')
    isBeginPBXGroup = False
    isPBXSourcesBuildPhase = False
    for line in Ropen:
        if '/* Begin PBXGroup section */' in line:
            isBeginPBXGroup = True
        if '/* Begin PBXSourcesBuildPhase section */' in line:
            isPBXSourcesBuildPhase = True
        if 'children = (' in line:
            if isBeginPBXGroup == True:
                isBeginPBXGroup = False
                file_data += line
                file_data += '                ' + _createFolderCode + '\n'
        elif 'files = (' in line:
            if isPBXSourcesBuildPhase == True:
                file_data += line
                for item in _PBXSourcesBuildPhaseList:
                    file_data += '                ' + item

        elif '/* End PBXGroup section */' in line:
            file_data += _createFolderChildrenCode
            file_data += line
        elif '/* End PBXFileReference section */' in line:
            for item in _PBXFileReferenceCodeList:
                file_data += '\t\t' + item

            file_data += line
        elif '/* End PBXBuildFile section */' in line:
            for item in _PBXBuildFileList:
                file_data += '\t\t' + item

            file_data += line
        else:
            file_data += line

    Ropen.close()
    Wopen = open(_projectPbxprojPath, 'w')
    Wopen.write(file_data)
    Wopen.close()


def resetData():
    global _createFileMap
    global _createFilePath
    global _createFolderChildrenCode
    global _createFolderName
    global _createFolderUDID
    global _createFolderchildrenList
    global _projectPbxprojPath
    _createFilePath = None
    _projectPbxprojPath = None
    _createFileMap = {}
    _createFolderName = None
    _createFolderUDID = None
    _createFolderCode = None
    _createFolderChildrenCode = None
    _createFolderchildrenList = []
    _PBXFileReferenceCodeList = []
    _PBXSourcesBuildPhaseList = []
    _PBXBuildFileList = []
    personinfo = ZFJPersoninfo()
    personinfo.rubbishFileMap = {}


def startAddRubFileClass(file_dir, fileCount=5, amount=5, rubPrefix=''):
    resetData()
    searchXcodeprojPath(file_dir)
    createRubbishOCFile(fileCount, amount, rubPrefix)
    conLog.info(':')
    conLog.info(_createFileMap)
    setCreateFolderChildrenCode()
    addCodeInProjectPbxproj()


if __name__ == '__main__':
    file_dir = '/Users/zhangfujie/Desktop/Obfuscated/'
    startAddRubFileClass(file_dir)