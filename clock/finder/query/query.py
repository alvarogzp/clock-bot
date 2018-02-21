import copy

from clock.finder.query.params import QUERY_PARAM_LANG


class SearchQueryParam:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    @property
    def value_lower(self):
        return self.value.lower()


class SearchQuery:
    def __init__(self, query_lower: str, params: dict):
        self.query_lower = query_lower
        self.params = params

    @property
    def lang(self):
        return self.get_param(QUERY_PARAM_LANG)

    def get_param(self, param: str):
        return self.params.get(param)

    def is_empty(self):
        return not self.has_basic_query() and \
               (len(self.params) == 0 or (len(self.params) == 1 and self.lang is not None))

    def has_basic_query(self):
        return len(self.query_lower) > 0

    def copy(self):
        return copy.copy(self)
