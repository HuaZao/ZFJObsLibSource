#! /usr/bin/env python 3.7 (3394)
#coding=utf-8
# Compiled at: 1969-12-31 18:00:00
#Powered by BugScaner
#http://tools.bugscaner.com/
#如果觉得不错,请分享给你朋友使用吧!
import addRandomCode, random, os, ignoreFiles as igFil, confusionLog as conLog
from singletonModel import ZFJPersoninfo
objectNamesMap = {}

def getObjectNames(file_dir, prefix):
    global objectNamesMap
    object_h_list = []
    object_m_list = []
    fs = os.listdir(file_dir)
    for dir in fs:
        tmp_path = os.path.join(file_dir, dir)
        if not os.path.isdir(tmp_path):
            if '/AppDelegate.' not in tmp_path:
                if '/ViewController.' not in tmp_path:
                    if not igFil.isIgnoreFiles(tmp_path):
                        object_name = tmp_path.split('/')[-1].split('.')[0]
                        if tmp_path.endswith('.h'):
                            if '+' not in tmp_path:
                                 object_h_list.append(object_name)
                        if tmp_path.endswith('.m'):
                            if '+' not in tmp_path:
                                 object_m_list.append(object_name)
                        if tmp_path.endswith('.swift'):
                            if '+' not in tmp_path:
                                 object_h_list.append(object_name)
                                 object_m_list.append(object_name)
                        if object_name in object_h_list:
                            if object_name in object_m_list:
                                replace_name = prefix + addRandomCode.getMissObjName(object_name).replace('new', 'ZFJ')
                                objectNamesMap[object_name] = replace_name
        else:
            getObjectNames(tmp_path, prefix)


def reviseObjectNames(tmp_path):
    file_data = ''
    Ropen = open(tmp_path, 'r')
    for line in Ropen:
        for object_name in objectNamesMap.keys():
            replace_name = objectNamesMap[object_name]
            if 'initWithRootViewController' in line or 'popToRootViewControllerAnimated' in line:
                if object_name == 'RootViewController':
                    conLog.tips('initWithRootViewController||popToRootViewControllerAnimated')
            elif 'navigationItem.titleView' in line:
                if object_name == 'titleView':
                    conLog.tips('titleView')
            elif 'project.pbxproj' in tmp_path or '#import' in line:
                line = line.replace(object_name + '.', replace_name + '.')
            else:
                line = line.replace(object_name, replace_name)

        file_data += line

    Ropen.close()
    Wopen = open(tmp_path, 'w')
    Wopen.write(file_data)
    Wopen.close()


def replaceFilesObjNames(file_dir):
    fs = os.listdir(file_dir)
    for dir in fs:
        tmp_path = os.path.join(file_dir, dir)
        if not os.path.isdir(tmp_path):
            try:
                if '/Pods/' not in tmp_path:
                    reviseObjectNames(tmp_path)
                    conLog.info('[ReObjNa OK] ' + tmp_path)
            except Exception as e:
                try:
                    conLog.error('[ReObjNa Fail] ' + str(e))
                finally:
                    e = None
                    del e

        else:
            replaceFilesObjNames(tmp_path)


def reviseFilesName(file_dir):
    fs = os.listdir(file_dir)
    for dir in fs:
        tmp_path = os.path.join(file_dir, dir)
        if not os.path.isdir(tmp_path):
            try:
                if not igFil.isIgnoreFiles(tmp_path):
                    if tmp_path.endswith('.h') or tmp_path.endswith('.m') or tmp_path.endswith('.xib') or tmp_path.endswith('.swift'):
                        for object_name in objectNamesMap.keys():
                            replace_name = objectNamesMap[object_name]
                            new_path = tmp_path.replace(object_name + '.', replace_name + '.')
                            if tmp_path != new_path:
                                os.rename(tmp_path, new_path)
                                conLog.info('[ReFilNa Scu] ' + tmp_path)

            except Exception as e:
                try:
                    conLog.error('[ReFilNa Fail] ' + str(e))
                finally:
                    e = None
                    del e

        else:
            reviseFilesName(tmp_path)


def initData():
    global objectNamesMap
    objectNamesMap = {}


def startObfuscatedObjName(path, prefix=''):
    initData()
    conLog.info('----------------------------------------')
    getObjectNames(path, prefix)
    personinfo = ZFJPersoninfo()
    personinfo.objectNamesMap = objectNamesMap
    conLog.info(objectNamesMap)
    replaceFilesObjNames(path)
    reviseFilesName(path)


if __name__ == '__main__':
    file_dir = '/Users/zhangfujie/Desktop/Obfuscated/'
    startObfuscatedObjName(file_dir)