import cv2 as cv
import numpy as np
import os
from asift import doFeatureMatch



if __name__ == '__main__':
    #首先初始化虚拟视角的全景图，这个由现有的拼接好的全景图提供，直接导入
    allViewPicturePath = 'C:\\Users\\HHX-PC\\Desktop\\panorama.jpg'
    allViewPicture = cv.imread(allViewPicturePath, 0)

    #初始化全景图的背景模型， 并开始进行查询反馈与更新
    C = 4
    M = 4
    stdInit = 10
    D = 2.5
    T = 0.7
    alpha = 0.01
    p = alpha / (1 / C)
    minIndex = 0

    heigh, width = allViewPicture.shape[:2]
    mean = np.zeros((heigh, width, C), np.float64)
    std = np.zeros((heigh, width, C), np.float64)
    weight = np.zeros((heigh, width, C), np.float64)
    uDiff = np.zeros((heigh, width, C), np.float64)
    bg_bw = np.zeros((heigh, width), np.int32)
    rank = np.zeros((1, C), np.float64)
    rankIndex = np.zeros((1, C), np.uint8)

    for i in range(heigh):
        for j in range(width):
            for k in range(C):
                mean[i, j, k] = allViewPicture[i, j]
                weight[i, j, k] = 1 / C
                std[i, j, k] = stdInit

    jpgPath = "E:\\胡浩星\\工作项目\\view_share\\测试图片\\团结广场"
    files = os.listdir(jpgPath)
    for file in files:
        filepath = jpgPath + "\\" + file
        queryImg = cv.imread(filepath, 0)

        #对于每一张查询的图片，先进行特征匹配，得到更宽广的视野图与全景图中待更新区域的坐标与宽高
        qureyResult, x, y, width, heigh = doFeatureMatch(queryImg, allViewPicture, "surf", "matchresult")
    updateReigon(allViewPicture, x, y, width, heigh)

    img1 = cv.imread(fn1, 0)
    img2 = cv.imread(fn2, 0)
    doFeatureMatch(img1, img2, 'surf', 'affineWindow')