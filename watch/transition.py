from watcher import Watcher
import operator
import numpy as np

def checkForBlack(frame):
    pixels = reduce(operator.mul, frame.shape)
    return pixels * 10 > np.sum(frame)

class TransitionWatcher(Watcher):
    numOutFrame = 9
    frame = 0
    
    def frameRate():
        pass

    def update(self):
        isBlack = checkForBlack(self.window)
        currentState = self.manager.state('mode')

        if currentState == "transition" and not isBlack:
            if self.frame < self.numOutFrame:
                self.frame += 1
            else:
                self.manager.state('mode', 'unknown', supress=True)
        elif isBlack:
            self.frame = 0
            self.manager.state('mode', 'transition')

export = TransitionWatcher
