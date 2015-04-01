class Watcher:
    predicate = {}

    def __init__(self, size=None, topLeft=(0,0)):
        # how big of an area are we concerned with
        self.size = size
        # where the area begins
        self.topLeft = topLeft

        self.window = None

    def shouldWatch(self):
        for key, val in self.predicate.items():
            if self.manager.state(key) != val:
                return False
        return True
    
    def transform(self, frame):
        return frame[self.topLeft[0]:self.topLeft[0]+self.size[0], self.topLeft[1]:self.topLeft[1]+self.size[1], ...]

    def updateFrame(self, frame):
        if not self.size:
            self.size = self.manager.size
        self.window = self.transform(frame)
        self.update()

    def update(self): 
        pass

