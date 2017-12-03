from clock.storage.data_source.data_sources.sqlite.component.component import SqliteStorageComponent
from clock.storage.data_source.data_sources.sqlite.component.components.user import UserSqliteComponent
from clock.storage.data_source.data_sources.sqlite.sql.item.column import Column, ROWID
from clock.storage.data_source.data_sources.sqlite.sql.item.constants.operator import EQUAL
from clock.storage.data_source.data_sources.sqlite.sql.item.constants.order_mode import DESC
from clock.storage.data_source.data_sources.sqlite.sql.item.constants.type import TEXT, INTEGER, REAL
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.compound.cast import Cast
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.compound.condition import Condition
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.constants import CURRENT_UNIX_TIMESTAMP
from clock.storage.data_source.data_sources.sqlite.sql.item.table import Table
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.insert import Insert
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.select import Select
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.update import Update


NAME = "query"
VERSION = 2


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


QUERY = Table("query")
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

CHOSEN_RESULT = Table("chosen_result")
CHOSEN_RESULT.column(TIMESTAMP)
CHOSEN_RESULT.column(USER_ID)
CHOSEN_RESULT.column(TIME_POINT_CHOSEN_RESULT)
CHOSEN_RESULT.column(CHOSEN_ZONE_NAME)
CHOSEN_RESULT.column(QUERY_TEXT)
CHOSEN_RESULT.column(CHOOSING_SECONDS)


SET_QUERY_LANGUAGE_CODE = Update()\
    .table(QUERY)\
    .set(LANGUAGE_CODE, ":language_code")\
    .where(Condition(ROWID, EQUAL, ":rowid"))\
    .build()

SAVE_QUERY = Insert()\
    .table(QUERY)\
    .columns(
        TIMESTAMP, USER_ID, TIME_POINT_QUERY, QUERY_TEXT, OFFSET, LANGUAGE_CODE, LOCALE, RESULTS_FOUND_LEN,
        RESULTS_SENT_LEN, PROCESSING_SECONDS
    )\
    .values(
        CURRENT_UNIX_TIMESTAMP, ":user_id", ":time_point", ":query", ":offset", ":language_code", ":locale",
        ":results_found_len", ":results_sent_len", ":processing_seconds"
    )\
    .build()

GET_ALL_QUERIES = Select()\
    .fields(ROWID, USER_ID, TIMESTAMP)\
    .table(QUERY)\
    .build()

GET_RECENT_QUERIES_LANGUAGE_CODES = Select()\
    .fields(LANGUAGE_CODE)\
    .table(QUERY)\
    .group_by(LANGUAGE_CODE)\
    .order_by(Cast(TIMESTAMP, INTEGER), DESC)\
    .limit(":limit")\
    .build()


class QuerySqliteComponent(SqliteStorageComponent):
    def __init__(self, user: UserSqliteComponent):
        super().__init__(NAME, VERSION)
        self.user = user
        self.managed_tables(QUERY, CHOSEN_RESULT)

    def upgrade_from_1_to_2(self):
        self.upgrade(1, 2)  # upgrade tables
        queries = self.statement(GET_ALL_QUERIES).execute()
        for query in queries:
            rowid = query[ROWID]
            user_id = query[USER_ID]
            timestamp = query[TIMESTAMP]
            language_code = self.user.get_user_language_code_at(user_id, timestamp)
            self.statement(SET_QUERY_LANGUAGE_CODE).execute(language_code=language_code, rowid=rowid)

    def save_query(self, user_id: int, timestamp: str, query: str, offset: str, language_code: str, locale: str,
                   results_found_len: int, results_sent_len: int, processing_seconds: float):
        self.statement(SAVE_QUERY).execute(
            user_id=user_id, time_point=timestamp, query=query, offset=offset, language_code=language_code,
            locale=locale, results_found_len=results_found_len, results_sent_len=results_sent_len,
            processing_seconds=processing_seconds
        )

    def save_chosen_result(self, user_id: int, timestamp: str, chosen_zone_name: str, query: str,
                           choosing_seconds: float):
        self._sql("insert into chosen_result "
                  "(timestamp, user_id, time_point, chosen_zone_name, query, choosing_seconds) "
                  "values (strftime('%s', 'now'), ?, ?, ?, ?, ?)",
                  (user_id, timestamp, chosen_zone_name, query, choosing_seconds))

    def get_recent_queries_language_codes(self, limit: int):
        return list(
            self.statement(GET_RECENT_QUERIES_LANGUAGE_CODES)
                .execute(limit=limit)
                .map_field()
        )
