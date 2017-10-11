import itertools

from babel import Locale

from clock.domain.finder.search_strategies.strategy import SearchStrategy
from clock.domain.finder.zone_finder.provider import ZoneFindersProvider
from clock.domain.time import TimePoint


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


class MatchSearchStrategy(SearchStrategy):
    def __init__(self, finders: ZoneFindersProvider, locale: Locale, query_lower: str, time_point: TimePoint):
        self.finders = finders
        self.locale = locale
        self.query_lower = query_lower
        self.time_point = time_point
        self.localized_date_time_zone_finder = self.finders.localized_date_time_zone_finder(self.locale, self.time_point)
        self.prioritized_results = [[] for _ in range(3)]

    def search(self):
        self.zone_name_search()
        self.localized_names_search()
        self.tzname_search()
        self.gmt_search()
        self.time_search()

    def zone_name_search(self):
        results = self.finders.name_zone_finder.match_lower(self.query_lower)
        self.__add_results(results)

    def localized_names_search(self):
        results = self.finders.localized_zone_finder(self.locale).match_names_lower(self.query_lower)
        self.__add_results(results)

    def tzname_search(self):
        results = self.localized_date_time_zone_finder.match_tzname_lower(self.query_lower)
        self.__add_results(results)

    def gmt_search(self):
        results = self.localized_date_time_zone_finder.match_gmt_lower(self.query_lower)
        self.__add_results(results)

    def time_search(self):
        results = self.localized_date_time_zone_finder.match_time_lower(self.query_lower)
        self.__add_results(results)

    def __add_results(self, results):
        for prioritized_result_list, result_list in zip(self.prioritized_results, results):
            prioritized_result_list.extend(result_list)

    def get_results(self):
        return itertools.chain.from_iterable(self.prioritized_results)
