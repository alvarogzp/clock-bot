from typing import Iterable

from clock.finder.search_strategies.strategy import SearchStrategy


class QuerySearchStrategy(SearchStrategy):
    def __init__(self, query_lower: str):
        super().__init__()
        self.query_lower = query_lower
        self.results = []

    def search(self):
        raise NotImplementedError()

    def _add_result(self, result):
        self.results.append(result)

    def _add_results(self, results: Iterable):
        self.results.extend(results)

    def get_results(self):
        return self.results
