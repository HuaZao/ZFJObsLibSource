# uncompyle6 version 3.4.0
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.2 (default, Feb 12 2019, 08:15:36) 
# [Clang 10.0.0 (clang-1000.11.45.5)]
# Embedded file name: encryptString.py
# Size of source mod 2**32: 5580 bytes
import importlib, os, re, sys, ignoreFiles as igFil, confusionLog as conLog
pch_code = '\nstatic char * decryptConstString(char* string){\n    char *origin_string = string;\n    while(*string) {\n        *string ^= 0xAA;\n        string++;\n    }\n    return origin_string;\n}\n\n#define ZFJ_NSSTRING(string) [NSString stringWithUTF8String:decryptConstString(string)]\n'
isAddCodeAtPCH = False

def searchPchFile(file_dir):
    fs = os.listdir(file_dir)
    for dir in fs:
        tmp_path = os.path.join(file_dir, dir)
        if not os.path.isdir(tmp_path):
            try:
                if tmp_path.endswith('.pch'):
                    pass
                if '/Pods/' not in tmp_path:
                    addCodeAtPch(tmp_path)
                    conLog.info('[SearPCH OK] ' + tmp_path)
            except Exception as e:
                try:
                    conLog.error('[SearPCH Fail] ' + str(e))
                finally:
                    e = None
                    del e

        else:
            searchPchFile(tmp_path)


def addCodeAtPch(tmp_path):
    global isAddCodeAtPCH
    file_data = ''
    Ropen = open(tmp_path, 'r')
    for line in Ropen:
        if '#endif' in line:
            file_data += pch_code + '\n'
            isAddCodeAtPCH = True
        file_data += line

    Ropen.close()
    Wopen = open(tmp_path, 'w')
    Wopen.write(file_data)
    Wopen.close()


def missCodeAtLine(line):
    line = line.replace('%@"', '%^*^"')
    new_line = ''
    line_list = line.split('@"')
    new_line_list = []
    for index in range(len(line_list)):
        item = line_list[index]
        if '"' in item:
            str_value = item[0:item.find('"')]
            str_reple = item[0:item.find('"') + 1]
            str_miss = 'ZFJ_NSSTRING("' + str_value + '")'
            item = item.replace(str_reple, str_miss)
            item = item.replace('%^*^"', '%@"')
            new_line_list.append(item)
        else:
            new_line_list.append(item)

    return ''.join(new_line_list)


def is_contain_chinese(check_str):
    for ch in check_str:
        if '一' <= ch <= '\u9fff':
            return True

    return False


def missCodeAtFile(file_path):
    file_data = ''
    isAddCodeAtM = False
    Ropen = open(file_path, 'r')
    for line in Ropen:
        if '@interface' in line or '@implementation' in line:
            if not isAddCodeAtPCH:
                if not isAddCodeAtM:
                    file_data += pch_code
                    file_data += line
                    isAddCodeAtM = True
        elif '@"' in line:
            if 'NSLog' not in line:
                if not is_contain_chinese(line):
                    if 'static' not in line:
                        if 'const' not in line:
                            file_data += missCodeAtLine(line)
        else:
            file_data += line

    Ropen.close()
    Wopen = open(file_path, 'w')
    Wopen.write(file_data)
    Wopen.close()


def searchMissCode(file_dir):
    fs = os.listdir(file_dir)
    for dir in fs:
        tmp_path = os.path.join(file_dir, dir)
        if not os.path.isdir(tmp_path):
            try:
                if not igFil.isIgnoreFiles(tmp_path):
                    pass
                if tmp_path.endswith('.m'):
                    missCodeAtFile(tmp_path)
                    conLog.info('[SearchStr OK] ' + tmp_path)
            except Exception as e:
                try:
                    conLog.error('[SearchStr Fail] ' + str(e))
                finally:
                    e = None
                    del e

        else:
            searchMissCode(tmp_path)


def replace(match):
    string = match.group(2) + '\x00'
    replaced_string = '((char []) {' + ', '.join(['%i' % (ord(c) ^ 170 if c != '\x00' else 0) for c in list(string)]) + '})'
    return match.group(1) + replaced_string + match.group(3)


def obfuscate(file):
    with open(file, 'r') as (f):
        code = f.read()
        f.close()
        code = re.sub('(ZFJ_NSSTRING\\(|ZFJ_CSTRING\\()"(.*?)"(\\))', replace, code)
        with open(file, 'w') as (f):
            f.write(code)
            f.close()


def encryptString(file_dir):
    fs = os.listdir(file_dir)
    for dir in fs:
        tmp_path = os.path.join(file_dir, dir)
        if not os.path.isdir(tmp_path):
            try:
                if not igFil.isIgnoreFiles(tmp_path):
                    pass
                if not tmp_path.endswith('.pch'):
                    obfuscate(tmp_path)
                    conLog.info('[EncrStr OK] ' + tmp_path)
            except Exception as e:
                try:
                    conLog.error('[EncrStr Fail] ' + str(e))
                finally:
                    e = None
                    del e

        else:
            encryptString(tmp_path)


def startEncryptStr(file_dir):
    conLog.info('--------------------开始查找PCH--------------------')
    searchPchFile(file_dir)
    conLog.info('--------------------开始查找字符串--------------------')
    searchMissCode(file_dir)
    conLog.info('--------------------开始加密字符串--------------------')
    encryptString(file_dir)
# okay decompiling /Users/tanwan/Downloads/encryptString.pyc
