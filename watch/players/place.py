from watcher import Watcher
import operator
import numpy as np
import cv2
import util
import scipy

templateFiles = ["first.jpg", "second.jpg", "third.jpg","fourth.jpg"]
templates = []

for filename in templateFiles:
    templates.append(cv2.Canny(cv2.imread("templates/" + filename, cv2.IMREAD_GRAYSCALE), 350, 400))

size = np.max([template.shape[::-1] for template in templates], 0) + 1
c = 0

class PlaceWatcher(Watcher):
    #predicate = {"mode": "racing"}
    #rect = ((66, 166), (122,225))
    debug = True
    topLeft = {"left": (51, 156), "right": (315,156)}

    def __init__(self):
        super(PlaceWatcher, self).__init__()
    
    def debugRect(self):
        return (tuple(self.topLeft[self.direction]), tuple(size))

    def update(self):
        
        gray = cv2.cvtColor(self.window, cv2.COLOR_BGR2GRAY)
        win = gray
        vals = []

        area = cv2.Canny(util.crop(win, np.hstack((self.topLeft[self.direction], size))), 400, 450)

        for template, pos in zip(templates, positions):
            vals.append(np.max(scipy.signal.correlate2d(area, template, mode="valid"))/float(np.sum(template)))

        

export = PlaceWatcher
