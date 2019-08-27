#! /usr/bin/env python 3.7 (3394)
#coding=utf-8
# Compiled at: 1969-12-31 18:00:00
#Powered by BugScaner
#http://tools.bugscaner.com/
#如果觉得不错,请分享给你朋友使用吧!
import confusionLog as conLog, ignoreFiles as igFil, os
last_type = False
 
def deleteNotesInLine(line):
    global last_type
    old_line = line
    if last_type == True:
        pass
    if '*/' not in line:
        return
    else:
        if last_type == True:
            if '*/' in line:
                last_type = False
                line = line[line.find('*/') + 2:]
                if len(line) > 0:
                    line += '\n'
                return line
            if '//' in line:
                line = deleteTwoLine(line)
            if '/*' in line:
                line = deleteLineStars(line)
            if line.strip().startswith('#pragma'):
                line = ''
            if line.strip().startswith('#warning'):
                line = ''
        return line
 
 
def deleteTwoLine(line):
    if line.strip().startswith('//'):
        line = ''
    else:
        newLineList = []
        count = 0
        for index in range(0, len(line.split('//'))):
            linePart = line.split('//')[index]
            count += linePart.count('"')
            if count <= 1:
                newLineList.append(linePart)
            if count == 2:
                newLineList.append(linePart)
                break
 
        line = '//'.join(newLineList)
    if len(line) > 0:
        line += '\n'
    return line
 
 
def deleteLineStars(line):
    global last_type
    if '*/' not in line:
        last_type = True
    else:
        last_type = False
    if line.strip().startswith('/*'):
        line = line[:line.find('/*')]
    else:
        newLineList = []
        count = 0
        for index in range(0, len(line.split('/*'))):
            linePart = line.split('/*')[index]
            count += linePart.count('"')
            if count <= 1:
                newLineList.append(linePart)
            if count == 2:
                newLineList.append(linePart)
                break
 
        line = '//'.join(newLineList)
    if len(line) > 0:
        line += '\n'
    return line + '\n'
 
 
def readFileEveryLine(file_path):
    file_data = ''
    Ropen = open(file_path, 'r')
    isHaveUIKit = False
    for line in Ropen:
        new_line = deleteNotesInLine(line)
        if new_line != None:
            if len(new_line) > 0:
                file_data += new_line
 
    Ropen.close()
    Wopen = open(file_path, 'w')
    Wopen.write(file_data)
    Wopen.close()
 
 
def startDeleteNotes(file_dir):
    fs = os.listdir(file_dir)
    for dir in fs:
        tmp_path = os.path.join(file_dir, dir)
        if not os.path.isdir(tmp_path):
            try:
                if not igFil.isIgnoreFiles(tmp_path):
                    if tmp_path.endswith('.h') or tmp_path.endswith('.m') or tmp_path.endswith('.mm') or tmp_path.endswith('.swift') or tmp_path.endswith('.pch'):
                        readFileEveryLine(tmp_path)
                        conLog.info('[DelNote OK] ' + tmp_path)
            except Exception as e:
                try:
                    conLog.error('[DelNote Fail] ' + str(e))
                finally:
                    e = None
                    del e
 
        else:
            startDeleteNotes(tmp_path)