from collections import OrderedDict

from babel import Locale

from clock.domain.time import TimePoint
from clock.finder.query.query import SearchQuery
from clock.finder.search_strategies.search_strategies.factory import SearchStrategyFactory
from clock.finder.zone_finder.provider import ZoneFindersProvider, LocalizedZoneFinderCache


class ZoneFinderApi:
    def __init__(self, find_countries: bool):
        self.finders = ZoneFindersProvider(find_countries)
        self.search_strategy_factory = SearchStrategyFactory(self.finders)
        self.locale_cache = ZoneFinderLocaleCache(self.finders.get_localized_zone_finder_cache())

    def find(self, query: SearchQuery, locale: Locale, time_point: TimePoint):
        search_strategy = self.__get_search_strategy(query, locale, time_point)
        search_strategy.search()
        return self.__removed_duplicates(search_strategy.get_results())

    def zones(self):
        return self.finders.zones

    def country_finder(self):
        return self.finders.country_zone_finder

    def cache(self):
        return self.locale_cache

    def __get_search_strategy(self, query: SearchQuery, locale: Locale, time_point: TimePoint):
        return self.search_strategy_factory.get(query, locale, time_point)

    @staticmethod
    def __removed_duplicates(results):
        return list(OrderedDict.fromkeys(results))


class ZoneFinderLocaleCache:
    def __init__(self, cache: LocalizedZoneFinderCache):
        self._cache = cache

    def cache(self, locale: Locale):
        self._cache.get_or_generate(locale)

    def cached_locales(self):
        return self._cache.cached_locales()

    def is_cached(self, locale: Locale):
        return self._cache.is_cached(locale)
