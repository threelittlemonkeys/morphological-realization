def load_lexicon(filename):

    lexicon = dict()

    fo = open(filename)

    for ln, line in enumerate(fo, 1):
        lemma, fs, *word = line.strip().split(" ")

        if lemma not in lexicon:
            lexicon[lemma] = [None, {}]

        fs = tuple(fs.split(":"))

        if word: # surface form
            lexicon[lemma][1][fs] = word[0]
        else: # lemma
            lexicon[lemma][0] = fs

    fo.close()

    return lexicon

def avmize(avm, fs):

    if not avm:
        avm = { # attribute value matrix
            "pos": None, # part of speech
            "gend": None, # gender
            "num": None, # number
            "case": None,
            "anim": None, # animacy
        }

    for f in fs:
        # part of speech
        if f in ("adj", "noun"):
            avm["pos"] = f
        elif f in ("m", "f", "n"):
            avm["gend"] = f
        elif f in ("sg", "pl"):
            avm["num"] = f
        elif f in ("nom", "acc"):
            avm["case"] = f

    return avm

def parse_fs(lemma, fs, lexicon):

    if type(fs) == list:
        fs = avmize(None, fs)

    cat, words = lexicon[lemma]
    fs = avmize(fs, cat)

    if fs["pos"] in ("adj", "noun") and not fs["num"]:
        fs["num"] = "sg"

    if fs["pos"] == "adj":
        word = lexicon[lemma][1][(fs["gend"], fs["num"], fs["case"])]

    if fs["pos"] == "noun":
        word = lexicon[lemma][1][(fs["num"], fs["case"])]

    return word, fs
