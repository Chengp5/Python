# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/28 15:28
# @Author  : chengp
# @File    : LZ77.py
# @Funtionality
import  struct
import  DataLoader
class LZ77:
    def __init__(self,data, sWinSize=4096, fWinSize=15):
        # Size for search window
        self.searchWindowSize = sWinSize
        self.forwardWindowSize = fWinSize
        self.encodeIndex=0
        self.content=data
        self.maxMatchLen=15
        self.lenMask=0xf000   #0xf0 0b11110000
        self.disMask=0x0fff #0x0fff 0b0000111111111111

    def get_edgeOfForwardWin(self):
        return min(self.encodeIndex+self.forwardWindowSize,len(self.content))

    def get_edgeOfSearchWin(self):
        return max(self.encodeIndex-self.searchWindowSize,0)

    def getBetterTuple(self,original_tuple,new_tuple):
        if new_tuple[1]>original_tuple[1] :
            return new_tuple
        return original_tuple

    def encode(self,needTupleList=False):
        tupleList=[]
        tempLen=len(self.content)
        #produce tuplelist from input stream
        while(self.encodeIndex<tempLen):
            leftEdge= self.get_edgeOfSearchWin()
            rightEdge=self.get_edgeOfForwardWin()
            backIndex=self.encodeIndex-1
            frontIndex=self.encodeIndex
            res_tuple=(0,0,self.content[frontIndex])
            # try to find longest  same pattern
            while(backIndex>=leftEdge):
                curBIndex=backIndex
                curFIndex=frontIndex
                count=0;
                while(curFIndex<tempLen and self.content[curBIndex]==self.content[curFIndex] and count<self.maxMatchLen):
                    curBIndex+=1;
                    curFIndex+=1;
                    count+=1;

                if(curFIndex<tempLen):
                    #tuple with format(distance, lenght ,next element)
                    new_tuple=(self.encodeIndex-1-backIndex,count,self.content[curFIndex])
                else:
                    #finial tuple
                    new_tuple = (self.encodeIndex-1-backIndex, count,'$')
                res_tuple=self.getBetterTuple(res_tuple,new_tuple)
                backIndex-=1
                # move index to next position and start next round
            if(res_tuple[1]==0):
                self.encodeIndex+=1
            else:
                self.encodeIndex+=res_tuple[1]
            tupleList.append(res_tuple)
            #if only need tuplelist return it
        if(needTupleList==True):
            return tupleList
        # if need a transformation between tuplelist and binary format....
        return self.tupleList2Bin(tupleList)

    def decode(self, content,toTupleList=False):
        res=""
        if(toTupleList==False):
            tupleList=self.Bin2tupleList(bytes(content))
        else:
            tupleList=content

        # get original data from tuplelist.
        for item in tupleList:

            if(item[1]==0):
                res+=chr(item[2])
            else:
                backIndex=len(res)-1-item[0]
                count=item[1]
                while(count>0):
                    res+=res[backIndex]
                    backIndex+=1
                    count-=1
        print(len(res))
        return res;

    def tupleList2Bin(self,tupleList):
        # trans tuplelist into byte stream
        res=b""
        for item in tupleList:
            if(item[1]==0):
                res+=struct.pack('B',0)
                res+=bytes(chr(item[2]), encoding = "utf8")
            else:
                res+=self.transTuple2TwoBytes(item[1],item[0])
        return res

    def Bin2tupleList(self,content_bytes):
        # trans byte stream into tuplelist
        tupleList=[]
        size=len(content_bytes)
        pos=0
        while pos<size:
            item=content_bytes[pos:pos+2]
            if item[0]==0 :
                new_tuple=(0,0,item[1])
            else:
                new_tuple=self.transTwoBytes2tuple(item)
            pos+=2
            tupleList.append(new_tuple)
        return tupleList

    def transTuple2TwoBytes(self,len, dis):
        #use two bytes to store distance and length
        blen=self.transLen2Bin(len)
        bdis=self.transDis2Bin(dis)
        num=blen|bdis

        p = num.to_bytes(2, byteorder='big', signed=False)
        #p=num&0xff00 + num&0x00ff
        return p

    def transTwoBytes2tuple(self, Bytes):
        # trans two bytes into store distance and length
        num = int.from_bytes(Bytes, byteorder='big', signed=False)
        a=self.transDisFromBin(num)
        b=self.transLenFromBin(num)
        new_tuple=(a,b)
        return new_tuple

    def transLen2Bin(self,numOflen):
        return numOflen<<12

    def transLenFromBin(self,num):
        a=num & self.lenMask
        a=a>>12
        return a

    def transDis2Bin(self, numOfDis):
        return numOfDis

    def transDisFromBin(self, num):
        return num & self.disMask