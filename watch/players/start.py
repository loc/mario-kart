from watcher import Watcher
import numpy as np
import cv2
import numpy.linalg as la 
import util

class StartWatcher(Watcher):
    startRect = ((235, 95),  (10, 30))
    finishRect = ((117, 95),  (170, 40))
    debug = True
    color = [21, 135, 229]

    def debugRect(self):
        return self.startRect

    def update(self):
        #print self.window
        if self.manager.state('raceStatus') is None:
            startCropped = util.crop(self.window, np.hstack(self.startRect))
            numOrange = np.sum(la.norm(startCropped-self.color, axis=2) < 10)
            if numOrange > 10:
                self.manager.state('raceStatus', "started")
        else:
            finishCropped = util.crop(self.window, np.hstack(self.finishRect))
            numOrange = np.sum(la.norm(finishCropped-self.color, axis=2) < 10)
            if numOrange > 100:
                self.manager.state('raceStatus', 'finished')


            #cv2.waitKey(0)
        #if numOrange > 0:
        #    print numOrange
        #    if numOrange > 10:
        #        cv2.waitKey(0)
        #print np.abs(self.window-self.color)

#        diff = np.abs(np.mean(self.window, axis=(0,1)) - np.array())
#        print np.all(diff < 5)
        pass


export = StartWatcher
