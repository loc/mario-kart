import util
import cv2
class Manager(object):
    debugRect = None
    debug = False
    supress = False

    def __init__(self):
        self.history = []
        self.watchers = []
        self.currentFrame = None
        self.size = None
        self.states = {}
        self.lastStates = {}
        self.frozenState = None
        super(Manager, self).__init__()

    def broadcastFrame(self, frame):
        for watcher in self.watchers:
            if watcher.shouldWatch():
                watcher.updateFrame(frame)

    def drawDebugRects(self, frame):
        for watcher in self.watchers:
            if watcher.debug:
                d = watcher.debugRect()
                if d:
                    if getattr(self, "rect", None) is not None:
                        adjusted = (self.rect[0][0] + d[0][0], self.rect[0][1] + d[0][1])
                    else:
                        adjusted = d
                    rect = util.pointSizeToRect((adjusted, d[1]))
                    cv2.rectangle(frame, rect[0], rect[1], (255,0,0), 1)

    def addWatcher(self, watcher):
        watcher.manager = self
        self.watchers.append(watcher)
        return watcher

    def loop():
        self.updateState();

    def updateState(self):
        self.frozenState = self.states.copy()

    def unset(self, key):
        self.states[key] = None

    def state(self, key, val=None, lookback=0, force=False, supress=False):
        if val == None:
            return self.getState(key, lookback)
        return self.setState(key, val, force=force, supress=supress)

    def getState(self, key, lookback=0):
        stateDict = self.states
        if self.frozenState:
            stateDict = self.frozenState

        if stateDict and key in stateDict:
            return stateDict[key]
        

    def setState(self, key, val, force=False, supress=False):
        if key not in self.states or force or self.states[key] != val:
            self.history.append(self.states.copy())
            self.states[key] = val
            if not self.supress and not supress:
                handler = getattr(self, key + "Changed", None)
                if handler:
                    handler(val)
            self.stateChange = True
        return val

