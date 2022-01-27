import re
from .constants import *

def load_glossary(filename):

    with open(filename) as fo:
        data = fo.read().strip().split("\n\n")

    glossary = dict()

    for block in data:

        keys = list()
        terms = list()
        block = block.split("\n")

        for line in block:

            key = list()
            term = list()
            heads = {None: -1, "*": "*"}
            lang, line = line.strip().split(" ", 1)

            for idx, token in enumerate(line.split(" ")):

                m = RE_TERM.search(token)
                if m:
                    _idx, head, lemma = m.groups()
                else:
                    _idx, head, lemma = None, None, token

                key.append(lemma)
                term.append((head, lemma))
                if _idx: # if head
                    heads[_idx] = idx

            keys.append(tuple(key))
            terms.append((lang, line, term))

        terms = {
            lang: (line, tuple((heads[head], lemma) for head, lemma in term))
            for lang, line, term in terms
        }

        for key in keys:
            glossary[key] = terms

    return glossary
