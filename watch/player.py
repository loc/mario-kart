import cv2
from watcher import Watcher
from manager import Manager
import numpy as np
from watch.players.place import PlaceWatcher
from watch.players.lap import LapWatcher
from watch.players.start import StartWatcher
import util
from collections import deque

watcherClasses = [PlaceWatcher, LapWatcher, StartWatcher]

class PlayersManager(Manager, Watcher):
    current = None
   # debug = True
    players = []
    verified = 0
    lastRanks = [None] * 4

    def __init__(self):
        super(PlayersManager, self).__init__()

    def shouldWatch(self):
        if self.manager.state('mode') == 'racing' and self.manager.state('crop') is not None or self.manager.state('mode') == "overview":
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
            player.screenManager = self.manager
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
        if self.manager.state('mode') == 'overview':
            for player in self.players:
                player.reset()
            return

        self.window = frame
        if len(self.players) == 0:
            self.createPlayers()
        
        for i, player in enumerate(self.players):
            player.broadcastFrame(frame)
        
        # update global state with race info from players
        if (self.manager.state('raceStatus') != "started" and player.state('raceStatus') == "started"):
            self.manager.state('raceStatus', "started")
        if self.manager.state('raceStatus') == "started" and np.all([player.state('raceStatus') == "finished" for player in self.players]):
            self.manager.state('raceStatus', "finished")

        if self.manager.state('raceStatus') == "started":
            dt = [("player", int), ("rank", int), ("certainty", float)]
            ranksAndCertainties = [(i + 1, player.state('unverifiedRank'), player.state('rankCertainty')) for i, player in enumerate(self.players)]
            adjusted = self.sortRank(np.array(ranksAndCertainties, dtype=dt))

            for i, player, rank, last in zip(range(len(self.players)), self.players, adjusted['rank'], self.lastRanks):
                if rank == last:
                    player.rankVerification += 1
                else:
                    player.rankVerification = 0
                    self.lastRanks[i] = rank
                
                if player.rankVerification == 2:
                    previous = player.state('rank')
                    if previous != rank:
                        player.state('rank', rank)


class PlayerManager(Manager):

    def __init__(self, direction="left", rect=None):
        self.rect = rect
        self.direction = direction
        super(PlayerManager, self).__init__()
#        self.states = {"raceStatus": "started"}
        self.initWatchers()
        self.rankVerification = 0

    def initWatchers(self):
        for watcherClass in watcherClasses:
            watcher = watcherClass()
            watcher.direction = self.direction
            self.addWatcher(watcher)

    def reset(self):
        if self.hasReset:
            return
        
        self.hasReset = True

        self.unset('raceStatus')
        self.unset('lap')
        self.unset('rank')
        self.unset('rankUncertainty')
        self.unset('unverifiedRank')

    def rankChanged(self, value):
        print self.frameNumber, "rank", value, self.id

    def lapChanged(self, value):
        print self.frameNumber, "lap", value, self.id 

    def raceStatusChanged(self, value):
        print self.frameNumber, "race", value, self.id

    def broadcastFrame(self, frame):
        self.hasReset = False
        self.frameNumber = self.screenManager.frameNumber
        cropped = util.cropRect(frame, self.rect)
        super(PlayerManager, self).broadcastFrame(cropped)
        self.drawDebugRects(frame)

        
export = PlayersManager
