from clock.storage.data_source.data_sources.sqlite.component.component import SqliteStorageComponent
from clock.storage.data_source.data_sources.sqlite.sql.item.column import Column
from clock.storage.data_source.data_sources.sqlite.sql.item.table import Table
from clock.storage.data_source.data_sources.sqlite.sql.schema.table import TableSchema


TABLE_NAME_USER = "user"
TABLE_NAME_USER_HISTORY = "user_history"

COLUMN_NAME_USER_ID = "user_id"
COLUMN_NAME_FIRST_NAME = "first_name"
COLUMN_NAME_LAST_NAME = "last_name"
COLUMN_NAME_USERNAME = "username"
COLUMN_NAME_LANGUAGE_CODE = "language_code"
COLUMN_NAME_IS_BOT = "is_bot"
COLUMN_NAME_TIMESTAMP_ADDED = "timestamp_added"
COLUMN_NAME_TIMESTAMP_REMOVED = "timestamp_removed"


USER = TableSchema()
USER.table = Table(TABLE_NAME_USER)
USER.column(Column(COLUMN_NAME_USER_ID, "integer", "primary key", "not null"))
USER.column(Column(COLUMN_NAME_FIRST_NAME, "text"))
USER.column(Column(COLUMN_NAME_LAST_NAME, "text"))
USER.column(Column(COLUMN_NAME_USERNAME, "text"))
USER.column(Column(COLUMN_NAME_LANGUAGE_CODE, "text"))
USER.column(Column(COLUMN_NAME_IS_BOT, "integer"), version=2)  # boolean
USER.column(Column(COLUMN_NAME_TIMESTAMP_ADDED, "text"))

USER_HISTORY = TableSchema()
USER_HISTORY.table = Table(TABLE_NAME_USER_HISTORY)
USER_HISTORY.column(Column(COLUMN_NAME_USER_ID, "integer", "not null"))
USER_HISTORY.column_from(USER, COLUMN_NAME_FIRST_NAME)
USER_HISTORY.column_from(USER, COLUMN_NAME_LAST_NAME)
USER_HISTORY.column_from(USER, COLUMN_NAME_USERNAME)
USER_HISTORY.column_from(USER, COLUMN_NAME_LANGUAGE_CODE)
USER_HISTORY.column_from(USER, COLUMN_NAME_IS_BOT)
USER_HISTORY.column_from(USER, COLUMN_NAME_TIMESTAMP_ADDED)
USER_HISTORY.column(Column(COLUMN_NAME_TIMESTAMP_REMOVED, "text"))


class UserSqliteComponent(SqliteStorageComponent):
    version = 2

    def __init__(self):
        super().__init__("user", self.version)

    def create(self):
        self._sql("create table if not exists user ("
                  "user_id integer primary key not null,"
                  "first_name text,"
                  "last_name text,"
                  "username text,"
                  "language_code text,"
                  "is_bot integer,"  # boolean
                  "timestamp_added text"
                  ")")
        self._sql("create table if not exists user_history ("
                  "user_id integer not null,"
                  "first_name text,"
                  "last_name text,"
                  "username text,"
                  "language_code text,"
                  "is_bot integer,"  # boolean
                  "timestamp_added text,"
                  "timestamp_removed text"
                  ")")

    def upgrade_from_1_to_2(self):
        self.add_columns("user", "is_bot integer")
        self.add_columns("user_history", "is_bot integer")

    def save_user(self, user_id: int, first_name: str, last_name: str, username: str, language_code: str, is_bot: bool):
        first_name = self._empty_if_none(first_name)
        last_name = self._empty_if_none(last_name)
        username = self._empty_if_none(username)
        language_code = self._empty_if_none(language_code)
        if not self.__is_user_saved_equal(user_id, first_name, last_name, username, language_code, is_bot):
            self.__add_to_user_history(user_id)
            self._sql("insert or replace into user "
                      "(user_id, first_name, last_name, username, language_code, is_bot, timestamp_added) "
                      "values (?, ?, ?, ?, ?, ?, strftime('%s', 'now'))",
                      (user_id, first_name, last_name, username, language_code, is_bot))

    def __is_user_saved_equal(self, user_id: int, first_name: str, last_name: str, username: str, language_code: str,
                              is_bot: bool):
        return self.sql("select 1 from user where "
                        "user_id = :user_id and first_name = :first_name and last_name = :last_name and "
                        "username = :username and language_code = :language_code "
                        "and (is_bot = :is_bot or (is_bot is null and :is_bot is null))",
                        user_id=user_id, first_name=first_name, last_name=last_name, username=username,
                        language_code=language_code, is_bot=is_bot).fetchone()

    def __add_to_user_history(self, user_id: int):
        # if user does not exists in user table, nothing will be inserted into user_history, as expected for new users
        self._sql("insert into user_history "
                  "(user_id, first_name, last_name, username, language_code, is_bot, timestamp_added, "
                  "timestamp_removed) "
                  "select user_id, first_name, last_name, username, language_code, is_bot, "
                  "timestamp_added, strftime('%s', 'now') "
                  "from user where user_id = ?", (user_id,))

    def get_user_language_code_at(self, user_id: int, timestamp: str):
        table, rowid = self._find_user_at(user_id, timestamp)
        return self.select_field_one(
            field="language_code",
            table=table,
            where="rowid = :rowid",
            rowid=rowid
        )

    def _find_user_at(self, user_id: int, timestamp: str):
        timestamp = int(timestamp)
        # try with current user info
        user = self.select(
            fields=("rowid", "timestamp_added"),
            table="user",
            where="user_id = :user_id",
            user_id=user_id
        ).fetchone()
        if user is None:
            # if the user is not in the user table, we do not know about their
            raise Exception("unknown user: {user_id}".format(user_id=user_id))
        last_added = user["timestamp_added"]
        if self.__was_valid_at(timestamp, last_added):
            rowid = user["rowid"]
            return "user", rowid
        # now iterate the user_history entries for that user
        user_history = self.select(
            fields=("rowid", "timestamp_added", "timestamp_removed"),
            table="user_history",
            where="user_id = :user_id",
            order_by="cast(timestamp_removed as integer) desc",
            user_id=user_id
        )
        for user in user_history:
            added = user["timestamp_added"]
            removed = user["timestamp_removed"]
            if self.__was_valid_at(timestamp, added, removed):
                rowid = user["rowid"]
                return "user_history", rowid
        return Exception("user {user_id} was unknown at {timestamp}".format(user_id=user_id, timestamp=timestamp))

    @staticmethod
    def __was_valid_at(timestamp: int, timestamp_added: str, timestamp_removed: str = None):
        if timestamp_removed is None:
            return int(timestamp_added) <= timestamp
        else:
            return int(timestamp_added) <= timestamp <= int(timestamp_removed)
