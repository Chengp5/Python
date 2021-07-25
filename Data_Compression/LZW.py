# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/2 16:18
# @Author  : chengp
# @File    : LZW.py
# @Funtionality

import DataLoader
class LZW:
    def __init__(self):
        self.curIndex=0
        self.pos=1
        self.dictionaySize=255
        self.letterDict={}
        self.InitDictSize=0

    def encode(self,content):
        letterDict={}
        res=[]
        size=len(content)
        index=0
        pos=1
        # make initial dictionary
        while index<size:
            if not self.letterDict.__contains__(chr(content[index])):
                self.letterDict[chr(content[index])]=pos
                pos+=1
            index+=1

        self.pos=pos
        self.InitDictSize=self.pos-1
        # saved
        letterDict=self.letterDict.copy()
        #trans input stream into tuple list
        while(self.curIndex<size):
            prefix=""
            tempIndex=self.curIndex
            prefix += chr(content[tempIndex])
            nextIndex=tempIndex+1
            if(nextIndex>=size):
                break
            next=chr(content[nextIndex])
            # if dictionary contains prefix+next, move index forward
            while letterDict.__contains__(prefix+next):
                nextIndex+=1
                prefix=prefix+next
                if nextIndex>=size :
                    break;
                next=chr(content[nextIndex])

            newCode=letterDict[prefix]
            letterDict[prefix+next]=self.pos
            res.append(newCode)
            self.pos+=1
            self.curIndex=nextIndex
            # if dictionary is full of elements ,clear and reuse saved dictionary
            if self.pos>self.dictionaySize :
                letterDict=self.letterDict.copy()
                self.pos=self.InitDictSize
        if(len(prefix)>0):
            # final element
            newCode = letterDict[prefix]
            res.append(newCode)
            # trans list to bytes
        return self.List2Bytes(res);

    def decode(self,content):
        self.letterDict={}
        # get list from bytes
        List=self.Bytes2List(content)
        #get initial dictionary
        letterDict=self.letterDict.copy()
        pos=self.pos
        res=""

        size=len(List)
        i=0
        # trans list to original data
        OCODE =List[i]
        res += letterDict[OCODE]
        while i+1<size:
            i+=1
            letter = ''
            NCODE=List[i]
            #
            if( letterDict.__contains__(NCODE)):
                prefix = letterDict[NCODE]
            else:
                prefix = letterDict[OCODE]
                prefix +=letter

            res+=prefix
            letter=prefix[0]
            letterDict[pos]=letterDict[OCODE]+letter
            pos+=1
            OCODE=NCODE
            if pos>self.dictionaySize:
                letterDict=self.letterDict.copy()
                pos=self.InitDictSize

        return res[:-1];

    def List2Bytes(self,IndexList):
        # trans list to bytes
        res=b""
        head=self.InitDictSize.to_bytes(1,byteorder='big', signed=False)
        res+=head
        # save both dictionary data and compressed data
        keyList=self.letterDict.keys()

        for item in keyList:
            res+= str.encode(item)

        for item in IndexList:
                p = item.to_bytes(1, byteorder='big', signed=False)
                res+=p

        return res

    def Bytes2List(self,content):
        # trans bytes 2 list
        self.InitDictSize=content[0]
        i=1
        size=len(content)
        self.pos=1
        # first trans bytes to initial dictionary
        while i<=self.InitDictSize:
            self.letterDict[self.pos]=chr(content[i])
            self.pos+=1
            i+=1
        List=[]
        # then make tuple list
        while i<size:
            List.append(content[i])
            i+=1
        return List
