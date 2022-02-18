import re
import sys

LOGGER_STREAM = sys.stderr

ERR_INVALID_SYNTAX = "invalid syntax at %s line %d"
ERR_UNKNOWN_FEATURE = "unknown feature '%s'"
ERR_LANGUAGE_NOT_FOUND = "language '%s' not found"
ERR_LEMMA_NOT_FOUND = "lemma '%s' not found"
ERR_SURFACE_FORM_NOT_FOUND = "surface form of '%s %s' not found"

LANGS = {"de", "en", "es", "fr", "ja", "ko", "pl", "ru", "zh"}

RE_NODE = re.compile("^\{([0-9]*):([0-9]+|\*)_([^}]+)\}$")
RE_TERM = re.compile("\{([0-9]*)(?::([0-9]+))?((?::[a-z]+)*)\}")
RE_WORD = re.compile("\{_([^}]+)\}")

# attribute to value
A_DICT = {
    "cat": ["adj", "noun"],
    "gend": ["m", "f", "n"],
    "num": ["sg", "pl"],
    "case": ["nom", "acc", "gen", "dat"],
    "anim": ["anim"]
}

# value to attribute
V_DICT = {v: a for a, vs in A_DICT.items() for v in vs}
