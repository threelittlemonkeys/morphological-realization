from .constants import *
from .utils import *

def load_lexicon(lexicon, filename):
    fo = open(filename)

    for ln, line in enumerate(fo, 1):

        i = line.find("#")
        if i >= 0:
            line = line[:i]
        line = line.strip()

        if line == "":
            continue

        lang, lemma, feats, *word = line.split(" ")
        feats = tuple(feats.split(":"))
        word = word[0] if word else None

        idx = 1
        if lang[-1] == "*":
            idx = 0
        if lang[-1] == "!":
            idx = 2
        lang = lang if idx == 1 else lang[:-1]

        if lang not in lexicon:
            lexicon[lang] = [dict(), dict(), dict()]

        if idx == 0:
            if lang == "ru":
                lemma = re.sub("(?<!<)C(?!>)", "[бвгджзклмнпрстфхцчшщ]", lemma)
                lemma = re.sub("(?<!<)V(?!>)", "[аеёийоуъыьэюя]", lemma)
            lemma = re.compile("^%s$" % lemma)

        if idx == 2:
            pt_a, pt_b = word.strip("/").split("/")
            word = (re.compile(pt_a), pt_b)

        if lemma not in lexicon[lang][idx]:
            lexicon[lang][idx][lemma] = dict()

        lexicon[lang][idx][lemma][feats] = word

    '''
    for lang in lexicon:
        for items in lexicon[lang]:
            for lemma, words in items.items():
                printl(lang, lemma, words)
    '''

    fo.close()
