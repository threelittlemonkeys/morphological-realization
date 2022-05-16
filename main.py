import sys
from morphological_realizer.parser import parser

if __name__ == "__main__":

    if len(sys.argv) not in (4, 5):
        sys.exit("Usage: %s lexicon glossary script -[ntv]" % sys.argv[0])
    flag = sys.argv[4] if len(sys.argv) == 5 else None

    mr = parser(
        lexicon = [
            "data/lexicon.ru.noun.csv",
            "data/lexicon.ru.adj.csv",
            "data/lexicon.ru.words.csv"
        ],
        glossary = sys.argv[2].split(","),
        verbose = (flag == "-v")
    )

    script = mr.read(sys.argv[3])

    for text, terms in script:

        out = list()
        for src, tgt, tree in mr.parse(text, terms):

            for e in tree[0].form:
                if e.head == "*":
                    feats = ":".join(e.feats.values())
                    break

            out.append(tgt)

            if flag in (None, "-n"):
                print(feats, tgt, sep = "\t")

        if flag == "-t":
            print(*out, sep = "\t")

        if flag in (None, "-n"):
            print()
