#! /usr/bin/env python 3.7 (3394)
#coding=utf-8
# Compiled at: 1969-12-31 18:00:00
#Powered by BugScaner
#http://tools.bugscaner.com/
#如果觉得不错,请分享给你朋友使用吧!
import logging, sys, rootViewUI, cleanRubResView
from singletonModel import ZFJPersoninfo
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s',
  datefmt='%H:%M:%S',
  filename='ZFJ.log',
  filemode='w')

def info(info):
    meg = 'Infor:' + str(info)
    logging.info(meg)
    rootViewUI.addTextEdit(meg)


def tips(info):
    meg = 'Tips:' + str(info)
    logging.info(meg)
    rootViewUI.addTextEdit(meg)


def warn(info):
    meg = 'Warn:' + str(info)
    logging.info(meg)
    rootViewUI.addTextEdit(meg)


def error(info):
    if "'utf-8' codec can't" not in info:
        if 'Permission denied' not in info:
            meg = 'Error:' + str(info)
            logging.info(meg)
            rootViewUI.addTextEdit(meg)


def info_delRes(info):
    meg = 'Infor:' + str(info)
    logging.info(meg)
    cleanRubResView.addTextEdit(meg)


def error_delRes(info):
    meg = 'Error:' + str(info)
    logging.info(meg)
    cleanRubResView.addTextEdit(meg)