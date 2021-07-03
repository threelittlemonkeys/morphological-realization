from .constants import *
from . import logger

def load_lexicon(filename):
    lexicon = dict()
    fo = open(filename)

    for ln, line in enumerate(fo, 1):
        if line == "\n":
            continue

        lemma, feats, *word = line.strip().split(" ")
        feats = tuple(feats.split(":"))

        if lemma not in lexicon:
            lexicon[lemma] = [None if word else feats, {}]

        if word: # surface form
            lexicon[lemma][1][feats] = word[0]

    fo.close()
    return lexicon

class avm(): # attribute value matrix

    def __init__(self, feats):
        self.pos = None # part of speech
        self.gend = None # gender
        self.num = None # number
        self.case = None
        self.anim = None # animacy

        self.set(feats)

    def set(self, feats):

        if not feats:
            return

        if type(feats) == avm:
            for x in feats.__dict__.items():
                setattr(self, *x)
            return

        for f in feats:
            if f in ("adj", "noun"):
                self.pos = f
            elif f in ("m", "f", "n"):
                self.gend = f
            elif f in ("sg", "pl"):
                self.num = f
            elif f in ("nom", "acc"):
                self.case = f
            elif f == "anim":
                self.anim = True
            elif f != "":
                logger.err(ERR_UNKNOWN_FEATURE, f)

def realize(lemma, feats, lexicon):

    if lemma not in lexicon:
        return lemma, None

    fs = avm(feats)
    cat, words = lexicon[lemma]
    fs.set(cat)

    if not fs.gend: fs.gend = "m"
    if not fs.num: fs.num = "sg"
    if not fs.case: fs.case = "nom"

    word = None

    if fs.pos == "adj":
        feats = (fs.gend, fs.num, fs.case)
        _feats = feats + ("anim",)
        if fs.anim and _feats in words:
            word = words[_feats]
        if not word:
            word = words[feats]

    if fs.pos == "noun":
        word = lexicon[lemma][1][(fs.num, fs.case)]

    return word, fs
