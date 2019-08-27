#! /usr/bin/env python 3.7 (3394)
#coding=utf-8
# Compiled at: 1969-12-31 18:00:00
#Powered by BugScaner
#http://tools.bugscaner.com/
#如果觉得不错,请分享给你朋友使用吧!
import userAgentList, requests, re
from lxml import html
from bs4 import BeautifulSoup
import base64, zfjTools
etree = html.etree
timeout = 30
requests.packages.urllib3.disable_warnings()
requests.adapters.DEFAULT_RETRIES = 5
imgType_list = [
 '.jpg', '.bmp', '.png', '.jpeg', '.rgb', '.tif', '.gif', '.jpeg']
audioType_list = [
 '.CD', '.WAVE', '.AIFF', '.MPEG', '.MP3', '.MPEG-4', '.MIDI', '.WMA', '.RealAudio', '.VQF', '.OggVorbis', '.AMR', '.APE', '.FLAC', '.AAC', '.OGG', '.M4A', '.WAV']
videoType_list = [
 '.MPEG', '.AVI', '.MOV', '.ASF', '.WMV', '.3GP', '.MKV', '.FLV', '.F4V', '.RMVB', '.RMHD', '.WebM', '.MP4']

def requestsDataBase(url):
    headers = {'User-Agent': userAgentList.getUserAgent()}
    response = None
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
    except Exception as e:
        try:
            response = requests.get(url, headers=headers, timeout=timeout, verify=False)
        except Exception as ee:
            try:
                print(ee)
            finally:
                ee = None
                del ee

        finally:
            e = None
            del e

    if response != None:
        response.encoding = 'GB2312'
        if response.status_code == 200:
            return response.text
        return ''


def getResourceUrlList(url, isImage, isAudio, isVideo):
    global audioType_list
    global imgType_list
    global videoType_list
    imageUrlList = []
    audioUrlList = []
    videoUrlList = []
    url = url.rstrip().rstrip('/')
    htmlStr = str(requestsDataBase(url))
    Wopen = open('reptileHtml.txt', 'w')
    Wopen.write(htmlStr)
    Wopen.close()
    Ropen = open('reptileHtml.txt', 'r')
    imageUrlList = []
    for line in Ropen:
        line = line.replace("'", '"')
        segmenterStr = '"'
        if "'" in line:
            segmenterStr = "'"
        lineList = line.split(segmenterStr)
        for partLine in lineList:
            if isImage == True:
                if 'data:image' in partLine:
                    base64List = partLine.split('base64,')
                    imgData = base64.urlsafe_b64decode(base64List[-1] + '=' * (4 - len(base64List[-1]) % 4))
                    base64ImgType = base64List[0].split('/')[-1].rstrip(';')
                    imageName = zfjTools.getTimestamp() + '.' + base64ImgType
                    imageUrlList.append(imageName + '$==$' + base64ImgType)
                for imageType in imgType_list:
                    if imageType in partLine:
                        imgUrl = partLine[:partLine.find(imageType) + len(imageType)].split(segmenterStr)[-1]
                        imgUrl = repairUrl(imgUrl, url)
                        sizeType = '_{size}'
                        if sizeType in imgUrl:
                            imgUrl = imgUrl.replace(sizeType, '')
                        imgUrl = imgUrl.strip()
                        if imgUrl.startswith('http://') or imgUrl.startswith('https://') and imgUrl not in imageUrlList:
                            imageUrlList.append(imgUrl)
                        else:
                            imgUrl = ''

            if isAudio == True:
                for audioType in audioType_list:
                    if audioType in partLine or audioType.lower() in partLine:
                        audioType = audioType.lower() if audioType.lower() in partLine else audioType
                        audioUrl = partLine[:partLine.find(audioType) + len(audioType)].split(segmenterStr)[-1]
                        audioUrl = repairUrl(audioUrl, url)
                        if audioUrl.startswith('http://') or audioUrl.startswith('https://') and audioUrl not in audioUrlList:
                            audioUrlList.append(audioUrl)
                        else:
                            audioUrl = ''

            if isVideo == True:
                for videoType in videoType_list:
                    if videoType in partLine or videoType.lower() in partLine:
                        videoType = videoType.lower() if videoType.lower() in partLine else videoType
                        videoUrl = partLine[:partLine.find(videoType) + len(videoType)].split(segmenterStr)[-1]
                        videoUrl = repairUrl(videoUrl, url)
                        if videoUrl.startswith('http://') or videoUrl.startswith('https://') or videoUrl.startswith('ed2k://') or videoUrl.startswith('magnet:?') or videoUrl.startswith('ftp://') and videoUrl not in videoUrlList:
                            videoUrlList.append(videoUrl)
                        else:
                            videoUrl = ''

    return (
     imageUrlList, audioUrlList, videoUrlList)


def repairUrl(resourceUrl, request_url):
    if resourceUrl.startswith('//'):
        resourceUrl = request_url.split('//')[0] + resourceUrl
    else:
        if resourceUrl.startswith('/'):
            if not resourceUrl.startswith('//'):
                urlList = request_url.replace('//', '$$').split('/')
                url_str = urlList[0].replace('$$', '//')
                resourceUrl = url_str + resourceUrl
    if 'u002F' in resourceUrl:
        resourceUrl = resourceUrl.replace('\\', '/').replace('/u002F', '/')
    resourceUrl = resourceUrl.strip()
    return resourceUrl


def getNoteInfors(url, fatherNode, childNode):
    url = url.rstrip().rstrip('/')
    htmlStr = requestsDataBase(url)
    Wopen = open('reptileHtml.txt', 'w')
    Wopen.write(htmlStr)
    Wopen.close()
    html_etree = etree.HTML(htmlStr)
    dataArray = []
    if html_etree != None:
        nodes_list = html_etree.xpath(fatherNode)
        for k_value in nodes_list:
            partValue = k_value.xpath(childNode)
            if len(partValue) > 0:
                dataArray.append(partValue[0])

    return dataArray


if __name__ == '__main__':
    url = 'https://www.woyaogexing.com/touxiang/'
    fatherNode = '//div[@class="pMain"]/div'
    childNode = './a/img/@src'
    dataArray = getNoteInfors(url, fatherNode, childNode)
    print(dataArray)