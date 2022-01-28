import sys
from .constants import LOGGER_STREAM

def log(*args):
    if LOGGER_STREAM == None:
        return
    print(*args, file = LOGGER_STREAM)

def err(error_id, *args):
    log("Error:", error_id % args)
    sys.exit()
