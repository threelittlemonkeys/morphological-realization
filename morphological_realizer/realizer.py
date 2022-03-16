from .constants import *

class avm(): # attribute value matrix

    # attribute to value
    atov = {
        "cat": ["adj", "noun"],
        "gend": ["m", "f", "n"],
        "num": ["sg", "pl"],
        "case": ["nom", "acc", "gen", "dat", "inst", "prep"],
        "anim": ["anim"]
    }

    # value to attribute
    vtoa = {v: a for a, vs in atov.items() for v in vs}

    def __init__(self, feats = None):
        '''
        for a in self.atov:
            setattr(self, a, None)
        '''
        self.update(feats)

    def __repr__(self):
        return "{%s}" % ", ".join("%s: %s" % x for x in self.__dict__.items())

    def _iter(self, feats):

        if not feats:
            return

        if type(feats) == avm:
            for a, v in feats.__dict__.items():
                yield a, v
            return

        for v in feats:
            if v not in self.vtoa:
                sys.exit(ERR_UNKNOWN_FEATURE % v)
            a = self.vtoa[v]
            yield a, v

    def exist(self, feats):
        for a, v in self._iter(feats):
            if hasattr(self, a) and getattr(self, a) != v:
                return True

    def update(self, feats):
        for a, v in self._iter(feats):
            setattr(self, a, v)

def realize(parser, lemma, query):

    if parser.lang not in parser.lexicon:
        return lemma, None
    lexicon = parser.lexicon[parser.lang]

    cands = dict()
    feats = [query]

    for pt in lexicon[0]:
        if pt.search(lemma):
            for fs, w in lexicon[0][pt].items():
                cands[fs] = (pt, w)

    if lemma in lexicon[1]:
        for fs, w in lexicon[1][lemma].items():
            if w:
                cands[fs] = w
                continue
            fs = avm(fs)
            if fs.exist(query):
                continue
            fs.update(query)
            feats.append(fs)

    def _criterion(cand):
        f1, f2, _ = cand
        f2 = set(f2)
        a = f2.intersection(f1.__dict__.values())
        b = f2 - a
        return (-len(a), len(b))

    cands = [(a, b, c) for a in feats for b, c in cands.items() if not a.exist(b)]
    cands = sorted(cands, key = _criterion)

    if not cands:
        return lemma, None

    f1, f2, word = cands[0]
    f1.update(f2)

    if type(word) == tuple:
        word = word[0].sub(word[1], lemma)

    return word, f1
