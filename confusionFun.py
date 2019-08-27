#! /usr/bin/env python 3.7 (3394)
#coding=utf-8
# Compiled at: 1969-12-31 18:00:00
#Powered by BugScaner
#http://tools.bugscaner.com/
#如果觉得不错,请分享给你朋友使用吧!
import os, ignoreFiles as igFil, confusionLog as conLog
from singletonModel import ZFJPersoninfo
import zfjTools
method_list_map = {}
property_list = []
_sysFun = [
 'removeFromSuperView',
 'removedOnCompletion',
 'touchesBegan',
 'touchesEnded',
 'application',
 'applicationWillResignActive',
 'applicationDidEnterBackground',
 'applicationWillEnterForeground',
 'applicationDidBecomeActive',
 'applicationWillTerminate',
 'setNilValueForKey',
 'setValue',
 'draw',
 'viewDidLoad']

def getFunNameMap(line, funNamePrefix):
    global _sysFun
    line = line.replace('\n', '').replace(': (', ':(').replace('*) ', '*)')
    line = line.lstrip()
    funName = None
    line_new = line.replace(' ', '')
    if line_new.startswith('+(') or line_new.startswith('-('):
        fun_list = getFunList(line)
        start_index = line.find(')') + 1
        end_index = line.find(';')
        if ':(' in line:
            end_index = line.find(':(') + 1
        funName = fun_list[0]
        if not igFil.isIgnoreFun(funName):
            repName = zfjTools.getWordFromLexicon() + zfjTools.getWordFromLexicon().capitalize() + zfjTools.getWordFromLexicon().capitalize() + 'Fun'
            if ':' in funName:
                repName += ':'
            if len(fun_list) > 1:
                funName = ':'.join(fun_list)
                repName = funName.replace(fun_list[0], repName)
            repName = funNamePrefix + repName
            if funName in _sysFun:
                return
        return {funName: repName}
    else:
        return


def getFunList(line):
    line = line.replace('+', '').replace('-', '').replace('+ ', '').replace('- ', '').rstrip(';').strip()
    fun_list = []
    if ':' in line:
        for item in line.split(' '):
            if ':' in item:
                item = item.split(':')[0]
                index = item.find(')') + 1
                item = item[index:]
                if len(item) > 0:
                    fun_list.append(item)

        if len(fun_list) == 1:
            fun_list[0] = fun_list[0] + ':'
        else:
            index = line.find(')') + 1
            fun_list.append(line[index:])
        return fun_list


def confusionAt_Swift_Obj(file_path, funNamePrefix):
    global method_list_map
    object_name = file_path.split('/')[-1].split('.')[0]
    method_list = []
    bracketsCount = 0
    file_data = ''
    Ropen = open(file_path, 'r')
    for line in Ropen:
        if bracketsCount == 1:
            if 'func ' in line:
                pass
        if '{' in line:
            if 'override' not in line:
                funcName = line[line.find('func ') + 5:line.find('{')].replace('_ ', '').replace(' ', '')
                main_funcName = funcName[:funcName.find('(')]
                if main_funcName not in _sysFun:
                    parameter = funcName[funcName.find('(') + 1:funcName.find(')')]
                    missFunName = zfjTools.getWordFromLexicon() + zfjTools.getWordFromLexicon().capitalize() + zfjTools.getWordFromLexicon().capitalize() + 'Fun'
                    funcName = main_funcName
                    if len(parameter) > 0:
                        funcName += '('
                        for item in parameter.split(','):
                            funcName += item.split(':')[0]
                            if parameter.split(',').index(item) != len(parameter.split(',')) - 1:
                                funcName += ','

                        funcName += ')'
                    line = line.replace(main_funcName, missFunName)
                    missFunName = funcName.replace(main_funcName, missFunName)
                    method_list.append({funcName: missFunName})
            if '{' in line:
                bracketsCount += 1
            else:
                if '}' in line:
                    bracketsCount -= 1
            file_data += line

    if len(method_list) > 0:
        method_list_map[object_name] = method_list
    Ropen.close()
    Wopen = open(file_path, 'w')
    Wopen.write(file_data)
    Wopen.close()


def confusionAt_H_Obj(file_path, funNamePrefix):
    file_data = ''
    object_name = file_path.split('/')[-1].split('.')[0]
    method_list = []
    Ropen = open(file_path, 'r')
    for line in Ropen:
        funNameMap = getFunNameMap(line, funNamePrefix)
        if funNameMap != None:
            method_list.append(funNameMap)
            funName = list(funNameMap.keys())[0]
            repName = funNameMap[funName]
            if ':' in line:
                funName_list = funName.split(':')
                count = 0
                for item in funName_list:
                    if item in line:
                        count += 1

                if count == len(funName_list):
                    file_data += line.replace(funName.split(':')[0], repName.split(':')[0])
                else:
                    file_data += line.replace(funName, repName)
        else:
            file_data += line

    if len(method_list) > 0:
        method_list_map[object_name] = method_list
    Ropen.close()
    Wopen = open(file_path, 'w')
    Wopen.write(file_data)
    Wopen.close()


def replaceMethod(line):
    global property_list
    for property_obj in property_list:
        property_name = property_obj.split('&')[-1]
        if property_name in line:
            object_name = property_obj.split('&')[0]
            line = replaceMethodWithObjectName(line, object_name)

    return line


def replaceMethodWithObjectName(line, object_name):
    method_list = method_list_map[object_name]
    funNameMap = getBestFunMap(line, method_list)
    if funNameMap == None:
        return line
    else:
        funName = list(funNameMap.keys())[0]
        repName = funNameMap[funName]
        if ':' in funName:
            funName = funName.split(':')[0] + ':'
            repName = repName.split(':')[0] + ':'
        line = line.replace(funName, repName)
        return line


def getBestFunMap(line, method_list):
    match_fun_list = []
    for funNameMap in method_list:
        funName = list(funNameMap.keys())[0]
        isMatch = True
        if len(funName.split(':')) >= 2:
            for method_name in funName.split(':'):
                if method_name not in line:
                    isMatch = False
                if len(method_name) == 0:
                    isMatch = method_name + ':' not in line and False

        else:
            if funName not in line:
                isMatch = False
        if isMatch == True:
            match_fun_list.append(funNameMap)

    funName_len = 0
    best_funNameMap = None
    for funNameMap_item in match_fun_list:
        funName = list(funNameMap_item.keys())[0]
        if len(funName) > funName_len:
            best_funNameMap = funNameMap_item
            funName_len = len(funName)

    if best_funNameMap == None:
        return
    else:
        return best_funNameMap


def getPropertyListForOC(file_path):
    object_name = file_path.split('/')[-1].split('.')[0]
    Ropen = open(file_path, 'r')
    for line in Ropen:
        all_obj_list = list(method_list_map.keys())
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
                property_list.append(obj_name + '&' + property_name)
            elif '[' + obj_name in line:
                if '[[' + obj_name not in line:
                    property_list.append(obj_name + '&' + obj_name)

    Ropen.close()


def getPropertyListForSwift(file_path):
    object_name = file_path.split('/')[-1].split('.')[0]
    Ropen = open(file_path, 'r')
    for line in Ropen:
        all_obj_list = list(method_list_map.keys())
        for obj_name in all_obj_list:
            if 'var ' in line or 'let ' in line:
                pass
            if obj_name + '(' in line:
                startIndex = line.find('var ') + 4 if 'var ' in line else line.find('let ') + 4
                endIndex = line.find('=') if '=' in line else line.find(':')
                propertyName = ''.join(line[startIndex:endIndex].split())
                if ':' in propertyName:
                    propertyName = propertyName[:propertyName.find(':')]
                property_list.append(obj_name + '&' + propertyName)
            else:
                if obj_name + '.' in line:
                    pass
                if obj_name + '.swift' not in line:
                    property_list.append(obj_name + '&' + obj_name)
                    continue

    Ropen.close()


def confusionAt_M_Obj(file_path):
    object_name = file_path.split('/')[-1].split('.')[0]
    file_data = ''
    Ropen = open(file_path, 'r')
    for line in Ropen:
        all_obj_list = list(method_list_map.keys())
        for obj_name in all_obj_list:
            if object_name == obj_name:
                line = replaceMethodWithObjectName(line, object_name)
            else:
                line = replaceMethod(line)

        file_data += line

    Ropen.close()
    Wopen = open(file_path, 'w')
    Wopen.write(file_data)
    Wopen.close()


def confusionSwiftObjFun(file_path):
    object_name = file_path.split('/')[-1].split('.')[0]
    file_data = ''
    Ropen = open(file_path, 'r')
    my_method_list = method_list_map[object_name]
    for line in Ropen:
        if len(my_method_list) > 0:
            my_funcNameMap = missMyFunForSwift(line, my_method_list)
            if my_funcNameMap != None:
                funcName = list(my_funcNameMap.keys())[0]
                missFunName = my_funcNameMap[funcName]
                if '(' in funcName:
                    if ')' in funcName:
                        funcName = funcName[:funcName.find('(')]
                        missFunName = missFunName[:missFunName.find('(')]
                line = line.replace(funcName, missFunName)
        for item in property_list:
            obj_name = item.split('&')[0]
            propertyName = item.split('&')[-1]
            if propertyName in line:
                if propertyName + '.swift' not in line:
                    method_list = method_list_map[obj_name]
                    funcNameMap = getBestFunMapForSwift(line, method_list)
                    if funcNameMap != None:
                        funcName = list(funcNameMap.keys())[0]
                        missFunName = funcNameMap[funcName]
                        if '(' in funcName:
                            if ')' in funcName:
                                funcName = funcName[:funcName.find('(')]
                                missFunName = missFunName[:missFunName.find('(')]
                    line = line.replace(funcName, missFunName)

        file_data += line

    Ropen.close()
    Wopen = open(file_path, 'w')
    Wopen.write(file_data)
    Wopen.close()


def missMyFunForSwift(line, my_method_list):
    newLine = line.replace(' ', '')
    for funcNameMap in my_method_list:
        funcName = list(funcNameMap.keys())[0]
        missFunName = funcNameMap[funcName]
        main_funcName = funcName
        if '(' in funcName:
            if ')' in funcName:
                missFunName = missFunName[:missFunName.find('(')]
                main_funcName = funcName[:funcName.find('(')]
        if main_funcName + '()' in newLine:
            return funcNameMap
        if main_funcName + '(' in newLine:
            if ')' in newLine:
                thisPraLiost = newLine[newLine.find('(') + 1:newLine.find(')')].split(',')
                yuanlaiPraList = funcName[funcName.find('(') + 1:funcName.find(')')].split(',')
                if len(yuanlaiPraList) == len(thisPraLiost):
                    isEqualCount = 0
                    for index in range(0, len(thisPraLiost)):
                        if yuanlaiPraList[index] == thisPraLiost[index].split(':')[0]:
                            isEqualCount += 1

        if isEqualCount == len(yuanlaiPraList) - 1:
            return funcNameMap
            continue


def getBestFunMapForSwift(line, method_list):
    newLine = line.replace(' ', '')
    for funcNameMap in method_list:
        funcName = list(funcNameMap.keys())[0]
        main_funcName = funcName[:funcName.find('(')]
        if funcName + '()' in newLine:
            return funcNameMap
        if main_funcName + '(' in newLine:
            if ')' in newLine:
                thisPraLiost = newLine[newLine.find('(') + 1:newLine.find(')')].split(',')
                yuanlaiPraList = funcName[funcName.find('(') + 1:funcName.find(')')].split(',')
                if len(yuanlaiPraList) == len(thisPraLiost):
                    isEqualCount = 0
                    for index in range(0, len(thisPraLiost)):
                        if yuanlaiPraList[index] == thisPraLiost[index].split(':')[0]:
                            isEqualCount += 1

        if isEqualCount == len(yuanlaiPraList) - 1:
            return funcNameMap
            continue


def cycTra_for_methodListMap(file_dir, funNamePrefix):
    fs = os.listdir(file_dir)
    for dir in fs:
        tmp_path = os.path.join(file_dir, dir)
        if not os.path.isdir(tmp_path):
            try:
                if tmp_path.endswith('.h'):
                    pass
                if not igFil.isIgnoreFiles(tmp_path):
                    if '+' not in tmp_path:
                        confusionAt_H_Obj(tmp_path, funNamePrefix)
                        conLog.info('[ConFunH OK] ' + tmp_path)
                    if tmp_path.endswith('.swift'):
                        if not igFil.isIgnoreFiles(tmp_path):
                            if '+' not in tmp_path:
                                if 'Tests.swift' not in tmp_path:
                                    confusionAt_Swift_Obj(tmp_path, funNamePrefix)
                                    conLog.info('[ConFunH OK] ' + tmp_path)
            except Exception as e:
                try:
                    conLog.error('[ConFunH Fail] ' + str(e))
                finally:
                    e = None
                    del e

        else:
            cycTra_for_methodListMap(tmp_path, funNamePrefix)


def cycTra_for_propertyList(file_dir):
    fs = os.listdir(file_dir)
    for dir in fs:
        tmp_path = os.path.join(file_dir, dir)
        if not os.path.isdir(tmp_path):
            try:
                if tmp_path.endswith('.m'):
                    if '/Pods/' not in tmp_path:
                        getPropertyListForOC(tmp_path)
                        conLog.info('[GetGroL OK] ' + tmp_path)
                    if tmp_path.endswith('.swift'):
                        if '/Pods/' not in tmp_path:
                            getPropertyListForSwift(tmp_path)
                            conLog.info('[GetGroL OK] ' + tmp_path)
            except Exception as e:
                try:
                    conLog.error('[GetGroL Fail] ' + str(e))
                finally:
                    e = None
                    del e

        else:
            cycTra_for_propertyList(tmp_path)


def cycTra_for_ConMFile(file_dir):
    fs = os.listdir(file_dir)
    for dir in fs:
        tmp_path = os.path.join(file_dir, dir)
        if not os.path.isdir(tmp_path):
            try:
                if tmp_path.endswith('.m'):
                    if '/Pods/' not in tmp_path:
                        confusionAt_M_Obj(tmp_path)
                        conLog.info('[ConFunM OK] ' + tmp_path)
                    if tmp_path.endswith('.swift'):
                        if '/Pods/' not in tmp_path:
                            confusionSwiftObjFun(tmp_path)
                            conLog.info('[ConFunM OK] ' + tmp_path)
            except Exception as e:
                try:
                    conLog.error('[ConFunM Fail] ' + str(e))
                finally:
                    e = None
                    del e

        else:
            cycTra_for_ConMFile(tmp_path)


def initData():
    global method_list_map
    global property_list
    method_list_map = {}
    property_list = []


def startConfusionFun(file_dir, funNamePrefix):
    initData()
    conLog.info('----------------------------------------')
    cycTra_for_methodListMap(file_dir, funNamePrefix)
    personinfo = ZFJPersoninfo()
    personinfo.method_list_map = method_list_map
    conLog.info(method_list_map)
    conLog.info('----------------------------------------')
    cycTra_for_propertyList(file_dir)
    conLog.info('----------------------------------------')
    cycTra_for_ConMFile(file_dir)


if __name__ == '__main__':
    file_dir = '/Users/zhangfujie/Desktop/Obfuscated/'
    startConfusionFun(file_dir, 'ms_')