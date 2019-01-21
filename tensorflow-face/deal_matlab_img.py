#!/usr/bin/python
#coding=utf-8

import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat

def reformat(samples, labels):
    '''
     （ 0       1       2     3）                   (3       0      1      2)
     (图片高，图片宽，通道数，图片数) -> (图片数，图片高，图片宽，通道数)'''
    new = np.transpose(samples, (3, 0, 1, 2)).astype(np.float32)

    # labels 变成 one-hot encoding,[2] -> [0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
    # digit 0 ,  represented as 10
    # labels 变成 one-hot encoding,[10] -> [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    labels = np.array([x[0] for x in labels])
    one_hot_labels = []
    for num in labels:
        one_hot = [0.0] * 10
        if num == 10:
            one_hot[0] = 1.0
        else:
            one_hot[num] = 1.0
        one_hot_labels.append(one_hot)
    labels = np.array(one_hot_labels).astype(np.float32)
    return new, labels


def normalize(samples):
    """
        灰度化: 从三色通道 -> 单色通道     省内存 ，加快训练速度
        (R + G + B) / 3
        将图片从 0 ~ 255 线性映射到-1.0 ~ +1.0 """
    rgb = np.add.reduce(samples, keepdims=True, axis=3)
    # shape (图片数，图片高，图片宽，通道数)，将rgb三个值，reduce到一个float里面
    rgb = rgb / 3.0
    return rgb / 128.0 - 1.0


def inspect(dataset, labels, i):
    ''' 将图片显示出来  如果第四维的维度为1，说明rgb的3维合并到一维了，
        就可以取消掉最后的维度，reshape成三维'''
    if dataset.shape[3] == 1:
        shape = dataset.shape
        dataset = dataset.reshape(shape[0], shape[1], shape[2])
    print (labels[i])
    plt.figure(figsize=(3, 3), dpi=80)
    plt.imshow(dataset[i])
    plt.show()

def getdata(nslicenum):
    ''' get data from mat'''
    train = loadmat('./train_32x32.mat')
    print ('train ', train['X'].shape, train['y'].shape)
    print (type(train['X']), type(train['y']))
    train_samples = train['X'][:, :, :, 0:nslicenum].copy()
    train_labels = train['y'][0:nslicenum, :].copy()
    print ('slice ', train_samples.shape, train_labels.shape)
    del train
    return train_samples, train_labels

def main():
    ''' go '''
    train_samples, train_labels = getdata(5000)
    _train_samples, _train_labels = reformat(train_samples, train_labels)
    normalize(_train_samples)
    inspect(_train_samples, _train_labels, 993)


if __name__ == '__main__':
    main()
