import os, glob, sys, time, cv2
import numpy as np
import pandas as pd
from pylab import rcParams
from scipy.ndimage.interpolation import rotate, zoom, shift
from tqdm import tqdm
import shutil

sys.path.append("/home/msmith/misc/py")
from removeFiles import removeFiles
import matplotlib.pyplot as plt

def show(img):
    plt.imshow(img)
    plt.show()

def makeDir(path):
    if not os.path.exists(path):
        os.makedirs(path) 

def makedirs():
    os.makedirs("data/trainAug") # all augmented tr
    os.makedirs("data/testAug") # all augmented te - hence add tr to te to get total
    os.makedirs("data/test") # single test image 
    os.makedirs("data/allAug") # single test image 

def aug(trOrTe, nAug=200, outShape=(500,500)):
    oW, oH = outShape
    tr = pd.read_csv("../trainCV.csv")
    te = pd.read_csv("../testCV.csv")
    csv = pd.concat([tr,te])
    nObs = csv.shape[0]
    csv.sort_values("label",inplace=1)
    savePath = "data/allAug/"

    for i in tqdm(range(447)):

        label = i
        obs = csv[csv.label==label]
        if obs.shape[0] == 0:
            print("No {0} in csv".format(i))
            continue
        else:
            count = 0
            
            while True:
                wp = savePath + str(label) + "/"
                if not os.path.exists(wp):
                    makeDir(wp)
                path = obs.sample(1).fullPath.values[0]
                if os.path.exists(path) == False:
                    continue
                makeDir(path)
                img = cv2.imread(path)
                w, h, c = img.shape

                if np.random.uniform() < 0.05:
                    angle = 0
                else:
                    angle = np.random.uniform(-10,10)
                scale = np.random.normal(1.0,0.1)
                shiftX = np.random.normal(0,w*0.01,1)
                shiftY = np.random.normal(0,h*0.01,1)
                M = cv2.getRotationMatrix2D((w/2,h/2),angle,scale=scale)
                M[0,1] += np.random.normal(0,0.2)
                M[0,2] = shiftX
                M[1,2] = shiftY
                imgC = cv2.warpAffine(img,M,(w,h),borderMode = 0,flags=cv2.INTER_CUBIC)
                number = len(glob.glob(wp+"*"))
                wp += "{0}.jpg".format(number)
                imgC = cv2.resize(imgC,outShape,interpolation=cv2.INTER_LINEAR)
                cv2.imwrite(wp,imgC)
                count += 1
                if count > nAug:
                    break

if __name__ == "__main__":

    import ipdb
    delete = True 
    if delete == True:
        try:
            [shutil.rmtree(x) for x in ["data/allAug/","data/trainAug","data/testAug","data/test"]]
        except OSError:
            "Doesn't exist"
        makedirs()
    aug(x)

