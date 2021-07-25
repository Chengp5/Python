# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/29 15:31
# @Author  : chengp
# @File    : LZ78.py
# @Funtionality
import DataLoader


class LZ78:
    def __init__(self):
        self.curIndex=0
        self.pos=1
        self.dictionaySize=255

    def encode(self,content):
        letterDict={}
        res=[]
        size=len(content)
        # get tuples from input stream
        while(self.curIndex<size):
            prefix=""
            tempIndex=self.curIndex
            prefix+=chr(content[tempIndex])
            newTuple=(0,str.encode(prefix[0]))
            while letterDict.__contains__(prefix):
                tempIndex+=1
                if tempIndex>=size :
                    prefix+='$'
                    break;
                prefix+=chr(content[tempIndex])

            if (tempIndex-self.curIndex)>newTuple[0]:
                newTuple=(letterDict[prefix[:-1]],str.encode(prefix[-1:]))

            res.append(newTuple)
            letterDict[prefix]=self.pos
            self.pos+=1
            self.curIndex=tempIndex+1;

            if self.pos>self.dictionaySize :
                letterDict.clear()
                self.pos=1

        #DataLoader.writeData('t1.txt',res)
        # trans tuples to bytes
        return self.tupleList2Bytes(res);

    def decode(self,content):
        tupleList=self.Bytes2tupleList(content)
       # DataLoader.writeData('t2.txt', tupleList)
        letterDict={}
        pos=1
        res=""
        # trans tuples to original data
        for item in tupleList:
            prefix=""
            if item[0]==0:
                prefix+=item[1].decode()
            else:
                prefix+=letterDict[item[0]]
                prefix+=item[1].decode()
            res+=prefix
            letterDict[pos]=prefix
            pos+=1
            if pos >self.dictionaySize:
                pos=1
                letterDict.clear()
        return res[:-1];

    def tupleList2Bytes(self,tupleList):
        res=b""
        infoHead=0
        pos=0
        temp=b""
        # if not in dictionary use 8 bits to store  add head flag 0,otherwise use 16 bits to store with head flag 1.
        for item in tupleList:
            if item[0]==0:
                temp += item[1]
                infoHead=infoHead|0
            else:
                p = item[0].to_bytes(1, byteorder='big', signed=False)
                temp+=p
                temp += item[1]
                infoHead = infoHead |1
            if (pos == 7):
                se=infoHead.to_bytes(1, byteorder='big', signed=False)
                res+=se
                res+=temp
                temp=b""
                infoHead=0
                pos=0
                continue
            pos+=1
            infoHead=infoHead<<1
        # fill one byte with 0-7 '0' bits
        if pos<7 and len(temp)>0:
            infoHead=infoHead<<(7-pos)
            se = infoHead.to_bytes(1, byteorder='big', signed=False)
            res += se
            res += temp

        return res

    def Bytes2tupleList(self,content):
        #trans bytes to tuplelist
        i=0
        size=len(content)
        tupleList=[]
        while i< size:
            infoHead=content[i]
            i+=1
            pos = 7
            while pos>=0:
                isNotChar=infoHead&(1<<pos)
                isNotChar=isNotChar>>pos
                if isNotChar==1:
                    if (i+2)<=size:
                        temp= content[i:i+2]
                        i+=2
                        new_tuple=(temp[0],str.encode(chr(temp[1])))
                        tupleList.append(new_tuple)
                    else:
                        break
                else:
                    if i < size:
                        temp = content[i]
                        i +=1
                        new_tuple=(0,str.encode(chr(temp)))
                        tupleList.append(new_tuple)
                    else:
                        break
                pos-=1
            if i>=size:
                break
        return tupleList



