class StorageDataSource:
    def save_query(self, user_id: int, timestamp: str, query: str, offset: str, locale: str, results_found_len: int,
                   results_sent_len: int, processing_seconds: float):
        raise NotImplementedError()

    def save_chosen_result(self, user_id: int, timestamp: str, chosen_zone_name: str, query: str,
                           choosing_seconds: float):
        raise NotImplementedError()

    def save_user(self, user_id: int, first_name: str, last_name: str, username: str, language_code: str):
        raise NotImplementedError()

    def commit(self):
        raise NotImplementedError()
