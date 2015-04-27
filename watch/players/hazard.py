from watcher import Watcher
import numpy as np
import cv2

class HazardWatcher(Watcher):
    high = 25
    low = 15
    numFrames = 10

    def __init__(self):
        super(HazardWatcher, self).__init__()
        self.count = 0

    def update(self):
        gray = cv2.cvtColor(self.window, cv2.COLOR_BGR2GRAY)
        avg = np.mean(gray)

        if avg < self.high:
            # pause the other watchers if we're in danger of a hazard
            self.manager.state('raceHazard', 'hazard', supress=True)
            # verify over some number of frames that it actually is a hazard
            if avg < self.low and self.count != self.numFrames:
                self.count += 1
                if self.count == self.numFrames:
                    self.manager.state('raceHazard', 'hazard', force=True)

        else:
            self.count = 0
            if avg > 40:
                if self.manager.state('raceHazard'):
                    self.manager.unset('raceHazard')
