from clock.finder.search_strategies.search_strategies.query.generic import GenericQuerySearchStrategy
from clock.finder.search_strategies.search_strategies.query.match import MatchSearchStrategyMixIn


class GenericMatchSearchStrategy(GenericQuerySearchStrategy, MatchSearchStrategyMixIn):
    def __init__(self, query_lower: str, match_func: callable):
        super().__init__(query_lower, match_func)

    def _add_result(self, result):
        MatchSearchStrategyMixIn._add_result(self, result)

    def _add_results(self, results):
        MatchSearchStrategyMixIn._add_results(self, results)

    def get_results(self):
        MatchSearchStrategyMixIn.get_results(self)

    def get_prioritized_results(self):
        MatchSearchStrategyMixIn.get_prioritized_results(self)
