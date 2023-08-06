import json
import os
from os.path import dirname
from whoosh import index

from whoosh.fields import ID, TEXT, Schema

from .models import Quran, Hadith
from ..utiles import type_check

"""
    The schema specifies the fields of documents in an index.
    Each document can have multiple fields, such as name,
    content, url, date, etc.
    Some fields can be indexed, and some fields can be stored with the document
    so the field value is available in search results.
    Some fields will be both indexed and stored.
    The schema is the set of all possible fields in a document.
    Each individual document might only use a
    subset of the available fields in the schema.

"""


class Indexer(object):
    BASE_URL = os.path.join(dirname(dirname(os.path.abspath(__file__))))

    __INDEX__ = 'dataset'
    __SEARCH_ATTRIBUTE__ = 'ptext'

    def __init__(self) -> None:
        super().__init__()
        self.__pk = ID(stored=True)
        self.__text = TEXT(stored=True)
        self.__name = TEXT(stored=True)
        self.__ptext = TEXT()
        self.__type = TEXT(stored=True)
        self.__extra_value = TEXT(stored=True)

    def __getIndexerPath(self) -> str:
        return os.path.join(self.BASE_URL, self.__INDEX__)

    def __schema(self) -> Schema:
        return Schema(**self.__dict__)

    def getOrCreateIndex(self):
        path = self.__getIndexerPath()
        if not os.path.exists(path):
            os.mkdir(path)
            return index.create_in(path, schema=self.__schema())
        return index.open_dir(path)

    @property
    def __str__(self):
        return f'Indexer [path = {self.__getIndexerPath()}]'

    @property
    def __repr__(self):
        return self.__str__

    @property
    def __dict__(self):
        return {
            'pk': self.__pk, 'text': self.__text,
            'name': self.__name, 'ptext': self.__ptext,
            'type': self.__type, 'extra_value': self.__extra_value
        }


class Corpus(object):
    ERROR_MESSAGES = {
        'invalid_file': 'you must enter json file',
    }

    __TYPE__ = {0: 'source', 1: 'quran', 2: 'hadith'}

    @type_check
    def __init__(self, absolute_path: str, type: int = 0) -> None:
        super().__init__()
        self.__indexer = Indexer().getOrCreateIndex()
        self.__path = absolute_path
        self.__type = type

    @property
    def path(self):
        return self.__path

    @property
    def type(self):
        return self.__type

    @path.setter
    @type_check
    def path(self, path: str):
        self.__path = path

    @type.setter
    @type_check
    def type(self, type: int):
        self.__type = type

    def write(self):
        writer = self.__indexer.writer()
        files = [file for file in self.__getFiles()] if self.__isDirectory() else [self.path]
        for file in files:
            with open(file, encoding="utf8") as json_file:
                data = json.load(json_file)
                if self.__type == 0:
                    pass
                elif self.__type == 1:
                    for verse in self.__writeQuran(data):
                        __dict__ = verse.__dict__()
                        extra_data = __dict__.pop('extra_data', {})
                        print(__dict__)
                        writer.add_document(
                            **__dict__,
                            extra_value=extra_data.__repr__(),
                            type=self.__TYPE__[self.__type]
                        )
                elif self.__type == 2:
                    for hadith in self.__writeHadith(data):
                        __dict__ = hadith.__dict__()
                        extra_data = __dict__.pop('extra_data', {})
                        print(__dict__)
                        writer.add_document(
                            **__dict__,
                            extra_value=extra_data.__repr__(),
                            type=self.__TYPE__[self.__type]
                        )
        writer.commit()
        return 'Done'

    def __isDirectory(self):
        return os.path.isdir(self.path)

    def __getFiles(self):
        for entry in os.listdir(self.path):
            yield os.path.join(self.path, entry)

    def __read(self, file):
        if os.path.isfile(file) and file.endswith('.json'):
            with open(file, encoding="utf8") as json_file:
                return json.load(json_file)
        else:
            raise ValueError(self.ERROR_MESSAGES['invalid_file'])

    def __writeQuran(self, data):
        data.pop('juz', None)
        verses = data.pop('verse')
        for key, verse in verses.items():
            yield Quran(text=verse, **data, verse_number=int(key.split('_')[-1]))

    def __writeHadith(self, data):
        for section in data.get('sections'):
            for hadith in section.get('hadiths'):
                yield Hadith(
                    name=data['name'], text=hadith['text'],
                    type=data['type'], section_title=section['title'],
                    index=hadith['number']
                )
