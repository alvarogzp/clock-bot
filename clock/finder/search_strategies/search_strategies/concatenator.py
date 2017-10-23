import itertools

from clock.finder.search_strategies.strategy import SearchStrategy


class SearchStrategyConcatenator(SearchStrategy):
    def __init__(self, *search_strategies: SearchStrategy):
        self.search_strategies = search_strategies

    def search(self):
        for search_strategy in self.search_strategies:
            search_strategy.search()

    def get_results(self):
        return itertools.chain.from_iterable((strategy.get_results() for strategy in self.search_strategies))
