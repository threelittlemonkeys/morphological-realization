from .constants import *
from .lexicon import *
from .glossary import *
from .realizer import *
from .script import *
from .utils import *

class parser():

    def __init__(self, lexicon, glossary):
        self.lang = None
        self.lexicon = dict()
        self.glossary = dict()

        for fn in lexicon:
            load_lexicon(self.lexicon, fn)

        for fn in glossary:
            load_glossary(self.glossary, fn)

    def read(self, script):
        return load_script(script)

    def parse_node(self, idx, tree, feats):
        e = tree[idx]

        if e.state:
            return
        e.state = True

        if not e.feats:

            if e.head not in (-1, "*"): # if head exists
                self.parse_node(e.head, tree, feats)
                feats = tree[e.head].feats
                if hasattr(feats, "cat"):
                    delattr(feats, "cat")

            if e.head != -1:
                e.form, e.feats = realize(self, e.form, feats)

        if idx < len(tree) - 1:
            self.parse_node(idx + 1, tree, feats)

    def parse_term(self, idx, tree):
        e = tree[idx]

        if e.state:
            return
        e.state = True

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
                term, head, feats = m.groups()
                term = terms[int(term)] if term.isdecimal() else (*term.split(" "),)
                head = int(head) if head else -1
                lemma = self.glossary[term][lang][1]
                feats = feats[1:].split(":") if feats else None
                tree.append(node(i, head, lemma, feats, m.span()))

            self.parse_term(0, tree)

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
                word = realize_ko_morpheme(tgt[i - 1], m.group(1))
                tgt = tgt[:i] + word + tgt[j:]
                k += len(word) - (j - i)

            if VERBOSE:
                printl("src =", src)
                printl("tgt =", tgt)
                printl("lang =", lang)
                for i, term in enumerate(terms):
                    try:
                        term = self.glossary[term][lang][0]
                        printl("term[%d] =" % i, term)
                    except:
                        pass
                printl("tree =")
                for e in tree:
                    printl(e)
                input() # printl()
            else:
                print(src, tgt, sep = "\t")
