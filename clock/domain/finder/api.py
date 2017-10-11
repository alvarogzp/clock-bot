from collections import OrderedDict

from babel import Locale

from clock.domain.finder.search_strategies.search_strategies.locale import LocaleSearchStrategy
from clock.domain.finder.search_strategies.search_strategies.query import QuerySearchStrategy
from clock.domain.finder.zone_finder.provider import ZoneFindersProvider
from clock.domain.time import TimePoint


class ZoneFinderApi:
    finders = ZoneFindersProvider()

    @classmethod
    def find(cls, query: str, locale: Locale, time_point: TimePoint):
        search_strategy = cls.__get_search_strategy(query, locale, time_point)
        search_strategy.search()
        return cls.__removed_duplicates(search_strategy.get_results())

    @classmethod
    def __get_search_strategy(cls, query: str, locale: Locale, time_point: TimePoint):
        if query:
            return QuerySearchStrategy(cls.finders, locale, query.lower(), time_point)
        else:
            return LocaleSearchStrategy(cls.finders, locale)

    @staticmethod
    def __removed_duplicates(results):
        return list(OrderedDict.fromkeys(results))
