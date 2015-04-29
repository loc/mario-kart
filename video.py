import cv2
import numpy as np
import subprocess as sp
import time
import signal
import os
import functools
import sys

class RTMPCapture():
    pipe = None
    size = (480, 854, 3)

    def __init__(self, url, size=None):
        if size:
            self.size = size

        command = [ "ffmpeg",
                   "-loglevel", "panic",
                    #"-pix_fmt", "yuv420p",
                    "-i", url,
                    '-vf', 'scale=%d:%d'%self.size[-2::-1],
                    "-c:v", "rawvideo", 
                    "-b:v", "3500",
                    "-probesize", "32768",
                    "-vsync", "0",
                    "-f", "rawvideo", 
                    "-pix_fmt", "bgr24",
                    "-an",
                    "-"
                    ]

        self.pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10**8, preexec_fn=os.setsid)

        signal.signal(signal.SIGINT, functools.partial(self.release, self))

    def read(self):
        rawimg = self.pipe.stdout.read(np.prod(self.size))
        self.pipe.stdout.flush()
        image = np.fromstring(rawimg, dtype=np.uint8)
        if image.size:
            image = image.reshape(self.size)
        else:
            sys.stderr.write("# Lost video connection\n")
            sys.exit(0)
            
        return True, image

    def isOpened(self):
        return True

    def release(self, *args):
        os.killpg(self.pipe.pid, signal.SIGTERM)

if __name__ == "__main__":
    cap = RTMPCapture("rtmp://192.168.89.160:1935/live/test")
    while 1:
        cv2.imshow('f', cap.read()[1])
        cv2.waitKey(1)


