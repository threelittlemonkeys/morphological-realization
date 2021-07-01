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

    def realize(self, idx, term, fs):
        if len(term[idx]) == 2:
            head, lemma = term[idx]
            if head not in (-1, "*"):
                self.realize(head, term, fs)
            if lemma in self.lexicon:
                if head not in (-1, "*"):
                    fs = term[head][2].copy()
                term[idx] = (head, *parse_fs(lemma, fs, self.lexicon))
            else:
                term[idx] = (head, lemma, None)
        if idx < len(term) - 1:
            self.realize(idx + 1, term, fs)

    def parse(self, texts, terms):
        for lang, text in texts:
            print()
            print(text)
            for m in re.finditer(RE_SCRIPT_TOKEN_A, text):
                idx, head, fs, _ = m.groups()
                idx = int(idx)
                head = head[1:] if head else None
                term = self.glossary[terms[idx]][lang].copy()
                fs = fs[1:].split(":")

                print(term)
                self.realize(idx, term, fs)
                print(term)

            for m in re.finditer(RE_SCRIPT_TOKEN_B, text):
                lemma = m.group(1)
