import itertools

from babel import Locale

from clock.domain.time import TimePoint
from clock.finder.search_strategies.strategy import SearchStrategy
from clock.finder.zone_finder.provider import ZoneFindersProvider


class MatchSearchStrategy(SearchStrategy):
    def __init__(self, finders: ZoneFindersProvider, locale: Locale, query_lower: str, time_point: TimePoint):
        self.finders = finders
        self.locale = locale
        self.query_lower = query_lower
        self.time_point = time_point
        self.localized_date_time_zone_finder = self.finders.localized_date_time_zone_finder(self.locale, self.time_point)
        self.prioritized_results = [[] for _ in range(3)]

    def search(self):
        pass

    def __add_results(self, results):
        for prioritized_result_list, result_list in zip(self.prioritized_results, results):
            prioritized_result_list.extend(result_list)

    def get_results(self):
        return itertools.chain.from_iterable(self.prioritized_results)
