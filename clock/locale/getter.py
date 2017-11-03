from babel import Locale
from bot.api.domain import ApiObject


DEFAULT_LOCALE = Locale.parse("en_US")


class LocaleGetter:
    @staticmethod
    def from_user(user: ApiObject):
        user_locale_code = user.language_code
        try:
            locale = Locale.parse(user_locale_code, sep="-")
        except Exception:
            locale = None
        if locale is None:
            locale = DEFAULT_LOCALE
        return locale
