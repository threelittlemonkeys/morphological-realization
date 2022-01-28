from . import logger
from .constants import *

def load_script(filename):

    fo = open(filename)
    texts = list()
    terms = list()

    for ln, line in enumerate(fo, 1):

        if line == "\n":
            yield texts, terms
            texts.clear()
            terms.clear()
            continue

        line = line.strip()
        tag, text = line.split(" ", 1)

        # term
        if tag.isnumeric():
            tag = int(tag)
            if tag == len(terms):
                key = tuple(text.split(" "))
                terms.append(key)
                continue

        # text
        if tag in LANGS:
            texts.append((tag, text))
            continue

        logger.err(ERR_INVALID_SYNTAX % (filename, ln))
        sys.exit()

    fo.close()
