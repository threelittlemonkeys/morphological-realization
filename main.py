import sys
from morphological_realizer.parser import parser

if __name__ == "__main__":

    if len(sys.argv) != 4:
        sys.exit("Usage: %s lexicon glossary script" % sys.argv[0])

    mr = parser(
        lexicon = [
            "data/lexicon.ru.noun.csv",
            "data/lexicon.ru.adj.csv",
            "data/lexicon.ru.words.csv"
        ],
        glossary = sys.argv[2].split(","),
    )

    script = mr.read(sys.argv[3])

    for text, terms in script:
        mr.parse(text, terms)
