from clock.finder.query.query import SearchQuery


QUERY_PARAM_LANG = "lang:"


class SearchQueryParser:
    def __init__(self, query: str):
        self.query = query
        self.query_lower = ""
        self.param_lang = None

    def parse(self):
        query_lower_words = []
        for word in self.query.split(" "):
            is_param = self._check_params(word)
            if not is_param:
                query_lower_words.append(word.lower())
        self.query_lower = " ".join(query_lower_words)

    def _check_params(self, word: str):
        param_found = False
        lang = self._check_param(word, QUERY_PARAM_LANG)
        if lang is not None:
            param_found = True
            self.param_lang = lang
        return param_found

    @staticmethod
    def _check_param(word: str, param: str):
        if word.lower().startswith(param):
            return word[len(param):]
        return None

    def parsed_query(self):
        return SearchQuery(self.query_lower, self.param_lang)
