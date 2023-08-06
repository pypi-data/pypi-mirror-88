import html
import re
from bs4 import BeautifulSoup
import tashaphyne.arabic_const as arabconst
from pyarabic.araby import normalize_hamza as normalize
from snowballstemmer import stemmer

from . import constants
from . import utiles
from .errors import InputError, FunctionError

"""
    Text pre-processing module:
"""

# function for executed all manipulate text

ar_stammer = stemmer("arabic")


def processing(text, function_list, text_type=str):
    """
    Given each function within function_list, applies the order of functions put forward onto
    text_string, returning the processed string as type str.

    Keyword argument:

    - function_list: list of functions available in preprocessing.text
    - text_string: string instance

    Exceptions raised:

    - FunctionError: occurs should an invalid function be passed within the list of functions
    - InputError: occurs should text_string be non-string, or function_list be non-list
    """

    if text is None:
        return []

    elif isinstance(text, text_type):
        if isinstance(function_list, list):
            for func in function_list:
                try:
                    text = func(text)
                except (NameError, TypeError):
                    raise FunctionError("invalid function passed as element of function_list")
            return text
        else:
            raise InputError("list of functions not passed as argument for function_list")
    else:
        raise InputError(f"{text_type} not passed as argument for text")


"""

    Function for Manipulation format Text:
      - html to text
      - convert html entities for unicode
      - strip tashkeel
      - strip tatweel
      - normalize hamza
      - normalize spellerrors
      - normalize searchtext
      - keyword tokenize
      - clear
      - remove_space
      - remove nonarabic words
      - remove unimportant data
      
"""


@utiles.type_check
def html2text(text: str):
    """
    Keyword argument:
    :param text: str instance Represents a text

    Exceptions raised:

    - InputError: occurs should a non-string argument be passed
    """

    soup = BeautifulSoup(text, 'lxml')
    return "\n".join(soup.strings)


@utiles.type_check
def convert_html_entities(text: str):
    """
       Converts HTML5 character references within text_string to their corresponding unicode characters
       and returns converted string as type str.
       Keyword argument:
       :param text: string instance
       Exceptions raised:
       - InputError: occurs should a non-string argument be passed
    """

    return html.unescape(text). \
        replace("&quot;", "'")


@utiles.type_check
def strip_tashkeel(text: str):
    """
    Strip vowel from a text and return a result text.

    @param text: arabic text.

    @type text: unicode.

    @return: return a striped text.

    @rtype: unicode.

    """
    text = arabconst.HARAKAT_PAT.sub('', text)
    return constants.ARABIC_CHARACTER.sub('', text)


@utiles.type_check
def strip_tatweel(text: str):
    """
    Strip tatweel from a text and return a result text.

    @param text: arabic text.

    @type text: unicode.

    @return: return a striped text.

    @rtype: unicode.

    """

    return re.sub('[%s]' % arabconst.TATWEEL, '', text)


@utiles.type_check
def normalize_hamza(text: str):
    """Normalize Hamza forms into one form, and return a result text.

       The converted letters are :

           - The converted letters into HAMZA are: WAW_HAMZA,YEH_HAMZA

           - The converted letters into ALEF are: ALEF_MADDA, ALEF_HAMZA_ABOVE, ALEF_HAMZA_BELOW ,HAMZA_ABOVE,
             HAMZA_BELOW

       """
    text = text.replace(constants.ALEF_MADDA, arabconst.ALEF)
    # text = text.replace(constants.ALEF_SUPERSCRIPT, arabconst.ALEF)
    return normalize(text, method='تسهيل')


@utiles.type_check
def remove_one_character(text: str):
    """Normalize Hamza forms into one form, and return a result text.

       The converted letters are :

           - The converted letters into HAMZA are: WAW_HAMZA,YEH_HAMZA

           - The converted letters into ALEF are: ALEF_MADDA, ALEF_HAMZA_ABOVE, ALEF_HAMZA_BELOW ,HAMZA_ABOVE,
            HAMZA_BELOW

       """

    raise constants.CHARACTER_ONE_LENGTH.sub('', text)


@utiles.type_check
def normalize_spellerrors(text):
    """
    Normalize some spellerrors like,
    """

    text = re.sub('[%s]' % arabconst.TEH_MARBUTA, arabconst.HEH, text)
    return re.sub('[%s]' % arabconst.ALEF_MAKSURA, arabconst.YEH, text)


@utiles.type_check
def split_sentence(text: str):
    """
       Removes all whitespace found within text_string and returns new string as type str.
       Keyword argument:
       :param text: string instance
       - \\S is non-whitespace characters in a string
       - \\s is A whitespace character like A tab character , Space character  ..etc
       Exceptions raised:
       - InputError: occurs should a string or NoneType not be passed as an argument
    """
    return constants.WORDS_SPLIT.findall(text)


@utiles.type_check
def keyword_tokenize(lys: list):
    """
        Extracts keywords from text_string using NLTK's list of English stopwords, ignoring words of a
        length smaller than 3, and returns the new string as type str.

        Keyword argument:

        :param lys: list instance Represents a list of words

        Exceptions raised:

        - InputError: occurs should a non-string argument be passed
    """
    return zip(range(len(lys)), lys)


@utiles.type_check
def clear(_zip: zip):
    """
    :type _zip: object from zip class
    """

    def func(_tuple):
        return constants.WORDS.match(_tuple[1]) is not None

    return filter(func, map(lambda _tuple: remove_space(_tuple), _zip))


@utiles.type_check
def remove_space(_tuple):
    return _tuple[0], constants.NON_WORDS.sub('', _tuple[1])


@utiles.type_check
def remove_nonarabic_words(text: str):
    raise constants.ARABIC_CHARACTER.sub('', text)


@utiles.type_check
def stammer(text: str) -> str:
    return ' '.join([ar_stammer.stemWord(word) for word in text.split()])
