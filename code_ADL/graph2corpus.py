# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 10:06:53 2016

@author: Stanley
"""
import random
import numpy as np
from sequence2graph import getGraph

def getNextWord(distriCum, tmp):
    """
    get next word,
    distriCum is a ascending list, 
    iterate num in distriCum, until tmp exceed num, and return index
    
    Args: 
        distriCum: cumulated distribution
        tmp: sampled number
        
    Returns:
        index of next word
    """
    for num in distriCum:
        if tmp < num:
            return distriCum.index(num)

def getSentence(W, itemList, nWords):
    """
    get one sentence,
    
    Args: 
        W: 
        itemList: all related items
        nWords: global par, number of words in a sentence
        
    Returns:
        sentence string
    """
    ### wordList stores index of words
    wordList = []
    sentence = ""
    
    nitem = len(itemList)
    ### random first word
    wordList.append(random.randint(0,nitem-1))
    for i in range(nWords-1):
#        print 'the', i, 'word is', wordList[i], itemList[wordList[i]]
        distri = W[wordList[i], :]
        distriCum = list(np.cumsum(distri))
        distriMax = distriCum[nitem-1]
        tmp = random.uniform(0, distriMax)
#        print 'sample within', distriMax
#        print 'sampled', tmp
#        print 'distriCum', distriCum
        wordList.append(getNextWord(distriCum, tmp))
#        print 'the next word is ', wordList[i+1], itemList[wordList[i+1]]
    
    for word in wordList:
#        print word
        if word is not None:
            sentence += (itemList[word] + " ")
    sentence += "\n"
    
    return sentence
    
def writeCorpus(fname, W, itemList, nWords, nSentence):
    """
    write corpus
    
    Args: 
        path: 
        fName: 
        W: 
        itemList: all related items
        nWords: global par, number of words in a sentence
        nSentence: global par, number of sentences
        
    Returns:
        corpus.txt
    """
    fout = open(fname, 'w')
    for i in range(nSentence):
        if i % 1000 == 0:
            print(i)
        sentence = getSentence(W, itemList, nWords)
        fout.write(sentence)
    fout.close()
    
    return 0



if __name__ == '__main__':
    
    W, itemList = getGraph(300, 3600)
    writeCorpus('ADL_corpus.txt', W, itemList, 20, 50000)


