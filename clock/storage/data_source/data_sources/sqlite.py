import sqlite3

from clock.storage.data_source.data_source import StorageDataSource


DATABASE_FILENAME = "state/clock.db"


class SqliteStorageDataSource(StorageDataSource):
    version = 1

    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_FILENAME)
        self.connection.row_factory = sqlite3.Row  # improved rows
        self._init_db()

    def _init_db(self):
        self.__sql("create table if not exists user ("
                   "user_id integer primary key not null,"
                   "first_name text,"
                   "last_name text,"
                   "username text,"
                   "language_code text,"
                   "timestamp_added text"
                   ")")
        self.__sql("create table if not exists user_history ("
                   "user_id integer not null,"
                   "first_name text,"
                   "last_name text,"
                   "username text,"
                   "language_code text,"
                   "timestamp_added text,"
                   "timestamp_removed text"
                   ")")
        self.__sql("create table if not exists query ("
                   "user_id integer not null,"
                   "timestamp text not null,"
                   "query text,"
                   "offset text,"
                   "locale text,"
                   "results_found_len integer,"
                   "results_sent_len integer"
                   ")")
        self.__sql("create table if not exists chosen_result ("
                   "user_id integer not null,"
                   "timestamp text,"
                   "chosen_zone_name text,"
                   "query text"
                   ")")

    def save_user(self, user_id: int, first_name: str, last_name: str, username: str, language_code: str):
        if not self.__is_user_saved_equal(user_id, first_name, last_name, username, language_code):
            self.__sql("insert into user_history "
                       "(user_id, first_name, last_name, username, language_code, timestamp_added, timestamp_removed) "
                       "select user_id, first_name, last_name, username, language_code, "
                       "timestamp_added, strftime('%s', 'now') "
                       "from user where user_id = ?", (user_id,))
            self.__sql("insert or replace into user "
                       "(user_id, first_name, last_name, username, language_code, timestamp_added) "
                       "values (?, ?, ?, ?, ?, strftime('%s', 'now'))",
                       (user_id, first_name, last_name, username, language_code))

    def __is_user_saved_equal(self, user_id: int, first_name: str, last_name: str, username: str, language_code: str):
        return self.__sql("select 1 from user where "
                          "user_id = ? and first_name = ? and last_name = ? and username = ? and language_code = ?",
                          (user_id, first_name, last_name, username, language_code)).fetchone()

    def save_query(self, user_id: int, timestamp: str, query: str, offset: str, locale: str, results_found_len: int,
                   results_sent_len: int):
        self.__sql("insert into query (user_id, timestamp, query, offset, locale, results_found_len, results_sent_len) "
                   "values (?, ?, ?, ?, ?, ?, ?)",
                   (user_id, timestamp, query, offset, locale, results_found_len, results_sent_len))

    def save_chosen_result(self, user_id: int, timestamp: str, chosen_zone_name: str, query: str):
        self.__sql("insert into chosen_result (user_id, timestamp, chosen_zone_name, query) values (?, ?, ?, ?)",
                   (user_id, timestamp, chosen_zone_name, query))

    def commit(self):
        self.connection.commit()

    def __sql(self, sql: str, params=()):
        return self.connection.execute(sql, params)
