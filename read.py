from watch import watchers
from managers.screen import ScreenManager
from args import args
import threading
import parser
from queue import queue

if args.store:
    parser_thread = threading.Thread(target=parser.read_queue)
    parser_thread.daemon = True
    parser_thread.start()

manager = ScreenManager(args.input)
manager.state('playerCount', 4)
for Watcher in watchers:
    watcher = Watcher()
    manager.addWatcher(watcher)

manager.loop()

if queue.qsize():
    print "# blocking until finished"
    queue.join()
