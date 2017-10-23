from clock.finder.search_strategies.search_strategies.query.match import MatchSearchStrategy
from clock.finder.zone_finder.zone_finders.localized import LocalizedZoneFinder
from clock.finder.zone_finder.zone_finders.name import NameZoneFinder


class BasicMatchSearchStrategy(MatchSearchStrategy):
    def __init__(self, query_lower: str, name_zone_finder: NameZoneFinder, localized_zone_finder: LocalizedZoneFinder):
        super().__init__(query_lower)
        self.name_zone_finder = name_zone_finder
        self.localized_zone_finder = localized_zone_finder

    def search(self):
        self.zone_name_search()
        self.localized_names_search()

    def zone_name_search(self):
        results = self.name_zone_finder.match_lower(self.query_lower)
        self._add_results(results)

    def localized_names_search(self):
        results = self.localized_zone_finder.match_names_lower(self.query_lower)
        self._add_results(results)
