import re
import sys

LOGGER_STREAM = sys.stderr

ERR_INVALID_SYNTAX = "invalid syntax at %s %d"
ERR_UNKNOWN_FEATURE = "unknown feature '%s'"

LANGS = {"de", "en", "es", "fr", "ko", "ru"}

RE_TERM = re.compile("^\{([0-9]*):([0-9]+|\*)_([^}]+)\}$")

RE_PHRASE = re.compile("\{([0-9]*)(:[0-9]+)?((:[a-z]+)*)\}")
RE_WORD = re.compile("\{_([^}]+)\}")
