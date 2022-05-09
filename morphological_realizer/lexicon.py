from .constants import *

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
            lang = lang[:-1]

        if lang not in lexicon:
            lexicon[lang] = [dict(), dict()]

        if not idx:
            if lang == "ru":
                lemma = re.sub("(?<!<)C(?!>)", "[бвгджзклмнпрстфхцчшщ]", lemma)
                lemma = re.sub("(?<!<)V(?!>)", "[аеёийоуъыьэюя]", lemma)
            lemma = re.compile("^%s$" % lemma)

        if lemma not in lexicon[lang][idx]:
            lexicon[lang][idx][lemma] = dict()

        lexicon[lang][idx][lemma][feats] = word

    '''
    for lang in lexicon:
        for items in lexicon[lang]:
            for lemma, words in items.items():
                print(lang, lemma, words)
    '''

    fo.close()
