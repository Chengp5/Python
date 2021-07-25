# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/28 17:03
# @Author  : chengp
# @File    : main.py
# @Funtionality
import heapq
import struct
import time

import  DataLoader
import  LZ77
import  LZ78
import  Evaluater
import  LZW
import  Deflate
import  LZS
import  LZSS

if __name__ == "__main__":

     file='Data\\mc160.dev.txt'
     outputfile='Data\\mc160.dev_result.txt'

     #####################################################################
     start=time.time()
     obj = LZ77.LZ77(DataLoader.readDataBin(file))
     Bytes=obj.encode()
     DataLoader.writeDataBin(Bytes, outputfile)
     end=time.time()
     print('encoder spend %.3f s'%(end-start));

     Evaluater.getSizeOfContent(file)
     Evaluater.getSizeOfContent(outputfile)

     start=time.time()
     content=DataLoader.readDataBin(outputfile)
     strA = obj.decode(content)
     end = time.time()
     print('decoder spend %.3f s'%(end - start))

     ##########################good###################################

     start = time.time()
     obj = LZ78.LZ78()
     Bytes = obj.encode(DataLoader.readDataBin(file))
     DataLoader.writeDataBin(Bytes, outputfile)
     end=time.time()
     print('encoder spend %.3f s'%(end-start));

     Evaluater.getSizeOfContent(file)
     Evaluater.getSizeOfContent(outputfile)

     start=time.time()
     content = DataLoader.readDataBin(outputfile)
     strA = obj.decode(content)
     end = time.time()
     print('decoder spend %.3f s'%(end - start))

     ####################################################################
     start = time.time()
     obj= LZW.LZW()
     bytes = obj.encode(DataLoader.readDataBin(file))
     DataLoader.writeDataBin(bytes,outputfile)

     end=time.time()
     print('encoder spend %.3f s'%(end-start));
     Evaluater.getSizeOfContent(file)
     Evaluater.getSizeOfContent(outputfile)
     start=time.time()
     content=DataLoader.readDataBin(outputfile)
     strA = obj.decode(content)
     end = time.time()
     print('decoder spend %.3f s'%(end - start))

     ######################################################################


     #########################################################################
     start = time.time()
     obj= Deflate.Deflate()
     bytes = obj.encode(DataLoader.readDataBin(file))
     DataLoader.writeDataBin(bytes,outputfile)
     end=time.time()
     print('encoder spend %.3f s'%(end-start));
     Evaluater.getSizeOfContent(file)
     Evaluater.getSizeOfContent(outputfile)
     start=time.time()
     content=DataLoader.readDataBin(outputfile)
     strA = obj.decode(content)
     end = time.time()
     print('decoder spend %.3f s'%(end - start))

     # #############################################################################
     start = time.time()
     obj = LZS.LZS()
     bytes = obj.encode(DataLoader.readDataBin(file))
     DataLoader.writeDataBin(bytes,outputfile)
     end = time.time()
     print('encoder spend %.3f s' % (end - start));
     Evaluater.getSizeOfContent(file)
     Evaluater.getSizeOfContent(outputfile)
     start = time.time()
     content=DataLoader.readDataBin(outputfile)
     strA = obj.decode(content)
     end = time.time()
     print('decoder spend %.3f s' % (end - start))

     #############################################################################



     ##############################################################################
     start = time.time()
     obj = LZSS.LZSS()
     bytes = obj.encode(DataLoader.readDataBin(file))
     DataLoader.writeDataBin(bytes,outputfile)
     end = time.time()
     print('encoder spend %.3f s' % (end - start));
     Evaluater.getSizeOfContent(file)
     Evaluater.getSizeOfContent(outputfile)
     start = time.time()
     content=DataLoader.readDataBin(outputfile)
     strA = obj.decode(content)
     end = time.time()
     print('decoder spend %.3f s' % (end - start))