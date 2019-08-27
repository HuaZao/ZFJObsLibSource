#! /usr/bin/env python 3.7 (3394)
#coding=utf-8
# Compiled at: 1969-12-31 18:00:00
#Powered by BugScaner
#http://tools.bugscaner.com/
#如果觉得不错,请分享给你朋友使用吧!
import os, confusionLog as conLog, ignoreFiles as igFil
from singletonModel import ZFJPersoninfo
import zfjTools
sourceMap = {}
sourceTypeMap = {}
xcassetsMap = {}

def saveNameToMap(tmp_path, imgPreFix):
    global sourceMap
    imageName = tmp_path.split('/')[-1].split('.')[0]
    newImgName = imgPreFix + zfjTools.getWordFromLexicon() + zfjTools.getWordFromLexicon().capitalize()
    sourceMap[imageName] = newImgName
    return (
     imageName, newImgName)


def searchXcassets(file_dir, imgPreFix):
    global sourceTypeMap
    global xcassetsMap
    fs = os.listdir(file_dir)
    for dir in fs:
        tmp_path = os.path.join(file_dir, dir)
        if os.path.isdir(tmp_path):
            pass
        if tmp_path.endswith('.imageset'):
            try:
                if not igFil.isIgnoreFiles(tmp_path):
                    imgArr = saveNameToMap(tmp_path, imgPreFix)
                    new_path = tmp_path.replace(imgArr[0] + '.imageset', imgArr[1] + '.imageset')
                    if tmp_path != new_path:
                        os.rename(tmp_path, new_path)
                        conLog.info('[SeaXcas Scu] ' + tmp_path)
                        searchXcassets(new_path, imgPreFix)
            except Exception as e:
                try:
                    conLog.error('[SeaXcas Fail] ' + str(e))
                    searchXcassets(tmp_path, imgPreFix)
                finally:
                    e = None
                    del e

        elif not os.path.isdir(tmp_path):
            if '.xcassets' in tmp_path:
                if isImage(tmp_path):
                    imageType = '.' + tmp_path.split('.')[-1]
                    fatherPath = '/'.join(tmp_path.split('/')[:-1])
                    imageName = tmp_path.split('/')[-1].split('.')[0]
                    newImgName = imgPreFix + zfjTools.getWordFromLexicon() + zfjTools.getWordFromLexicon().capitalize()
                    new_path = tmp_path.replace('/' + imageName + imageType, '/' + newImgName + imageType)
                    os.rename(tmp_path, new_path)
                    partMap = {}
                    if fatherPath in xcassetsMap.keys():
                        partMap = xcassetsMap[fatherPath]
                    partMap[imageName] = newImgName
                    xcassetsMap[fatherPath] = partMap
        elif not os.path.isdir(tmp_path):
            if isNeedMissImg(tmp_path):
                if not igFil.isIgnoreFiles(tmp_path):
                    imageName = tmp_path.strip().split('/')[-1]
                    imageType = ''
                    if '@' in imageName:
                        nameList = imageName.split('@')
                        imageName = nameList[0]
                        imageType = '@' + nameList[-1]
                    else:
                        nameList = imageName.split('.')
                        imageName = nameList[0]
                        imageType = '.' + nameList[-1]
                    if imageName not in sourceMap.keys():
                        newImgName = imgPreFix + zfjTools.getWordFromLexicon() + zfjTools.getWordFromLexicon().capitalize()
                        sourceMap[imageName] = newImgName
                    else:
                        newImgName = sourceMap[imageName]
                    if imageName in sourceTypeMap.keys():
                        old_imageType = sourceTypeMap[imageName]
                        if old_imageType != imageType:
                            old_imageType += ',' + imageType
                            sourceTypeMap[imageName] = old_imageType
                        else:
                            sourceTypeMap[imageName] = imageType
                        new_path = tmp_path.replace(imageName, newImgName)
                        os.rename(tmp_path, new_path)
                        conLog.info('[SeaXcas Scu] ' + tmp_path)
        else:
            if os.path.isdir(tmp_path):
                searchXcassets(tmp_path, imgPreFix)


def upDateContentsJson():
    for fatherPath in xcassetsMap.keys():
        contentsJsonPath = fatherPath + '/Contents.json'
        imageNameMap = xcassetsMap[fatherPath]
        file_data = ''
        Ropen = open(contentsJsonPath, 'r')
        for line in Ropen:
            for imageName in imageNameMap.keys():
                line = line.replace(imageName, imageNameMap[imageName])

            file_data += line

        Ropen.close()
        Wopen = open(contentsJsonPath, 'w')
        Wopen.write(file_data)
        Wopen.close()


def isNeedMissImg(tmp_path):
    psss_path = [
     '.xcassets/', '.appiconset/', '.imageset/', '.launchimage/', '/Contents.json']
    for item in psss_path:
        if item in tmp_path:
            return False

    return isImage(tmp_path)


def isImage(tmp_path):
    imgType_list = [
     '.jpg', '.bmp', '.png', '.jpeg', '.rgb', '.tif', '.gif', '.jpeg']
    for imgType in imgType_list:
        if tmp_path.endswith(imgType):
            return True

    return False


def isHaveImage(line):
    image_list = []
    imgType_list = [
     '.jpg', '.bmp', '.png', '.jpeg', '.rgb', '.tif', '.gif', '.jpeg']
    for item in imgType_list:
        if item in line:
            if item not in image_list:
                image_list.append(item)

    return image_list


def replaceAtFile(file_path):
    isStoryboard = True if file_path.endswith('.storyboard') else False
    file_data = ''
    Ropen = open(file_path, 'r')
    for line in Ropen:
        for imageName in sourceMap:
            newImgName = sourceMap[imageName]
            if isStoryboard == True:
                line = line.replace('text="', '$$$$$').replace('title="', '')
                line = line.replace('"' + imageName + '"', '"' + newImgName + '"')
                line = line.replace('$$$$$', 'text="').replace('', 'title="')
            elif file_path.endswith('.swift'):
                if '"' + imageName + '"' in line:
                    line = line.replace(imageName, newImgName)
            elif imageName in sourceTypeMap.keys():
                if 'imageNamed:@"' not in line:
                    imageType = sourceTypeMap[imageName]
                    if ',' in imageType:
                        imageTypeList = imageType.split(',')
                        for item_imgType in imageTypeList:
                            line = line.replace(imageName + item_imgType, newImgName + item_imgType)

                    else:
                        line = line.replace(imageName + imageType, newImgName + imageType)
            elif 'imageNamed:@"' in line:
                line = imageName in line and line.replace('imageNamed:@"' + imageName, 'imageNamed:@"' + newImgName)
            elif '"' + imageName + '"' in line:
                line = line.replace('"' + imageName + '"', '"' + newImgName + '"')

        file_data += line

    Ropen.close()
    Wopen = open(file_path, 'w')
    Wopen.write(file_data)
    Wopen.close()


def startReplaceSouName(file_dir):
    fs = os.listdir(file_dir)
    for dir in fs:
        tmp_path = os.path.join(file_dir, dir)
        if not os.path.isdir(tmp_path):
            try:
                if not igFil.isIgnoreFiles(tmp_path):
                    if '/Contents.json' not in tmp_path:
                        replaceAtFile(tmp_path)
                        conLog.info('[RepSouNa OK] ' + tmp_path)
            except Exception as e:
                try:
                    conLog.error('[RepSouNa Fail] ' + str(e))
                finally:
                    e = None
                    del e

        else:
            startReplaceSouName(tmp_path)


def initData():
    global sourceMap
    global sourceTypeMap
    global xcassetsMap
    sourceMap = {}
    sourceTypeMap = {}
    xcassetsMap = {}


def startSourceName(file_dir, imgPreFix):
    initData()
    conLog.info('----------------------------------------')
    searchXcassets(file_dir, imgPreFix)
    personinfo = ZFJPersoninfo()
    personinfo.sourceMap = sourceMap
    personinfo.xcassetsMap = xcassetsMap
    conLog.info(sourceMap)
    conLog.info(xcassetsMap)
    conLog.info('----------------------------------------')
    upDateContentsJson()
    startReplaceSouName(file_dir)


if __name__ == '__main__':
    file_dir = '/Users/zhangfujie/Desktop/Obfuscated/'
    startSourceName(file_dir, '')