#! /usr/bin/env python 3.7 (3394)
#coding=utf-8
# Compiled at: 1969-12-31 18:00:00
#Powered by BugScaner
#http://tools.bugscaner.com/
#如果觉得不错,请分享给你朋友使用吧!
from PIL import Image
import hashlib, random, os, sys, confusionLog as conLog, ignoreFiles as igFil

def isImage(file_path):
    imgType = file_path.lower().split('.')[-1]
    imgType_list = ['jpg', 'bmp', 'png', 'jpeg', 'rgb', 'tif']
    if imgType in imgType_list:
        return True
    else:
        return False


def updateImgHash(file_path):
    img = Image.open(file_path)
    if '.jpeg' in file_path:
        img = img.convert('RGB')
    randomx = random.randint(0, img.size[0] - random.randint(0, 5))
    randomy = random.randint(0, img.size[1] - random.randint(0, 5))
    randomvalue = random.randint(0, 255)
    img.putpixel((randomx, randomy), randomvalue)
    img.save(file_path)


def getFileHash(file_path):
    Rbopen = open(file_path, 'rb')
    sha1obj = hashlib.sha1()
    sha1obj.update(Rbopen.read())
    hash = sha1obj.hexdigest()
    return hash


def startUpdateSourceHash(file_dir):
    fs = os.listdir(file_dir)
    for dir in fs:
        tmp_path = os.path.join(file_dir, dir)
        if not os.path.isdir(tmp_path):
            try:
                if not igFil.isIgnoreFiles(tmp_path):
                    if isImage(tmp_path):
                        old_hash = getFileHash(tmp_path)
                        updateImgHash(tmp_path)
                        new_hash = getFileHash(tmp_path)
                        conLog.info('[UPdHash OK] ' + tmp_path)
                        conLog.tips('[UPdHash Meg] Old:' + old_hash + '<->New:' + new_hash)
            except Exception as e:
                try:
                    conLog.error('[UPdHash Fail] ' + str(e))
                finally:
                    e = None
                    del e

        else:
            startUpdateSourceHash(tmp_path)


if __name__ == '__main__':
    file_dir = '/Users/zhangfujie/Desktop/Obfuscated/'
    startUpdateSourceHash(file_dir)