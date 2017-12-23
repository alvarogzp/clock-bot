from clock.finder.search_strategies.search_strategies.query.match import MatchSearchStrategy


class GenericMatchSearchStrategy(MatchSearchStrategy):
    def __init__(self, query_lower: str, match_func: callable):
        super().__init__(query_lower)
        self.match_func = match_func

    def search(self):
        self.generic_search()

    def generic_search(self):
        results = self.match_func(self.query_lower)
        self._add_results(results)
