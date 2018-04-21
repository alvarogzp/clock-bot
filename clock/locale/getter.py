from bot.api.domain import ApiObject

from clock.finder.query.query import SearchQuery
from clock.locale.parser import LocaleParser
from clock.util.cache import Cache


class LocaleGetter:
    instance = None

    @classmethod
    def getter(cls):
        if cls.instance is None:
            cls.instance = LocaleGetter()
        return cls.instance

    def __init__(self):
        self.cache = Cache()

    def get(self, language_code: str):
        return self.cache.get_or_generate(language_code, lambda: self._parse_locale(language_code))

    @staticmethod
    def _parse_locale(language_code: str):
        return LocaleParser.parse(language_code)

    @classmethod
    def from_language_code(cls, language_code: str):
        return cls.getter().get(language_code)

    @classmethod
    def from_user(cls, user: ApiObject):
        user_language_code = user.language_code
        return cls.from_language_code(user_language_code)


class LanguageCode:
    @classmethod
    def from_query_or_user(cls, query: SearchQuery, user: ApiObject):
        lang = query.lang
        if lang is not None:
            return lang
        return user.language_code
