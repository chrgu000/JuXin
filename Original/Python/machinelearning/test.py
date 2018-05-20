from __future__ import print_function
import FaceDetector
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report

import numpy as np
import argparse,glob,cv2

ap=argparse.ArgumentParser()
ap.add_argument('-i','--images',required=True,\
                help='path to the image dataset')
ap.add_argument('-m','--masks',required=True,\
                help='path to the image masks')
args=vars(ap.parse_args())


imagePaths=sorted(glob.glob(args['images']+'/*.png'))
maskPaths=sorted(glob.glob(args['masks']+'/*.png'))

data=[]
target=[]

desc=FaceDetector.RGBHistogram([8,8,8])

for (imagePath,maskPath) in zip(imagePaths,maskPaths):
    image=cv2.imread(imagePath)
    mask=cv2.imread(maskPath)
    mask=cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY)
    
    features=desc.describe(image,mask)
    
    data.append(features)
    target.append(imagePath.split('_')[-2])

targetNames=np.unique(target)
le=LabelEncoder()
target=le.fit_transform(target)

(trainData,testData,trainTarget,testTarget)=train_test_split(data,target,\
test_size=0.3,random_state=42)

model=RandomForestClassifier(n_estimators=25,random_state=84)
model.fit(trainData,trainTarget)
print(classification_report(testTarget,model.predict(testData),\
                            target_names=targetNames))


for i in np.random.choice(np.arange(0,len(imagePaths)),10):
    






















