#! /usr/bin/env python 3.7 (3394)
#coding=utf-8
# Compiled at: 1969-12-31 18:00:00
#Powered by BugScaner
#http://tools.bugscaner.com/
#如果觉得不错,请分享给你朋友使用吧!
from PIL import Image
import imageScaleView, glob, os
sizeTupList = []
imgType_list = [
 '.jpg', '.bmp', '.png', '.jpeg', '.rgb', '.tif', '.gif', '.webp']

def isImage(tmp_path):
    global imgType_list
    for imgType in imgType_list:
        if tmp_path.endswith(imgType):
            return True

    return False


def scale_image(image_path, save_path, isCloseAlpha):
    global sizeTupList
    if save_path.endswith('/') == False:
        save_path += '/'
    image_ori = Image.open(image_path)
    image_name = image_path.split('/')[-1].split('.')[-2]
    image_type = image_path.split('/')[-1].split('.')[-1]
    image_wid = image_ori.width
    image_hei = image_ori.height
    img_path = None
    image_new = None
    if sizeTupList != None:
        if len(sizeTupList) > 0:
            myImg_wid = int(sizeTupList[0][0])
            myImg_hei = int(sizeTupList[0][-1])
            if myImg_wid != 0:
                if myImg_hei != 0:
                    image_new = image_ori.resize((myImg_wid, myImg_hei), Image.BILINEAR)
                    img_path = save_path + image_name + '@1x.' + image_type
                image_new = image_ori.resize((int(image_wid / 3), int(image_wid / 3)), Image.BILINEAR)
                img_path = save_path + image_name + '@1x.' + image_type
    if img_path != None:
        if image_new != None:
            saveImg(img_path, image_new, isCloseAlpha)
    img_path = None
    image_new = None
    if sizeTupList != None:
        if len(sizeTupList) > 0:
            myImg_wid = int(sizeTupList[1][0])
            myImg_hei = int(sizeTupList[1][-1])
            if myImg_wid != 0:
                if myImg_hei != 0:
                    image_new = image_ori.resize((myImg_wid, myImg_wid), Image.BILINEAR)
                    img_path = save_path + image_name + '@2x.' + image_type
                image_new = image_ori.resize((int(image_wid / 3 * 2), int(image_wid / 3 * 2)), Image.BILINEAR)
                img_path = save_path + image_name + '@2x.' + image_type
    if img_path != None:
        if image_new != None:
            saveImg(img_path, image_new, isCloseAlpha)
    img_path = None
    image_new = None
    if sizeTupList != None:
        if len(sizeTupList) > 0:
            myImg_wid = int(sizeTupList[2][0])
            myImg_hei = int(sizeTupList[2][-1])
            if myImg_wid != 0:
                if myImg_hei != 0:
                    image_new = image_ori.resize((myImg_wid, myImg_hei), Image.BILINEAR)
                    img_path = save_path + image_name + '@3x.' + image_type
                image_new = image_ori.resize((int(image_wid), int(image_wid)), Image.BILINEAR)
                img_path = save_path + image_name + '@3x.' + image_type
    if img_path != None:
        if image_new != None:
            saveImg(img_path, image_new, isCloseAlpha)


def saveImg(save_path, image_new, isCloseAlpha):
    if isCloseAlpha == True:
        try:
            image_new = remove_transparency(image_new)
            image_new = image_new.convert('RGB')
            image_new.save(save_path)
        except Exception as e:
            try:
                image_new.save(save_path)
            finally:
                e = None
                del e

    else:
        image_new.save(save_path)


def start_scale_image(old_image_path, new_image_path, isCloseAlpha):
    if old_image_path.endswith('/') == False:
        old_image_path += '/'
    old_image_path += '*.png'
    image_list = glob.glob(old_image_path)
    for image_path in image_list:
        try:
            scale_image(image_path, new_image_path, isCloseAlpha)
            meg = '[ScaleImg OK] ' + image_path
            imageScaleView.addTextEdit(meg)
        except Exception as e:
            try:
                meg = '[ScaleImg Fail] ' + str(e)
                imageScaleView.addTextEdit(meg)
            finally:
                e = None
                del e


def remove_transparency(img_pil, bg_colour=(255, 255, 255)):
    if img_pil.mode in ('RGBA', 'LA') or img_pil.mode == 'P' and 'transparency' in img_pil.info:
        alpha = img_pil.convert('RGBA').split()[-1]
        bg = Image.new('RGBA', img_pil.size, bg_colour + (255, ))
        bg.paste(img_pil, mask=alpha)
        return bg
    else:
        return img_pil


def changeImgFormat(image_path, new_image_path):
    if image_path.endswith('/') == False:
        image_path += '/'
    image_path += '*.png'
    image_list = glob.glob(image_path)
    for tmp_path in image_list:
        try:
            print(tmp_path)
            if new_image_path.endswith('/') == False:
                new_image_path += '/'
            imgType = tmp_path.split('.')[-1]
            imgName = tmp_path.split('/')[-1].split('.')[0]
            newImgPath = new_image_path + imgName + '.webp'
            im = Image.open(tmp_path).convert('RGB')
            im.save(newImgPath, 'WEBP')
            meg = '[ModifyImgType OK] ' + newImgPath
            imageScaleView.addTextEdit(meg)
        except Exception as e:
            try:
                meg = '[ModifyImgType Fail] ' + str(e) + tmp_path
                imageScaleView.addTextEdit(meg)
            finally:
                e = None
                del e


def startScaleImg(old_image_path, new_image_path, sizeTupList_pass, isCloseAlpha, upDateImgType=False):
    global sizeTupList
    meg = '***************Start:***************'
    imageScaleView.addTextEdit(meg)
    if sizeTupList_pass != None:
        sizeTupList = sizeTupList_pass
        start_scale_image(old_image_path, new_image_path, isCloseAlpha)
    if upDateImgType == True:
        changeImgFormat(old_image_path, new_image_path)
    meg = '***************End:***************'
    imageScaleView.addTextEdit(meg)