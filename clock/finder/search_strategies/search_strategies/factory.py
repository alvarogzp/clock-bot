from babel import Locale

from clock.domain.time import TimePoint
from clock.finder.query.params import QUERY_PARAM_TIME, QUERY_PARAM_GMT, QUERY_PARAM_TZNAME
from clock.finder.query.query import SearchQuery, SearchQueryParam
from clock.finder.search_strategies.search_strategies.concatenator import AndSearchStrategyConcatenator, \
    OrSearchStrategyConcatenator
from clock.finder.search_strategies.search_strategies.locale import LocaleSearchStrategy
from clock.finder.search_strategies.search_strategies.query.basic import BasicQuerySearchStrategy
from clock.finder.search_strategies.search_strategies.query.factory import QuerySearchStrategyFactory
from clock.finder.search_strategies.search_strategies.query.match.concatenator import MatchSearchStrategyConcatenator
from clock.finder.search_strategies.search_strategies.query.match.factory import MatchSearchStrategyFactory
from clock.finder.zone_finder.provider import ZoneFindersProvider
from clock.locale.parser import DEFAULT_LOCALE


class SearchStrategyFactory:
    def __init__(self, finders: ZoneFindersProvider):
        self.finders = finders

    def get(self, query: SearchQuery, locale: Locale, time_point: TimePoint):
        return SearchStrategyBuilder(self.finders, query, locale, time_point).build()


class SearchStrategyBuilder:
    def __init__(self, finders: ZoneFindersProvider, query: SearchQuery, locale: Locale, time_point: TimePoint):
        self.finders = finders
        self.query = query
        self.locale = locale
        self.time_point = time_point
        self.match_strategy_factory_for_query = self._match_strategy_factory_for_query()

    @property
    def query_lower(self):
        return self.query.query_lower

    def build(self):
        if self.query.is_empty():
            return self.build_locale_search()
        strategies = self.build_advanced_search()
        if self.query.has_query_string():
            strategies.append(self.build_basic_search())
        return AndSearchStrategyConcatenator(*strategies)

    def build_advanced_search(self):
        strategies = []
        for param in self.query.params:
            name = param.name
            if name == QUERY_PARAM_TIME:
                strategies.append(self.build_time_match_search(param))
            elif name == QUERY_PARAM_GMT:
                strategies.append(self.build_gmt_offset_match_search(param))
            elif name == QUERY_PARAM_TZNAME:
                strategies.append(self.build_tzname_match_search(param))
        return strategies

    def build_locale_search(self):
        return LocaleSearchStrategy(self.locale, self.finders.country_zone_finder)

    def build_basic_search(self):
        return OrSearchStrategyConcatenator(
            BasicQuerySearchStrategy(
                self.query_lower,
                self.finders.name_zone_finder,
                self.finders.country_zone_finder
            ),
            MatchSearchStrategyConcatenator(
                self.match_strategy_factory_for_query.zone_name(self.finders.name_zone_finder),
                self.match_strategy_factory_for_query.localized_names(self._localized_zone_finder()),
                self.match_strategy_factory_for_query.localized_names(self._default_localized_zone_finder())
            )
        )

    # specific search strategies builder methods

    def build_time_match_search(self, param: SearchQueryParam):
        return self._match_strategy_factory_for_param(param).time(self._localized_date_time_zone_finder())

    def build_gmt_offset_match_search(self, param: SearchQueryParam):
        return self._match_strategy_factory_for_param(param).gmt_offset(self._localized_date_time_zone_finder())

    def build_tzname_match_search(self, param: SearchQueryParam):
        return self._match_strategy_factory_for_param(param).tzname(self._localized_date_time_zone_finder())

    # finder retriever methods

    def _localized_zone_finder(self):
        return self.finders.localized_zone_finder(self.locale)

    def _default_localized_zone_finder(self):
        return self.finders.localized_zone_finder(DEFAULT_LOCALE)

    def _localized_date_time_zone_finder(self):
        return self.finders.localized_date_time_zone_finder(self.locale, self.time_point)

    # MatchSearchStrategyFactory helper methods

    def _match_strategy_factory_for_param(self, param: SearchQueryParam):
        return self._match_strategy_factory(param.value_lower)

    def _match_strategy_factory_for_query(self):
        return self._match_strategy_factory(self.query_lower)

    @staticmethod
    def _match_strategy_factory(query_lower: str):
        return MatchSearchStrategyFactory(query_lower)

    # QuerySearchStrategyFactory helper methods

    def _query_strategy_factory_for_param(self, param: SearchQueryParam):
        return self._query_strategy_factory(param.value_lower)

    def _query_strategy_factory_for_query(self):
        return self._query_strategy_factory(self.query_lower)

    @staticmethod
    def _query_strategy_factory(query_lower: str):
        return QuerySearchStrategyFactory(query_lower)
