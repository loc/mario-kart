import numpy as np
import cv2
from scipy import signal, ndimage
import time
from functools32 import lru_cache
import operator
from fysom import Fysom
from watch import watchers

class ScreenManager:

    def __init__(self, filename):
        self.cap = cv2.VideoCapture(filename)
        self.history = []
        self.states = {}
        self.watchers = []
        self.currentFrame = None
        self.size = None

    def loop(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret is True:
                if not self.size:
                    self.size = frame.shape
                self.broadcastFrame(frame)

                cv2.imshow('frame', frame)
            if cv2.waitKey(1)==27:
                break

        self.cleanup()

    def broadcastFrame(self, frame):
        for watcher in self.watchers:
            if watcher.shouldWatch():
                watcher.updateFrame(frame)

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def addWatcher(self, watcher):
        watcher.manager = self
        self.watchers.append(watcher)
        return watcher

    def state(self, key, val=None, lookback=0):
        if not val:
            return self.getState(key, lookback)
        return self.setState(key, val)

    def getState(self, key, lookback=0):
        if lookback == 0:
            stateDict = self.states
        else:
            stateDict = self.states[-lookback]

        if stateDict and key in stateDict:
            return stateDict[key]
        

    def setState(self, key, val):
        if key not in self.states or self.states[key] != val:
            self.history.append(self.states.copy())
            self.states[key] = val
            print self.states
            self.stateChange = True
        return val

manager = ScreenManager('black-screen.mp4')

for Watcher in watchers:
    manager.addWatcher(Watcher())

manager.loop()


# generates a matrix with ones in the middle in both directions
# e.g. 
#        [ 0 0 0 1 0 0 0
#          0 0 0 1 0 0 0 
#          0 0 0 1 0 0 0 
#          1 1 1 1 1 1 1 
#          0 0 0 1 0 0 0 
#          0 0 0 1 0 0 0 
#          0 0 0 1 0 0 0 ]
#@lru_cache()
#def genCrosshair(size):
#    crosshair = np.zeros((size, size))
#    for i in range(size):
#        for j in range(size):
#            mid = (size-1)/2
#            if i in range(mid-1, mid+1) or j in range(mid-1, mid+1) :
#                crosshair[i][j] = 1;
#    return crosshair
#
#def findScreenMiddle(frame, size = 101):
#    crosshair = genCrosshair(size)
#    w, h, d = frame.shape
#    half = (size - 1) / 2
#    mid_w, mid_h = (w / 2, h / 2)
#    conv2 = ndimage.generic_filter(\
#                np.sum(frame[mid_w - half:mid_w + half, mid_h - half:mid_h + half], axis=2), \
#                np.sum, footprint=crosshair, mode="constant", cval=255)
#    cv2.imshow('frame', np.repeat(conv2[:,:,None], 3, axis=2))
#    return np.unravel_index(conv2.argmin(), conv2.shape)
#
#
#while cap.isOpened():
#    ret, frame = cap.read()
#    if ret is True:
#        #print findScreenMiddle(frame)
#        start = time.time()
#        checkForBlack(frame)
#        print time.time() - start 
#        print np.argwhere(frame)
#        cv2.imshow('frame', frame)
#
#    if cv2.waitKey(33)==27:
#        break
#
