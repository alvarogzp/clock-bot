import babel
from babel import Locale


DEFAULT_COUNTRY_CODE = "US"


class CountryCode:
    @classmethod
    def from_locale(cls, locale: Locale):
        # try to get the territory from the locale
        country_code = locale.territory
        if country_code is None:
            # locale does not have territory info
            # try to get a territory from the language-only locale
            country_code = cls._find_from_language_only_locale(locale)
        if country_code is None:
            # if still none, use default country code
            country_code = DEFAULT_COUNTRY_CODE
        return country_code

    @staticmethod
    def _find_from_language_only_locale(locale: Locale):
        # try to get a territory specific locale (eg. "es_ES") from a language-only locale (eg. "es")
        locale_with_territory = Locale.negotiate([str(locale)], babel.core.LOCALE_ALIASES.values())
        if locale_with_territory:
            return locale_with_territory.territory
