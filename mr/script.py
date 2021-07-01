from .constants import LANGS
from . import logger

def load_script(filename):

    fo = open(filename)
    texts = []
    terms = []

    for ln, line in enumerate(fo, 1):

        if line == "\n":
            yield texts, terms
            texts.clear()
            terms.clear()
            continue

        line = line.strip()
        tag, text = line.split(" ", 1)

        # text
        if tag in LANGS:
            texts.append((tag, text))
            continue

        # term
        if tag.isnumeric():
            tag = int(tag)
            if tag == len(terms):
                key = tuple(text.split(" "))
                terms.append(key)
                continue

        logger.error(filename, ln)

    fo.close()
