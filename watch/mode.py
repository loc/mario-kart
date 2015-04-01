from watcher import Watcher
import operator
import numpy as np
import cv2

class ModeWatcher(Watcher):
    predicate = {"mode": "unknown"}
    rect = ((20, 10), (550,30))
    debug = True
    setupThreshold = 240

    def update(self):
        if (np.mean(self.window) > self.setupThreshold):
            self.manager.state("mode", "setup")
        else:
            self.manager.state("mode", "racing")

export = ModeWatcher
