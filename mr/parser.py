import sys
import re
from . import logger
from .constants import *
from .lexicon import *
from .glossary import *
from .grammar import *
from .script import *
from .utils import *

class parser():

    def __init__(self, lexicon, glossary):
        self.lexicon = load_lexicon(lexicon)
        self.glossary = load_glossary(glossary)

    def read(self, script):
        return load_script(script)

    def parse_term(self, idx, phrase, feats):
        term = phrase[idx]

        if not term.feats:

            if term.head not in (-1, "*"): # if head exists
                self.parse_term(term.head, phrase, feats)
                feats = phrase[term.head].feats

            term.form, term.feats = realize(term.form, feats, self.lexicon)

        if idx < len(phrase) - 1:
            self.parse_term(idx + 1, phrase, feats)

    def parse_phrase(self, idx, tree):
        phrase = tree[idx]

        if type(phrase.feats) != avm:
            if phrase.head >= 0:
                self.parse_phrase(phrase.head, tree)
                feats.set(tree[phrase.head].feats)
            phrase.form = [node(i, *x) for i, x in enumerate(phrase.form)]
            self.parse_term(0, phrase.form, phrase.feats)

        if idx < len(tree) - 1:
            self.parse_phrase(idx + 1, tree)

    def parse(self, texts, terms):
        for lang, src in texts:

            tree = list()
            for i, m in enumerate(re.finditer(RE_PHRASE, src)):
                idx, head, feats, _ = m.groups()
                idx = int(idx)
                head = int(head[1:]) if head else -1
                lemma = self.glossary[terms[idx]][lang]
                feats = feats[1:].split(":") if feats else None
                tree.append(node(i, head, lemma, feats, m.span()))
            self.parse_phrase(0, tree)

            tgt = src

            k = 0
            for phrase in tree:
                i, j = phrase.span
                term = " ".join(x.form for x in phrase.form)
                tgt = tgt[:i + k] + term + tgt[j + k:]
                k += len(term) - (j - i)

            k = 0
            for m in re.finditer(RE_WORD, tgt):
                i, j = m.start() + k, m.end() + k
                word = m.group(1)
                if i > 0 and word in "와을":
                    word = realize_ko_morpheme(tgt[i - 1], word)
                tgt = tgt[:i] + word + tgt[j:]
                k += len(word) - (j - i)

            logger.log("src =", src)
            logger.log("tgt =", tgt)
            logger.log("lang =", lang)
            for i, term in enumerate(terms):
                logger.log("term[%d] =" % i, " ".join(term))
            logger.log("tree =")
            for i, phrase in enumerate(tree):
                logger.log(phrase)

            logger.log()
