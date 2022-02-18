from . import logger
from .constants import *

class avm(): # attribute value matrix

    def __init__(self, feats = None):
        '''
        for attr in A_DICT:
            setattr(self, attr, None)
        '''
        self.update(feats)

    def __repr__(self):
        pairs = ("%s: %s" % x for x in self.__dict__.items() if x[1])
        return "{%s}" % ", ".join(pairs)

    def values(self):
        return set(v for k, v in self.__dict__.items() if v)

    def update(self, feats):
        if not feats:
            return

        if type(feats) == avm:
            for k, v in feats.__dict__.items():
                setattr(self, k, v)
            return

        for f in feats:
            if f not in V_DICT:
                logger.err(ERR_UNKNOWN_FEATURE, f)
            setattr(self, V_DICT[f], f)

def realize(parser, lemma, feats):

    lang = parser.lang
    lexicon = parser.lexicon

    if lang not in lexicon:
        return lemma, None

    words = None
    _lemma = None
    if lemma in lexicon[lang][0]:
        words = lexicon[lang][0][lemma]
    else:
        for _lemma in lexicon[lang][1]:
            if _lemma.search(lemma):
                words = lexicon[lang][1][_lemma]
                _re = True
                break

    if not words:
        return lemma, None

    feats = avm(feats)
    vs = feats.values()

    cands = [(x, set(x[0]).intersection(vs)) for x in words.items()]
    c_feats, c_word = sorted(cands, key = lambda x: -len(x[1]))[0][0]

    if _lemma:
        c_word = _lemma.sub(c_word, lemma)
    feats.update(c_feats)

    return c_word, feats
