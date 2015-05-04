import sys
from queue import queue
from args import args

f = None
funcs = []

def toQueue(datum):
    queue.put(datum)

def toStdout(datum):
    print datum

def toFile(datum):
    if f:
        f.write(datum + "\n")

def log(*data):
    datum = " ".join(map(str, data))
    for func in funcs:
        func(datum)

if args.log:
    f = open(args.log, 'a')
    funcs.append(toFile)

if args.store:
    funcs.append(toQueue)

#if args.debug:
funcs.append(toStdout)
