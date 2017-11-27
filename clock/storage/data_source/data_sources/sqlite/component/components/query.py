from clock.storage.data_source.data_sources.sqlite.component.component import SqliteStorageComponent
from clock.storage.data_source.data_sources.sqlite.component.components.user import UserSqliteComponent
from clock.storage.data_source.data_sources.sqlite.sql.item.column import Column
from clock.storage.data_source.data_sources.sqlite.sql.item.constants.type import TEXT, INTEGER, REAL
from clock.storage.data_source.data_sources.sqlite.sql.item.table import Table
from clock.storage.data_source.data_sources.sqlite.sql.schema.table import TableSchema


TIMESTAMP = Column("timestamp", TEXT)
USER_ID = Column("user_id", INTEGER, "not null")
TIME_POINT_QUERY = Column("time_point", TEXT, "not null")
QUERY_TEXT = Column("query", TEXT)
OFFSET = Column("offset", TEXT)
LANGUAGE_CODE = Column("language_code", TEXT)
LOCALE = Column("locale", TEXT)
RESULTS_FOUND_LEN = Column("results_found_len", INTEGER)
RESULTS_SENT_LEN = Column("results_sent_len", INTEGER)
PROCESSING_SECONDS = Column("processing_seconds", REAL)
TIME_POINT_CHOSEN_RESULT = Column("time_point", TEXT)
CHOSEN_ZONE_NAME = Column("chosen_zone_name", TEXT)
CHOOSING_SECONDS = Column("choosing_seconds", REAL)


QUERY = TableSchema()
QUERY.table = Table("query")
QUERY.column(TIMESTAMP)
QUERY.column(USER_ID)
QUERY.column(TIME_POINT_QUERY)
QUERY.column(QUERY_TEXT)
QUERY.column(OFFSET)
QUERY.column(LANGUAGE_CODE, version=2)
QUERY.column(LOCALE)
QUERY.column(RESULTS_FOUND_LEN)
QUERY.column(RESULTS_SENT_LEN)
QUERY.column(PROCESSING_SECONDS)

CHOSEN_RESULT = TableSchema()
CHOSEN_RESULT.table = Table("chosen_result")
CHOSEN_RESULT.column(TIMESTAMP)
CHOSEN_RESULT.column(USER_ID)
CHOSEN_RESULT.column(TIME_POINT_CHOSEN_RESULT)
CHOSEN_RESULT.column(CHOSEN_ZONE_NAME)
CHOSEN_RESULT.column(QUERY_TEXT)
CHOSEN_RESULT.column(CHOOSING_SECONDS)


class QuerySqliteComponent(SqliteStorageComponent):
    version = 2

    def __init__(self, user: UserSqliteComponent):
        super().__init__("query", self.version)
        self.user = user

    def create(self):
        self.statement.create_table().from_schema(QUERY).execute()
        self.statement.create_table().from_schema(CHOSEN_RESULT).execute()

    def upgrade_from_1_to_2(self):
        self.statement.alter_table().from_schema(QUERY, 2).execute()
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
            limit=":limit_param",
            limit_param=limit
        ))
