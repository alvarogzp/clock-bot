from clock.finder.search_strategies.search_strategies.query import QuerySearchStrategy
from clock.finder.zone_finder.zone_finders.country import CountryZoneFinder
from clock.finder.zone_finder.zone_finders.name import NameZoneFinder


class BasicQuerySearchStrategy(QuerySearchStrategy):
    def __init__(self, query_lower: str, name_zone_finder: NameZoneFinder, country_zone_finder: CountryZoneFinder):
        super().__init__(query_lower)
        self.name_zone_finder = name_zone_finder
        self.country_zone_finder = country_zone_finder

    def search(self):
        # first zone name exact match
        self.zone_name_search()
        # then country code exact match
        self.country_code_search()

    def zone_name_search(self):
        zone = self.name_zone_finder.get_lower(self.query_lower)
        if zone is not None:
            self._add_result(zone)

    def country_code_search(self):
        results = self.country_zone_finder.get_country_zones(self.query_lower)
        self._add_results(results)
