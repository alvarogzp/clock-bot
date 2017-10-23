from clock.finder.search_strategies.search_strategies.query.match import MatchSearchStrategy
from clock.finder.zone_finder.zone_finders.localized_date_time import LocalizedDateTimeZoneFinder


class AdvancedMatchSearchStrategy(MatchSearchStrategy):
    def __init__(self, query_lower: str, localized_date_time_zone_finder: LocalizedDateTimeZoneFinder):
        super().__init__(query_lower)
        self.localized_date_time_zone_finder = localized_date_time_zone_finder

    def search(self):
        raise NotImplementedError()
