class Watcher(object):
    predicate = {}
    debug = False
    rect = None

    def __init__(self, rect=None):
        # how big of an area are we concerned with
        if rect:
            self.rect = rect

        self.window = None
        super(Watcher, self).__init__()

    def shouldWatch(self):
        for key, val in self.predicate.items():
            if self.manager.state(key) != val:
                return False
        return True
    
    def transform(self, frame):
        return frame[self.rect[0][1]:self.rect[1][1], self.rect[0][0]:self.rect[1][0], ...]

    def debugRect(self):
        return self.rect

    def updateFrame(self, frame):
        if not self.rect:
            self.rect = ((0,0), frame.shape[:2][::-1])
        self.window = self.transform(frame)
        self.update()

    def update(self): 
        pass
