from . import logger
from .constants import *

def load_script(filename):

    with open(filename) as fo:
        data = fo.read().strip().split("\n\n")

    for block in data:

        texts = []
        terms = []
        block = block.split("\n")

        for line in block:

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

        yield texts, terms
