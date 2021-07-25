# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/5 15:14
# @Author  : chengp
# @File    : Deflate.py
# @Funtionality
import heapq

import DataLoader
import  LZ77
class Deflate:

    class TreeNode:
        def __init__(self,weight,value):
            self.left=None
            self.right=None
            self.value=value
            self.weight=weight
            self.road=''

    def encode(self,content):
        #first LZ77 encode
        tupleList=self.LZ77encoder(content)
        #second Huffman encode
        Bytes=self.Huffmanencoder(tupleList)
        print(len(Bytes))
        return Bytes

    def decode(self,content):
        #first Huffman decode
        tupleList=self.Huffmandecoder(content)
        #second LZ77 decode
        res=self.LZ77decoder(tupleList)
        return res

    def LZ77decoder(self,content):
        obj=LZ77.LZ77("")
        res=obj.decode(content,toTupleList=True)
        return res

    def Huffmandecoder(self,content):
        #get tree structure data
        treeTructLen=content[0:8]
        content=content[8:]
        treeTructLen=int.from_bytes(treeTructLen,byteorder='big',signed=False)
        treeTruct=''
        while treeTructLen>=8:
            temp=content[0:1]
            content=content[1:]
            temp=int.from_bytes(temp,byteorder='big',signed=False)
            temp=bin(temp)
            treeTruct+=temp[2:].zfill(8)
            treeTructLen-=8


        if(treeTructLen>0):
            temp = content[0:1]

            content = content[1:]
            temp = int.from_bytes(temp, byteorder='big', signed=False)
            temp = bin(temp)[2:].zfill(8)
            ll=temp[-treeTructLen:]
            treeTruct+=ll


        #####################################################
        # get values data
        dictLen=content[0:8]
        content=content[8:]
        dictLen=int.from_bytes(dictLen,byteorder='big',signed=False)
        dicthead=''
        while dictLen >= 8:
            temp = content[0:1]
            content = content[1:]
            temp = int.from_bytes(temp, byteorder='big', signed=False)
            temp = bin(temp)
            dicthead += temp[2:].zfill(8)
            dictLen -= 8
        if dictLen>0:
            temp = content[0:1]
            content = content[1:]
            temp = int.from_bytes(temp, byteorder='big', signed=False)
            temp = bin(temp)[2:].zfill(8)
            ll = temp[-dictLen:]
            dicthead += ll

        #####################################################################
        i=0
        dict=[]
        size=len(dicthead)
        while i< size:
            if(dicthead[i]=='1'):
                temp=content[0:2]
                content=content[2:]
                temp=int.from_bytes(temp,byteorder='big',signed=False)
                dict.append(str(temp))
            else:
                temp = content[0:1]
                content = content[1:]
                temp =temp.decode()
                dict.append(temp)
            i+=1
        ######################################################################
        # rebuild tree and get dictionary back
        treeDict=self.rebuildHuffmanTree(treeTruct,dict)
        ######################################################################
        # get all huffman code
        last=content[0:1]
        last=int.from_bytes(last,byteorder='big',signed=False)
        content=content[1:]
        binCode=''
        while(len(content)>0):
            if(len(content)==1 and last>0):
                print(content[0])
                temp = content[0:1]
                content = content[1:]
                temp = int.from_bytes(temp, byteorder='big', signed=False)
                temp = bin(temp)
                lastContent=temp[2:].zfill(8)
                break
            temp=content[0:1]
            content=content[1:]
            temp = int.from_bytes(temp, byteorder='big', signed=False)
            temp = bin(temp)
            binCode += temp[2:].zfill(8)
        if last>0:
            binCode+=lastContent[-last:]
        index=0
        curIndex=1
        size=len(binCode)
        #DataLoader.writeStr('t2.txt', binCode)
        res=[]
        # get all elements according to huffman code
        while(curIndex<=size):
            if treeDict.__contains__(binCode[index:curIndex]):
                res.append(treeDict[binCode[index:curIndex]])
                index=curIndex
                curIndex=index+1
            else:
                curIndex+=1
        size=len(res)
        i=0
        tupleList=[]
        # make tuplelist.
        while i<size:
            if res[i]=='0':
                tupleList.append((0,0,int(res[i+1])))
            else:
                tupleList.append((int(res[i+1]),int(res[i])))
            i+=2
        return tupleList

    def rebuildHuffmanTree(self,treeStruct,dict):
        # use DFS to rebuild tree
        Root=self.DFS4RebuildHuffmanTree(list(treeStruct),dict)
        TreeDict={}
        # get huffman code based on DFS
        self.DFSWithBuildingRoad(Root,TreeDict,'0')
        # return huffman code dictionary
        return TreeDict;


    def DFS4RebuildHuffmanTree(self,treeStruct,dict):
        #DFS    0means non-leaf node, 1 means leaf node.
        if len(treeStruct)==0:
            return
        if treeStruct[0]=='1':
            node=self.TreeNode('-1',dict[0])
            del treeStruct[0]
            del dict[0]
            return node
        node=self.TreeNode('-1','-1')
        del treeStruct[0]
        node.left=self.DFS4RebuildHuffmanTree(treeStruct,dict)
        node.right=self.DFS4RebuildHuffmanTree(treeStruct,dict)
        return node



    def LZ77encoder(self,content):
        obj=LZ77.LZ77(content)
        tupleList=obj.encode(needTupleList=True)
        return tupleList

    def Huffmanencoder(self,tupleList):
        #calculate frequency of each element in tuplelist
        letterDict={}
        for item in tupleList:
            item0=str(item[0])
            item1=str(item[1])
            item2=str(item[2])
            if(not letterDict.__contains__(item0)):
                letterDict[item0]=0
            if (not letterDict.__contains__(item1)):
                letterDict[item1] = 0
            if (not letterDict.__contains__(item2)):
                letterDict[item2] = 0

            letterDict[item0]+=1
            letterDict[item1]+= 1
            letterDict[item2]+= 1

        NodeList=[]
        #make Nodes to build huffman tree
        for item in letterDict.items():
            NodeList.append(self.TreeNode( item[1],item[0]))
        # build tree
        tree=self.BuildHuffmanTree(NodeList)
        # save tree structure
        TreeBin=self.saveTree(tree)
        # save values
        BinDict=self.TreeTogetBinCodeDict(tree)

        #get huffman code for all tuples
        res=b""
        last=""
        BinCode=""
        for item in tupleList:
            item0 = str(item[0])
            item1 = str(item[1])
            item2 = str(item[2])
            if item1=='0':
                BinCode += BinDict['0']
                BinCode += BinDict[item2]
            else:
                BinCode += BinDict[item1]
                BinCode += BinDict[item0]
        DataLoader.writeStr('t1.txt', BinCode)
        while (len(BinCode)>=8):
            temp=BinCode[0:8]
            BinCode=BinCode[8:]
            temp='0b'+temp
            res+=int(temp,2).to_bytes(1, byteorder='big', signed=False)
        last=BinCode
        # indicates last byte have how many bits + binary code
        lastLen=len(last)
        if(lastLen>0):
            last='0b'+last
            print(int(last,2))
            res+=int(last,2).to_bytes(1, byteorder='big', signed=False)
        res=lastLen.to_bytes(1,byteorder='big',signed=False)+res


        print(len(TreeBin))
        print(len(res))
        #return final results
        return TreeBin+res

    def TreeTogetBinCodeDict(self,tree):
        BinDict={}
        # use huffman tree to make a dictionary
        self.DFS(tree,BinDict)
        return BinDict

    def DFSWithBuildingRoad(self,treeNode,BinDict,road):
        # usd when building buffman tree
        if treeNode==None:
            return
        if treeNode.left==None and treeNode.right==None:
            treeNode.road=road
            BinDict[treeNode.road]=treeNode.value
            return
        self.DFSWithBuildingRoad(treeNode.left,BinDict,road+'0')
        self.DFSWithBuildingRoad(treeNode.right,BinDict,road+'1')

    def DFS(self,treeNode,BinDict):
        #used when building dictionary
        if treeNode==None:
            return
        if treeNode.left==None and treeNode.right==None:
            BinDict[treeNode.value]=treeNode.road
            return
        self.DFS(treeNode.left,BinDict)
        self.DFS(treeNode.right,BinDict)

    def BuildHuffmanTree(self,NodeList):
        #build huffman tree
        while len(NodeList)>1:
            res=heapq.nsmallest(2,NodeList,lambda x:x.weight)
            NodeList.remove(res[0])
            NodeList.remove(res[1])
            totalWeight=res[0].weight+res[1].weight
            newNode=self.TreeNode(weight=totalWeight,value=0)
            newNode.left=res[0]
            newNode.right=res[1]
            NodeList.append(newNode)
        self.DFS4buildRoad(NodeList[0],'0')
        return NodeList[0]

    def DFS4buildRoad(self,treeNode,road):
        #build road from root to leaf node to get huffman code
        if treeNode == None:
            return
        if treeNode.left == None and treeNode.right == None:
            treeNode.road = road
            return
        self.DFS4buildRoad(treeNode.left,  road + '0')
        self.DFS4buildRoad(treeNode.right, road + '1')

    def saveTree(self,tree):
        #save tree structure and values
        NodeList=self.DFS4saveTree(tree)
        TreeBin=''
        valueList=[]
        for item in NodeList:
            if not item[1]==-1:
                valueList.append(item[1])
            TreeBin+=item[0]

        TreeLen=len(TreeBin)
        valueLen=len(valueList)
        ans=b""
        while( len(TreeBin)>=8):
            temp = TreeBin[0:8]
            TreeBin = TreeBin[8:]
            temp = '0b' + temp
            ans += int(temp, 2).to_bytes(1, byteorder='big', signed=False)

        if(len(TreeBin)>0):
            TreeBin='0b'+TreeBin
            ans += int(TreeBin, 2).to_bytes(1, byteorder='big', signed=False)
        ans=TreeLen.to_bytes(8,byteorder='big',signed=False)+ans
        # tree structure length+ tree structure  length is 8 bytes



        valueBin=b""
        head=""
        headBin=b""
        for item in valueList:
            if item.isdigit():
                valueBin+=int(item).to_bytes(2, byteorder='big', signed=False)
                head+='1'
            else:
                temp=item.encode(encoding='utf-8')
                valueBin +=temp
                head+='0'
        while (len(head) >= 8):
            temp = head[0:8]
            head = head[8:]
            temp = '0b' + temp
            headBin += int(temp, 2).to_bytes(1, byteorder='big', signed=False)
        if(len(head)>0):
            head='0b'+head
            headBin += int(head, 2).to_bytes(1, byteorder='big', signed=False)
        # length +indicate value type(0= read 1 byte，1= read 2 bytes2)+values lenght 8 bytes
        valueLenBin=valueLen.to_bytes(8,byteorder='big',signed=False)

        return ans+valueLenBin+headBin+valueBin

    def DFS4saveTree(self,treeNode):
        #used when save tree
        if treeNode == None:
            return
        if treeNode.left == None and treeNode.right == None:
            return [('1',treeNode.value)]
        res=[('0',-1)]
        l=self.DFS4saveTree(treeNode.left)
        r=self.DFS4saveTree(treeNode.right)
        return res+l+r
