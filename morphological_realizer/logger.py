from .constants import *

def log(*args):
    if LOGGER_STREAM == None:
        return
    print(*args, file = LOGGER_STREAM)

def err(error_id, *args):
    log("Error:", error_id % args)
    sys.exit()
