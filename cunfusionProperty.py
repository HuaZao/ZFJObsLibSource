#! /usr/bin/env python 3.7 (3394)
#coding=utf-8
# Compiled at: 1969-12-31 18:00:00
#Powered by BugScaner
#http://tools.bugscaner.com/
#如果觉得不错,请分享给你朋友使用吧!
import os, zfjTools, confusionLog as conLog, ignoreFiles as igFil
from singletonModel import ZFJPersoninfo
propertyMisMap = {}
property_list = []
swiftSysClass = []

def cycTraPropertyListMap(file_dir, propertyPrefix):
    fs = os.listdir(file_dir)
    for dir in fs:
        tmp_path = os.path.join(file_dir, dir)
        if not os.path.isdir(tmp_path):
            try:
                if tmp_path.endswith('.h'):
                    if not igFil.isIgnoreFiles(tmp_path):
                        pass
                if '+' not in tmp_path:
                    if 'AppDelegate.' not in tmp_path:
                        getPropertyNameAtHFile(tmp_path, propertyPrefix)
                        conLog.info('[ReadProH OK] ' + tmp_path)
                    if tmp_path.endswith('.swift'):
                        if not igFil.isIgnoreFiles(tmp_path):
                            if '+' not in tmp_path:
                                if 'AppDelegate.' not in tmp_path:
                                    getPropertyNameAtSwiftAndMiss(tmp_path, propertyPrefix)
                                    conLog.info('[ReadProH OK] ' + tmp_path)
            except Exception as e:
                try:
                    conLog.error('[ReadProH Fail] ' + str(e))
                finally:
                    e = None
                    del e

        else:
            cycTraPropertyListMap(tmp_path, propertyPrefix)


def getPropertyNameAtSwiftAndMiss(file_path, propertyPrefix):
    global propertyMisMap
    file_data = ''
    object_name = file_path.split('/')[-1].split('.')[0]
    partMap = {}
    bracketsCount = 0
    Ropen = open(file_path, 'r')
    for line in Ropen:
        propertyName = ''
        if 'var ' in line or 'let ' in line:
            if bracketsCount == 1:
                startIndex = line.find('var ') + 4 if 'var ' in line else line.find('let ') + 4
                endIndex = line.find('=') if '=' in line else line.find(':')
                propertyName = ''.join(line[startIndex:endIndex].split())
                if ':' in propertyName:
                    propertyName = propertyName[:propertyName.find(':')]
                propertyMissName = propertyPrefix + zfjTools.getWordFromLexicon() + zfjTools.getWordFromLexicon().capitalize()
                partMap[propertyName] = propertyMissName
                line = line.replace(propertyName, propertyMissName)
            if '{' in line:
                bracketsCount += 1
            else:
                if '}' in line:
                    bracketsCount -= 1
            for propertyName in list(partMap.keys()):
                if propertyName in line:
                    line = replaceForSwift(True, propertyName, partMap[propertyName], line)

            file_data += line

    if len(partMap.keys()) > 0:
        propertyMisMap[object_name] = partMap
    Ropen.close()
    Wopen = open(file_path, 'w')
    Wopen.write(file_data)
    Wopen.close()


def replaceForSwift(isMySelf, propertyName, propertyMissName, line):
    firstList = [
     ' ', '(', 'self.', ':']
    secondList = [' ', ')', ';', ',', '.', '{', '(', '\n']
    if isMySelf != True:
        firstList.append('.')
    for firstStr in firstList:
        for secondStr in secondList:
            if firstStr == 'set':
                repPropertyName = firstStr + propertyName.capitalize() + secondStr
                repPropertyMissName = repPropertyName.replace(propertyName.capitalize(), propertyMissName.capitalize())
            else:
                repPropertyName = firstStr + propertyName + secondStr
                repPropertyMissName = repPropertyName.replace(propertyName, propertyMissName)
            line = line.replace(repPropertyName, repPropertyMissName)

    return line


def getPropertyNameAtHFile(file_path, propertyPrefix):
    file_data = ''
    object_name = file_path.split('/')[-1].split('.')[0]
    partMap = {}
    Ropen = open(file_path, 'r')
    for line in Ropen:
        propertyNameTup = getPropertyNameTup(line, propertyPrefix)
        if propertyNameTup != None:
            propertyName = propertyNameTup[0]
            propertyMissName = propertyNameTup[-1]
            partMap[propertyName] = propertyMissName
            line = line.replace(propertyName, propertyMissName)
        file_data += line

    if len(partMap.keys()) > 0:
        propertyMisMap[object_name] = partMap
    Ropen.close()
    Wopen = open(file_path, 'w')
    Wopen.write(file_data)
    Wopen.close()


def getPropertyNameTup(line, propertyPrefix):
    line = line.replace('\n', '').strip()
    line = line[:line.find(';')]
    if '@property' in line:
        propertyName = None
        newLine = ''.join(line.split())
        if '(^' in newLine:
            propertyName = newLine[newLine.find('(^') + 2:newLine.find(')(')]
        else:
            propertyName = line.split()[-1].replace('*', '').replace(')', '')
        if len(propertyPrefix) > 0:
            propertyMissName = propertyPrefix + zfjTools.getWordFromLexicon() + zfjTools.getWordFromLexicon().capitalize()
        else:
            propertyMissName = zfjTools.getWordFromLexicon() + zfjTools.getWordFromLexicon().capitalize()
        return (
         propertyName, propertyMissName)
    else:
        return


def cycTraMyPropertyList(file_dir):
    fs = os.listdir(file_dir)
    for dir in fs:
        tmp_path = os.path.join(file_dir, dir)
        if not os.path.isdir(tmp_path):
            try:
                if tmp_path.endswith('.m') or tmp_path.endswith('.mm'):
                    if '/Pods/' not in tmp_path:
                        getMyPropertyList(tmp_path)
                        conLog.info('[GetGroL OK] ' + tmp_path)
                    if tmp_path.endswith('.swift'):
                        if '/Pods/' not in tmp_path:
                            getMyPropertyListForSwift(tmp_path)
                            conLog.info('[GetGroL OK] ' + tmp_path)
            except Exception as e:
                try:
                    conLog.error('[GetGroL Fail] ' + str(e))
                finally:
                    e = None
                    del e

        else:
            cycTraMyPropertyList(tmp_path)


def getMyPropertyListForSwift(file_path):
    global property_list
    object_name = file_path.split('/')[-1].split('.')[0]
    bracketsCount = 0
    file_data = ''
    Ropen = open(file_path, 'r')
    obj_nameList_2 = []
    for line in Ropen:
        if '{' in line:
            bracketsCount += 1
        else:
            if '}' in line:
                bracketsCount -= 1
        if bracketsCount == 1:
            obj_nameList_2 = []
        all_obj_list = list(propertyMisMap.keys())
        valueStr = None
        for obj_name in all_obj_list:
            new_line = ''.join(line.split())
            if ' ' + obj_name + '(' in line:
                startIndex = line.find('var ') + 4 if 'var ' in line else line.find('let ') + 4
                property_name = line[startIndex:line.find(obj_name + '(')].strip()
                property_name = property_name.split()[0]
                valueStr = obj_name + '&' + property_name
                if bracketsCount == 2:
                    obj_nameList_2.append(valueStr)
                else:
                    property_list.append(valueStr)
            elif ':' + obj_name + ')' in new_line:
                property_name = new_line[new_line.find('(') + 1:new_line.find(':')]
                if property_name.startswith('_'):
                    property_name = property_name.split('_')[-1]
                valueStr = obj_name + '&' + property_name
                if bracketsCount == 2:
                    obj_nameList_2.append(valueStr)
                else:
                    property_list.append(valueStr)
                continue

        if len(obj_nameList_2) > 0:
            for valueStr in obj_nameList_2:
                objName = valueStr.split('&')[0]
                proMap = propertyMisMap[objName]
                for proName in list(proMap.keys()):
                    line = replaceForSwift(False, proName, proMap[proName], line)

        file_data += line

    Ropen.close()
    Wopen = open(file_path, 'w')
    Wopen.write(file_data)
    Wopen.close()


def getMyPropertyList(file_path):
    object_name = file_path.split('/')[-1].split('.')[0]
    Ropen = open(file_path, 'r')
    for line in Ropen:
        all_obj_list = list(propertyMisMap.keys())
        for obj_name in all_obj_list:
            property_name = None
            obj_all = '[[' + obj_name + ' alloc]'
            obj_new = '[[' + obj_name + ' new]'
            new_line = ''.join(line.split())
            if obj_all in line or obj_new in line:
                if new_line.startswith(obj_name):
                    start_index = new_line.find('*') + 1
                    end_index = new_line.find('=')
                else:
                    start_index = 0
                    end_index = new_line.find('=')
                property_name = new_line[start_index:end_index]
                property_name = property_name.split('_')[-1].split('.')[-1]
                if obj_name + '&' + property_name not in property_list:
                    property_list.append(obj_name + '&' + property_name)
            elif obj_name + '*' in line or obj_name + ' *' in line or obj_name + ' * ' in line:
                if obj_name + ' *)' not in line:
                    property_name = line[line.find('*') + 1:].strip()
                    property_name = property_name[:property_name.find(' ')].strip()
                    if obj_name + '&' + property_name not in property_list:
                        property_list.append(obj_name + '&' + property_name)
            elif '[[' + obj_name + ' share' in line:
                if obj_name + '&' + obj_name not in property_list:
                    property_list.append(obj_name + '&' + obj_name)
                else:
                    if '[[' + obj_name in line:
                        if obj_name + '&' + obj_name not in property_list:
                            property_list.append(obj_name + '&' + obj_name)

    Ropen.close()


def cycTraMissPropertyAtMFile(file_dir):
    fs = os.listdir(file_dir)
    for dir in fs:
        tmp_path = os.path.join(file_dir, dir)
        if not os.path.isdir(tmp_path):
            try:
                if tmp_path.endswith('.m') or tmp_path.endswith('.mm') or tmp_path.endswith('.xib') or tmp_path.endswith('.storyboard'):
                    if '/Pods/' not in tmp_path:
                        missPropertyAtMFile(tmp_path)
                        conLog.info('[ConFunM OK] ' + tmp_path)
                    if tmp_path.endswith('.swift'):
                        if '/Pods/' not in tmp_path:
                            missPublicProAtSwiftFile(tmp_path)
                            conLog.info('[ConFunM OK] ' + tmp_path)
            except Exception as e:
                try:
                    conLog.error('[ConFunM Fail] ' + str(e))
                finally:
                    e = None
                    del e

        else:
            cycTraMissPropertyAtMFile(tmp_path)


def missPublicProAtSwiftFile(file_path):
    file_data = ''
    Ropen = open(file_path, 'r')
    for line in Ropen:
        for property_obj in property_list:
            property_name = property_obj.split('&')[-1]
            if property_name + '.' in line:
                object_name = property_obj.split('&')[0]
                partMap = propertyMisMap[object_name]
                for propertyName in partMap:
                    if property_name in line:
                        line = propertyName in line and replaceForSwift(False, propertyName, partMap[propertyName], line)

        file_data += line

    Ropen.close()
    Wopen = open(file_path, 'w')
    Wopen.write(file_data)
    Wopen.close()


def missPropertyAtMFile(file_path):
    object_name = file_path.split('/')[-1].split('.')[0]
    file_data = ''
    Ropen = open(file_path, 'r')
    for line in Ropen:
        line = missPropertyMySelf(line, object_name)
        line = missPropertyOther(line)
        file_data += line

    Ropen.close()
    Wopen = open(file_path, 'w')
    Wopen.write(file_data)
    Wopen.close()


def missPropertyMySelf(line, object_name):
    if object_name in propertyMisMap:
        partMap = propertyMisMap[object_name]
        for propertyName in list(partMap.keys()):
            if propertyName in line or propertyName.capitalize() in line:
                line = replaceLine(True, propertyName, partMap[propertyName], line)
                continue

    return line


def replaceLine(isMySelf, propertyName, propertyMissName, line):
    if propertyName == 'name':
        if '[[NSNotificationCenter defaultCenter] addObserver' in line:
            return line
        firstList = ['_', ' ', '=', 'set', '[', '(', ')', ':', '!']
        if isMySelf == True:
            firstList.append('self.')
            firstList.append('weakSelf.')
        else:
            firstList.append('.')
        secondList = [' ', '.', ']', ';', '(', ')', ':', '[', '{']
        for firstStr in firstList:
            for secondStr in secondList:
                if firstStr == 'set':
                    repPropertyName = firstStr + propertyName.capitalize() + secondStr
                    repPropertyMissName = repPropertyName.replace(propertyName.capitalize(), propertyMissName.capitalize())
                else:
                    repPropertyName = firstStr + propertyName + secondStr
                    repPropertyMissName = repPropertyName.replace(propertyName, propertyMissName)
                line = line.replace(repPropertyName, repPropertyMissName)

        return line


def isSpaceFront(line, propertyName):
    keyWorldList = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890'
    if propertyName in line:
        nextWorld = line[line.find(propertyName) - 1:line.find(propertyName)]
        if nextWorld not in keyWorldList:
            return True
        return False


def missPropertyOther(line):
    for property_obj in property_list:
        property_name = property_obj.split('&')[-1]
        if property_name in line:
            object_name = property_obj.split('&')[0]
            partMap = propertyMisMap[object_name]
            for propertyName in list(partMap.keys()):
                if propertyName in line or propertyName.capitalize() in line:
                    line = replaceLine(False, propertyName, partMap[propertyName], line)

    return line


def initData():
    global propertyMisMap
    global property_list
    global swiftSysClass
    propertyMisMap = {}
    property_list = []
    swiftSysClass = []


def startConfusionPro(file_dir, propertyPrefix):
    initData()
    conLog.info('----------------------------------------')
    cycTraPropertyListMap(file_dir, propertyPrefix)
    personinfo = ZFJPersoninfo()
    personinfo.propertyMisMap = propertyMisMap
    conLog.info(propertyMisMap)
    conLog.info('----------------------------------------')
    cycTraMyPropertyList(file_dir)
    conLog.info('----------------------------------------')
    cycTraMissPropertyAtMFile(file_dir)


if __name__ == '__main__':
    file_dir = '/Users/zhangfujie/Desktop/Obfuscated/'
    propertyPrefix = ''
    startConfusionPro(file_dir, propertyPrefix)