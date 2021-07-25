# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/28 16:21
# @Author  : chengp
# @File    : Evaluater.py
# @Funtionality
import os
import DataLoader
# usde to calculate file size
def getSizeOfContent(file_name):
    file_stats = os.stat(file_name)
    print(f'File Size in Bytes is {file_stats.st_size}')
    print(f'File Size in KiloBytes is {file_stats.st_size / (1024)}')
