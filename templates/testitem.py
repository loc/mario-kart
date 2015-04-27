#from watcher import Watcher
import operator
import numpy as np
import cv2
#import util
import scipy

rhist = []
ghist = []
bhist = []

templateFiles = ["banana.jpg", "blooper.jpg", "blue-shell.jpg","bob-omb.jpg","bullet-bill.jpg","fakebox.jpg","gold-mushroom.jpg", \
                        "green-shell.jpg","mega-mushroom.jpg","mushroom.jpg","pow-block.jpg","red-shell.jpg","star.jpg","thunderbolt.jpg", \
                        "thundercloud.jpg","triple-banana.jpg","triple-green-shell.jpg","triple-mushroom.jpg","triple-red-shell.jpg"]
templates = []


#could always have a pre-populated file with the exact color histograms pulled from ingame, may be superior
#maybe need normalization
for filename in templateFiles:
    im = cv2.imread(filename, cv2.IMREAD_COLOR)
    templates.append(im)
    #three color channel histograms per image
    bhist.append((cv2.calcHist([im],[0],None,[32], [0,256])))
    ghist.append((cv2.calcHist([im],[1],None,[32], [0,256])))
    rhist.append((cv2.calcHist([im],[2],None,[32], [0,256])))

#color = self.window
#win = color
vals = []
bcor = []
gcor = []
rcor = []
#not quite sure ask
crop = cv2.imread("triple-banana.jpg",cv2.IMREAD_COLOR)
bvec = (cv2.calcHist([crop],[0],None,[32],[0,256]))
gvec = (cv2.calcHist([crop],[1],None,[32],[0,256]))
rvec = (cv2.calcHist([crop],[2],None,[32],[0,256]))
#area = cv2.Canny(crop, 350, 300)
#calculate minimum correlation maybe overcomplicated
for i in range(0,len(templateFiles)):
    bcor.append(cv2.compareHist(bvec,bhist[i],cv2.cv.CV_COMP_CORREL))
    gcor.append(cv2.compareHist(gvec,ghist[i],cv2.cv.CV_COMP_CORREL))
    rcor.append(cv2.compareHist(rvec,rhist[i],cv2.cv.CV_COMP_CORREL))
min = 0;
for i in range(0,len(templateFiles)):
    if (2*bcor[i]+gcor[i]+2*rcor[i]) > (bcor[min]+gcor[min]+2*rcor[min]):
        min = i
#check relevance
#self.manager.state('rank', self.currentRank)
#self.manager.state('rankCertainty', certainty)
print bcor[min] + gcor[min] + rcor[min]
print bvec, gvec, rvec
print bhist[min], ghist[min], rhist[min]
print (templateFiles[min])[:-4]
#print bcor
#print gcor
#print rcor