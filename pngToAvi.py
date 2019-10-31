import numpy as np
import cv2
import time
import datetime
import os
 
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
frame1 = np.zeros((360,240))
out = cv2.VideoWriter(datetime.datetime.now().strftime("%A_%d_%B_%Y_%I_%M_%S%p")+'.avi',fourcc, 15.0, np.shape(frame1))

rootpath = 'C:\\Users\\HHX-PC\\Desktop\\RawImages'
files = os.listdir(rootpath)
for file in files:
    filepath = rootpath + "\\" + file
    frame = cv2.imread(filepath)
    out.write(frame)
out.release()
cv2.destroyAllWindows()