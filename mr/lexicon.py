def load_lexicon(filename):
    lexicon = dict()
    fo = open(filename)

    for ln, line in enumerate(fo, 1):
        if line == "\n":
            continue

        lang, lemma, feats, *word = line.strip().split(" ")
        feats = tuple(feats.split(":"))

        if lemma not in lexicon:
            lexicon[lemma] = [lang, None if word else feats, {}]

        if word: # surface form
            lexicon[lemma][2][feats] = word[0]

    fo.close()
    return lexicon
