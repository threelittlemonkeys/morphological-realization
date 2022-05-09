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
            if hasattr(self, a): # and getattr(self, a) != v:
                return True

    def update(self, feats):
        for a, v in self._iter(feats):
            setattr(self, a, v)

def _criterion(args):

    query, fs, (pt, word) = args
    fs = set(fs)

    if hasattr(query, "gend") and "c" in fs:
        fs.remove("c")
        fs.add(query.gend)

    a = fs.intersection(query.__dict__.values())
    b = fs - a
    c = pt.pattern if pt else word # TODO

    return (-len(a), len(b), -len(c))

def realize(parser, lemma, query):

    if parser.lang not in parser.lexicon:
        return lemma, avm()
    lexicon = parser.lexicon[parser.lang]

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
            if fs.exist(query):
                continue
            fs.update(query)
            queries.append(fs)

    cands = sorted([
        (query, fs, (pt, word))
        for query in queries
        for fs, (pt, word) in cands.items()
    ], key = _criterion)

    if VERBOSE:
        print("lemma =", lemma)
        for i, args in enumerate(cands[:5]):
            query, *cand = args
            printl("cand[%d] =" % i, cand, end = ", ")
            printl("query =", query, end = ", ")
            printl("key =", _criterion(args))
        printl()

    feats = avm()

    if not cands:
        return lemma, feats

    f1, f2, (pt, word) = cands[0]
    if pt:
        word = pt.sub(word, lemma)
    feats.update(f1)
    feats.update(f2)

    return word, feats
