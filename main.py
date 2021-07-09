import sys
from mr.parser import parser

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit("Usage: %s lexicon glossary script" % sys.argv[0])

    mr = parser(
        lexicon = sys.argv[1],
        glossary = sys.argv[2]
    )

    script = mr.read(sys.argv[3])

    for texts, terms in script:
        mr.parse(texts, terms)
