#!/usr/bin/env python

import sys
from schema import *
import sqlalchemy
import datetime

conn = engine.connect()

setId = 1
conn.execute(races.insert(), set_id=setId, date=datetime.date.today())
stmt = select([races]).order_by(desc("id"))
race = conn.execute(stmt).fetchone()

state = {
    "started": False,
    "startFrame": None,
    "players": [{},{},{},{}]
}

def getFrameElapse(start, end):
    return (end - start) / 30.0

def updateLap(frame, lap, playerNum):
    player = state["players"][playerNum]

    if "lap" in player:
        current = player["lap"]
        elapsed = getFrameElapse(player["lapFrame"], frame)
        if lap > current:
            sinceBegin = getFrameElapse(state["startFrame"], player["lapFrame"])
            print "lap:", lap-1, "player:", playerNum, "elapsed:", elapsed
            try: 
                conn.execute(laps.insert(), race_id=race.id, elapsed=elapsed, timestamp=sinceBegin, lap=lap-1, player=playerNum)
            except sqlalchemy.exc.IntegrityError:
                print "Integrity error", "lap", lap-1, "player", playerNum, "elapsed", elapsed
        else:
            player["lap"] = lap
            return

    player["lap"] = lap
    player["lapFrame"] = frame

def startRace(frame):
    if state["startFrame"]:
        return

    state["startFrame"] = frame

    for i in range(4):
        updateLap(frame, 1, i)

def finish(frame, playerNum):
    player = state["players"][playerNum]
    hazard = 0

    if "hazards" in player:
        hazard = player["hazards"]

    player["finished"] = True
    updateLap(frame, 4, playerNum)
    rankUpdate(frame, player["rank"], playerNum)

    raceTime = getFrameElapse(state["startFrame"], player["lapFrame"])


    print "race", race.id, "player:", playerNum, "hazard:", hazard, "rank:", player["rank"], "time:", raceTime, "times:", player["rankTimes"]

    if all(["finished" in p for p in state["players"]]):
        endRace(frame)

def hazard(frame, playerNum):
    player = state["players"][playerNum]

    if "finished" not in player:
        if "hazards" not in player:
            player["hazards"] = 1
        else:
            player["hazards"] += 1

    conn.execute(hazards.insert(), race_id=race.id, player=playerNum, timestamp=getFrameElapse(state["startFrame"], frame))
    print "hazard", "player:", playerNum, "time:", getFrameElapse(state["startFrame"], frame)

def rankUpdate(frame, rank, playerNum):
    player = state["players"][playerNum]

    if "rank" in player:
        lastRank = player["rank"]
        lastFrame = player["rankFrame"]
        elapsed = getFrameElapse(lastFrame, frame)
        sinceBegin = getFrameElapse(state["startFrame"], lastFrame)

        print 'rank:', lastRank, "elapsed:", elapsed, "player:", playerNum, "currentRank:", rank
        conn.execute(ranks.insert(), race_id=race.id, elapsed=elapsed, timestamp=sinceBegin, rank=lastRank, player=playerNum)

        player["rankTimes"][lastRank-1] += getFrameElapse(lastFrame, frame)
        player["rankFrame"] = frame

    else:
        player["rankTimes"] = [0.,0.,0.,0.]
        player["rankFrame"] = state["startFrame"]

    player["rank"] = rank

def endRace(frame):
    elapsed = getFrameElapse(state["startFrame"], frame)

with open(sys.argv[1], 'r') as f:
    for line in f:
        chunks = line.split(" ")
        frame, info = chunks[0], chunks[1:]

        if frame == "#":
            continue

        frame = int(frame)
        
        if info[0] == "race":
            if info[1] == "started":
                startRace(frame)
                print info
            elif info[1] == "finished":
                finish(frame, int(info[2]))
            elif info[1] == "hazard":
                hazard(frame, int(info[2]))

        elif info[0] == "lap":
            lap, player = int(info[1]), int(info[2])
            if lap > 1:
                updateLap(frame, lap, player)

        elif info[0] == "rank":
            rank, player = int(info[1]), int(info[2])
            rankUpdate(frame, rank, player)


