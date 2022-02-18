from . import logger
from .constants import *

def load_lexicon(filename):

    fo = open(filename)
    lexicon = dict()
    _feats = None

    for ln, line in enumerate(fo, 1):

        i = line.find("#")
        if i >= 0:
            line = line[:i]
        line = line.strip()

        if line == "":
            continue

        lang, lemma, feats, *word = line.split(" ")
        feats = tuple(feats.split(":"))

        idx = 0
        if lang[-1] == "*":
            idx = 1
            lang = lang[:-1]

        if lang not in lexicon:
            lexicon[lang] = [dict(), dict()]

        if idx:
            lemma = re.compile("^%s$" % lemma)
        if lemma not in lexicon[lang][idx]:
            lexicon[lang][idx][lemma] = dict()

        if not word:
            _feats = feats
            continue

        print(lemma, _feats + feats, word[0])
        lexicon[lang][idx][lemma][_feats + feats] = word[0]

    fo.close()
    return lexicon
