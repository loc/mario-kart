import cv2
from manager import Manager
import util

class ScreenManager(Manager):
    debugRect = None
    debug = False

    def __init__(self, filename):
        self.cap = cv2.VideoCapture(filename)
        super(ScreenManager, self).__init__()
        self.states = {"mode": "unknown"}

    def loop(self):
        while self.cap.isOpened():
            self.updateState()
            ret, frame = self.cap.read()
            if ret is True:

                if self.state('crop') != None:
                    frame = util.cropRect(frame, self.state('crop'))

                self.broadcastFrame(frame)

                for watcher in self.watchers:
                    rect = watcher.debugRect()
                    if watcher.debug and rect:
                        cv2.rectangle(frame, rect[0], rect[1], (255,0,0), 1)
                cv2.imshow('frame', frame)
            if cv2.waitKey(1)==27:
                break

        self.cleanup()

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def addWatcher(self, watcher):
        super(ScreenManager, self).addWatcher(watcher)
        if watcher.debug:
            self.debugRect = watcher.rect

