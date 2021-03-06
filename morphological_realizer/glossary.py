from .constants import *

def load_glossary(glossary, filename):
    fo = open(filename)

    keys = list()
    terms = list()

    for ln, line in enumerate(fo, 1):

        i = line.find("#")
        if i >= 0:
            line = line[:i]
        line = line.strip()

        if line == "":

            _terms = {
                lang: (line, tuple((heads[head], lemma) for head, lemma in term))
                for lang, line, term, heads in terms
            }

            for key in keys:
                glossary[key] = _terms

            keys.clear()
            terms.clear()
            continue

        key = list()
        term = list()
        heads = {None: -1, "*": "*"}
        lang, line = line.strip().split(" ", 1)

        for idx, token in enumerate(line.split(" ")):

            m = RE_NODE.search(token)
            if m:
                _idx, head, lemma = m.groups()
            else:
                _idx, head, lemma = None, None, token

            key.append(lemma)
            term.append((head, lemma))
            if _idx: # if head
                heads[_idx] = idx

        keys.append(tuple(key))
        terms.append((lang, line, term, heads))

    fo.close()
