from clock.finder.query.params import QUERY_PARAM_TIME, QUERY_PARAM_GMT, QUERY_PARAM_TZNAME
from clock.finder.query.query import SearchQuery
from clock.finder.search_strategies.search_strategies.query.match.generic import GenericMatchSearchStrategy
from clock.finder.zone_finder.zone_finders.localized import LocalizedZoneFinder
from clock.finder.zone_finder.zone_finders.localized_date_time import LocalizedDateTimeZoneFinder
from clock.finder.zone_finder.zone_finders.name import NameZoneFinder


class MatchSearchStrategyFactory:
    def __init__(self, query: SearchQuery):
        self.query = query

    def zone_name(self, name_zone_finder: NameZoneFinder):
        return self._create(name_zone_finder.match_lower)

    def localized_names(self, localized_zone_finder: LocalizedZoneFinder):
        return self._create(localized_zone_finder.match_names_lower)

    def time(self, localized_date_time_zone_finder: LocalizedDateTimeZoneFinder):
        return self._create(localized_date_time_zone_finder.match_time_lower, QUERY_PARAM_TIME)

    def gmt_offset(self, localized_date_time_zone_finder: LocalizedDateTimeZoneFinder):
        return self._create(localized_date_time_zone_finder.match_gmt_lower, QUERY_PARAM_GMT)

    def tzname(self, localized_date_time_zone_finder: LocalizedDateTimeZoneFinder):
        return self._create(localized_date_time_zone_finder.match_tzname_lower, QUERY_PARAM_TZNAME)

    def _create(self, func: callable, param: str = None):
        if param is None:
            query = self.query.query_lower
        else:
            query = self.query.get_param(param).lower()
        return GenericMatchSearchStrategy(query, func)
