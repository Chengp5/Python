# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/28 15:24
# @Author  : chengp
# @File    : DataLoader.py
# @Funtionality

import  os
def readData(fileName):
    file = fileName
    f = open(file)
    cotent = f.read()
    f.close()
    return cotent

def readDataBin(fileName):
    buf = bytearray(os.path.getsize(fileName))
    with open(fileName, 'rb') as f:
        f.readinto(buf)
    f.close()
    return buf

def writeData(fileName,content):
    f = open(fileName, 'w+')
    for item in content:
        line=""
        i=0
        while i < 2:
            line+=str(item[i])
            line+=','
            i+=1
        line+='\n'
        f.write(line)
    f.close()

def writeStr(fileName,content):
    f = open(fileName, 'w+')
    f.write(content)
    f.close()

def writeData2(fileName,content):
    f = open(fileName, 'w+')
    for item in content:
        line=""
        line+=str(item)
        line+='\n'
        f.write(line)
    f.close()

def writeDataBin(content,file_name):
    f=open(file_name,'wb+')
    f.write(content)
    f.close()