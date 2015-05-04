#!/usr/bin/env python

import sys
from schema import *
import sqlalchemy
import datetime
from queue import queue
from Queue import Empty as QueueEmpty

conn = None

shouldWait = True

names = ["Joe", "Vince", "Chris", "Andy"]
characters = ["Funky Kong", "Bowser Jr.", "Baby Mario", "Mario"]
vehicles = ["Flame Runner", "Mach Bike", "Blue Falcon", "Wild Wing"]

setId = int(15)
state, race = None, None

class Parser():

    def __init__(self):
        self.db = Database()
        self.conn = self.db.engine.connect()

        self.reset()
        for index, (name, character, vehicle) in enumerate(zip(names, characters, vehicles)):
            self.conn.execute(self.db.players.insert(), set_id=setId, player=index, name=name, character=character, vehicle=vehicle)

    def reset(self):
        self.state = {
            "started": False,
            "startFrame": None,
            "players": [{},{},{},{}]
        }
        self.conn.execute(self.db.races.insert(), set_id=setId, date=datetime.date.today())
        stmt = select([self.db.races]).order_by(desc("id"))
        self.race = self.conn.execute(stmt).fetchone()
        return self.race, self.state 

    def getFrameElapse(self, start, end):
        return (end - start) / 30.0

    def updateLap(self, frame, lap, playerNum):
        player = self.state["players"][playerNum]

        if "lap" in player:
            current = player["lap"]
            elapsed = self.getFrameElapse(player["lapFrame"], frame)
            if lap == current + 1 and elapsed > 20:
                sinceBegin = self.getFrameElapse(self.state["startFrame"], player["lapFrame"])
                print "lap:", lap-1, "player:", playerNum, "elapsed:", elapsed
                try: 
                    self.conn.execute(self.db.laps.insert(), race_id=self.race.id, elapsed=elapsed, timestamp=sinceBegin, lap=lap-1, player=playerNum)
                except sqlalchemy.exc.IntegrityError:
                    print "Integrity error", "lap", lap-1, "player", playerNum, "elapsed", elapsed
            else:
                player["lap"] = lap
                return

        player["lap"] = lap
        player["lapFrame"] = frame

    def startRace(self, frame):
        if self.state["startFrame"]:
            return

        self.state["startFrame"] = frame

        for i in range(4):
            self.updateLap(frame, 1, i)

    def finish(self, frame, playerNum):
        player = self.state["players"][playerNum]
        hazard = 0

        if "hazards" in player:
            hazard = player["hazards"]

        player["finished"] = True
        self.updateLap(frame, 4, playerNum)
        self.rankUpdate(frame, player["rank"], playerNum)

        raceTime = self.getFrameElapse(self.state["startFrame"], player["lapFrame"])


        print "race", self.race.id, "player:", playerNum, "hazard:", hazard, "rank:", player["rank"], "time:", raceTime, "times:", player["rankTimes"]

        if all(["finished" in p for p in self.state["players"]]):
            self.endRace(frame)

    def hazard(self, frame, playerNum):
        player = self.state["players"][playerNum]

        if self.state["startFrame"] and "finished" not in player:
            if "hazards" not in player:
                player["hazards"] = 1
            else:
                player["hazards"] += 1
            self.conn.execute(self.db.hazards.insert(), race_id=self.race.id, player=playerNum, timestamp=self.getFrameElapse(self.state["startFrame"], frame))
            print "hazard", "player:", playerNum, "time:", self.getFrameElapse(self.state["startFrame"], frame)

    def rankUpdate(self, frame, rank, playerNum):
        player = self.state["players"][playerNum]

        if "rank" in player:
            lastRank = player["rank"]
            lastFrame = player["rankFrame"]
            elapsed = self.getFrameElapse(lastFrame, frame)
            sinceBegin = self.getFrameElapse(self.state["startFrame"], lastFrame)

            print 'rank:', lastRank, "elapsed:", elapsed, "player:", playerNum, "currentRank:", rank
            self.conn.execute(self.db.ranks.insert(), race_id=self.race.id, elapsed=elapsed, timestamp=sinceBegin, rank=lastRank, player=playerNum)

            player["rankTimes"][lastRank-1] += self.getFrameElapse(lastFrame, frame)
            player["rankFrame"] = frame

        else:
            player["rankTimes"] = [0.,0.,0.,0.]
            player["rankFrame"] = self.state["startFrame"]

        player["rank"] = rank

    def endRace(self, frame):
        elapsed = self.getFrameElapse(self.state["startFrame"], frame)
        self.race, self.state = self.reset()

# main worker
def read_queue():
    p = Parser()
    # if we're in a thread, we'll eventually be terminated
    while True:
        try:
            line = queue.get(shouldWait)
        # if we're reading this from a file this should happen at EOF
        except QueueEmpty:
            break

        chunks = line.split(" ")
        frame, info = chunks[0], chunks[1:]

        if frame == "#":
            continue

        frame = int(frame)
        
        if info[0] == "race":
            if info[1] == "started":
                p.startRace(frame)
                print info
            elif info[1] == "finished":
                p.finish(frame, int(info[2]))
            elif info[1] == "hazard":
                p.hazard(frame, int(info[2]))

        elif info[0] == "lap":
            lap, player = int(info[1]), int(info[2])
            if lap > 1:
                p.updateLap(frame, lap, player)

        elif info[0] == "rank":
            rank, player = int(info[1]), int(info[2])
            p.rankUpdate(frame, rank, player)

        queue.task_done()

# read from log file
if __name__ == "__main__":
    shouldWait = False
    with open(sys.argv[1], 'r') as f:
        for line in f:
            queue.put(line)

    read_queue()
