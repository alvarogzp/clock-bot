from babel import Locale

from clock.domain.time import TimePoint
from clock.finder.query.query import SearchQuery
from clock.finder.search_strategies.search_strategies.concatenator import SearchStrategyConcatenator
from clock.finder.search_strategies.search_strategies.locale import LocaleSearchStrategy
from clock.finder.search_strategies.search_strategies.query.basic import BasicQuerySearchStrategy
from clock.finder.search_strategies.search_strategies.query.match.concatenator import MatchSearchStrategyConcatenator
from clock.finder.search_strategies.search_strategies.query.match.factory import MatchSearchStrategyFactory
from clock.finder.zone_finder.provider import ZoneFindersProvider
from clock.locale.parser import DEFAULT_LOCALE


ADVANCED_SEARCH_TIME_PREFIX = "-time"
ADVANCED_SEARCH_GMT_OFFSET_PREFIX = "-gmt"
ADVANCED_SEARCH_TZNAME_PREFIX = "-tzname"

ADVANCED_SEARCH_PREFIXES = [
    ADVANCED_SEARCH_TIME_PREFIX,
    ADVANCED_SEARCH_GMT_OFFSET_PREFIX,
    ADVANCED_SEARCH_TZNAME_PREFIX
]


class SearchStrategyFactory:
    def __init__(self, finders: ZoneFindersProvider):
        self.finders = finders

    def get(self, query: SearchQuery, locale: Locale, time_point: TimePoint):
        return SearchStrategyBuilder(self.finders, query, locale, time_point).build()


class SearchStrategyBuilder:
    def __init__(self, finders: ZoneFindersProvider, query: SearchQuery, locale: Locale, time_point: TimePoint):
        self.finders = finders
        self.query = query.copy()
        self.locale = locale
        self.time_point = time_point
        self.match_strategy_factory = MatchSearchStrategyFactory(self.query)

    @property
    def query_lower(self):
        return self.query.query_lower

    @query_lower.setter
    def query_lower(self, new_query_lower: str):
        self.query.query_lower = new_query_lower

    def build(self):
        if self.query.is_empty():
            return self.build_locale_search()
        strategy = self.build_advanced_search()
        if strategy is None:
            strategy = self.build_basic_search()
        return strategy

    def build_advanced_search(self):
        query_words = self.query_lower.split()
        if len(query_words) > 1:
            advanced_search_type = query_words[0]
            if advanced_search_type in ADVANCED_SEARCH_PREFIXES:
                self.query_lower = " ".join(query_words[1:])
                if advanced_search_type == ADVANCED_SEARCH_TIME_PREFIX:
                    return self.build_time_match_search()
                elif advanced_search_type == ADVANCED_SEARCH_GMT_OFFSET_PREFIX:
                    return self.build_gmt_offset_match_search()
                elif advanced_search_type == ADVANCED_SEARCH_TZNAME_PREFIX:
                    return self.build_tzname_match_search()
                else:
                    raise AssertionError("advanced search of unexpected type")

    def build_locale_search(self):
        return LocaleSearchStrategy(self.locale, self.finders.country_zone_finder)

    def build_basic_search(self):
        return SearchStrategyConcatenator(
            BasicQuerySearchStrategy(
                self.query_lower,
                self.finders.name_zone_finder,
                self.finders.country_zone_finder
            ),
            MatchSearchStrategyConcatenator(
                self.match_strategy_factory.zone_name(self.finders.name_zone_finder),
                self.match_strategy_factory.localized_names(self._localized_zone_finder()),
                self.match_strategy_factory.localized_names(self._default_localized_zone_finder())
            )
        )

    def build_time_match_search(self):
        return self.match_strategy_factory.time(self._localized_date_time_zone_finder())

    def build_gmt_offset_match_search(self):
        return self.match_strategy_factory.gmt_offset(self._localized_date_time_zone_finder())

    def build_tzname_match_search(self):
        return self.match_strategy_factory.tzname(self._localized_date_time_zone_finder())

    def _localized_zone_finder(self):
        return self.finders.localized_zone_finder(self.locale)

    def _default_localized_zone_finder(self):
        return self.finders.localized_zone_finder(DEFAULT_LOCALE)

    def _localized_date_time_zone_finder(self):
        return self.finders.localized_date_time_zone_finder(self.locale, self.time_point)
