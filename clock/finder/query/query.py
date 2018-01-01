import copy


class SearchQuery:
    def __init__(self, query_lower: str, lang: str = None):
        self.query_lower = query_lower
        self.lang = lang

    def copy(self):
        return copy.copy(self)
