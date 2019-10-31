import numpy as np 
import cv2 as cv
import random
import math

mframe = cv.imread("C:\\Users\\HHX-PC\\Desktop\\panorama.jpg")

heigh, width = mframe.shape[:2]
print(width, heigh)
C = 4
M = 4
stdInit = 10
D = 2.5
T = 0.7
alpha = 0.01
p = alpha / (1 / C)
minIndex = 0
current = np.zeros(mframe.shape, np.uint8)
test = np.zeros(mframe.shape, np.uint8)
frg = np.zeros(mframe.shape, np.uint8)

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
            mean[i, j, k] = random.random() * 255
            weight[i, j, k] = 1 / C
            std[i, j, k] = stdInit

while(1):
    current = cv.cvtColor(mframe, cv.COLOR_BGR2GRAY)
    for i in range(heigh):
        for j in range(width):
            for k in range(C):
                uDiff[i, j, k] = abs(current[i, j] - mean[i, j, k])
    
    for i in range(heigh):
        for j in range(width):
            match = 0
            temp = 0
            singleTemp = 0
            for k in range(C):
                if abs(uDiff[i, j, k]) < (D * std[i, j, k]):
                    match = 1
                    weight[i, j, k] += alpha * (1 - weight[i, j, k])
                    p = alpha / weight[i, j, k]
                    mean[i, j, k] = (1 - p) * mean[i, j, k] + p * current[i, j]
                    std[i, j, k] = math.sqrt((1 - p)*(std[i, j, k] * std[i, j, k]) + p * (pow(current[i, j] - mean[i, j, k], 2)))
                else:
                    weight[i, j, k] = (1 - alpha) * weight[i, j, k];
            if match == 1:
                for k in range(C):
                    temp += weight[i, j, k]
                for k in range(C):
                    weight[i, j, k] = weight[i, j, k] / temp
            else:
                singleTemp = weight[i, j, 0]
                for k in range(C):
                    if weight[i, j, k] < singleTemp:
                        minIndex = k
                        singleTemp = weight[i, j, k]

                mean[i, j, minIndex] = current[i, j]
                std[i, j, minIndex] = stdInit

                for k in range(C):
                    temp += weight[i, j, k]
                for k in range(C):
                    weight[i, j, k] = weight[i, j, k] / temp
            
            for k in range(C):
                rank[0, k] = weight[i, j, k] / std[i, j, k]
                rankIndex[0, k] = k
            for k in range(1, C):
                for m in range(C):
                    if rank[0, k] > rank[0, m]:
                        randTemp = rank[0, m]
                        rank[0, m] = rank[0, k]
                        rank[0, k] = randTemp

                        rankIndexTemp = rankIndex[0, m]
                        rankIndex[0, m] = rankIndex[0, k]
                        rankIndex[0, k] = rankIndexTemp
            
            bg_bw[i, j] = 0
            for k in range(C):
                temp += weight[i, j, rankIndex[0, k]]
                bg_bw[i, j] += mean[i, j, rankIndex[0, k]] * weight[i, j, rankIndex[0, k]] 
                if temp >= T:
                    M = k
                    break
            
            test[i, j] = bg_bw[i, j]

            match = 0
            k = 0

            while((match == 0) and (k <= M)):
                if(abs(uDiff[i, j, rankIndex[0, k]]) <= D * std[i, j, rankIndex[0, k]]):
                    frg[i, j] = 0
                    match = 1
                else:
                    frg[i, j] = current[i, j]
                k += 1
    
    _, mframe = cap.read()
    cv.namedWindow('frg')
    cv.imshow("frg", frg)
    cv.imshow("back", test)
    cv.waitKey(33)

cv.waitKey()
cv.destroyAllWindows()