class FindUtil:
    @staticmethod
    def match_key(data_set: iter, query: str, search_equal=True, search_start=True, search_fuzzy=True):
        matches_equal = []
        matches_start = []
        matches_fuzzy = []
        if search_fuzzy:
            query_words = query.split()
        for key, value in data_set:
            if search_equal and key == query:
                matches_equal.append(value)
            elif search_start and key.startswith(query):
                matches_start.append(value)
            # it performs better (on 3.6) with a list comprehension than with a generator
            elif search_fuzzy and (query in key or all([query_word in key for query_word in query_words])):
                matches_fuzzy.append(value)
        return matches_equal, matches_start, matches_fuzzy
