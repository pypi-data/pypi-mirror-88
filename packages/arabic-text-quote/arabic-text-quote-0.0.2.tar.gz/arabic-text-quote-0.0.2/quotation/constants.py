import re
K = 3
WORDS = re.compile(r'\w', re.UNICODE)
NON_WORDS = re.compile(r'\W', re.UNICODE)
WORDS_SPLIT = re.compile(r'\S+|\s+', re.UNICODE)
ARABIC_CHARACTER = re.compile('[^\u0621-\u064a|\\s+]')
ALEF_MADDA = u'\u0671'
ALEF_SUPERSCRIPT = u'\u0670'
CHARACTER_ONE_LENGTH = re.compile(r'\b\w\b')
