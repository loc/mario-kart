import numpy as np
import cv2
from scipy import signal, ndimage
import time
import operator
from watch import watchers
from managers.screen import ScreenManager


#manager = ScreenManager('rtmp://192.168.89.160:1935/live/test')
manager = ScreenManager('bowsers-castle.mp4')
manager.state('playerCount', 4)
for Watcher in watchers:
    watcher = Watcher()
    manager.addWatcher(watcher)

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
