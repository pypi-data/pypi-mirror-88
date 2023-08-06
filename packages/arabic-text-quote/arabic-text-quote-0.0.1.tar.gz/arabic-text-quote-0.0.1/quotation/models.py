import ast
from . import utiles


class Match(object):
    @utiles.type_check
    def __init__(self, first_index: int, last_index: int, text: str,
                 sources: list) -> None:
        super().__init__()
        self.__first_index = first_index
        self.__last_index = last_index
        self.__text = text
        self.__sources = sources

    @property
    def firstIndex(self):
        return self.__first_index

    @firstIndex.setter
    @utiles.type_check
    def firstIndex(self, first_index: int):
        self.__first_index = first_index

    @property
    def lastIndex(self):
        return self.__last_index

    @lastIndex.setter
    @utiles.type_check
    def lastIndex(self, last_index: int):
        self.__last_index = last_index

    @property
    def text(self):
        return self.__text

    @text.setter
    @utiles.type_check
    def text(self, text: str):
        self.__text = text

    @property
    def sources(self):
        return self.__sources

    @sources.setter
    @utiles.type_check
    def sources(self, sources: list):
        self.__sources = sources

    def getLastWord(self):
        return self.__text.split()[-1]

    def __str__(self):
        return f'Match = [text = {self.__text}]'

    def __repr__(self):
        return self.__str__()


class Result(object):
    @utiles.type_check
    def __init__(self, pk: str, text: str, name: str, type: str, extra_value: str) -> None:
        super().__init__()
        self.__pk = pk
        self.__text = text
        self.__subtext = text
        self.__subtext = ''
        self.__name = name
        self.__type = type
        self.__extra_value = ast.literal_eval(extra_value)

    @property
    def text(self):
        return self.__text

    @text.setter
    @utiles.type_check
    def text(self, text: str):
        self.__text = text

    @property
    def subtext(self):
        return self.__subtext

    @subtext.setter
    @utiles.type_check
    def subtext(self, subtext: str):
        self.__subtext = subtext

    @property
    def name(self):
        return self.__name

    @name.setter
    @utiles.type_check
    def name(self, name: str):
        self.__name = name

    @property
    def type(self):
        return self.__type

    @type.setter
    @utiles.type_check
    def type(self, type: str):
        self.__type = type

    @property
    def extra_value(self):
        return self.__extra_value

    @extra_value.setter
    @utiles.type_check
    def extra_value(self, extra_value: str):
        self.__extra_value = ast.literal_eval(extra_value)

    def __str__(self):
        return f"Result [text={self.__text}, subtext={self.__subtext}, typ={self.__type}, extra_data={self.__extra_value} ]"

    def __repr__(self):
        return self.__str__()
