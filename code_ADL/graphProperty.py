# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 10:05:34 2016

@author: Stanley
"""
import numpy as np
import matplotlib.pyplot as plt

def getNodeDistri(W):
    nodeDegree = []
    for row in W:
        nodeDegree.append(sum(row != 0))
    nodeDegree = [item for item in nodeDegree if item != 0]
    y = np.bincount(nodeDegree)
    x = range(len(y))
    plt.scatter(x, y)
    plt.title("node distribution")
    
    return 0

def getDensity(W):
    print("graph density is:", 1.0 * sum(sum(W != 0)) / (len(W)**2))
    
    return 0
    
def checkConnectivity(W):
    for i in range(len(W)):
        if sum(W[:,i]) == 0 and sum(W[i,:]) == 0:
            print(i, 'error')
    print("check connectivity done")
    return 0
    
def getExistItem(W):
    nn = 0
    for i in range(len(W)):
        if sum(W[:,i]) != 0 or sum(W[i,:]) != 0:
            nn += 1
    print("Exist item number", nn)
    return 0

def getExistItemList(W, itemList):
    existItemList = []
    existItemIndexList = []
    for i in range(len(W)):
        if sum(W[:,i]) != 0 or sum(W[i,:]) != 0:
            existItemList.append(itemList[i])
            existItemIndexList.append(i)
    return existItemList, existItemIndexList

def plot2D(model, itemList):
    x = []
    y = []
    itemMy = []
    for item in itemList:
        try:
            x.append(model[item][0])
            y.append(model[item][1])
            itemMy.append([item, model[item][0], model[item][1]])
        except KeyError:
            continue
    plt.scatter(x, y)
    
    return 0