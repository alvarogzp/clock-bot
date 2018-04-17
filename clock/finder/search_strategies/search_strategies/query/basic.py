from clock.finder.search_strategies.search_strategies.query import QuerySearchStrategy
from clock.finder.zone_finder.zone_finders.name import NameZoneFinder


class BasicQuerySearchStrategy(QuerySearchStrategy):
    def __init__(self, query_lower: str, name_zone_finder: NameZoneFinder):
        super().__init__(query_lower)
        self.name_zone_finder = name_zone_finder

    def search(self):
        # do a zone name exact match
        self.zone_name_search()

    def zone_name_search(self):
        zone = self.name_zone_finder.get_lower(self.query_lower)
        if zone is not None:
            self._add_result(zone)
