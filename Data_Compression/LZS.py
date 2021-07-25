# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/6 20:58
# @Author  : chengp
# @File    : LZS.py
# @Funtionality
import struct

import DataLoader


class LZS:
    def __init__(self,sWinSize=2047, fWinSize=15):
        # Size for search window
        self.searchWindowSize = sWinSize
        self.forwardWindowSize = fWinSize
        self.encodeIndex = 0

    def get_edgeOfSearchWin(self):
        return max(self.encodeIndex - self.searchWindowSize, 0)

    def getBetterTuple(self, original_tuple, new_tuple):
        if new_tuple[1] > original_tuple[1]:
            return new_tuple
        return original_tuple

    def encode(self,content):
        tupleList = []
        tempLen = len(content)
        # trans input stream into tuplelist
        while (self.encodeIndex < tempLen):
            leftEdge = self.get_edgeOfSearchWin()
            backIndex = self.encodeIndex - 1
            frontIndex = self.encodeIndex
            res_tuple = (0, 0, content[frontIndex])
            while (backIndex >= leftEdge):
                curBIndex = backIndex
                curFIndex = frontIndex
                count = 0;
                while (curFIndex < tempLen and content[curBIndex] == content[
                    curFIndex]):
                    curBIndex += 1;
                    curFIndex += 1;
                    count += 1;
                # only length> 1 will be trans to distance/length tuple
                if count>1:
                    if (curFIndex < tempLen):
                        new_tuple = (self.encodeIndex -1- backIndex, count, content[curFIndex])
                    else:
                        new_tuple = (self.encodeIndex -1- backIndex, count, '$')
                else:
                    new_tuple=(0, 0, content[frontIndex])

                res_tuple = self.getBetterTuple(res_tuple, new_tuple)
                backIndex -= 1
            if (res_tuple[1] == 0):
                self.encodeIndex += 1
            else:
                self.encodeIndex += res_tuple[1]
            tupleList.append(res_tuple)
            #trans tuplelist into binary string
        BinStr=self.tupleList2BinStr(tupleList)
        return  self.BinStr2Bytes(BinStr)

    def decode(self, content):
        #get binary string from bytes
        BinStr=self.Bytes2BinStr(content)
        # get tuplelist
        tupleList=self.BinStr2tupleList(BinStr)
        res=''
        # trans all tuple list into original data
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

    def tupleList2BinStr(self,tupleList):
        BinStr=''
        #define endMark
        endMark='110000000'
        for item in tupleList:
            # if length=0 add flag bit '0' use 8 bits to store data
            if item[1]==0:
                BinStr+='0'
                temp=bin(item[2])[2:].zfill(8)
                BinStr+=temp
            else:
                # otherwise add flag bit '1' , if distance <128 add flag bit '1' and use 7 bits to store distance
                BinStr+='1'
                Offset=item[0]+1
                if Offset<128:
                    BinStr+='1'
                    temp=bin(Offset)[2:].zfill(7)
                    BinStr+=temp
                    # or add flag bit'0', and use 11 bits to store distance
                else:
                    BinStr+='0'
                    temp=bin(Offset)[2:].zfill(11)
                    BinStr+=temp
                # for length
                length=item[1]
                if(length==2):
                    # if length=2 use '00' the following are the same
                    BinStr+='00'
                elif length==3:
                    BinStr+="01"
                elif length == 4:
                    BinStr+="10"
                elif length == 5:
                    BinStr += "1100"
                elif length == 6:
                    BinStr += "1101"
                elif length == 7:
                    BinStr+='1110'
                elif length >=8 and length <=22:
                    # if length is in this range, first add '1111' the calculate lenoff and use 4 bits to store, following are similar
                    BinStr+='1111'
                    lenOff=length-8
                    BinStr+=bin(lenOff)[2:].zfill(4)
                elif length>=23 and length <=37:
                    BinStr += '11111111'
                    lenOff = length - 23
                    temp=bin(lenOff)[2:].zfill(4)
                    BinStr += temp
                elif length>37:
                    N=int((length+7)/15)
                    prefix='1111'*N
                    lenOff=length-(N*15-7)
                    BinStr +=prefix
                    temp=bin(lenOff)[2:].zfill(4)
                    BinStr +=temp
                    # finally, add endMark
        BinStr+=endMark
        zeroNeeded=8-len(BinStr)%8
        # fill zeros
        if zeroNeeded<8:
            BinStr+='0'*zeroNeeded
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
        # remove endMark
        if BinStr[-9:]=='110000000':
            BinStr=BinStr[:-9]
        else:
            i=1
            while not BinStr[-i-9:-i] =='110000000':
                i+=1
            BinStr=BinStr[:-i-9]

        while(len(BinStr)>0):
            # if flag is '0', read element
            if BinStr[0]=='0':
                num=BinStr[1:9]
                BinStr=BinStr[9:]
                num='0b'+num
                num=int(num,2)
                new_tuple=(0,0,num)
                tupleList.append(new_tuple)
            else:
                # otherwise, read distance flag, if it is '1' then read 7 bits to get data,
                BinStr = BinStr[1:]
                if BinStr[0]=='1':
                    Offset='0b'+BinStr[1:8]
                    Offset=int(Offset,2)-1
                    BinStr=BinStr[8:]
                else:
                    # or read 11 bits to get data
                    Offset = '0b' + BinStr[1:12]
                    Offset = int(Offset, 2)-1
                    BinStr=BinStr[12:]

                # for length read 2 bits to see is 2 or 3, following are the same
                if BinStr[0:2]=='00':
                    length=2
                    BinStr=BinStr[2:]
                    new_tuple=(Offset,length)
                    tupleList.append(new_tuple)

                elif BinStr[0:2]=='01':
                    length = 3
                    BinStr = BinStr[2:]
                    new_tuple = (Offset, length)
                    tupleList.append(new_tuple)

                elif BinStr[0:2]=='10':
                    length = 4
                    BinStr = BinStr[2:]
                    new_tuple = (Offset, length)
                    tupleList.append(new_tuple)

                elif BinStr[0:4]=='1100':
                    length = 5
                    BinStr = BinStr[4:]
                    new_tuple = (Offset, length)
                    tupleList.append(new_tuple)

                elif BinStr[0:4]=='1101':
                    length = 6
                    BinStr = BinStr[4:]
                    new_tuple = (Offset, length)
                    tupleList.append(new_tuple)

                elif BinStr[0:4]=='1110':
                    length = 7
                    BinStr = BinStr[4:]
                    new_tuple = (Offset, length)
                    tupleList.append(new_tuple)
                # if 4 bits are '1111' read 4 more bits to see if it is '1111' if so, read 4 more ,
                # if not get lenoff data and calculate length
                # following are the same
                elif BinStr[0:4]=='1111':
                    N=1
                    while BinStr[N*4:N*4+4]=='1111':
                        N+=1
                    lenOff=BinStr[N*4:N*4+4]
                    BinStr=BinStr[N*4+4:]
                    lenOff='0b'+lenOff
                    lenOff=int(lenOff,2)

                    if N==1:
                        length=8+lenOff
                        new_tuple = (Offset, length)
                        tupleList.append(new_tuple)
                    elif N==2:
                        length = 23 + lenOff
                        new_tuple = (Offset, length)
                        tupleList.append(new_tuple)
                    else:
                        length=N*15-7+lenOff
                        new_tuple = (Offset, length)
                        tupleList.append(new_tuple)
        #return result.
        return tupleList
