import cv2
import cv2.cv as cv
from manager import Manager
import util
from video import RTMPCapture
import signal
from functools import partial
from args import args

class ScreenManager(Manager):
    debugRect = None
    debug = False
    frameNumber = 0

    def __init__(self, filename):
        if filename.startswith('rtmp'):
            self.cap = RTMPCapture(filename)
        else:
            #self.cap = cv2.VideoCapture(filename)
            self.cap = RTMPCapture(filename)
        super(ScreenManager, self).__init__()
        self.shouldQuit = False
        self.states = {"mode": "unknown"}
        signal.signal(signal.SIGINT, partial(self.quit, self))

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

            if args.debug:
                self.drawDebugRects(frame)
                cv2.imshow('frame', frame)
                if cv2.waitKey(1)==27:
                    break
            if self.shouldQuit:
                break

        self.cleanup()

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def quit(self, *args):
        print "# User interrupt"
        self.shouldQuit = True

    def modeChanged(self, value):
        print self.frameNumber, "mode", value

    def addWatcher(self, watcher):
        super(ScreenManager, self).addWatcher(watcher)
        if watcher.debug:
            self.debugRect = watcher.rect

