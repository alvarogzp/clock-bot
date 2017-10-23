from babel import Locale

from clock.domain.time import TimePoint
from clock.finder.search_strategies.search_strategies.concatenator import SearchStrategyConcatenator
from clock.finder.search_strategies.search_strategies.locale import LocaleSearchStrategy
from clock.finder.search_strategies.search_strategies.query.basic import BasicQuerySearchStrategy
from clock.finder.search_strategies.search_strategies.query.match.advanced.gmt_offset import \
    GmtOffsetMatchSearchStrategy
from clock.finder.search_strategies.search_strategies.query.match.advanced.time import TimeMatchSearchStrategy
from clock.finder.search_strategies.search_strategies.query.match.advanced.tzname import TznameMatchSearchStrategy
from clock.finder.search_strategies.search_strategies.query.match.basic import BasicMatchSearchStrategy
from clock.finder.zone_finder.provider import ZoneFindersProvider


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

    def get(self, query: str, locale: Locale, time_point: TimePoint):
        return SearchStrategyBuilder(self.finders, query, locale, time_point).build()


class SearchStrategyBuilder:
    def __init__(self, finders: ZoneFindersProvider, query: str, locale: Locale, time_point: TimePoint):
        self.finders = finders
        self.query_lower = query.lower()
        self.locale = locale
        self.time_point = time_point

    def build(self):
        if not self.query_lower:
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

    def build_locale_search(self):
        return LocaleSearchStrategy(self.locale, self.finders.country_zone_finder)

    def build_basic_search(self):
        return SearchStrategyConcatenator(
            BasicQuerySearchStrategy(
                self.query_lower,
                self.finders.name_zone_finder,
                self.finders.country_zone_finder
            ),
            BasicMatchSearchStrategy(
                self.query_lower,
                self.finders.name_zone_finder,
                self.finders.localized_zone_finder(self.locale)
            )
        )

    def build_time_match_search(self):
        return TimeMatchSearchStrategy(
            self.query_lower,
            self._localized_date_time_zone_finder()
        )

    def build_gmt_offset_match_search(self):
        return GmtOffsetMatchSearchStrategy(
            self.query_lower,
            self._localized_date_time_zone_finder()
        )

    def build_tzname_match_search(self):
        return TznameMatchSearchStrategy(
            self.query_lower,
            self._localized_date_time_zone_finder()
        )

    def _localized_date_time_zone_finder(self):
        return self.finders.localized_date_time_zone_finder(self.locale, self.time_point)
