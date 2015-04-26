from watcher import Watcher
import numpy as np
import cv2
import numpy.linalg as la 
import util
import scipy

goTemplate = cv2.Canny(cv2.imread("templates/go.jpg", cv2.IMREAD_GRAYSCALE), 270, 200)
finishTemplate = cv2.Canny(cv2.imread("templates/finish.jpg", cv2.IMREAD_GRAYSCALE), 300, 200)
finishTemplateColor = cv2.imread("templates/finish-color.jpg")

class StartWatcher(Watcher):
    startRect = ((157, 92),  goTemplate.shape[::-1])
    finishRect = ((121, 95),  finishTemplate.shape[::-1])
    debug = True
    color = np.array([21, 135, 229])

    def debugRect(self):
        return self.finishRect

    def update(self):
        if self.manager.state('raceStatus') is None:
            startCropped = cv2.Canny(util.crop(self.window, np.hstack(self.startRect) + (-5, -5, 10, 10)), 350, 200)

            val = np.max(scipy.signal.correlate2d(startCropped, goTemplate, mode="valid"))
            if val > 200:
                self.manager.state('raceStatus', "started")
            
        else:
            cropped = util.crop(self.window, np.hstack(self.finishRect) + (-5, -5, 10, 10))
            threshold = 25
            # three channels
            numPixels = cropped.size / 3
            numOrangeish = np.sum(np.logical_and(np.all(cropped > (self.color - threshold), axis=2), np.all(cropped < (self.color + threshold), axis=2)))
            if numOrangeish / float(numPixels) > .15:
                finishCropped = cv2.Canny(cropped, 350, 200)
                vals = scipy.signal.correlate2d(finishCropped, finishTemplate, mode="valid")

                if (np.max(vals) > 210):
                    if self.manager.state('raceStatus') != 'finished':
                        self.manager.state('raceStatus', 'finished')

export = StartWatcher
