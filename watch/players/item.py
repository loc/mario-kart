from watcher import Watcher
import operator
import numpy as np
import cv2
import util
import scipy

templateFiles = ["banana.jpg", "blooper.jpg", "blue-shell.jpg","bob-omb.jpg","bullet-bill.jpg","fakebox.jpg","gold-mushroom.jpg", \
                        "green-shell.jpg","mega-mushroom.jpg","mushroom.jpg","pow-block.jpg","red-shell.jpg","star.jpg","thunderbolt.jpg", \
                        "thundercloud.jpg","triple-banana.jpg","triple-green-shell.jpg","triple-mushroom.jpg","triple-red-shell.jpg"]
templates = []
rhist = []
ghist = []
bhist = []

#could always have a pre-populated file with the exact color histograms pulled from ingame, may be superior
#maybe need normalization
for filename in templateFiles:
    im = cv2.imread("templates/" + filename, cv2.IMREAD_COLOR)
    templates.append(im)
    #three color channel histograms per image
    bhist.append(cv2.calcHist([im],[0],None,[32], [0,256]))
    ghist.append(cv2.calcHist([im],[1],None,[32], [0,256]))
    rhist.append(cv2.calcHist([im],[2],None,[32], [0,256]))

size = np.max([template.shape[::-1] for template in templates], 0)[1:] + 1
    
#capture screen region


class ItemWatcher(Watcher):
    #predicate = {"mode": "racing"}
    #rect = ((66, 166), (122,225))
    debug = True
    topLeft = {"left": (51, 156), "right": (315,156)}
    #darkWeights = (0.2, 0.1, 0.5, 0.0)

    def __init__(self):
        super(ItemWatcher, self).__init__()
        self.item = None
    
    def debugRect(self):
        return (tuple(self.topLeft[self.direction]), tuple(size))

    def update(self):
        
        color = self.window
        win = color
        vals = []
        bcor = []
        gcor = []
        rcor = []
        print size
        #not quite sure ask
        crop = util.crop(win, np.hstack((self.topLeft[self.direction], size)))
        print crop.shape
        bvec = cv2.calcHist([crop],[0],None,[32],[0,256])
        gvec = cv2.calcHist([crop],[1],None,[32],[0,256])
        rvec = cv2.calcHist([crop],[2],None,[32],[0,256])
        #area = cv2.Canny(crop, 350, 300)
        #calculate minimum correlation maybe overcomplicated
        for i in range(0,len(templateFiles)):
            bcor.append(cv2.compareHist(bvec,bhist[i],cv2.CV_COMP_CORREL))
            gcor.append(cv2.compareHist(gvec,ghist[i],cv2.CV_COMP_CORREL))
            rcor.append(cv2.compareHist(rvec,rhist[i],cv2.CV_COMP_CORREL))
        min = 0;
        for i in range(0,len(templateFiles)):
            if (bcor[i]+gcor[i]+rcor[i]) > (bcor[min]+gcor[min]+rcor[min]):
                min = i
           
        #check relevance
        #self.manager.state('rank', self.currentRank)
        #self.manager.state('rankCertainty', certainty)
        if (item == None and (bcor[min] + gcor[min] + rcor[min]) >= 2):
            self.item = (templateFiles[min])[:-4]
            self.manager.state('item', self.item)
        elif (item != None and (bcor[min] + gcor[min] + rcor[min]) < 2):
            self.item = None
            self.manager.state('item', None)

export = ItemWatcher
