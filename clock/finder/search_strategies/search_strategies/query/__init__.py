from babel import Locale

from clock.domain.time import TimePoint
from clock.finder.search_strategies.search_strategies.query.match import MatchSearchStrategy
from clock.finder.search_strategies.strategy import SearchStrategy
from clock.finder.zone_finder.provider import ZoneFindersProvider


class QuerySearchStrategy(SearchStrategy):
    def __init__(self, finders: ZoneFindersProvider, locale: Locale, query_lower: str, time_point: TimePoint):
        self.finders = finders
        self.locale = locale
        self.query_lower = query_lower
        self.time_point = time_point
        self.results = []

    def search(self):
        # now inexact search
        # if len(self.query_lower) > 2:
        self.match_search()

    def match_search(self):
        match_search_strategy = MatchSearchStrategy(self.finders, self.locale, self.query_lower, self.time_point)
        match_search_strategy.search()
        self.results.extend(match_search_strategy.get_results())

    def get_results(self):
        return self.results
