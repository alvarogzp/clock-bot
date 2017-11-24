from clock.storage.data_source.data_sources.sqlite.component.component import SqliteStorageComponent
from clock.storage.data_source.data_sources.sqlite.component.components.user import UserSqliteComponent


class QuerySqliteComponent(SqliteStorageComponent):
    version = 2

    def __init__(self, user: UserSqliteComponent):
        super().__init__("query", self.version)
        self.user = user

    def create(self):
        self._sql("create table if not exists query ("
                  "timestamp text,"
                  "user_id integer not null,"
                  "time_point text not null,"
                  "query text,"
                  "offset text,"
                  "language_code text,"
                  "locale text,"
                  "results_found_len integer,"
                  "results_sent_len integer,"
                  "processing_seconds real"
                  ")")
        self._sql("create table if not exists chosen_result ("
                  "timestamp text,"
                  "user_id integer not null,"
                  "time_point text,"
                  "chosen_zone_name text,"
                  "query text,"
                  "choosing_seconds real"
                  ")")

    def upgrade_from_1_to_2(self):
        self.add_columns("query", "language_code text")
        queries = self.select(fields=("rowid", "user_id", "timestamp"), table="query")  # get all queries
        for query in queries:
            rowid = query["rowid"]
            user_id = query["user_id"]
            timestamp = query["timestamp"]
            language_code = self.user.get_user_language_code_at(user_id, timestamp)
            self.sql("update query "
                     "set language_code = :language_code "
                     "where rowid = :rowid",
                     language_code=language_code, rowid=rowid)

    def save_query(self, user_id: int, timestamp: str, query: str, offset: str, language_code: str, locale: str,
                   results_found_len: int, results_sent_len: int, processing_seconds: float):
        self._sql("insert into query "
                  "(timestamp, user_id, time_point, query, offset, language_code, locale, results_found_len, "
                  "results_sent_len, processing_seconds) "
                  "values (strftime('%s', 'now'), ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (user_id, timestamp, query, offset, language_code, locale, results_found_len, results_sent_len,
                   processing_seconds))

    def save_chosen_result(self, user_id: int, timestamp: str, chosen_zone_name: str, query: str,
                           choosing_seconds: float):
        self._sql("insert into chosen_result "
                  "(timestamp, user_id, time_point, chosen_zone_name, query, choosing_seconds) "
                  "values (strftime('%s', 'now'), ?, ?, ?, ?, ?)",
                  (user_id, timestamp, chosen_zone_name, query, choosing_seconds))

    def get_recent_queries_language_codes(self, limit: int):
        return list(self.select_field(
            field="language_code",
            table="query",
            group_by="language_code",
            order_by="cast(timestamp as integer) desc",
            limit=limit
        ))
