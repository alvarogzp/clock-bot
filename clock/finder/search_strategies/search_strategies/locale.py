import babel
from babel import Locale

from clock.finder.search_strategies.strategy import SearchStrategy
from clock.finder.zone_finder.zone_finders.country import CountryZoneFinder


DEFAULT_COUNTRY_CODE = "US"


class LocaleSearchStrategy(SearchStrategy):
    def __init__(self, locale: Locale, country_zone_finder: CountryZoneFinder):
        self.locale = locale
        self.country_zone_finder = country_zone_finder
        self.results = []

    def search(self):
        self.country_search()

    def country_search(self):
        country_code = self._get_country_code()
        results = self.country_zone_finder.get_country_zones(country_code)
        self.results.extend(results)

    def _get_country_code(self):
        # try to get the territory from the locale
        country_code = self.locale.territory
        if country_code is None:
            # locale does not have territory info
            # try to get a territory from the language-only locale
            country_code = self.__get_territory_from_language_only_locale()
        if country_code is None:
            # if still none, use default country code
            country_code = DEFAULT_COUNTRY_CODE
        return country_code

    def __get_territory_from_language_only_locale(self):
        # try to get a territory specific locale (eg. "es_ES") from a language-only locale (eg. "es")
        locale_with_territory = Locale.negotiate([str(self.locale)], babel.core.LOCALE_ALIASES.values())
        if locale_with_territory:
            return locale_with_territory.territory

    def get_results(self):
        return self.results
