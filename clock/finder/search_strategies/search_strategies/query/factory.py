from clock.finder.search_strategies.search_strategies.query.generic import GenericQuerySearchStrategy
from clock.finder.zone_finder.zone_finders.country import CountryZoneFinder


class QuerySearchStrategyFactory:
    def __init__(self, query_lower: str):
        self.query_lower = query_lower

    def country(self, country_zone_finder: CountryZoneFinder):
        return self._create(country_zone_finder.get_country_zones)

    def _create(self, func: callable):
        return GenericQuerySearchStrategy(self.query_lower, func)
