import re
from .constants import RE_GLOSSARY_TOKEN

def load_glossary(filename):

    glossary = dict()

    fo = open(filename)
    keys = []
    terms = []

    for ln, line in enumerate(fo, 1):

        if line == "\n":
            terms = {
                lang: [(heads[head], lemma) for head, lemma in term]
                for lang, term in terms
            }
            for key in keys:
                glossary[key] = terms
            keys = []
            heads = {}
            terms = []
            continue

        key = []
        term = []
        heads = {None: -1, "*": "*"}
        lang, line = line.strip().split(" ", 1)

        for idx, token in enumerate(line.split(" ")):

            m = RE_GLOSSARY_TOKEN.search(token)
            if m:
                _idx, head, lemma = m.groups()
            else:
                _idx, head, lemma = None, None, token

            key.append(lemma)
            term.append((head, lemma))
            if _idx: # if head
                heads[_idx] = idx

        keys.append(tuple(key))
        terms.append((lang, term))

    fo.close()

    print(glossary)
    return glossary
