# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/28 19:55
# @Author  : chengp
# @File    : LZSS.py
# @Funtionality
class LZSS:
    def __init__(self,sWinSize=4096, fWinSize=15):
        # Size for search window
        self.searchWindowSize = sWinSize
        self.forwardWindowSize = fWinSize
        self.encodeIndex = 0
        self.maxMatchLen = 15
        self.lenMask = 0xf000  # 0xf0 0b11110000
        self.disMask = 0x0fff  # 0x0fff 0b0000111111111111
        self.thresHold=2

    def get_edgeOfSearchWin(self):
        return max(self.encodeIndex-self.searchWindowSize,0)

    def getBetterTuple(self,original_tuple,new_tuple):
        if new_tuple[1]>original_tuple[1] :
            return new_tuple
        return original_tuple

    def encode(self,content):
        tupleList=[]
        tempLen=len(content)
        #trans input  stream to tuple list
        while(self.encodeIndex<tempLen):
            leftEdge= self.get_edgeOfSearchWin()
            backIndex=self.encodeIndex-1
            frontIndex=self.encodeIndex
            res_tuple=(0,0,content[frontIndex])
            while(backIndex>=leftEdge):
                curBIndex=backIndex
                curFIndex=frontIndex
                count=0;
                while(curFIndex<tempLen and content[curBIndex]==content[curFIndex] and count< self.maxMatchLen):
                    curBIndex+=1;
                    curFIndex+=1;
                    count+=1;
                    # only length> threshold will be stored with distance/length tuple
                if(count>= self.thresHold):
                    if(curFIndex<tempLen):
                        new_tuple=(self.encodeIndex-1-backIndex,count,content[curFIndex])
                    else:
                        new_tuple = (self.encodeIndex -1- backIndex, count,'$')
                else:
                    new_tuple=(0,0,content[frontIndex])
                res_tuple=self.getBetterTuple(res_tuple,new_tuple)
                backIndex-=1
            if(res_tuple[1]==0):
                self.encodeIndex+=1
            else:
                self.encodeIndex+=res_tuple[1]
            tupleList.append(res_tuple)
        # trans tuple list to binary string
        BinStr=self.tupleList2BinStr(tupleList)
        return self.BinStr2Bytes(BinStr)

    def tupleList2BinStr(self,tupleList):
        BinStr=''
        for item in tupleList:
            if(item[1]==0):
                #if length=0 add flag '0' and use 8 bits to store data
                BinStr+='0'
                BinStr+=bin(item[2])[2:].zfill(8)
            else:
                #otherwise , add flag '1' and use 16 bits to store data.
                BinStr+='1'
                BinStr+=self.transTuple2BinStr(item[1],item[0])
        zeroNeeded=8-len(BinStr)%8
        if zeroNeeded<8:
            BinStr+='0'*zeroNeeded
            BinStr=bin(zeroNeeded)[2:].zfill(8)+BinStr
        return BinStr

    def BinStr2Bytes(self,BinStr):
        # trans binary string to bytes
        res=b""
        i=0
        size=len(BinStr)
        while i<size:
            b=BinStr[i:i+8]
            b='0b'+b
            res+=int(b,2).to_bytes(1,byteorder='big',signed=False)
            i+=8
        return res

    def decode(self, content):
        # get binary string
        BinStr=self.Bytes2BinStr(content)
        # get tuplelist
        tupleList=self.BinStr2tupleList(BinStr)
        # trans tuple list into original data
        res=""
        for item in tupleList:

            if (item[1] == 0):
                res += chr(item[2])
            else:
                backIndex = len(res) - 1 - item[0]
                count = item[1]
                while (count > 0):
                    res += res[backIndex]
                    backIndex += 1
                    count -= 1
        print(len(res))
        return res;

    def transTuple2BinStr(self,len, dis):
        # trans distance and length to 2 bytes
        blen=self.transLen2Bin(len)
        bdis=self.transDis2Bin(dis)
        num=blen|bdis

        num=bin(num)[2:].zfill(16)
        return num

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

    def Bytes2BinStr(self,res):
        # trans bytes to binary string
        i=0
        size=len(res)
        BinStr=''
        while i<size:
            b=res[i:i+1]
            b=int.from_bytes(b,byteorder='big',signed=False)
            b=bin(b)[2:].zfill(8)
            BinStr+=b
            i+=1
        return BinStr

    def BinStr2tupleList(self,BinStr):
        tupleList=[]
        #calculate how manry zeros are needed
        zeroNeed=int('0b'+BinStr[0:8],2);
        # remove the tail
        BinStr=BinStr[8:]
        BinStr=BinStr[:-zeroNeed]
        i=0
        size=len(BinStr)
        # trans binary string to tuple list
        while i<size:
            if BinStr[i]=='0':
                num=BinStr[i+1:i+9]
                num = '0b' + num
                num = int(num, 2)
                new_tuple = (0, 0, num)
                tupleList.append(new_tuple)
                i+=9
            else:
                num = BinStr[i + 1:i + 17]
                num = '0b' + num
                num=int(num,2)
                a=self.transDisFromBin(num)
                b=self.transLenFromBin(num)
                new_tuple=(a,b)
                tupleList.append(new_tuple)
                i+=17
        return tupleList