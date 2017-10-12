from babel import Locale

from clock.finder.search_strategies.strategy import SearchStrategy
from clock.finder.zone_finder.provider import ZoneFindersProvider


class LocaleSearchStrategy(SearchStrategy):
    def __init__(self, finders: ZoneFindersProvider, locale: Locale):
        self.finders = finders
        self.locale = locale
        self.results = []

    def search(self):
        self.country_search()

    def country_search(self):
        country_code = self.locale.territory
        results = self.finders.country_zone_finder.get_country_zones(country_code)
        self.results.extend(results)

    def get_results(self):
        return self.results
