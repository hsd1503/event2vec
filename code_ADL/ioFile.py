# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 10:16:53 2016

@author: Stanley
"""
import os
import csv
import numpy as np
import pickle

def getItemListSmall(path):
    """
    get item list, for small test
    !!!may be slow
    
    Args: 
        path: data file path
        
    Returns:
        itemList
    """
    itemList = []
    fileList = os.listdir(path)
    for fName in fileList:
        fin = open(path + fName)
        for line in fin.readlines():
            content = line.split(',')
            item = content[1].strip()
            if item not in itemList:
                itemList.append(item)
        fin.close()
    return itemList

def getItemList(f_name):
    """
    get item list, for all
    !!!W may be sparse
    
    Args: 
        path: data file path
        
    Returns:
        itemList
    """
    itemList = []
    fin = open(f_name)
    fin.readline()
    for line in fin.readlines():
        item = line.split(',')[1]
        itemList.append(item)
    return itemList


def getItemDic(path):

    itemDic = {}
    fin = open(path + "items.csv")
    fin.readline()
    for line in fin.readlines():
        content = line.split(',')
        itemDic[content[1]] = content[2]
    return itemDic
    
def writeResult(path, name, model, itemList):
    fin = open('items.csv')
    with open(path+name, 'wb') as csvfile:
        mywriter = csv.writer(csvfile, delimiter=',')
        for line in fin.readlines():
            item = line.split(',')[1]
            if item in itemList:
                try:
                    mywriter.writerow([item] + list(model[item]))
                except KeyError:
                    print(item, "not sampled")
    fin.close()
    print("write result done")
    return 0

def writeResult_pkl(fname, model, itemList):
    mydata = []
    existItemList = []
    fin = open('items.csv')
    for line in fin.readlines():
        item = line.split(',')[1]
        if item in itemList:
            try:
                mydata.append(model[item])
                existItemList.append(item)
            except KeyError:
                print(item, "not sampled")
    fin.close()
    
    output = open(fname, 'wb')
    pickle.dump( existItemList, output)
    pickle.dump( mydata, output)
    output.close()  
    
    print("write result done")
    return 0