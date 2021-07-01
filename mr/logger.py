import sys
from .constants import LOGGER_STREAM

def log(*args):
    if LOGGER_STREAM == None:
        return
    print(*args, file = LOGGER_STREAM)

def error(filename, ln):
    log("Error: invalid syntax at %s %d" % (filename, ln))
    sys.exit()
