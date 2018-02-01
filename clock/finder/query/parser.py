from clock.finder.query.params import QUERY_PARAM_LANG
from clock.finder.query.query import SearchQuery


class SearchQueryParser:
    def __init__(self, query: str):
        self.query = query
        self.query_lower = ""
        self.param_lang = None

    def parse(self):
        query_lower_words = []
        for word in self.query.split(" "):
            word = SearchQueryWordParser(word)
            self._update_params(word)
            if not word.is_param:
                query_lower_words.append(word.lower)
        self.query_lower = " ".join(query_lower_words)

    def _update_params(self, word):
        """:type word: SearchQueryWordParser"""
        self.param_lang = word.get_param(QUERY_PARAM_LANG, self.param_lang)

    def parsed_query(self):
        return SearchQuery(self.query_lower, self.param_lang)

    @staticmethod
    def parsed(query: str):
        parser = SearchQueryParser(query)
        parser.parse()
        return parser.parsed_query()


class SearchQueryWordParser:
    def __init__(self, word: str):
        self.word = word
        self.word_lower = word.lower()
        self.is_param = False

    @property
    def lower(self):
        return self.word_lower

    def get_param(self, param: str, default_value):
        value = self._get_value(param)
        if value is None:
            return default_value
        self.is_param = True
        return value

    def _get_value(self, param: str):
        if self.word_lower.startswith(param):
            return self.word[len(param):]
        return None
