import sys
import re

def enum(xs):
    return {x: i for i, x in enumerate(xs)}

def ftoi(fs, fmap): # feature to int
    try:
        f = fs.intersection(fmap.keys())
        return fmap[next(iter(f))]
    except:
        return -1

def _criterion(args):
    lang, lemma, feats, word = args
    feats = set(feats.split(":"))

    cat = ftoi(feats, cat_to_idx)
    gend = ftoi(feats, gend_to_idx)
    num = ftoi(feats, num_to_idx)
    case = ftoi(feats, case_to_idx)

    return (lang[:2], lemma, cat, gend, num, case, len(feats))

cats = ("adj", "noun")
gends = ("m", "f", "n", "c")
nums = ("sg", "pl")
cases = ("nom", "acc", "gen", "dat", "inst", "prep")

cat_to_idx = enum(cats)
gend_to_idx = enum(gends)
num_to_idx = enum(nums)
case_to_idx = enum(cases)

lines = dict()

for line in sys.stdin:
    line = re.sub("\s+", " ", line).strip()
    args, cmt = re.search("^([^#]*)(.*)", line).groups()
    if not args:
        continue
    args = args.split(" ")
    if len(args) == 3:
        args.append("")
    args = tuple(args)
    if args in lines:
        print("<", (*args, lines[args]), file = sys.stderr)
        print(">", (*args, cmt), file = sys.stderr)
    lines[args] = cmt

for args in sorted(lines, key = _criterion):
    cmt = lines[args]
    print(*args, cmt)
