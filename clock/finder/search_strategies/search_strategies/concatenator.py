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
        if len(self.search_strategies) == 1:
            # quick path for simple searches
            return results
        results = self.__list_without_duplicates(results)
        for search_strategy in self.search_strategies[1:]:
            # we need a static list to check for presence of results in it
            search_strategy_results = list(search_strategy.get_results())
            for result in results[:]:  # iterate over a copy, as it will be modified
                if result not in search_strategy_results:
                    # if result is not present in all strategies' results, remove from returned results
                    results.remove(result)
        return results

    @staticmethod
    def __list_without_duplicates(iterable: iter):
        return list(OrderedDict.fromkeys(iterable))
