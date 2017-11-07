from clock.storage.data_source.data_sources.sqlite.component.component import SqliteStorageComponent


class UserSqliteComponent(SqliteStorageComponent):
    def init(self):
        self._sql("create table if not exists user ("
                  "user_id integer primary key not null,"
                  "first_name text,"
                  "last_name text,"
                  "username text,"
                  "language_code text,"
                  "timestamp_added text"
                  ")")
        self._sql("create table if not exists user_history ("
                  "user_id integer not null,"
                  "first_name text,"
                  "last_name text,"
                  "username text,"
                  "language_code text,"
                  "timestamp_added text,"
                  "timestamp_removed text"
                  ")")

    def save_user(self, user_id: int, first_name: str, last_name: str, username: str, language_code: str):
        first_name = self.__empty_if_none(first_name)
        last_name = self.__empty_if_none(last_name)
        username = self.__empty_if_none(username)
        language_code = self.__empty_if_none(language_code)
        if not self.__is_user_saved_equal(user_id, first_name, last_name, username, language_code):
            self.__add_to_user_history(user_id)
            self._sql("insert or replace into user "
                      "(user_id, first_name, last_name, username, language_code, timestamp_added) "
                      "values (?, ?, ?, ?, ?, strftime('%s', 'now'))",
                      (user_id, first_name, last_name, username, language_code))

    def __is_user_saved_equal(self, user_id: int, first_name: str, last_name: str, username: str, language_code: str):
        return self._sql("select 1 from user where "
                         "user_id = ? and first_name = ? and last_name = ? and username = ? and language_code = ?",
                         (user_id, first_name, last_name, username, language_code)).fetchone()

    def __add_to_user_history(self, user_id: int):
        # if user does not exists in user table, nothing will be inserted into user_history, as expected for new users
        self._sql("insert into user_history "
                  "(user_id, first_name, last_name, username, language_code, timestamp_added, timestamp_removed) "
                  "select user_id, first_name, last_name, username, language_code, "
                  "timestamp_added, strftime('%s', 'now') "
                  "from user where user_id = ?", (user_id,))

    @staticmethod
    def __empty_if_none(field: str):
        return field if field is not None else ""
