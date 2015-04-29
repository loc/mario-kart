from watcher import Watcher
import operator
import numpy as np
import cv2
import util
import scipy

templateFiles = ["banana-c.jpg", "blooper-c.jpg", "blue-shell-c.jpg","bob-omb-c.jpg","bullet-bill-c.jpg","fakebox-c.jpg","gold-mushroom-c.jpg", \
                        "green-shell-c.jpg","mega-mushroom-c.jpg","mushroom-c.jpg","pow-block-c.jpg","red-shell-c.jpg","star-c.jpg","thunderbolt-c.jpg", \
                        "thundercloud-c.jpg","triple-banana-c.jpg","triple-green-shell-c.jpg","triple-mushroom-c.jpg","triple-red-shell-c.jpg"]
templates = []
rhist = []
ghist = []
bhist = []
templatesc = []
#could always have a pre-populated file with the exact color histograms pulled from ingame, may be superior
#maybe need normalization
for filename in templateFiles:
    im = cv2.imread("templates/" + filename, cv2.IMREAD_COLOR)
    templates.append(im)
    #three color channel histograms per image
    bhist.append(cv2.calcHist([im],[0],None,[32], [0,256]))
    ghist.append(cv2.calcHist([im],[1],None,[32], [0,256]))
    rhist.append(cv2.calcHist([im],[2],None,[32], [0,256]))

size = np.min([template.shape[::-1] for template in templates], 0)[1:] + 1
#size = [50, 65]

#size = (50 55)
#capture screen region

#for filename in templateFiles:
#    templatesc.append(cv2.Canny(cv2.imread("templates/" + filename, cv2.IMREAD_GRAYSCALE), 350, 200))

#size = np.max([template.shape[::-1] for template in templates], 0) + 1
c = 0
size = [50,65]
class ItemWatcher(Watcher):
    #predicate = {"mode": "racing"}
    #rect = ((66, 166), (122,225))
    debug = True
    topLeft = {"left": (23, 8), "right": (233,8)}
    #darkWeights = (0.2, 0.1, 0.5, 0.0)
    
    def __init__(self):
        super(ItemWatcher, self).__init__()
        self.item = 'None'
        self.duration = 0
    def debugRect(self):
        return (tuple(self.topLeft[self.direction]), tuple(size))
        
  
    def update(self):
        
        color = self.window
        win = color
        vals = []
        bcor = []
        gcor = []
        rcor = []
        #print size
        #not quite sure ask
        crop = util.crop(win, np.hstack((self.topLeft[self.direction], size)))
        
        #print crop.shape
        
        bvec = cv2.calcHist([crop],[0],None,[32],[0,256])
        gvec = cv2.calcHist([crop],[1],None,[32],[0,256])
        rvec = cv2.calcHist([crop],[2],None,[32],[0,256])
        #calculate minimum correlation maybe overcomplicated
        for i in range(0,len(templateFiles)):
            bcor.append(cv2.compareHist(bvec,bhist[i],cv2.cv.CV_COMP_CORREL))
            gcor.append(cv2.compareHist(gvec,ghist[i],cv2.cv.CV_COMP_CORREL))
            rcor.append(cv2.compareHist(rvec,rhist[i],cv2.cv.CV_COMP_CORREL))
        min = 0;
        for i in range(0,len(templateFiles)):
            if (bcor[i]+gcor[i]+rcor[i]) > (bcor[min]+gcor[min]+rcor[min]):
                min = i
        #tries to ensure that random frames don't throw off the itemwatcher, also can be used to check if the item has "settled" instead of picking up the randomization process
        
        if (self.item == 'None' and (bcor[min] + gcor[min] + rcor[min]) >= 2.85):
            self.item = (templateFiles[min])[:-6]
            self.duration = self.duration + 1
            
        elif (self.item == 'None' and (bcor[min] + gcor[min] + rcor[min]) < 2.85):
            self.duration = 0
        elif (self.item != 'None' and (bcor[min] + gcor[min] + rcor[min]) >= 2.85):
            if self.item == templateFiles[min][:-6] and self.duration >= 3:
                self.manager.state('item', self.item)
            else:
                self.item = templateFiles[min][:-6] 
                self.duration = self.duration + 3
        elif (self.item != 'None' and (bcor[min] + gcor[min] + rcor[min]) < 2.85):
            self.item = 'None'
            self.duration = 0
            if self.duration >= 3:
                self.manager.state('item', 'None')\
export = ItemWatcher
