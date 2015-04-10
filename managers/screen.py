import cv2
import cv2.cv as cv
from manager import Manager
import util
from video import RTMPCapture

class ScreenManager(Manager):
    debugRect = None
    debug = False
    frameNumber = 0

    def __init__(self, filename):
        if filename.startswith('rtmp'):
            self.cap = RTMPCapture(filename)
        else:
            self.cap = cv2.VideoCapture(filename)
        super(ScreenManager, self).__init__()
        self.states = {"mode": "unknown"}

    def loop(self):
        while self.cap.isOpened():
            self.updateState()
            ret, frame = self.cap.read()
            if ret is True:
                self.frameNumber += 1
                self.rect = ((0,0), frame.shape[-2::-1])

                if self.state('crop') != None:
                    frame = util.cropRect(frame, self.state('crop'))

                self.broadcastFrame(frame)

                self.drawDebugRects(frame)
                cv2.imshow('frame', frame)
            if cv2.waitKey(1)==27:
                break

        self.cleanup()

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def modeChanged(self, value):
        print "# mode changed:", value

    def addWatcher(self, watcher):
        super(ScreenManager, self).addWatcher(watcher)
        if watcher.debug:
            self.debugRect = watcher.rect

