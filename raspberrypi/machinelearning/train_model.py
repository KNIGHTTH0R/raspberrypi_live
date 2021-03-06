#! /usr/bin/python
# -*- coding:utf-8 -*-
import time
import pickle
import glob
import numpy as np
from sklearn.svm import LinearSVC as SVM
from sklearn.model_selection import train_test_split
from util import get_train_features

# def down_dimision(features):
#     nsamples, nblockx, nblocky,ncellx,ncelly,nbins = features.shape
#     return  features.reshape((nsamples,nblockx*nblocky*ncellx*ncelly*nbins))

def train():
    # 读取正负样本
    # notcars = glob.glob('non-vehicles/*.*')
    # cars = glob.glob('vehicles/*.*')
    negtive = glob.glob('negtive/*.*')
    positive = glob.glob('positive/*.*')
    # 每个cell多少像素
    pix_per_cell = 16
    #每个block几个cell
    cell_perblock= 2
    # 分多少个bin
    bin_count = 12
    # bin_count = 30
    # 重新resize大小
    target_pic_size = 128
    t1 = time.time()
    # 获取汽车和非汽车的特征
    positive_features = get_train_features(imgs=positive, cell_size=pix_per_cell,bin_count=bin_count,target_pic_size=(target_pic_size,target_pic_size),cell_perblock=cell_perblock)
    negtive_features = get_train_features(imgs=negtive, cell_size=pix_per_cell,bin_count=bin_count,target_pic_size=(target_pic_size,target_pic_size),cell_perblock=cell_perblock)
    # car_features = down_dimision(car_features)
    # notcar_features = down_dimision(notcar_features)
    t2 = time.time()
    print(round(t2 - t1, 2), 'Seconds to extract features...')
    # hstack沿第二轴，vstack沿第一条轴合成一个数组，如array([[ 8., 8.],[ 0., 0.]])和array([[ 1., 8.],[ 0., 4.]])
    # 通过vs是array([[ 8., 8.],[ 0., 0.],[ 1., 8.],[ 0., 4.]])，通过hstack是array([[ 8., 8., 1., 8.],[ 0., 0., 0., 4.]])
    X = np.vstack((positive_features, negtive_features))
    X = X.astype(np.float64)
    # 标记数据
    y = np.hstack((np.ones(len(positive_features)), np.zeros(len(negtive_features))))
    # 获取随机数种子
    rand_state = np.random.randint(0, 100)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.1, random_state=rand_state)
    print('Feature vector length:', len(X_train[0]))
    #下面开始机器学习了啊，看清楚了
    svc = SVM()
    t1 = time.time()
    svc.fit(X_train, y_train)
    t2 = time.time()
    print(round(t2 - t1, 2), 'Seconds to train classfier...')
    print('Test Accuracy of classfier = ', round(svc.score(X_test, y_test), 4))
    # 测试集
    rand_start = np.random.randint(0, X_test.shape[0] - 10)
    n_predict = 10
    right = 0
    i = 0
    for p in svc.predict(X_test):
        if p == y_test[i]:
            right = right + 1
        i = i + 1
    print("right",right,"total",X_test.shape[0])
    print('My classfier predicts: ', svc.predict(X_test[rand_start:rand_start+n_predict]))
    print('For these', n_predict, 'labels: ', y_test[0:n_predict])
    train_dist = {}
    train_dist['clf'] = svc
    train_dist['scaler'] = None
    train_dist['orient'] = None
    train_dist['pix_per_cell'] = pix_per_cell
    train_dist['cell_per_block'] = cell_perblock
    train_dist['hog_channel'] = None
    train_dist['spatial_size'] = target_pic_size
    train_dist['hist_bins'] = bin_count

    output = open('train_dist.p', 'wb')
    pickle.dump(train_dist, output)

if __name__ == '__main__':
    train()