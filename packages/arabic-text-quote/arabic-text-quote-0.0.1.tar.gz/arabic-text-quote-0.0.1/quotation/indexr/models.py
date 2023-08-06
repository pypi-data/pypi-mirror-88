import hashlib

from .. import sanitize
from ..utiles import type_check


class Source(object):
    @type_check
    def __init__(self, text: str, name: str, type: str) -> None:
        super().__init__()
        self.__text = text
        self.__name = name
        self.__type = type
        self.__ptext = self.__sanitize()
        self.__pk = self.__generate_pk()

    def __generate_pk(self):
        return hashlib.sha1(self.__name.encode()).hexdigest()

    @property
    def pk(self):
        return self.__pk

    @property
    def id(self):
        return self.__pk

    @id.setter
    @type_check
    def id(self, pk: int):
        self.__pk = pk

    @property
    def text(self):
        return self.__text

    @text.setter
    @type_check
    def text(self, text: str):
        self.__text = text
        self.__ptext = self.__sanitize()

    @property
    def name(self):
        return self.__name

    @name.setter
    @type_check
    def name(self, name: str):
        self.__name = name
        self.__pk = self.__generate_pk()

    @property
    def processed_text(self):
        return self.__ptext

    @property
    def type(self):
        return self.__type

    @type.setter
    @type_check
    def type(self, type: str):
        self.__type = type

    def __sanitize(self):
        return sanitize.processing(
            self.text,
            [
                sanitize.html2text,
                sanitize.convert_html_entities,
                sanitize.strip_tatweel,
                sanitize.normalize_hamza,
                sanitize.strip_tashkeel,
                sanitize.normalize_spellerrors,
                sanitize.stammer,
            ]
        )

    # def update_dict(self, extra_data):
    #     print(self.__dict__())
    #     return self.__dict__().update({'extra_data': extra_data})

    def __str__(self) -> str:
        return 'Source = [pk = {}, title = {},  text = {}]'.format(
            self.__pk,
            self.__name,
            self.__text
        )

    def __repr__(self) -> str:
        return self.__str__()

    def __dict__(self):
        return {
            'pk': self.__pk, 'text': self.__text, 'name': self.__name,
            'ptext': self.processed_text, 'extra_data': {}
        }


class Quran(Source):
    @type_check
    def __init__(
            self, text: str, name: str, type: str, index: str, page: str,
            nzool: str, sajdah: str, count: int, verse_number: int
    ) -> None:
        super().__init__(text, name, type)
        self.__index = index
        self.__page = page
        self.__nzool = nzool
        self.__sajdah = sajdah
        self.__count = count
        self.__verse_number = verse_number

    @property
    def index(self):
        return self.__index

    @index.setter
    @type_check
    def index(self, index: str):
        self.__index = index

    @property
    def page(self):
        return self.__page

    @page.setter
    @type_check
    def page(self, page: str):
        self.__page = page

    @property
    def nzool(self):
        return self.__nzool

    @nzool.setter
    @type_check
    def nzool(self, nzool: str):
        self.__nzool = nzool

    @property
    def sajdah(self):
        return self.__sajdah

    @sajdah.setter
    @type_check
    def sajdah(self, sajdah: str):
        self.__sajdah = sajdah

    @property
    def count(self):
        return self.__count

    @count.setter
    @type_check
    def count(self, count: int):
        self.__count = count

    @property
    def verse_number(self):
        return self.__verse_number

    @verse_number.setter
    @type_check
    def verse_number(self, verse_number: int):
        self.__verse_number = verse_number

    def __str__(self):
        return f'Quran[pk={self.pk}, text={self.text[:50]}, ptext={self.processed_text[:50]},' \
               f' name={self.name}]'

    def __dict__(self):
        data = super(Quran, self).__dict__()
        data['extra_data'] = dict(
            index=self.index, page=self.page, type=self.type,
            nzool=self.nzool, sajdah=self.sajdah, count=self.__count,
            verse_number=self.__verse_number
        )
        return data


class Hadith(Source):
    @type_check
    def __init__(
            self, text: str, name: str, type: str,
            section_title: str, index: int,
    ) -> None:
        super().__init__(text, name, type)
        self.__section_title = section_title
        self.__index = index

    @property
    def section_title(self):
        return self.__section_title

    @section_title.setter
    @type_check
    def section_title(self, title: str):
        self.__section_title = title

    @property
    def index(self):
        return self.__index

    @index.setter
    @type_check
    def index(self, index: str):
        self.__index = index

    def __str__(self):
        return f'Hadith[pk={self.pk}, text={self.text[:50]}, ptext={self.processed_text[:50]}, name={self.name}]'

    def __dict__(self):
        data = super(Hadith, self).__dict__()
        data['extra_data'] = dict(
            index=self.index, section_title=self.section_title
        )
        return data


class Poetry(Source):
    pass
