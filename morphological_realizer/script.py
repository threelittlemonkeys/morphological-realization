from . import logger
from .constants import *

def load_script(filename):

    fo = open(filename)
    text = list()
    terms = list()

    for ln, line in enumerate(fo, 1):

        if line == "\n":
            yield text, terms
            text.clear()
            terms.clear()
            continue

        line = line.strip()
        tag, src = line.split(" ", 1)

        # term
        if tag.isnumeric():
            tag = int(tag)
            if tag == len(terms):
                key = tuple(src.split(" "))
                terms.append(key)
                continue

        # text
        if tag in LANGS:
            text.append((tag, src))
            continue

        logger.err(ERR_INVALID_SYNTAX % (filename, ln))
        sys.exit()

    fo.close()
