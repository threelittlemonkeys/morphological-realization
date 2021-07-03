import sys
import re
from . import logger
from .constants import *
from .lexicon import *
from .glossary import *
from .script import *

class realizer():

    def __init__(self, lexicon, glossary):
        self.lexicon = load_lexicon(lexicon)
        self.glossary = load_glossary(glossary)

    def read(self, script):
        return load_script(script)

    def parse(self, idx, term, feats):

        if len(term[idx]) == 2:
            head, lemma = term[idx]

            if head not in (-1, "*"): # if head exists
                self.parse(head, term, feats)
                feats = term[head][3]

            term[idx] += realize(lemma, feats, self.lexicon)

        if idx < len(term) - 1:
            self.parse(idx + 1, term, feats)

    def run(self, texts, terms):
        out = []
        for lang, text in texts:
            k = 0

            print(text)
            for m in re.finditer(RE_SCRIPT_TOKEN_A, text):
                idx, head, feats, _ = m.groups()
                i, j = m.start(), m.end()
                idx = int(idx)
                head = head[1:] if head else None
                term = self.glossary[terms[idx]][lang].copy()
                feats = feats[1:].split(":")

                self.parse(0, term, feats)
                term = " ".join(x[2] for x in term)
                text = text[:i + k] + term + text[j + k:]
                k += len(term) - (j - i)

            for m in re.finditer(RE_SCRIPT_TOKEN_B, text):
                lemma = m.group(1)

            out.append(text)
        print("\n".join(out))
        return out
