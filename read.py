import numpy as np
import cv2
from scipy import signal, ndimage
import time
import operator
from watch import watchers
from managers.screen import ScreenManager
import sys
from args import args


#manager = ScreenManager('rtmp://192.168.89.160:1935/live/test')
manager = ScreenManager(args.input)
manager.state('playerCount', 4)
for Watcher in watchers:
    watcher = Watcher()
    manager.addWatcher(watcher)

manager.loop()
