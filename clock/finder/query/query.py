import copy
from typing import List

from clock.finder.query.params import QUERY_PARAM_LANG, RESULT_PARAMS


class SearchQueryParam:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    @property
    def value_lower(self):
        return self.value.lower()


class SearchQueryParamList:
    def __init__(self, params: List[SearchQueryParam]):
        self.params = params

    def __iter__(self):
        return self.params.__iter__()

    def get(self, param: str):
        return self._get_last(param)

    def _get_last(self, param_name: str):
        value = None
        for param in self:
            if param.name == param_name:
                value = param.value
        return value

    def has_result_params(self):
        """
        A result param is one that produces results on its own (like advanced search params),
        in contrast to query modifier params (like lang param).
        """
        for param in self:
            if param.name in RESULT_PARAMS:
                return True
        return False


class SearchQuery:
    def __init__(self, query_lower: str, params: SearchQueryParamList):
        self.query_lower = query_lower
        self.params = params

    @property
    def lang(self):
        return self.params.get(QUERY_PARAM_LANG)

    def is_empty(self):
        return not self.has_query_string() and not self.params.has_result_params()

    def has_query_string(self):
        return len(self.query_lower) > 0

    def copy(self):
        return copy.copy(self)
