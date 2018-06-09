import cv2,pdb
import numpy as np

Image=cv2.imread('E:\\TrainIJCNN2013\\00003.ppm')
#image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
(B,G,R)=cv2.split(Image)
image=R
(r,c)=image.shape
filterH=np.array([[-0.5,0,0.5]]*r)
filterV=np.array([[-0.5]*c,[0]*c,[0.5]*c])
gradientH=[]
gradientV=[]
for i in range(2,c):
    gradientH.append(np.sum(image[:,i-2:i+1]*filterH,axis=1))
gradientH=np.array(gradientH).T
zeros=np.zeros(r)
gradientH=np.column_stack([zeros,gradientH,zeros])
for i in range(2,r):
    gradientV.append(np.sum(image[i-2:i+1,:]*filterV,axis=0))
gradientV=np.array(gradientV)
zeros=np.zeros(c)
gradientV=np.row_stack([zeros,gradientV,zeros])

gradientAll=gradientH+gradientV

cv2.imshow('gradient',gradientAll)
cv2.imshow('raw',Image)
cv2.waitKey(0)
#cv2.imshow("raw picture",image)
#(w,h,c)=image.shape
#print(w)
#print(h)
#img_resized = cv2.resize(image, (w*2,h*2))
#cv2.imshow('resized',image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()











































































