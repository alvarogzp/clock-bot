from babel import Locale

from clock.locale.territory import Territory


DEFAULT_COUNTRY_CODE = "US"


class CountryCode:
    @classmethod
    def from_locale(cls, locale: Locale):
        # ensure locale has territory (if possible)
        locale = Territory.with_territory(locale)
        # try to get the territory from the locale
        country_code = locale.territory
        if country_code is None:
            # locale does not have territory info
            # use default country code
            country_code = DEFAULT_COUNTRY_CODE
        return country_code
