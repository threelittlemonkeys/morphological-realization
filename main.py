import sys
from morphological_realizer.parser import parser

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit("Usage: %s lexicon glossary script" % sys.argv[0])

    mr = parser(
        lexicon = sys.argv[1],
        glossary = sys.argv[2]
    )

    script = mr.read(sys.argv[3])

    for text, terms in script:
        mr.parse(text, terms)
