import babel
from babel import Locale


class Territory:
    @classmethod
    def with_territory(cls, locale: Locale):
        """Ensure locale has territory (if possible)"""
        if not locale.territory:
            locale = cls._find_locale_with_territory_from_language_only_locale(locale) or locale
        return locale

    @staticmethod
    def _find_locale_with_territory_from_language_only_locale(locale: Locale):
        # try to get a territory specific locale (eg. "es_ES") from a language-only locale (eg. "es")
        locale_with_territory = Locale.negotiate([str(locale)], babel.core.LOCALE_ALIASES.values())
        if locale_with_territory:
            return locale_with_territory
