import itertools


class MatchSearchStrategyMixIn:
    def __init__(self):
        super().__init__()  # continue the calling chain
        self.prioritized_results = [[] for _ in range(3)]

    def _add_result(self, result):
        raise RuntimeError("_add_result is not supported on match searches")

    def _add_results(self, results):
        for prioritized_result_list, result_list in zip(self.prioritized_results, results):
            prioritized_result_list.extend(result_list)

    def get_results(self):
        return itertools.chain.from_iterable(self.prioritized_results)

    def get_prioritized_results(self):
        return self.prioritized_results
