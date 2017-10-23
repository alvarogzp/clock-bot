from clock.finder.search_strategies.strategy import SearchStrategy


class QuerySearchStrategy(SearchStrategy):
    def __init__(self, query_lower: str):
        self.query_lower = query_lower
        self.results = []

    def search(self):
        raise NotImplementedError()

    def get_results(self):
        return self.results
