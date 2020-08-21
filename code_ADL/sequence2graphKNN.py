# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 10:55:02 2016

@author: Stanley
"""

from datetime import datetime
import numpy as np
import os

def readDataFile(path, fName):
    """
    read separated chartevents.csv of each patient
    
    Args: 
        path: data file path
        fName: data file name
        
    Returns:
        dataTable: stored as list
    """
    dataTable = []
    fin = open(path + fName)
    for line in fin.readlines():
        content = line.split(',')
        item = content[1].strip()
        
        dataTable.append(item)
        
    return dataTable
        

def dataTable2Graph(W, dataTable, itemList, K):
    nRow = len(dataTable)
    chunk = []
    for i in range(nRow-K):
        chunk = dataTable[i:i+K]
        for item1 in chunk:
            for item2 in chunk:
                pos1 = itemList.index(item1)
                pos2 = itemList.index(item2)
                if pos1 == pos2:
                    continue
                W[pos1, pos2] += 1
        
    return W
    
def getGraph(path, itemList, K):
    
    nitem = len(itemList)
    W = np.zeros((nitem,nitem))
    
    fileList = os.listdir(path)
    for fName in fileList:
        print(fName)
        dataTable = readDataFile(path, fName)
        W = dataTable2Graph(W, dataTable, itemList, K)
        
    return W
    
def trimW(W, existItemIndexList):
    nExistItem = len(existItemIndexList)
    trimedW = np.zeros((nExistItem,nExistItem))
    for i in range(nExistItem):
        for j in range(nExistItem):
            trimedW[i, j] = W[existItemIndexList[i], existItemIndexList[j]]
            
    return trimedW
    