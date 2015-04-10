import cv2
import numpy as np
import subprocess as sp
import time

class RTMPCapture():
    pipe = None
    size = (480, 853, 3)

    def __init__(self, url, size=None):
        if size:
            self.size = size

        command = [ "ffmpeg",
                    "-r", "24",
                    "-i", url,
                    '-vf', 'scale=%d:%d'%self.size[-2::-1],
                    "-c:v", "rawvideo", 
                    "-f", "rawvideo", 
                    "-pix_fmt", "bgr24",
                    "-an",
                    "-"]

        self.pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10**8)

    def read(self):
        rawimg = self.pipe.stdout.read(np.prod(size))
        image = np.fromstring(rawimg, dtype=np.uint8)
        image = image.reshape(size)
        self.pipe.stdout.flush()
        return True, image

    def isOpened(self):
        return True

    def release(self):
        pass

