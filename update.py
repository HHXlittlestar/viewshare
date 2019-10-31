import cv2 as cv

##########################################################################
#将图片划分为9个单元格
#参数：
#     img：待划分的图片矩阵

#返回值：
#     无
###########################################################################
def segImage(img):
    heigh, width = img.shape[:2]
    red = (0, 0, 255)
    cv.line(img, (0, (heigh - 1) // 3), (width - 1, (heigh - 1) // 3), red, 2)
    cv.line(img, (0, (heigh - 1)  * 2 // 3), (width - 1, (heigh - 1)  * 2 // 3), red, 2)
    cv.line(img, ((width - 1) // 3, 0), ((width - 1) // 3, heigh - 1), red, 2)
    cv.line(img, ((width - 1) * 2 // 3, 0), ((width - 1) * 2 // 3, heigh - 1), red, 2)

##########################################################################
#统计每个格子中特征点的个数
#参数：
#     x：特征点的横坐标值
#     y：特征点得纵坐标值
#     width：特征点所属图片的宽度
#     heigh：特征点所属图片的高度
#     sub_width：需要减去的宽度（针对在一张图中显示匹配结果时使用， 查询图和全景图被并排放在同一张图片上，所以全景图中的特征点横坐标要减去查询图的宽度
#     statistic：用于存储每个单元格中特征点个数的列表
#     dic：用于存储每个单元格中特征点坐标的字典

#返回值：
#     无
###########################################################################
def Statistic(x, y, width, heigh, sub_width, statistic, dic):
    x = x - sub_width
    if (((x > 0) and (x <= (width - 1) // 3)) and ((y > 0) and (y <= (heigh - 1) // 3))):
        statistic[0] += 1
        dic[1].append((x, y))
    elif (((x > (width - 1) // 3) and (x <= (width - 1) * 2 // 3)) and ((y > 0) and (y <= (heigh - 1) // 3))):
        statistic[1] += 1
        dic[2].append((x, y))
    elif (((x > (width - 1) * 2 // 3) and (x <= width - 1)) and ((y > 0) and (y <= (heigh - 1) // 3))):
        statistic[2] += 1
        dic[3].append((x, y))
    elif (((x > 0) and (x <= (width - 1) // 3)) and ((y > (heigh - 1) // 3) and (y <= (heigh - 1) * 2 // 3))):
        statistic[3] += 1
        dic[4].append((x, y))
    elif (((x > (width - 1) // 3) and (x <= (width - 1) * 2 // 3)) and ((y > (heigh - 1) // 3) and (y <= (heigh - 1) * 2 // 3))):   
        statistic[4] += 1
        dic[5].append((x, y))
    elif (((x > (width - 1) * 2 // 3) and (x <= width - 1)) and ((y > (heigh - 1) // 3) and (y <= (heigh - 1) * 2 // 3))):  
        statistic[5] += 1
        dic[6].append((x, y))
    elif (((x > 0) and (x <= (width - 1) // 3)) and ((y > (heigh - 1) * 2 // 3) and (y <= (heigh - 1)))):   
        statistic[6] += 1
        dic[7].append((x, y))
    elif (((x > (width - 1) // 3) and (x <= (width - 1) * 2 // 3)) and ((y > (heigh - 1) * 2 // 3) and (y <= (heigh - 1)))):  
        statistic[7] += 1
        dic[8].append((x, y))
    else:
        statistic[8] += 1
        dic[9].append((x, y))

##########################################################################
#返回车辆上传的图片在全景图中的查询结果(其实返回的是包含所有匹配到的特征点的区域)
#参数：
#     p：特征点在图中的坐标
#返回值：
#     xMinIndex：特征点最小的横坐标值
#     yMinIndex：特征点最小的纵坐标值
#     xMaxIndex：特征点最大的横坐标值
#     yMaxIndex：特征点最大的纵坐标值
###########################################################################
def queryResult(p):
    x = []
    y = []
    for x1, y1 in p:
        x.append(x1)
        y.append(y1)
        xMinIndex = min(x)
        xMaxIndex = max(x)
        yMinIndex = min(y)
        yMaxIndex = max(y)
    return xMinIndex, xMaxIndex, yMinIndex, yMaxIndex


##########################################################################
#在全景图中定位需要更新的区域
#参数：
#     dic:包含有9个格子中所有特征点坐标的字典
#     index:含有最多特征点的区域的索引（1-9中的一个数）
#返回值：
#     xMinIndex：待更新区域中特征点最小的横坐标值
#     yMinIndex：待更新区域中特征点最小的纵坐标值
#     xMaxIndex：待更新区域中特征点最大的横坐标值
#     yMaxIndex：待更新区域中特征点最大的纵坐标值
###########################################################################
def locateUpdateRange(dic, index):
    x = []
    y = []
    for x_id, y_id in dic[index]:
        x.append(x_id)
        y.append(y_id)
        xMinIndex = min(x)
        yMinIndex = min(y)
        xMaxIndex = max(x)
        yMaxIndex = max(y)
    return xMinIndex, xMaxIndex, yMinIndex, yMaxIndex

###############################################################
#使用高斯背景建模对选定区域进行背景更新
#参数：
#     img:需要更新的全景图
#     x：待更新区域的左上角点横坐标值
#     y：待更新区域的左上角点纵坐标值
#     width：待更新区域的宽度
#     heigh：待更新区域的高度
#     img2: 需要更新进去的新内容
#返回值：
#     更新过后的全景图
##############################################################
def gmmUpdate(img, x, y, width, heigh, img2):
    heigh, width = img.shape[:2]
    print(width, heigh)
    C = 4
    M = 4
    stdInit = 10
    D = 2.5
    T = 0.7
    alpha = 0.01
    p = alpha / (1 / C)
    minIndex = 0

    current = np.zeros((heigh, width), np.uint8) #车辆上传的需要对全景图更新的那一部分
    test = np.zeros(img.shape, np.uint8)        #全景图背景
    frg = np.zeros((heigh, width), np.uint8)    #上传的图片与全景图背景差分出来的前景

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

