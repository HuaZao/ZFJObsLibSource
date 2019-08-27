#! /usr/bin/env python 3.7 (3394)
#coding=utf-8
# Compiled at: 1969-12-31 18:00:00
#Powered by BugScaner
#http://tools.bugscaner.com/
#如果觉得不错,请分享给你朋友使用吧!
"""
1.xxx.xcodeprojproject.pbxprojPBXGroupMap
2.,
3.xxx.xcodeprojproject.pbxproj
"""
import os, zfjTools, confusionLog as conLog
from singletonModel import ZFJPersoninfo
import ignoreFiles as igFil
ignoreFolder = [
 '.xcassets',
 'Tests',
 'UITests',
 'Products',
 'Pods',
 'Frameworks',
 '.xcworkspace',
 '.xcodeproj',
 '.lproj',
 '.git',
 '.DS_Store',
 '.idea',
 'Icon\r']
PBXGroupMap = {}
PathChildMap = {}
pbxprojPath = ''
PeplacePathMap = {}
MissPbxprojMap = {}
relayTup = None
_folderPreFix = ''
_pchPath = None
_plistPath = None
 
def getProjectPbxprojPath(file_dir):
    global pbxprojPath
    fs = os.listdir(file_dir)
    for dir in fs:
        tmp_path = os.path.join(file_dir, dir)
        if not os.path.isdir(tmp_path):
            try:
                if tmp_path.endswith('project.pbxproj'):
                    if '/Pods/' not in tmp_path:
                        pbxprojPath = tmp_path
                        getPBXGroupMap(tmp_path)
                        conLog.info('[GetPbxPath OK] ' + tmp_path)
            except Exception as e:
                try:
                    conLog.error('[GetPbxPath Fail] ' + str(e))
                finally:
                    e = None
                    del e
 
        else:
            getProjectPbxprojPath(tmp_path)
 
 
def getPBXGroupMap(tmp_path):
    isPBXGroup = False
    row = ''
    Ropen = open(tmp_path, 'r')
    for line in Ropen:
        if '/* Begin PBXGroup section */' in line:
            isPBXGroup = True
        else:
            if '/* End PBXGroup section */' in line:
                isPBXGroup = False
        if isPBXGroup == True:
            if '/* Begin PBXGroup section */' not in line:
                row += line
                if '};\n' in line:
                    PBXGroupOneRow(row)
                row = ''
 
    Ropen.close()
 
 
def PBXGroupOneRow(row):
    global PBXGroupMap
    global _folderPreFix
    UDID = ''
    name = ''
    missName = ''
    isa = ''
    children = ''
    childrenNames = ''
    path = ''
    sourceTree = ''
    row = row.replace('\n', '').split()
    row = ''.join(row)
    UDID_Name = row[:row.find('=')]
    if '/*' in UDID_Name:
        if '*/' in UDID_Name:
            UDID = UDID_Name[:UDID_Name.find('/*')]
            name = UDID_Name[UDID_Name.find('/*') + 2:UDID_Name.find('*/')]
        UDID = UDID_Name
    if len(name) > 0:
        value_arr = row[row.find('={') + 2:row.find('};')].split(';')
        for value in value_arr:
            if 'isa=' in value:
                isa = value.split('isa=')[-1]
            elif 'children=' in value:
                children = value.split('children=')[-1][1:-2]
                children_name_list = []
                for item in children.split(','):
                    children_name = item[item.find('/*') + 2:item.find('*/')]
                    children_name_list.append(children_name)
                childrenNames = ','.join(children_name_list)
            elif 'path=' in value:
                path = value.split('path=')[-1]
            elif 'sourceTree=' in value:
                sourceTree = value.split('sourceTree=')[-1]
        lower_name = name.lower()
    else:
        return
    if 'view' in lower_name:
        missName = zfjTools.getWordFromLexicon().capitalize() + 'Views'
    else:
        if 'control' in lower_name:
            missName = zfjTools.getWordFromLexicon().capitalize() + 'Controllers'
        else:
            if 'cell' in lower_name:
                missName = zfjTools.getWordFromLexicon().capitalize() + 'Cells'
            else:
                if 'model' in lower_name:
                    missName = zfjTools.getWordFromLexicon().capitalize() + 'Models'
                else:
                    if 'tool' in lower_name:
                        missName = zfjTools.getWordFromLexicon().capitalize() + 'Tools'
                    else:
                        if 'label' in lower_name:
                            missName = zfjTools.getWordFromLexicon().capitalize() + 'Labels'
                        else:
                            if 'vendor' in lower_name:
                                missName = zfjTools.getWordFromLexicon().capitalize() + 'Vendor'
                            else:
                                if 'resources' in lower_name:
                                    missName = zfjTools.getWordFromLexicon().capitalize() + 'Resources'
                                else:
                                    if 'util' in lower_name:
                                        missName = zfjTools.getWordFromLexicon().capitalize() + 'Util'
                                    else:
                                        if 'category' in lower_name:
                                            missName = zfjTools.getWordFromLexicon().capitalize() + 'Category'
                                        else:
                                            missName = zfjTools.getWordFromLexicon().capitalize() + 'Folder'
    missName = _folderPreFix + missName
    part_map = {}
    part_map['UDID'] = UDID
    part_map['name'] = name
    part_map['missName'] = missName
    part_map['isa'] = isa
    part_map['children'] = children
    part_map['path'] = path
    part_map['sourceTree'] = sourceTree
    PBXGroupMap[childrenNames] = part_map


def getPathChildMap(file_dir):
    global PathChildMap
    fs = os.listdir(file_dir)
    for dir in fs:
        tmp_path = os.path.join(file_dir, dir)
        pathList = tmp_path.split('/')
        childName = pathList[-1]
        del pathList[-1]
        keyPath = pathList[-2] + '/' + pathList[-1]
        if '.DS_Store' not in childName:
            if 'Icon\r' not in childName:
                if '.git' not in childName:
                    if keyPath in PathChildMap.keys():
                        childList = PathChildMap[keyPath]
                        childList.append(childName)
                        PathChildMap[keyPath] = childList
                    else:
                        childList = [
                         childName]
                        PathChildMap[keyPath] = childList
                    if not os.path.isdir(tmp_path):
                        pass
            else:
                if not isIgnoreFolder(tmp_path):
                    getPathChildMap(tmp_path)
 
 
def isIgnoreFolder(tmp_path):
    global ignoreFolder
    for item in ignoreFolder:
        if tmp_path.endswith(item) or item in tmp_path:
            return True
 
    return False
 
 
def setPathForPBXGroupMap():
    global MissPbxprojMap
    global PeplacePathMap
    for keyPath in PathChildMap:
        childList = PathChildMap[keyPath]
        for children_name in PBXGroupMap.keys():
            myChildList = children_name.split(',')
            if set(childList) == set(myChildList):
                part_map = PBXGroupMap[children_name]
                UDID = part_map['UDID']
                name = part_map['name']
                missName = part_map['missName']
                fatherName = keyPath.split('/')[0]
                key_name = fatherName + '&&' + name
                fatherMissName = getFatherMissName(fatherName, name)
                PeplacePathMap[key_name] = (name, missName, fatherName, fatherMissName)
                MissPbxprojMap[UDID] = (name, missName)
 
 
def getFatherMissName(fatherName, childrenName):
    for item in PBXGroupMap:
        part_map = PBXGroupMap[item]
        if fatherName == part_map['name']:
            if childrenName in part_map['children']:
                return part_map['missName']
 
    return ''
 
 
def findFolderAndMiss(file_dir):
    global _pchPath
    global _plistPath
    fs = os.listdir(file_dir)
    for dir in fs:
        tmp_path = os.path.join(file_dir, dir)
        if not os.path.isdir(tmp_path):
            if tmp_path.endswith('.pch'):
                if '/Pods/' not in tmp_path:
                    _pchPath = tmp_path
                if tmp_path.endswith('/Info.plist'):
                    if 'Tests/' not in tmp_path:
                        if '/Pods/' not in tmp_path:
                            _plistPath = tmp_path
        else:
            missName = os.path.isdir(tmp_path) and getThisPathMissName(tmp_path)
            if missName != None:
                pathList = tmp_path.split('/')
                del pathList[-1]
                pathList.append(missName)
                temp = '/'.join(pathList)
                oldname = os.path.join(file_dir, tmp_path)
                newname = os.path.join(file_dir, temp)
                try:
                    os.rename(oldname, newname)
                    findFolderAndMiss(newname)
                    conLog.info('[MissFolder OK] ' + newname)
                except Exception as e:
                    try:
                        conLog.error('[MissFolder Fail] ' + str(e))
                        findFolderAndMiss(tmp_path)
                    finally:
                        e = None
                        del e
 
            else:
                findFolderAndMiss(tmp_path)
 
 
def getThisPathMissName(tmp_path):
    pathList = tmp_path.split('/')
    this_path_name = pathList[-1]
    father_path_name = pathList[-2]
    for key_name in PeplacePathMap:
        value_tub = PeplacePathMap[key_name]
        if '&&' + this_path_name in key_name:
            if father_path_name == value_tub[2] or father_path_name == value_tub[3]:
                return value_tub[1]
 
 
def getNewProjectPbxprojPath(file_dir):
    fs = os.listdir(file_dir)
    for dir in fs:
        tmp_path = os.path.join(file_dir, dir)
        if not os.path.isdir(tmp_path):
            try:
                if tmp_path.endswith('project.pbxproj'):
                    if '/Pods/' not in tmp_path:
                        missProjectPbxproj(tmp_path)
                        conLog.info('[MissFolder OK] ' + tmp_path)
            except Exception as e:
                try:
                    conLog.error('[MissFolder Fail] ' + str(e))
                finally:
                    e = None
                    del e
 
        else:
            getNewProjectPbxprojPath(tmp_path)
 
 
def missProjectPbxproj(tmp_path):
    global relayTup
    file_data = ''
    Ropen = open(tmp_path, 'r')
    for line in Ropen:
        if '/*' in line:
            if '*/' in line:
                file_data += missProjectPbxprojInLine(line)
        elif 'path =' in line:
            if relayTup != None:
                file_data += line.replace(relayTup[0], relayTup[1])
        elif '};' in line:
            relayTup = None
            file_data += line
        elif 'GCC_PREFIX_HEADER =' in line:
            if _pchPath != None:
                lineList = line.split('/')
                if len(lineList) >= 2:
                    if len(_pchPath.split('/')) >= 2:
                        lineList[-2] = _pchPath.split('/')[-2]
                file_data += '/'.join(lineList)
        elif 'INFOPLIST_FILE =' in line:
            if _plistPath != None:
                if 'Tests/' not in line:
                    lineList = line.split('/')
                    if len(lineList) >= 2:
                        if len(_plistPath.split('/')) >= 2:
                            if 'INFOPLIST_FILE =' in lineList[-2]:
                                lineList[-2] = '\t\t\t\tINFOPLIST_FILE = ' + _plistPath.split('/')[-2]
                            else:
                                lineList[-2] = _plistPath.split('/')[-2]
                    file_data += '/'.join(lineList)
        else:
            file_data += line
 
    Ropen.close()
    Wopen = open(tmp_path, 'w')
    Wopen.write(file_data)
    Wopen.close()
 
 
def missProjectPbxprojInLine(line):
    global relayTup
    line_UDID = ''.join(line[:line.find('/*')].split())
    line_Name = ''.join(line[line.find('/*') + 2:line.find('*/')].split())
    if line_UDID in MissPbxprojMap.keys():
        missName = MissPbxprojMap[line_UDID][-1]
        line = line.replace(line_Name, missName)
        if '*/ = {' in line:
            relayTup = MissPbxprojMap[line_UDID]
    return line
 
 
def initData():
    global MissPbxprojMap
    global PBXGroupMap
    global PathChildMap
    global PeplacePathMap
    global _folderPreFix
    global _pchPath
    global _plistPath
    global pbxprojPath
    global relayTup
    PBXGroupMap = {}
    PathChildMap = {}
    pbxprojPath = ''
    PeplacePathMap = {}
    MissPbxprojMap = {}
    relayTup = None
    _folderPreFix = ''
    _pchPath = None
    _plistPath = None
 
 
def startMissFolder(file_dir, folderPreFix):
    global _folderPreFix
    initData()
    _folderPreFix = folderPreFix
    conLog.info('----------------------------------------')
    getProjectPbxprojPath(file_dir)
    personinfo = ZFJPersoninfo()
    personinfo.method_list_map = PBXGroupMap
    conLog.info(PBXGroupMap)
    getPathChildMap(file_dir)
    setPathForPBXGroupMap()
    findFolderAndMiss(file_dir)
    getNewProjectPbxprojPath(file_dir)
 
 
if __name__ == '__main__':
    file_dir = '/Users/zhangfujie/Desktop/Obfuscated/'
    startMissFolder(file_dir, '')