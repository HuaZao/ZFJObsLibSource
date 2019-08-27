#! /usr/bin/env python 3.7 (3394)
#coding=utf-8
# Compiled at: 1969-12-31 18:00:00
#Powered by BugScaner
#http://tools.bugscaner.com/
#如果觉得不错,请分享给你朋友使用吧!


class ZFJPersoninfo(object):
    """docstring for ZFJPersoninfo"""
    _ZFJPersoninfo__instance = None

    def __init__(self):
        super(ZFJPersoninfo, self).__init__()

    def __new__(cls):
        if not cls._ZFJPersoninfo__instance:
            cls._ZFJPersoninfo__instance = object.__new__(cls)
        return cls._ZFJPersoninfo__instance

    account = 0
    expireDate = ''
    lexicon_list = []
    propertyMisMap = None
    PBXGroupMap = None
    method_list_map = None
    objectNamesMap = None
    sourceMap = None
    xcassetsMap = None
    rootView = None
    mainRootView = None
    scaleView = None
    cleanResView = None
    lexiconView = None
    reptileView = None
    missPrefixView = None
    isMissing = False
    mapView = None
    rubbishFileMap = {}
    prefixMap = {'proPreFix':'',  'objPreFix':'',  'funPreFix':'',  'imgPreFix':'',  'rubPreFix':'',  'folderPreFix':'',  'projectNamePreFix':''}

    def resetPersonInfo_Start_Miss(self):
        method_list_map = None
        objectNamesMap = None
        sourceMap = None