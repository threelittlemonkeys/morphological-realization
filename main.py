import sys
from mr.realizer import realizer

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit("Usage: %s lexicon glossary script" % sys.argv[0])

    mr = realizer(
        lexicon = sys.argv[1],
        glossary = sys.argv[2]
    )

    script = mr.read(sys.argv[3])

    for texts, terms in script:
        mr.run(texts, terms)
