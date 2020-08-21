# -*- coding: utf-8 -*-

import numpy as np
import os
import matplotlib.pyplot as plt
import gensim
import sequence2graph as s2g
import graph2corpus as g2c
import ioFile
import graphProperty as gp
import csv
import pickle
from collections import Counter
from sequence2graph import getGraph
from sequence2graph import readDataFile
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import pylab


def plot_with_labels(low_dim_embs, labels, filename='tsne.png'):
  assert low_dim_embs.shape[0] >= len(labels), "More labels than embeddings"
  plt.figure(figsize=(6, 4))  # in inches
  for i, label in enumerate(labels):
    x, y = low_dim_embs[i, :]
    plt.scatter(x, y)
    if label == 'Showering':
        plt.annotate(label,
                     xy=(x, y),
                     xytext=(-5, 2),
                     textcoords='offset points',
                     size = 16,
                     ha='right',
                     va='top')    
    else:
        plt.annotate(label,
                     xy=(x, y),
                     xytext=(5, 2),
                     textcoords='offset points',
                     size = 16,
                     ha='left',
                     va='top')
    plt.savefig('ALD.eps')

def read_corpus(fname = 'ADL_corpus.txt'):
    data = []
    with open(fname) as fin:
        for line in fin:
            content = line.strip().split(' ')
            data.extend(content)
    return data

def get_embedding():
    data = read_corpus()
    print(Counter(data))
    
    W, itemList = getGraph(300, 3600)
    sentences = gensim.models.word2vec.LineSentence("ADL_corpus.txt")
    model = gensim.models.word2vec.Word2Vec(sentences, size=2, window=5, min_count=3, workers=4, min_alpha=0.1, batch_words=128)
    
    embeddings = []
    for item in itemList:
        embeddings.append(model[item])
    embeddings = np.array(embeddings)
    
    return embeddings

def plot_item():
    
#    tsne = TSNE(perplexity=5, n_components=2, init='pca', n_iter=5000)
#    low_dim_embs = tsne.fit_transform(embeddings)
#    pca = PCA(n_components=2)
#    low_dim_embs = pca.fit_transform(embeddings)
    low_dim_embs = embeddings
    
    plot_with_labels(low_dim_embs, itemList)

    np.savetxt('raw_embs.csv', low_dim_embs, delimiter=',')

def plot_activity(fname):
#    low_dim_embs = np.genfromtxt('low_dim_embs.csv', delimiter=',')
#    low_dim_embs = low_dim_embs + np.array([1.0, 1.0])

    low_dim_embs = embeddings
    
    _, dataTable_1 = readDataFile(fname)
    _, itemList = getGraph(300, 3600)
    
    daily_activity = []
    one_day = []
    current_day = dataTable_1[0][1].date()
    for item, my_time in dataTable_1:
        if my_time.date() == current_day:
            one_day.append(item)
        else:
            daily_activity.append(one_day)
            current_day = my_time.date()
            one_day = [item]
    
    plt.figure()
    pylab.ylim([-5,5])
    pylab.xlim([0,15])
    for one_day in daily_activity:
        tmp_data = []
        start_point = np.array([0.0, 0.0])
        tmp_data.append(list(start_point))
        for item in one_day:
            end_point = start_point + low_dim_embs[itemList.index(item)]
            tmp_data.append(list(end_point))
            start_point = end_point
        tmp_data = np.array(tmp_data)
    
        plt.plot(tmp_data[:,0], tmp_data[:,1])
    plt.savefig(fname+'_act_A.eps')


plot_activity('../DailyLife/OrdonezA_ADLs.txt')
plot_activity('../DailyLife/OrdonezB_ADLs.txt')


#plot_item()