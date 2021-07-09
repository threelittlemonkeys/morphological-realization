from .logger import *
from .constants import *

class node():
    def __init__(self, head, form, feats = None, span = None):
        self.head = head
        self.form = form
        self.feats = feats
        self.span = span

    def __repr__(self):
        pairs = ("%s: %s" % x for x in self.__dict__.items())
        return "{%s}" % ", ".join(pairs)

class avm(): # attribute value matrix

    def __init__(self, feats = None):
        self.cat = None # category (part of speech)
        self.gend = None # gender
        self.num = None # number
        self.case = None
        self.anim = False # animacy

        self.set(feats)

    def __repr__(self):
        pairs = ("%s: %s" % x for x in self.__dict__.items())
        return "{%s}" % ", ".join(pairs)

    def set(self, feats):

        if not feats:
            return

        if type(feats) == avm:
            for x in feats.__dict__.items():
                setattr(self, *x)
            return

        for f in feats:
            if f in ("adj", "noun"):
                self.cat = f
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
    lang, cat, words = lexicon[lemma]
    fs.set(cat)

    word = None

    if fs.cat == "adj":
        feats = (fs.gend, fs.num, fs.case)
        _feats = feats + ("anim",)
        if fs.anim and _feats in words:
            word = words[_feats]
        if not word:
            word = words[feats]

    if fs.cat == "noun":
        if not fs.num:
            fs.num = "sg"
        if lang == "en":
            word = lexicon[lemma][2][(fs.num,)]
        else:
            word = lexicon[lemma][2][(fs.num, fs.case)]

    return word, fs
