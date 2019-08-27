#! /usr/bin/env python 3.7 (3394)
#coding=utf-8
# Compiled at: 1969-12-31 18:00:00
#Powered by BugScaner
#http://tools.bugscaner.com/
#如果觉得不错,请分享给你朋友使用吧!
import zfjTools, random, os, shutil, confusionLog as conLog
_resourceTypeList = zfjTools.imageTypeList + zfjTools.otherTypeList
_resNameMap = {}
_projectPbxprojPath = None
_hadDelMap = {}
_isCleaing = False

def searchAllResName(file_dir):
    global _resNameMap
    fs = os.listdir(file_dir)
    for dir in fs:
        tmp_path = os.path.join(file_dir, dir)
        if not os.path.isdir(tmp_path):
            if isResource(tmp_path) == True:
                if '/Pods/' not in tmp_path:
                    if '.appiconset' not in tmp_path:
                        pass
        if '.launchimage' not in tmp_path:
            imageName = tmp_path.split('/')[-1].split('.')[0]
            _resNameMap[imageName] = tmp_path
            conLog.info_delRes('[FindRes OK] ' + tmp_path)
        elif os.path.isdir(tmp_path):
            if tmp_path.endswith('.imageset'):
                if '/Pods/' not in tmp_path:
                    imageName = tmp_path.split('/')[-1].split('.')[0]
                    _resNameMap[imageName] = tmp_path
                    conLog.info_delRes('[FindRes OK] ' + tmp_path)
        else:
            searchAllResName(tmp_path)


def isResource(tmp_path):
    global _resourceTypeList
    resName = tmp_path.split('/')[-1]
    for resType in _resourceTypeList:
        if resName.endswith(resType):
            return True

    return False


def searchProjectCode(file_dir):
    global _projectPbxprojPath
    fs = os.listdir(file_dir)
    for dir in fs:
        tmp_path = os.path.join(file_dir, dir)
        if tmp_path.endswith('project.pbxproj'):
            _projectPbxprojPath = tmp_path
        if not os.path.isdir(tmp_path):
            if '/Pods/' not in tmp_path:
                try:
                    findResNameAtFileLine(tmp_path)
                    conLog.info_delRes('[ReadFileForRes OK] ' + tmp_path)
                except Exception as e:
                    try:
                        pass
                    finally:
                        e = None
                        del e

        else:
            searchProjectCode(tmp_path)


def findResNameAtFileLine(tmp_path):
    Ropen = open(tmp_path, 'r')
    for line in Ropen:
        lineList = line.split('"')
        for item in lineList:
            if '.' in item:
                item = item.split('.')[0]
            if item in _resNameMap:
                del _resNameMap[item]
            elif item + '@1x' in _resNameMap:
                item = item + '@1x'
                del _resNameMap[item]
            elif item + '@2x' in _resNameMap:
                item = item + '@2x'
                del _resNameMap[item]
            elif item + '@3x' in _resNameMap:
                item = item + '@3x'
                del _resNameMap[item]

    Ropen.close()


def delAllRubRes():
    global _hadDelMap
    for resName in list(_resNameMap.keys()):
        tmp_path = _resNameMap[resName]
        if tmp_path.endswith('.imageset'):
            if os.path.exists(tmp_path):
                if os.path.isdir(tmp_path):
                    try:
                        _hadDelMap[resName] = tmp_path
                        delImagesetFolder(tmp_path)
                        del _resNameMap[resName]
                        conLog.info_delRes('[DelRubRes OK] ' + tmp_path)
                    except Exception as e:
                        try:
                            conLog.error_delRes('[DelRubRes Fail] [' + str(e) + ']' + tmp_path)
                        finally:
                            e = None
                            del e

        else:
            conLog.error_delRes('[DelRubRes Fail] [not exists] ' + tmp_path)

    delResAtProjectPbxproj()


def delImagesetFolder(rootdir):
    filelist = []
    filelist = os.listdir(rootdir)
    for f in filelist:
        filepath = os.path.join(rootdir, f)
        if os.path.isfile(filepath):
            os.remove(filepath)
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath, True)

    shutil.rmtree(rootdir, True)


def delResAtProjectPbxproj():
    if _projectPbxprojPath != None:
        _needDelResName = []
        file_data = ''
        Ropen = open(_projectPbxprojPath, 'r')
        for line in Ropen:
            idAdd = True
            for resName in _resNameMap:
                if resName in line:
                    idAdd = False
                    if resName not in _needDelResName:
                        _needDelResName.append(resName)

            if idAdd == True:
                file_data += line

        Ropen.close()
        Wopen = open(_projectPbxprojPath, 'w')
        Wopen.write(file_data)
        Wopen.close()
        for item in _needDelResName:
            tmp_path = _resNameMap[item]
            if os.path.exists(tmp_path):
                pass
            if not os.path.isdir(tmp_path):
                _hadDelMap[item] = tmp_path
                os.remove(tmp_path)
                del _resNameMap[item]
                conLog.info_delRes('[DelRubRes OK] ' + tmp_path)
                continue


def initData():
    global _hadDelMap
    global _projectPbxprojPath
    global _resNameMap
    global _resourceTypeList
    _resourceTypeList = zfjTools.imageTypeList + zfjTools.otherTypeList
    _resNameMap = {}
    _projectPbxprojPath = None
    _hadDelMap = {}


def startCleanRubRes(file_dir, ignoreList=[]):
    global _isCleaing
    if _isCleaing == True:
        return
    _isCleaing = True
    initData()
    conLog.info('------------------------------------------------------------')
    searchAllResName(file_dir)
    conLog.info_delRes('----------------------------------------')
    conLog.info_delRes(_resNameMap)
    for item in ignoreList:
        if item in list(_resNameMap.keys()):
            del _resNameMap[item]

    conLog.info_delRes('----------------------------------------')
    conLog.info_delRes(ignoreList)
    searchProjectCode(file_dir)
    conLog.info_delRes('----------------------------------------')
    conLog.info_delRes(_resNameMap)
    delAllRubRes()
    conLog.info_delRes('----------------------------------------')
    conLog.info_delRes(_hadDelMap)
    conLog.info_delRes('----------------------------------------')
    conLog.info_delRes(_resNameMap)
    _isCleaing = False


if __name__ == '__main__':
    line = '[self.tipsImageView sd_setImageWithURL:[NSURL URLWithString:self.extUrl] placeholderImage:[UIImage imageNamed:@"ZH_.jpg"]];'
    _resNameMap['ZH_'] = 'ZH_ZH_ZH_ZH_'
    lineList = line.split('"')
    print(lineList)
    for item in lineList:
        if item in _resNameMap or item.split('.')[0] in _resNameMap or item + '@1x' in _resNameMap or item + '@2x' in _resNameMap or item + '@3x' in _resNameMap:
            print('aaaaaaaaaaaaaaaaaa')