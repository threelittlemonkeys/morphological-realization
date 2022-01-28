import re
import sys

LOGGER_STREAM = sys.stderr

ERR_INVALID_SYNTAX = "invalid syntax at %s line %d"
ERR_UNKNOWN_FEATURE = "unknown feature '%s'"
ERR_SURFACE_FORM_NOT_FOUND = "surface form not found for '%s' %s"

LANGS = {"de", "en", "es", "fr", "ja", "ko", "pl", "ru", "zh"}

RE_TERM_NODE = re.compile("^\{([0-9]*):([0-9]+|\*)_([^}]+)\}$")

RE_TERM = re.compile("\{([0-9]*)(:[0-9]+)?((?::[a-z]+)*)\}")
RE_WORD = re.compile("\{_([^}]+)\}")

A_DICT = { # attribute to value
    "cat": ["adj", "noun"],
    "gend": ["m", "f", "n"],
    "num": ["sg", "pl"],
    "case": ["nom", "acc", "gen", "dat"],
    "anim": ["anim"]
}

V_DICT = {v: a for a, vs in A_DICT.items() for v in vs}
