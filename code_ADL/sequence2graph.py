# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 09:27:56 2016

@author: Stanley
"""

from datetime import datetime
import numpy as np
import os
import pandas as pd
import re
import matplotlib.pyplot as plt


def readDataFile(fname = '../DailyLife/OrdonezA_ADLs.txt'):
    """
    read separated chartevents.csv of each patient
    
    Args: 
        path: data file path
        fName: data file name
        
    Returns:
        dataTable: stored as list
    """
    itemList = set([])
    dataTable = []
    fin = open(fname)
    fin.readline()
    fin.readline()
    for line in fin.readlines():
        content = re.split(r'\t\t| \t' ,line.strip())
        item = content[2].strip()
        raw_time = content[0].strip()
        itemList.add(item)

        timeStamp = datetime.strptime(raw_time, '%Y-%m-%d %H:%M:%S')
        dataTable.append([item, timeStamp])
        
    dataDF = pd.DataFrame(dataTable, columns=['item', 'timeStamp'])
    dataDF = dataDF.sort_values(['timeStamp'], ascending=True)
    dataTable = dataDF.values.tolist()
            
    return sorted(list(itemList)), dataTable

def getWeightMap(Delta, Gama):
    weightMap = {}
    for i in range(int(Delta)+1):
        weightMap[i] = np.exp(-i/Gama)
        
    return weightMap

def calWeight(t1, t2, Gama, Delta, weightMap):
    """
    calculate weight by time interval
    
    Args: 
        t1: time stamp 1
        t2: time stamp 2
        Gama: a global par, a larger r captures the similarities among events 
            in a longer temporal range, and potentially increases the 
            connectivity of the tem- poral graph. A small r only considers 
            closely adjacent sym- bols as similar, and makes the temporal graph 
            more spread.
        Delta: a global par, If t2 minus t1 exceed Delta, weight is 0
        
    Returns:
        If t2 minus t1 exceed Delta, no more cal need, return -1, else
        
    """
#    delta is second
    time_delta = t2 - t1
    delta = int(time_delta.total_seconds())
    
#    year_delta = t2[0] - t1[0]
#    month_delta = t2[1] - t1[1]
#    day_delta = t2[2] - t1[2]
#    hour_delta = t2[3] - t1[3]
#    minute_delta = t2[4] - t1[4]
#    second_delta = t2[5] - t1[5]
    
    if delta > Delta:
        return -1
    else:
#        print(t2, t1, delta)
        return weightMap[delta]
        

def dataTable2Graph(W, dataTable, itemList, Gama, Delta, weightMap):
    """
    process one patient sequence data and add weight into W
    
    Args: 
        W: global weight matrix
        dataTable: patient sequence data
        itemList: all related items
        Gama, Delta: see in 'calWeight'
        
    Returns:
        W
        
    """
    nRow = len(dataTable)
    start = 1
    chunk = 0
    for i in range(nRow-1):
        ### if time stamp of i change, start of j need update, and reset chunk to 1
        if i > 0 and dataTable[i][1] > dataTable[i-1][1]:
            start += chunk
            chunk = 1
        ### if time stamp of i not change, chunk increment 1 
        else:
            chunk += 1
#        print i+1, start
        ### j iters from start to last
        for j in range(start-1, nRow):
            item1 = dataTable[i][0]
            item2 = dataTable[j][0]
            pos1 = itemList.index(item1)
            pos2 = itemList.index(item2)
            
            t1 = dataTable[i][1]
            t2 = dataTable[j][1]
            w = calWeight(t1, t2, Gama, Delta, weightMap)
            
#            print i+1, j+1, w
            
            ### if t2 exceed Delta to t1, early stop
            if w < 0:
                break
            ### if item1 is the same item2, not cal
            elif pos1 == pos2:
                continue
            ### others
            else:
                W[pos1, pos2] += w
        
    return W
    
#if __name__ == '__main__':
#    Gama = 300
#    Delta = 3600

def getGraph(Gama, Delta):
    """
    main, get graph
    !!!global par
    
    Args: 
        itemList: all related items
        
    Returns:
        W
        
    """

    ##################
    itemList, dataTable_1 = readDataFile('../DailyLife/OrdonezA_ADLs.txt')
    itemList, dataTable_2 = readDataFile('../DailyLife/OrdonezB_ADLs.txt')
    dataTable = dataTable_1 + dataTable_2
    itemList = sorted(list(itemList))
    nitem = len(itemList)
    W = np.zeros((nitem,nitem))
    weightMap = getWeightMap(Delta, Gama)
    
    W = dataTable2Graph(W, dataTable, itemList, Gama, Delta, weightMap)
    
    return W, itemList
    
if __name__ == '__main__':
    
    Delta_list = [100*1, 100*6, 100*36]
    T_list = [100*1, 100*6, 100*36, 100*36*6]
    
#    fig, ax = plt.subplots(nrows=3,ncols=4)
#    fig.tight_layout(pad=0)
#    plt.subplots_adjust(left=0, right=1.0, top=1.0, bottom=0, wspace=0, hspace=0.1)
    
    fig = plt.figure()
    W, itemList= getGraph(10, 10)
    plt.imshow(W, cmap='binary', interpolation='none')
    plt.colorbar()
    
#    for i in range(len(Delta_list)):
#        for j in range(len(T_list)):
#            Delta = Delta_list[i]
#            T = T_list[j]
#            W = None
#            W, itemList= getGraph(Delta, T)
#            W = W / np.max(W)
#            sub_fig = ax[i, j].imshow(W, cmap='binary', interpolation='none')
##            sub_fig.set_size_inches([10, 10])
#            sub_fig.axes.get_xaxis().set_visible(False)
#            sub_fig.axes.get_yaxis().set_visible(False)
##            ax[i, j].set_title('$\Delta$={0}, T={1}'.format(Delta, T), fontsize=8)

    plt.show()
    
    fig.savefig("bar.png", bbox_inches='tight', dpi=1600)












