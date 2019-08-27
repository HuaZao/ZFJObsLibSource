#! /usr/bin/env python 3.7 (3394)
#coding=utf-8
# Compiled at: 1969-12-31 18:00:00
#Powered by BugScaner
#http://tools.bugscaner.com/
#如果觉得不错,请分享给你朋友使用吧!
import addRandomCode
import random
import os
import confusionLog as conLog
import ignoreFiles as igFil
from singletonModel import ZFJPersoninfo
allObjRubCodeMap = {}
 
def callRubbishFun(line, rubFunMap):
    count = getSpaceCount(line)
    space = ' ' * count
    rubbishFun = ''
    for key in rubFunMap:
        rubbishFun += space + '[self ' + rubFunMap[key] + '];' + '\n'
 
    return rubbishFun
 
 
def addCodeAtHFile(file_path, rubCodeTuple):
    stateCode = 0
    file_data = ''
    Ropen = open(file_path, 'r')
    for line in Ropen:
        if '#import' in line:
            stateCode = 1
        if '<uikit uikit.h="">' in line:
            stateCode = -1
        if stateCode == 1:
            if len(''.join(line.split())) == 0:
                file_data += '#import <uikit uikit.h="">\n'
                stateCode = -1
        if '@end' in line:
            file_data += '\n' + rubCodeTuple[0]
            file_data += line
        else:
            file_data += line
 
    Ropen.close()
    Wopen = open(file_path, 'w')
    Wopen.write(file_data)
    Wopen.close()
 
 
def addCodeAtMFile(file_path, rubCodeTuple):
    file_data = ''
    Ropen = open(file_path, 'r')
    isLastEnd = False
    isCallRubbishFun = False
    isAddImportCode = False
    for line in Ropen:
        new_line = ''.join(line.split())
        if '@interface' in new_line:
            isLastEnd = False
        if '@implementation' in new_line:
            isLastEnd = True
        if '#import' in new_line:
            if isAddImportCode == False:
                file_data += line
                file_data += rubCodeTuple[4]
                isAddImportCode = True
        elif 'super viewDidLoad' in line or 'self == [super init' in line or 'self = [super init' in line:
            if not isCallRubbishFun:
                if not line.startswith('//'):
                    file_data += line
                    isCallRubbishFun = True
                    file_data += callRubbishFun(line, rubCodeTuple[3])
        elif '@end' == new_line:
            if isLastEnd == True:
                if isCallRubbishFun == False:
                    file_data += '\n' + createInitFun(rubCodeTuple[3])
                file_data += '\n' + rubCodeTuple[1] + '\n'
                file_data += line
        else:
            file_data += line
 
    Ropen.close()
    Wopen = open(file_path, 'w')
    Wopen.write(file_data)
    Wopen.close()
 
 
def createInitFun(rubFunMap):
    initCode = ''
    initCode += '- (instancetype)init{\n'
    previousLine = '    if (self == [super init]){\n'
    initCode += previousLine
    initCode += callRubbishFun(previousLine, rubFunMap) + '\n'
    initCode += '    }\n'
    initCode += '    return self;\n'
    initCode += '}\n'
    return initCode
 
 
def realizeRubbishFunCode(file_dir, amount, rubPrefix):
    global allObjRubCodeMap
    personinfo = ZFJPersoninfo()
    rubbishFileMap = personinfo.rubbishFileMap
    fs = os.listdir(file_dir)
    for dir in fs:
        tmp_path = os.path.join(file_dir, dir)
        if not os.path.isdir(tmp_path):
            object_name = tmp_path.split('/')[-1].split('.')[0]
            if object_name not in rubbishFileMap.keys():
                rubCodeTuple = None
                if object_name not in allObjRubCodeMap.keys():
                    rubCodeTuple = addRandomCode.addRandomClass(amount, rubPrefix)
                    allObjRubCodeMap[object_name] = rubCodeTuple
                else:
                    rubCodeTuple = allObjRubCodeMap[object_name]
                if tmp_path.endswith('.h'):
                    if not notUpdateFile(tmp_path):
                        addCodeAtHFile(tmp_path, rubCodeTuple)
                        conLog.info('[AddCode OK] ' + tmp_path)
                if tmp_path.endswith('.m'):
                    if not notUpdateFile(tmp_path):
                        addCodeAtMFile(tmp_path, rubCodeTuple)
                        conLog.info('[AddCode OK] ' + tmp_path)
            continue
            realizeRubbishFunCode(tmp_path, amount, rubPrefix)
 
 
def notUpdateFile(tmp_path):
    if '+' in tmp_path:
        return True
    elif '/Pods/' in tmp_path:
        return True
    elif 'AppDelegate.' in tmp_path:
        return True
    else:
        return igFil.isIgnoreFiles(tmp_path)
 
 
def propertyListAtMFile(file_dir):
    fs = os.listdir(file_dir)
    for dir in fs:
        tmp_path = os.path.join(file_dir, dir)
        if not os.path.isdir(tmp_path):
            try:
                if tmp_path.endswith('.m'):
                    if not notUpdateFile(tmp_path):
                        getPropertyList(tmp_path)
                        conLog.info('[CallFun OK] ' + tmp_path)
            except Exception as e:
                try:
                    conLog.error('[CallFun Fail] ' + str(e))
                finally:
                    e = None
                    del e
 
        else:
            propertyListAtMFile(tmp_path)
 
 
def getPropertyList(file_path):
    object_name = file_path.split('/')[-1].split('.')[0]
    file_data = ''
    Ropen = open(file_path, 'r')
    for line in Ropen:
        spaceCount = getSpaceCount(line)
        file_data += line
        for obj_name in allObjRubCodeMap:
            rubCodeTuple = allObjRubCodeMap[obj_name]
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
                file_data += ' ' * spaceCount + '[' + property_name + ' ' + rubCodeTuple[2] + '];\n'
 
    Ropen.close()
    Wopen = open(file_path, 'w')
    Wopen.write(file_data)
    Wopen.close()
 
 
def getSpaceCount(line):
    count = 0
    line_list = line.split(' ')
    for item in line_list:
        if len(item) == 0:
            count += 1
        else:
            count += 1
            break
 
    if line.split('\n')[0].endswith('{'):
        count += 4
    return count - 1
 
 
def initData():
    global allObjRubCodeMap
    allObjRubCodeMap = {}
 
 
def startAddRubbishCode(file_dir, amount, rubPrefix):
    if amount <= 0:
        conLog.error('[AddCode Fail] <=0')
        return
    initData()
    realizeRubbishFunCode(file_dir, amount, rubPrefix)
    propertyListAtMFile(file_dir)
 
 
if __name__ == '__main__':
    file_dir = '/Users/zhangfujie/Desktop/Obfuscated/'
    startAddRubbishCode(file_dir, 5, '')