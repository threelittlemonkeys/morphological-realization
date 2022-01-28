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

        out += "feats: %s}" % (self.feats or "{}")

        if type(self.form) == list:
            for i, form in enumerate(self.form):
                out += "\n  %s" % form

        return out

class avm(): # attribute value matrix

    def __init__(self, *feats):

        for attr in A_DICT:
            setattr(self, attr, None)

        self.add(feats)

    def __repr__(self):

        pairs = ("%s: %s" % x for x in self.__dict__.items() if x[1])
        return "{%s}" % ", ".join(pairs)

    def add(self, feats):

        if not feats:
            return

        if type(feats) == avm:
            for x in feats.__dict__.items():
                setattr(self, *x)
            return

        for f in feats:
            if f not in V_DICT:
                logger.err(ERR_UNKNOWN_FEATURE, f)
            setattr(self, V_DICT[f], f)

def realize(lemma, feats, lexicon):

    if lemma not in lexicon:
        return lemma, None

    lang, cat, words = lexicon[lemma]
    fs = avm() # feature structure
    fs.add(feats)
    fs.add(cat)

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
