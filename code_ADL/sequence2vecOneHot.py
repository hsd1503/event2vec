# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 14:36:44 2016

@author: Stanley
"""

from datetime import datetime
import numpy as np
import os

def getMat(path, itemList):
    nitem = len(itemList)
    matOneHot = []

    fileList = os.listdir(path)
    for fName in fileList:
        print(fName)
        fin = open(path + fName)
        dimOneHot = [0.0]*nitem
        for line in fin.readlines():
            content = line.split(',')
            item = content[1].strip()
            pos = itemList.index(item)
            
            dimOneHot[pos] = dimOneHot[pos] + 1
    
        fin.close()
        matOneHot.append(dimOneHot)

    return matOneHot
    
def getExistItemList(mat, itemList):
    ndim = len(mat)
    nitem = len(mat[0])
    
    existItemList = []
    existItemIndexList = []
    
    for i in range(nitem):
        sum_dim = 0.0
        for j in range(ndim):
            sum_dim = sum_dim + mat[j][i]

        if sum_dim > 0:
            existItemList.append(itemList[i])
            existItemIndexList.append(i)
            
    return existItemList, existItemIndexList
                
    
def trimW(mat, existItemIndexList):
    nExistItem = len(existItemIndexList)
    
    ndim = len(mat)
    
    trimedW = np.zeros((nExistItem,ndim))
    for i in range(nExistItem):
        for j in range(ndim):
            trimedW[i, j] = mat[j][existItemIndexList[i]]
            
    return trimedW
    