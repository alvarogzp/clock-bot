class FindUtil:
    @staticmethod
    def match_key(data_set: iter, query, search_equal=True, search_start=True, search_fuzzy=True):
        matches_equal = []
        matches_start = []
        matches_fuzzy = []
        for key, value in data_set:
            if search_equal and key == query:
                matches_equal.append(value)
            elif search_start and key.startswith(query):
                matches_start.append(value)
            elif search_fuzzy and (query in key or all([query_word in key for query_word in query.split()])):
                matches_fuzzy.append(value)
        return matches_equal, matches_start, matches_fuzzy
