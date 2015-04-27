from watcher import Watcher
import operator
import numpy as np
import cv2
import util
import scipy

templateFiles = ["first.jpg", "second.jpg", "third.jpg","fourth.jpg"]
templates = []

for filename in templateFiles:
    templates.append(cv2.Canny(cv2.imread("templates/" + filename, cv2.IMREAD_GRAYSCALE), 350, 200))

size = np.max([template.shape[::-1] for template in templates], 0) + 1
c = 0


class PlaceWatcher(Watcher):
    predicate = {"raceStatus": "started", "raceHazard": None}
    #predicate = {"mode": "racing"}
    #rect = ((66, 166), (122,225))
    debug = True
    topLeft = {"left": (51, 156), "right": (315,156)}
    darkWeights = (0.2, 0.1, 0.5, 0.0)

    def __init__(self):
        super(PlaceWatcher, self).__init__()
        self.lastRank = None
    
    def shouldWatch(self):
        raceStatus = self.manager.state('raceStatus')
        # could finish while in a hazard
        return raceStatus == 'started' or raceStatus == 'hazard'

    def debugRect(self):
        return (tuple(self.topLeft[self.direction]), tuple(size))

    def update(self):
        
        gray = cv2.cvtColor(self.window, cv2.COLOR_BGR2GRAY)
        win = gray
        vals = []

        crop = util.crop(win, np.hstack((self.topLeft[self.direction], size)))
        area = cv2.Canny(crop, 350, 300)
        luminance = np.mean(crop)
        lumWeight = np.clip((1-((luminance-30)/80)), 0, 1)

        for index, template in enumerate(templates):
            darkWeight = self.darkWeights[index] * lumWeight
            val = np.max(scipy.signal.correlate2d(area, template, mode="valid")/float(np.sum(template)))
            vals.append(val + (val * darkWeight))
        
        self.currentRank = np.argmax(vals) + 1
        certainty = abs(np.subtract(*(np.sort(vals)[-2:])))

        self.manager.state('unverifiedRank', self.currentRank, supress=True)
        self.manager.state('rankCertainty', certainty, supress=True)

        self.lastRank = self.currentRank

export = PlaceWatcher
