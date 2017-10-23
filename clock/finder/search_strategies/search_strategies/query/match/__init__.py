import itertools

from clock.finder.search_strategies.search_strategies.query import QuerySearchStrategy


class MatchSearchStrategy(QuerySearchStrategy):
    def __init__(self, query_lower: str):
        super().__init__(query_lower)
        self.prioritized_results = [[] for _ in range(3)]

    def search(self):
        raise NotImplementedError()

    def _add_results(self, results):
        for prioritized_result_list, result_list in zip(self.prioritized_results, results):
            prioritized_result_list.extend(result_list)

    def get_results(self):
        return itertools.chain.from_iterable(self.prioritized_results)

    def get_prioritized_results(self):
        return self.prioritized_results
