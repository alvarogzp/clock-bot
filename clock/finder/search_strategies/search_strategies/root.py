from babel import Locale

from clock.domain.time import TimePoint
from clock.finder.search_strategies.search_strategies.query import QuerySearchStrategy
from clock.finder.search_strategies.search_strategies.locale import LocaleSearchStrategy
from clock.finder.search_strategies.strategy import SearchStrategy
from clock.finder.zone_finder.provider import ZoneFindersProvider


class RootSearchStrategy(SearchStrategy):
    def __init__(self, finders: ZoneFindersProvider, locale: Locale, query: str, time_point: TimePoint):
        self.finders = finders
        self.locale = locale
        self.query = query
        self.time_point = time_point
        self.results = []

    def search(self):
        if self.query:
            self.query_search()
        else:
            self.locale_search()

    def query_search(self):
        strategy = QuerySearchStrategy(self.finders, self.locale, self.query.lower(), self.time_point)
        strategy.search()
        self.results.extend(strategy.get_results())

    def locale_search(self):
        strategy = LocaleSearchStrategy(self.finders, self.locale)
        strategy.search()
        self.results.extend(strategy.get_results())

    def get_results(self):
        return self.results
