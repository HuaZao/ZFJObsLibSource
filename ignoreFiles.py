#! /usr/bin/env python 3.7 (3394)
#coding=utf-8
# Compiled at: 1969-12-31 18:00:00
#Powered by BugScaner
#http://tools.bugscaner.com/
#如果觉得不错,请分享给你朋友使用吧!
import confusionLog as conLog
ignore_Files = [
 '/Pods/', '/Vendor/', '/LIB/', '/Lib/', '/lib/', '/.git/', '/Gategory/', '/Podfile', '/Podfile.lock', '/README.md']

def isIgnoreFiles(tmp_path):
    for item in ignore_Files:
        if item in tmp_path:
            return True

    return False


fun_list = [
 'init']

def isIgnoreFun(funName):
    for item in fun_list:
        if funName.startswith(item):
            return True

    return False