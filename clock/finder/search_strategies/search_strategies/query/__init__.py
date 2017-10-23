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
        pass

    def get_results(self):
        return self.results
