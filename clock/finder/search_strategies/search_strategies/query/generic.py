from clock.finder.search_strategies.search_strategies.query import QuerySearchStrategy


class GenericQuerySearchStrategy(QuerySearchStrategy):
    def __init__(self, query_lower: str, search_func: callable):
        super().__init__(query_lower)
        self.search_func = search_func

    def search(self):
        self.generic_search()

    def generic_search(self):
        results = self.search_func(self.query_lower)
        self._add_results(results)
