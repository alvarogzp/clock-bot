from babel import Locale
from bot.api.domain import ApiObject

from clock.util.cache import Cache


DEFAULT_LOCALE = Locale.parse("en_US")


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
        self.cache.get_or_generate(language_code, lambda: self._parse_locale(language_code))

    @staticmethod
    def _parse_locale(language_code: str):
        try:
            locale = Locale.parse(language_code, sep="-")
        except Exception:
            locale = None
        if locale is None:
            locale = DEFAULT_LOCALE
        return locale

    @classmethod
    def from_language_code(cls, language_code: str):
        return cls.getter().get(language_code)

    @classmethod
    def from_user(cls, user: ApiObject):
        user_language_code = user.language_code
        return cls.from_language_code(user_language_code)
