import os
import glob
from importlib import import_module

modules = [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__)+"/*.py") if os.path.isfile(f) and not os.path.basename(f).startswith('_')]
watchers = [import_module("." + m, "watch").export for m in modules]
