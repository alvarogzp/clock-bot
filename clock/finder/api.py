from collections import OrderedDict

from babel import Locale

from clock.domain.time import TimePoint
from clock.finder.search_strategies.search_strategies.root import RootSearchStrategy
from clock.finder.zone_finder.provider import ZoneFindersProvider


class ZoneFinderApi:
    finders = ZoneFindersProvider()

    @classmethod
    def find(cls, query: str, locale: Locale, time_point: TimePoint):
        search_strategy = cls.__get_search_strategy(query, locale, time_point)
        search_strategy.search()
        return cls.__removed_duplicates(search_strategy.get_results())

    @classmethod
    def __get_search_strategy(cls, query: str, locale: Locale, time_point: TimePoint):
        return RootSearchStrategy(cls.finders, locale, query, time_point)

    @staticmethod
    def __removed_duplicates(results):
        return list(OrderedDict.fromkeys(results))
