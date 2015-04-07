import cv2
from watcher import Watcher
from manager import Manager
import numpy as np
from watch.players.place import PlaceWatcher
from watch.players.lap import LapWatcher
import util
from collections import deque

watcherClasses = [PlaceWatcher, LapWatcher]

class PlayersManager(Manager, Watcher):
    current = None
   # debug = True
    players = []
    verified = 0
    lastRanks = None

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
        rects = (((0,0), (midX, midY)), ((midX + 2, 0), (w, midY)), ((0, midY+2), (midX, h)), ((midX + 2, midY + 2), (w, h)))
        for i in range(self.manager.state('playerCount')):
            player = PlayerManager(positions[i], rects[i])
            player.id = i
            self.players.append(player)
            
    def sortRank(self, ranksAndCertainties):
        ranksAndCertainties = np.sort(ranksAndCertainties, order="certainty")
        ranks = ranksAndCertainties['rank'].tolist()

        unfilled = set(range(1,5)) ^ set(ranks)
        counts = [ranks.count(i) for i in range(1, 5)]

        i = 0
        while len(unfilled):
            if (counts[ranks[i]-1] > 1):
                ranksAndCertainties[i]["rank"] = unfilled.pop()
                counts[ranks[i]-1] -= 1
            i+=1

        return np.sort(ranksAndCertainties, order="player")
        

    def updateFrame(self, frame):
        self.window = frame
        if len(self.players) == 0:
            self.createPlayers()
        
        for i, player in enumerate(self.players):
            player.broadcastFrame(frame)

        dt = [("player", int), ("rank", int), ("certainty", float)]
        ranksAndCertainties = [(i + 1, player.state('rank'), player.state('rankCertainty')) for i, player in enumerate(self.players)]
        adjusted = self.sortRank(np.array(ranksAndCertainties, dtype=dt))

        if np.array_equal(self.lastRanks, adjusted['rank']):
            self.verified += 1
        else:
            self.verified = 0
            self.lastRanks = adjusted['rank']
        if self.verified == 2:
            last = self.manager.state('ranks')
            if last is None or not np.array_equal(last, adjusted['rank']):
                self.manager.state('ranks', adjusted['rank'], force=True)


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
