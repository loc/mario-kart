import cv2
from watcher import Watcher
from manager import Manager
import numpy as np
from watch.players.place import PlaceWatcher
import util

watcherClasses = [PlaceWatcher]

class PlayersManager(Manager, Watcher):
    current = None
   # debug = True
    players = []

    def __init__(self):
        super(PlayersManager, self).__init__()

    def shouldWatch(self):
        if self.manager.state('mode') == 'racing' and self.manager.state('crop') is not None:
            return True
        return False

    def debugRect(self):
        if self.window is not None:
            return ((0,0), (self.window.shape[1]/2, self.window.shape[0]/2))

    def createPlayers(self):
        # screen direction (where the rank is)
        h, w = self.window.shape[:2]
        midX = w/2
        midY = h/2

        positions = ("left", "right", "left", "right")
        rects = (((0,0), (midX, midY)), ((midX + 1, 0), (w, midY)), ((0, midY), (midX, h)), ((midX + 1, midY + 1), (w, h)))
        for i in range(self.manager.state('playerCount')):
            self.players.append(PlayerManager(positions[i], rects[i]))

    def updateFrame(self, frame):
        self.window = frame
        if len(self.players) == 0:
            self.createPlayers()
        
        for player in self.players:
            player.broadcastFrame(frame)



class PlayerManager(Manager):
    def __init__(self, direction="left", rect=None):
        self.rect = rect
        self.direction = direction
        super(PlayerManager, self).__init__()
        self.initWatchers()

    def drawDebugRects(self, frame):
        for watcher in self.watchers:
            if watcher.debug:
                d = watcher.debugRect()
                if d:
                    adjusted = (self.rect[0][0] + d[0][0], self.rect[0][1] + d[0][1])
                    rect = util.pointSizeToRect((adjusted, d[1]))
                    cv2.rectangle(frame, rect[0], rect[1], (255,0,0), 1)

    def initWatchers(self):
        for watcherClass in watcherClasses:
            watcher = watcherClass()
            watcher.direction = self.direction
            self.addWatcher(watcher)

    def broadcastFrame(self, frame):
        cropped = util.cropRect(frame, self.rect)
        #cv2.imshow(str(self.rect), cropped)
        super(PlayerManager, self).broadcastFrame(cropped)
        self.drawDebugRects(frame)

        
export = PlayersManager
