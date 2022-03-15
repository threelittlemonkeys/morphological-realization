import re
import sys

LOG_FILE_STREAM = sys.stderr

ERR_INVALID_SYNTAX = "invalid syntax at %s line %d"
ERR_UNKNOWN_FEATURE = "unknown feature '%s'"
ERR_ATTRIBUTE_ALREADY_EXISTS = "attribute '%s' already exists"
ERR_LANGUAGE_NOT_FOUND = "language '%s' not found"
ERR_LEMMA_NOT_FOUND = "lemma '%s' not found"
ERR_SURFACE_FORM_NOT_FOUND = "surface form of '%s %s' not found"

LANGS = {"de", "en", "es", "fr", "ja", "ko", "pl", "ru", "zh"}

RE_NODE = re.compile("^\{([0-9]*):([0-9]+|\*)_([^}]+)\}$")
RE_TERM = re.compile("\{([0-9]*)(?::([0-9]+))?((?::[a-z]+)*)\}")
RE_WORD = re.compile("\{_([^}]+)\}")
