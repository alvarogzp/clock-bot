import sqlite3

from clock.storage.data_source.data_source import StorageDataSource
from clock.storage.data_source.data_sources.sqlite.component.components.user import UserSqliteComponent


DATABASE_FILENAME = "state/clock.db"


class SqliteStorageDataSource(StorageDataSource):
    version = 1

    def __init__(self):
        # initialized in init to avoid creating sqlite objects outside the thread in which it will be operating
        self.connection = None
        self.user = None  # type: UserSqliteComponent

    def init(self):
        self.connection = sqlite3.connect(DATABASE_FILENAME)
        self.connection.row_factory = sqlite3.Row  # improved rows
        self.user = UserSqliteComponent(self.connection)
        self.user.init()
        self._init_db()

    def _init_db(self):
        self.__sql("create table if not exists query ("
                   "timestamp text,"
                   "user_id integer not null,"
                   "time_point text not null,"
                   "query text,"
                   "offset text,"
                   "locale text,"
                   "results_found_len integer,"
                   "results_sent_len integer,"
                   "processing_seconds real"
                   ")")
        self.__sql("create table if not exists chosen_result ("
                   "timestamp text,"
                   "user_id integer not null,"
                   "time_point text,"
                   "chosen_zone_name text,"
                   "query text,"
                   "choosing_seconds real"
                   ")")

    def save_user(self, user_id: int, first_name: str, last_name: str, username: str, language_code: str):
        self.user.save_user(user_id, first_name, last_name, username, language_code)

    def save_query(self, user_id: int, timestamp: str, query: str, offset: str, locale: str, results_found_len: int,
                   results_sent_len: int, processing_seconds: float):
        self.__sql("insert into query "
                   "(timestamp, user_id, time_point, query, offset, locale, results_found_len, results_sent_len, "
                   "processing_seconds) "
                   "values (strftime('%s', 'now'), ?, ?, ?, ?, ?, ?, ?, ?)",
                   (user_id, timestamp, query, offset, locale, results_found_len, results_sent_len, processing_seconds))

    def save_chosen_result(self, user_id: int, timestamp: str, chosen_zone_name: str, query: str,
                           choosing_seconds: float):
        self.__sql("insert into chosen_result "
                   "(timestamp, user_id, time_point, chosen_zone_name, query, choosing_seconds) "
                   "values (strftime('%s', 'now'), ?, ?, ?, ?, ?)",
                   (user_id, timestamp, chosen_zone_name, query, choosing_seconds))

    def commit(self):
        self.connection.commit()

    def __sql(self, sql: str, params=()):
        return self.connection.execute(sql, params)
