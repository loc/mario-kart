from watcher import Watcher
import numpy as np

class CropWatcher(Watcher):
    current = None
    debug = True
    crop = None

    def shouldWatch(self):
        if self.manager.state('mode') in ("setup", "racing") and self.manager.state('crop') == None:
            return True
        return False

    def debugRect(self):
        return self.crop

    def update(self):
        comp = np.sum(self.window, axis=2)
        across = np.mean(comp, axis=0).astype(int)
        down = np.mean(comp, axis=1).astype(int)
        sign = 1
        labels = ["left", "right", "top", "bottom"]
        vals = []

        for arr in (across, down):
            for sign in (1, -1):
                for i, ele in enumerate(arr[::sign]):
                    if ele > 15:
                        vals.append(i)
                        break
        
        self.margins = dict(zip(labels, vals))
        
        top = self.margins["top"]
        left = self.margins["left"]
        w = self.window.shape[1] - self.margins["right"]
        h = self.window.shape[0] - self.margins["bottom"]
        self.crop = ((left, top), (w, h))

        self.manager.state('crop', self.crop)

export = CropWatcher
