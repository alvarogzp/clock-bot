import itertools
from collections import OrderedDict

from clock.finder.search_strategies.strategy import SearchStrategy


class SearchStrategyConcatenator(SearchStrategy):
    def __init__(self, *search_strategies: SearchStrategy):
        self.search_strategies = search_strategies

    def search(self):
        for search_strategy in self.search_strategies:
            search_strategy.search()

    def get_results(self):
        raise NotImplementedError()


class OrSearchStrategyConcatenator(SearchStrategyConcatenator):
    def get_results(self):
        return itertools.chain.from_iterable((strategy.get_results() for strategy in self.search_strategies))


class AndSearchStrategyConcatenator(SearchStrategyConcatenator):
    def get_results(self):
        if len(self.search_strategies) == 0:
            return ()
        results = self.search_strategies[0].get_results()
        results = list(OrderedDict.fromkeys(results))
        for search_strategy in self.search_strategies[1:]:
            search_strategy_results = search_strategy.get_results()
            for result in results[:]:
                if result not in search_strategy_results:
                    results.remove(result)
        return results
