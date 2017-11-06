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
        first_name = self.__empty_if_none(first_name)
        last_name = self.__empty_if_none(last_name)
        username = self.__empty_if_none(username)
        language_code = self.__empty_if_none(language_code)
        if not self.__is_user_saved_equal(user_id, first_name, last_name, username, language_code):
            self.__add_to_user_history(user_id)
            self.__sql("insert or replace into user "
                       "(user_id, first_name, last_name, username, language_code, timestamp_added) "
                       "values (?, ?, ?, ?, ?, strftime('%s', 'now'))",
                       (user_id, first_name, last_name, username, language_code))

    def __is_user_saved_equal(self, user_id: int, first_name: str, last_name: str, username: str, language_code: str):
        return self.__sql("select 1 from user where "
                          "user_id = ? and first_name = ? and last_name = ? and username = ? and language_code = ?",
                          (user_id, first_name, last_name, username, language_code)).fetchone()

    def __add_to_user_history(self, user_id: int):
        # if user does not exists in user table, nothing will be inserted into user_history, as expected for new users
        self.__sql("insert into user_history "
                   "(user_id, first_name, last_name, username, language_code, timestamp_added, timestamp_removed) "
                   "select user_id, first_name, last_name, username, language_code, "
                   "timestamp_added, strftime('%s', 'now') "
                   "from user where user_id = ?", (user_id,))

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

    @staticmethod
    def __empty_if_none(field: str):
        return field if field is not None else ""
