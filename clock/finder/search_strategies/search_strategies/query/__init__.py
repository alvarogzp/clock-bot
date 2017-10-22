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
        # first zone name exact match
        self.zone_name_search()
        # then country code exact match
        self.country_code_search()
        # now inexact search
        # if len(self.query_lower) > 2:
        self.match_search()

    def zone_name_search(self):
        zone = self.finders.name_zone_finder.get_lower(self.query_lower)
        if zone is not None:
            self.results.append(zone)

    def country_code_search(self):
        results = self.finders.country_zone_finder.get_country_zones(self.query_lower)
        self.results.extend(results)

    def match_search(self):
        match_search_strategy = MatchSearchStrategy(self.finders, self.locale, self.query_lower, self.time_point)
        match_search_strategy.search()
        self.results.extend(match_search_strategy.get_results())

    def get_results(self):
        return self.results
