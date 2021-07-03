import sys
from .constants import LOGGER_STREAM

def log(*args):
    if LOGGER_STREAM == None:
        return
    print(*args, file = LOGGER_STREAM)

def err(err_id, *args):
    log("Error:", err_id % args)
    sys.exit()
