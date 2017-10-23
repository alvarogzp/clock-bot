from collections import OrderedDict

from babel import Locale

from clock.domain.time import TimePoint
from clock.finder.search_strategies.search_strategies.factory import SearchStrategyFactory
from clock.finder.zone_finder.provider import ZoneFindersProvider


class ZoneFinderApi:
    def __init__(self, find_countries: bool):
        finders = ZoneFindersProvider(find_countries)
        self.search_strategy_factory = SearchStrategyFactory(finders)

    def find(self, query: str, locale: Locale, time_point: TimePoint):
        search_strategy = self.__get_search_strategy(query, locale, time_point)
        search_strategy.search()
        return self.__removed_duplicates(search_strategy.get_results())

    def __get_search_strategy(self, query: str, locale: Locale, time_point: TimePoint):
        return self.search_strategy_factory.get(query, locale, time_point)

    @staticmethod
    def __removed_duplicates(results):
        return list(OrderedDict.fromkeys(results))
