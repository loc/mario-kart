from watcher import Watcher
import operator
import numpy as np
import cv2
import util
import numpy.linalg as la

class ModeWatcher(Watcher):
    predicate = {"mode": "unknown"}
    setupRect = ((20, 10), (550,20))
    overviewRect = ((550, 410), (280, 30))
    debug = True
    setupThreshold = 243
    lastMode = None

    def debugRect(self):
        return self.setupRect;

    def update(self):
        setupCrop = util.crop(self.window, np.hstack(self.setupRect))
        if (np.mean(setupCrop) > self.setupThreshold):
            self.lastMode = "setup"
            self.manager.state("mode", "setup")
            return
        else:
            # must be either overview, racing, or endSequence
            if self.lastMode == "overview":
                # if we just came from the overview
                self.lastMode = "racing"
                self.manager.state("mode", "racing")
                return
            if self.lastMode == None:
                # if we just started the video. usually debugging
                self.lastMode = "racing"
                self.manager.state("mode", "racing")
                return
            else:
                # last mode either racing or setup
                # could be either overview or endSequence
                isOverview = False
                overviewCrop = util.crop(self.window, np.hstack(self.overviewRect))
                gray = cv2.cvtColor(overviewCrop, cv2.COLOR_BGR2GRAY)
                t = np.zeros(overviewCrop.shape)
                if (np.sum(gray < 2) > 200):
                    isOverview = True

                if isOverview:
                    self.lastMode = "overview"
                    self.manager.state("mode", "overview")
                else:
                    self.lastMode = "endSequence"
                    self.manager.state("mode", "endSequence")
                return

export = ModeWatcher
