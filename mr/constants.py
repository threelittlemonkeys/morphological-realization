import re
import sys

LOGGER_STREAM = sys.stderr

ERR_INVALID_SYNTAX = "invalid syntax at %s %d"
ERR_UNKNOWN_FEATURE = "unknown feature '%s'"

LANGS = {"de", "en", "es", "fr", "ko", "ru"}

RE_GLOSSARY_TOKEN = re.compile("^\{([0-9]*):([0-9]+|\*)_([^}]+)\}$")

RE_SCRIPT_TOKEN_A = re.compile("\{([0-9]*)(:[0-9]+)?((:[a-z]+)*)\}")
RE_SCRIPT_TOKEN_B = re.compile("\{_([^}]+)\}")
