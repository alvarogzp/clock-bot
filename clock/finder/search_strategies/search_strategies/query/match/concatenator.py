import itertools

from clock.finder.search_strategies.search_strategies.concatenator import SearchStrategyConcatenator
from clock.finder.search_strategies.search_strategies.query.match import MatchSearchStrategy


class MatchSearchStrategyConcatenator(SearchStrategyConcatenator):
    def __init__(self, *match_search_strategies: MatchSearchStrategy):
        super().__init__(*match_search_strategies)

    def get_results(self):
        return itertools.chain.from_iterable(  # [1st_strategy_1st_prio0_result, 1st_strategy_2nd_prio0_result, ...]
            itertools.chain.from_iterable(  # [1st_strategy_prio0_results, 2nd_strategy_prio0_results, ...]
                zip(  # [(1st_strategy_priority0_results, 2nd_strategy_priority0_results), (...)]
                    *[strategy.get_prioritized_results() for strategy in self.search_strategies]
                )
            )
        )
