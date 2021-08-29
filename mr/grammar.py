from . import logger
from .constants import *

class node():

    def __init__(self, idx, head, form, feats = None, span = None):

        self.idx = idx
        self.head = head
        self.span = span
        self.form = form
        self.feats = feats

    def __repr__(self):

        out = "node[%d] = {head: %s, " % (self.idx, self.head)

        if self.span:
            out += "span: %s, " % (self.span,)

        if type(self.form) == str:
            out += "form: %s, " % self.form

        out += "feats: %s}" % (self.feats if self.feats else "{}")

        if type(self.form) == list:
            for i, form in enumerate(self.form):
                out += "\n  %s" % form

        return out

class avm(): # attribute value matrix

    v2k = { # value to key
        "adj": "cat", "noun": "cat",
        "m": "gend", "f": "gend", "n": "gend",
        "sg": "num", "pl": "num",
        "nom": "case", "acc": "case",
        "anim": "anim"
    }

    def __init__(self, *feats):

        self.cat = None # category (part of speech)
        self.gend = None # gender
        self.num = None # number
        self.case = None
        self.anim = None # animacy

        self.set(feats)

    def __repr__(self):

        pairs = ("%s: %s" % x for x in self.__dict__.items() if x[1])
        return "{%s}" % ", ".join(pairs)

    def set(self, feats):

        if not feats:
            return

        if type(feats) == avm:
            for x in feats.__dict__.items():
                setattr(self, *x)
            return

        for f in feats:
            if f in self.v2k:
                setattr(self, self.v2k[f], f)
                continue
            logger.err(ERR_UNKNOWN_FEATURE, f)

def realize(lemma, feats, lexicon):

    if lemma not in lexicon:
        return lemma, None

    lang, cat, words = lexicon[lemma]
    fs = avm()
    fs.set(feats)
    fs.set(cat)

    if fs.cat == "adj":

        if (fs.gend, fs.num, fs.case, fs.anim) in words:
         return words[(fs.gend, fs.num, fs.case, fs.anim)], fs

        if (fs.gend, fs.num, fs.case) in words:
         return words[(fs.gend, fs.num, fs.case)], fs

    if fs.cat == "noun":

        if (fs.num,) in words:
            return words[(fs.num,)], fs

        if (fs.num, fs.case) in words:
            return words[(fs.num, fs.case)], fs

        if lang == "ru" and (fs.num, fs.case, fs.anim) == ("sg", "acc", None):
            return lemma, fs

    logger.err(ERR_SURFACE_FORM_NOT_FOUND % (lemma, fs))
