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
        self.frozenState = None
        super(Manager, self).__init__()

    def broadcastFrame(self, frame):
        for watcher in self.watchers:
            if watcher.shouldWatch():
                watcher.updateFrame(frame)

    def addWatcher(self, watcher):
        watcher.manager = self
        self.watchers.append(watcher)
        return watcher

    def loop():
        self.updateState();

    def updateState(self):
        self.frozenState = self.states.copy()

    def state(self, key, val=None, lookback=0, force=False):
        if val == None:
            return self.getState(key, lookback)
        return self.setState(key, val, force=force)

    def getState(self, key, lookback=0):
        stateDict = self.states
        if self.frozenState:
            stateDict = self.frozenState

        if stateDict and key in stateDict:
            return stateDict[key]
        

    def setState(self, key, val, force=False):
        if key not in self.states or force or self.states[key] != val:
            self.history.append(self.states.copy())
            self.states[key] = val
            if not self.supress:
                print self.states
            self.stateChange = True
        return val

