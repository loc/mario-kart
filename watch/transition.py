from watcher import Watcher
import operator
import numpy as np

def checkForBlack(frame):
    pixels = reduce(operator.mul, frame.shape)
    return pixels > np.sum(frame)

class TransitionWatcher(Watcher):

    def frameRate():
        pass

    def update(self):
        isBlack = checkForBlack(self.window)
        currentState = self.manager.state('mode')

        if currentState == "transition" and not isBlack:
            self.manager.state('mode', 'unknown')
        elif isBlack:
            self.manager.state('mode', 'transition')



export = TransitionWatcher
