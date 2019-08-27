# uncompyle6 version 3.4.0
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.2 (default, Feb 12 2019, 08:15:36) 
# [Clang 10.0.0 (clang-1000.11.45.5)]
# Embedded file name: zfjTools.py
# Size of source mod 2**32: 5580 bytes
import uuid, random
from singletonModel import ZFJPersoninfo
import time, datetime, os, sys, threading
from psutil import net_if_addrs
version = 'V1.1.5'
baseTitle = 'ZFJObsLib-' + version + '特别版'
imageTypeList = [
 '.jpg', '.bmp', '.png', '.jpeg', '.rgb', '.tif', '.gif']
otherTypeList = [
 '.mp3', '.mp4', '.caf']

def is_number(num_str):
    try:
        float(num_str)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(num_str)
        return True
    except (TypeError, ValueError):
        pass

    return False


def get_mac_address():
    mac = uuid.UUID(int=(uuid.getnode())).hex[-12:]
    return ':'.join([mac[e:e + 2] for e in range(0, 11, 2)])


def getMacAddList():
    macList = []
    for valueItem in list(net_if_addrs().items()):
        for net in valueItem[1]:
            if ':' in net.address:
                if len(net.address) == 17:
                    macList.append(net.address)

    return macList


def getWordFromLexicon():
    personinfo = ZFJPersoninfo()
    lexicon_list = personinfo.lexicon_list
    if len(lexicon_list) == 0:
        readLexiconList()
        lexicon_list = personinfo.lexicon_list
    index = random.randint(0, len(lexicon_list) - 1)
    returnWord = lexicon_list[index].replace('\n', '')
    if returnWord == 'virtual':
        returnWord += 'Obj'
    return returnWord


def readLexiconList():
    global lexicon_str
    lexiconList = []
    if os.path.exists('lexicon20.txt') == True:
        Ropen = open('lexicon20.txt', 'r')
        text = Ropen.read()
        Ropen.close()
        lexiconList = text.split(',')
    else:
        lexiconList = lexicon_str.split(',')
        Wopen = open('lexicon20.txt', 'w')
        Wopen.write(lexicon_str.replace('\n', ''))
        Wopen.close()
        lexicon_str = None
    startIndex = random.randint(0, len(lexiconList) - 1005)
    lexicon_list = lexiconList[startIndex:startIndex + 1000]
    personinfo = ZFJPersoninfo()
    personinfo.lexicon_list = lexicon_list
    return lexicon_list


def is_contain_chinese(check_str):
    for ch in check_str:
        if '一' <= ch <= '\u9fff':
            return True

    return False


def getTimestamp():
    t = time.time()
    return str(int(t))


def getTimeStr():
    now_time = datetime.datetime.now().strftime('%Y/%m/%d')
    return now_time


def createZFJObsLibConfig():
    if os.path.exists('ZFJObsLibConfig') == False:
        Wopen = open('ZFJObsLibConfig', 'w')
        Wopen.close()
    elif os.path.exists('userInfors.txt') == True:
        os.remove('userInfors.txt')
        print('已删除userInfors.txt')


def savePrefixMap(prefixMap):
    createZFJObsLibConfig()
    file_data = ''
    isAdd = False
    Ropen = open('ZFJObsLibConfig', 'r')
    for line in Ropen:
        if 'prefixMap=' in line:
            file_data = 'prefixMap=' + str(prefixMap) + '\n'
            isAdd = True
        else:
            file_data += line

    if isAdd == False:
        file_data += 'prefixMap=' + str(prefixMap) + '\n'
        isAdd = True
    Ropen.close()
    Wopen = open('ZFJObsLibConfig', 'w')
    Wopen.write(file_data)
    Wopen.close()


def readPrefixMap():
    createZFJObsLibConfig()
    prefixMap = "{'proPreFix':'', 'objPreFix':'', 'funPreFix':'', 'imgPreFix':'', 'rubPreFix':'', 'folderPreFix':'', 'projectNamePreFix':''}"
    Ropen = open('ZFJObsLibConfig', 'r')
    for line in Ropen:
        if 'prefixMap=' in line:
            prefixMap = line.split('prefixMap=')[(-1)]

    Ropen.close()
    personinfo = ZFJPersoninfo()
    personinfo.prefixMap = eval(prefixMap)
    return eval(prefixMap)


def saveAccountPassWord(logInMap):
    createZFJObsLibConfig()
    file_data = ''
    isAdd = False
    Ropen = open('ZFJObsLibConfig', 'r')
    for line in Ropen:
        if 'logInMap=' in line:
            file_data = 'logInMap=' + str(logInMap) + '\n'
            isAdd = True
        else:
            file_data += line

    if isAdd == False:
        file_data += 'logInMap=' + str(logInMap) + '\n'
        isAdd = True
    Ropen.close()
    Wopen = open('ZFJObsLibConfig', 'w')
    Wopen.write(file_data)
    Wopen.close()


def readAccountPassWord():
    createZFJObsLibConfig()
    logInMap = "{'account':'', 'password':''}"
    Ropen = open('ZFJObsLibConfig', 'r')
    for line in Ropen:
        if 'logInMap=' in line:
            logInMap = line.split('logInMap=')[(-1)]

    Ropen.close()
    return eval(logInMap)


def startTiming():
    personinfo = ZFJPersoninfo()
    expireDate = personinfo.expireDate
    timeArray = time.strptime(expireDate, '%Y-%m-%d %H:%M:%S')
    expireDateStamp = int(time.mktime(timeArray))
    nowTimeStamp = int(time.time())
    if nowTimeStamp >= expireDateStamp:
        print('你好,你使用时间已经到期，继续使用可优惠购买!')
        os._exit(0)
    else:
        threading.Timer(1, startTiming).start()
# okay decompiling /Users/tanwan/Downloads/zfjTools.pyc