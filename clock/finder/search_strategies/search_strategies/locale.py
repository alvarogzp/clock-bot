from babel import Locale

from clock.finder.search_strategies.strategy import SearchStrategy
from clock.finder.zone_finder.zone_finders.country import CountryZoneFinder
from clock.locale.country_code import CountryCode


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
        return CountryCode.from_locale(self.locale)

    def get_results(self):
        return self.results
