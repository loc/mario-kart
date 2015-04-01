from watcher import Watcher
import operator


class ModeWatcher(Watcher):
    predicate = {"mode": "unknown"}

    def update(self):
        self.manager.state("mode", "racing")


export = ModeWatcher
