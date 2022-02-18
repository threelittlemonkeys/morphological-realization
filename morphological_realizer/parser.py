from . import logger
from .constants import *
from .lexicon import *
from .glossary import *
from .realizer import *
from .script import *
from .utils import *

class parser():

    def __init__(self, lexicon, glossary):
        self.lang = None
        self.lexicon = load_lexicon(lexicon)
        self.glossary = load_glossary(glossary)

    def read(self, script):
        return load_script(script)

    def parse_node(self, idx, tree, feats = None):
        e = tree[idx]

        if not e.feats:

            if e.head not in (-1, "*"): # if head exists
                self.parse_node(e.head, tree, feats)
                feats = tree[e.head].feats

            e.form, e.feats = realize(self, e.form, feats)

        if idx < len(tree) - 1:
            self.parse_node(idx + 1, tree, feats)

    def parse_term(self, idx, tree):
        e = tree[idx]

        if type(e.feats) != avm:

            if e.head >= 0: # if head exists
                pass # TODO

            e.form = [node(i, *x) for i, x in enumerate(e.form)]
            e.feats = avm(e.feats)
            self.parse_node(0, e.form, e.feats)

        if idx < len(tree) - 1:
            self.parse_term(idx + 1, tree)

    def parse(self, text, terms):

        for lang, src in text:
            self.lang = lang

            # term realization

            tree = list()
            for i, m in enumerate(re.finditer(RE_TERM, src)):
                idx, head, feats = m.groups()
                idx = int(idx)
                head = int(head) if head else -1
                lemma = self.glossary[terms[idx]][lang][1]
                feats = feats[1:].split(":") if feats else None
                tree.append(node(i, head, lemma, feats, m.span()))
            self.parse_term(0, tree)

            # term substitution

            k = 0
            tgt = src
            for e in tree:
                i, j = e.span
                term = " ".join(x.form for x in e.form)
                tgt = tgt[:i + k] + term + tgt[j + k:]
                k += len(term) - (j - i)

            # function word realization

            k = 0
            for m in re.finditer(RE_WORD, tgt):
                i, j = m.start() + k, m.end() + k
                word = m.group(1)
                if i > 0 and word in ("와", "을"):
                    word = realize_ko_morpheme(tgt[i - 1], word)
                tgt = tgt[:i] + word + tgt[j:]
                k += len(word) - (j - i)

            # results

            logger.log("src =", src)
            logger.log("tgt =", tgt)
            logger.log("lang =", lang)

            for i, term in enumerate(terms):
                try:
                    term = self.glossary[term][lang][0]
                    logger.log("term[%d] =" % i, term)
                except:
                    pass

            logger.log("tree =")
            for e in tree:
                logger.log(e)

            logger.log()
