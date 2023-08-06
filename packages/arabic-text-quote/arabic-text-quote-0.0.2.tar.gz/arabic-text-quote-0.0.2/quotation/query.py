from whoosh import scoring
from whoosh.qparser import QueryParser
from . import sanitize
from . import ngram
from . import constants
from . import indexr
from .models import Result
from .utiles import type_check


class Query(object):
    __text: str

    @type_check
    def __init__(self, text: str) -> None:
        super().__init__()
        self.__text = text
        self.__indexer = indexr.get_or_create_indexer()
        self.__search_attribute = indexr.get_search_attribute()
        self.__limit = 20
        self.__k = constants.K

    @property
    def text(self):
        return self.__text

    @text.setter
    @type_check
    def text(self, text: str):
        self.__text = text

    def __clear_text(self, text=None):
        text = self.text if not text else text
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
                sanitize.split_sentence
            ]
        )

    def __clear_list(self):
        return sanitize.processing(
            self.__clear_text(),
            [
                sanitize.keyword_tokenize,
                sanitize.clear
            ],
            text_type=list
        )

    def __sanitize(self):
        return ngram.winnowing(tokens=self.__clear_list(), k=self.__k)

    def search(self):
        matches = list()
        overlap = False
        ngrams = self.__sanitize()
        with self.__indexer.searcher(weighting=scoring.TF_IDF()) as s:
            qp = QueryParser(self.__search_attribute, schema=self.__indexer.schema)
            for index in range(len(ngrams)):
                new_gram = ngrams[index]
                if overlap is False:
                    all_result = self.__parse(s, qp, new_gram.text)
                    if bool(all_result) is not False:
                        new_gram.sources = self.__getResult(all_result)
                        matches.append(new_gram)
                        overlap = True
                else:
                    last_gram = matches[-1]
                    text = last_gram.text + " " + new_gram.getLastWord()
                    all_result = self.__parse(s, qp, text)
                    if bool(all_result) is not False:
                        last_gram.lastIndex = new_gram.lastIndex
                        last_gram.text = text
                        last_gram.sources = self.__getResult(all_result)
                    else:
                        index += self.__k - 1
                        overlap = False
        return self.__getMatches(matches)

    def __parse(self, s, qp, text):
        q = qp.parse(u'"%s"' % text)
        return list(s.search(q, limit=self.__limit))

    def __getResult(self, all_result):
        response = []
        for result in all_result:
            response.append(Result(**result))
        return response

    def __getMatches(self, all_matches):
        words_list = sanitize.processing(self.text, [sanitize.split_sentence])
        for match in all_matches:
            match.text = "".join(words_list[match.firstIndex: match.lastIndex])
        del words_list
        return all_matches
