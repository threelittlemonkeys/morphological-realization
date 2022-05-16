from .constants import *
from .utils import *

class avm(): # attribute value matrix

    # attribute to value
    atov = {
        "cat": ["adj", "noun"],
        "gend": ["m", "f", "n", "c"],
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
        return "{%s}" % ", ".join(": ".join(x) for x in self.items())

    def _iter(self, feats):

        if not feats:
            return

        if type(feats) == avm:
            for a, v in feats.items():
                yield a, v
            return

        for v in feats:
            if v not in self.vtoa:
                sys.exit(ERR_UNKNOWN_FEATURE % v)
            a = self.vtoa[v]
            yield a, v

    def items(self):
        for a in self.atov:
            if hasattr(self, a):
                yield (a, getattr(self, a))

    def values(self):
        return [v for a, v in self.items()]

    def update(self, feats):
        for a, v in self._iter(feats):
            setattr(self, a, v)

    def diff(self, feats):
        for a, v in self._iter(feats):
            if hasattr(self, a) and getattr(self, a) != v:
                return True

def _criterion(args):

    query, fs, (pt, word) = args
    fs = set(fs)

    if hasattr(query, "gend") and "c" in fs:
        fs.remove("c")
        fs.add(query.gend)

    a = fs.intersection(query.values())
    b = fs - a
    c = (pt != None)
    d = pt.pattern if pt else word # TODO

    return (-len(a), len(b), c, -len(d))

def realize(parser, lemma, query):

    if parser.lang not in parser.lexicon:
        return lemma, avm()
    lexicon = parser.lexicon[parser.lang]
    verbose = parser.verbose

    cands = dict()
    queries = [query]

    for pt in lexicon[0]:
        if pt.search(lemma):
            for fs, word in lexicon[0][pt].items():
                cands[fs] = (pt, word)

    if lemma in lexicon[1]:
        for fs, word in lexicon[1][lemma].items():

            if word:
                cands[fs] = (None, word)
                continue

            fs = avm(fs)
            if fs.diff(query):
                continue
            fs.update(query)
            queries.append(fs)

    cands = sorted([
        (query, fs, (pt, word))
        for query in queries
        for fs, (pt, word) in cands.items()
    ], key = _criterion)

    if verbose:
        printl("lemma =", lemma)
        for i, args in enumerate(cands[:5]):
            query, *cand = args
            printl("cand[%d] =" % i, cand, end = ", ")
            printl("query =", query, end = ", ")
            printl("score =", _criterion(args))
        printl()

    feats = avm()

    if not cands:
        return lemma, feats

    f1, f2, (pt, word) = cands[0]
    if pt:
        word = pt.sub(word, lemma)
    feats.update(f1)
    feats.update(f2)

    if word != lemma and lemma in lexicon[2]:
        for fs, (pt_a, pt_b) in lexicon[2][lemma].items():
            if not feats.diff(fs):
                word = pt_a.sub(pt_b, word)

    return word, feats
