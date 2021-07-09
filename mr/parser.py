import sys
import re
from .logger import *
from .constants import *
from .lexicon import *
from .glossary import *
from .grammar import *
from .script import *

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

    def parse_phrase(self, idx, sent):
        phrase = sent[idx]

        if type(phrase.feats) != avm:
            if phrase.head >= 0:
                self.parse_phrase(phrase.head, sent)
                feats.set(sent[phrase.head].feats)
            phrase.form = [node(*x) for x in phrase.form]
            self.parse_term(0, phrase.form, phrase.feats)

        if idx < len(sent) - 1:
            self.parse_phrase(idx + 1, sent)

    def parse(self, texts, terms):
        out = list()
        for lang, text in texts:

            sent = list()
            for m in re.finditer(RE_PHRASE, text):
                idx, head, feats, _ = m.groups()
                idx = int(idx)
                head = int(head[1:]) if head else -1
                lemma = self.glossary[terms[idx]][lang]
                feats = feats[1:].split(":")
                sent.append(node(head, lemma, feats, m.span()))
            self.parse_phrase(0, sent)

            for phrase in sent:
                term = " ".join(term.form for term in phrase.form)
                print(term)

            print(text)
            for x in sent:
                print(x)

            '''
            k = 0
                self.parse(0, term, feats)
                term = " ".join(x[2] for x in term)
                text = text[:i + k] + term + text[j + k:]
                k += len(term) - (j - i)

            for m in re.finditer(RE_WORD, text):
                lemma = m.group(1)

            out.append(text)
            '''
        return out
