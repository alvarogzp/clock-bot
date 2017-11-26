from clock.storage.data_source.data_sources.sqlite.component.component import SqliteStorageComponent
from clock.storage.data_source.data_sources.sqlite.sql.item.column import Column, COLUMN_ROWID
from clock.storage.data_source.data_sources.sqlite.sql.item.constants.operator import OPERATOR_EQUAL
from clock.storage.data_source.data_sources.sqlite.sql.item.constants.order_mode import ORDER_DESC
from clock.storage.data_source.data_sources.sqlite.sql.item.constants.type import TYPE_INTEGER, TYPE_TEXT
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.compound.cast import Cast
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.compound.condition import Condition
from clock.storage.data_source.data_sources.sqlite.sql.item.table import Table
from clock.storage.data_source.data_sources.sqlite.sql.schema.table import TableSchema


COLUMN_USER_ID = Column("user_id", TYPE_INTEGER, "primary key", "not null")
COLUMN_FIRST_NAME = Column("first_name", TYPE_TEXT)
COLUMN_LAST_NAME = Column("last_name", TYPE_TEXT)
COLUMN_USERNAME = Column("username", TYPE_TEXT)
COLUMN_LANGUAGE_CODE = Column("language_code", TYPE_TEXT)
COLUMN_IS_BOT = Column("is_bot", TYPE_INTEGER)  # boolean
COLUMN_TIMESTAMP_ADDED = Column("timestamp_added", TYPE_TEXT)
COLUMN_USER_ID_USER_HISTORY = Column("user_id", TYPE_INTEGER, "not null")
COLUMN_TIMESTAMP_REMOVED = Column("timestamp_removed", TYPE_TEXT)


USER = TableSchema()
USER.table = Table("user")
USER.column(COLUMN_USER_ID)
USER.column(COLUMN_FIRST_NAME)
USER.column(COLUMN_LAST_NAME)
USER.column(COLUMN_USERNAME)
USER.column(COLUMN_LANGUAGE_CODE)
USER.column(COLUMN_IS_BOT, version=2)
USER.column(COLUMN_TIMESTAMP_ADDED)

USER_HISTORY = TableSchema()
USER_HISTORY.table = Table("user_history")
USER_HISTORY.column(COLUMN_USER_ID_USER_HISTORY)
USER_HISTORY.column(COLUMN_FIRST_NAME)
USER_HISTORY.column(COLUMN_LAST_NAME)
USER_HISTORY.column(COLUMN_USERNAME)
USER_HISTORY.column(COLUMN_LANGUAGE_CODE)
USER_HISTORY.column(COLUMN_IS_BOT, version=2)
USER_HISTORY.column(COLUMN_TIMESTAMP_ADDED)
USER_HISTORY.column(COLUMN_TIMESTAMP_REMOVED)


class UserSqliteComponent(SqliteStorageComponent):
    version = 2

    def __init__(self):
        super().__init__("user", self.version)

    def create(self):
        self.statement.create_table().from_schema(USER).execute()
        self.statement.create_table().from_schema(USER_HISTORY).execute()

    def upgrade_from_1_to_2(self):
        self.statement.alter_table().from_schema(USER, 2).execute()
        self.statement.alter_table().from_schema(USER_HISTORY, 2).execute()

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
        return self.statement.select()\
            .fields("1").table(USER.table)\
            .where("user_id = :user_id and first_name = :first_name and last_name = :last_name and "
                   "username = :username and language_code = :language_code "
                   "and (is_bot = :is_bot or (is_bot is null and :is_bot is null))")\
            .execute(user_id=user_id, first_name=first_name, last_name=last_name, username=username,
                     language_code=language_code, is_bot=is_bot)\
            .first()

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
        return self.statement.select()\
            .fields(COLUMN_LANGUAGE_CODE)\
            .table(table)\
            .where(Condition(COLUMN_ROWID, OPERATOR_EQUAL, ":rowid"))\
            .execute(rowid=rowid)\
            .first_field()

    def _find_user_at(self, user_id: int, timestamp: str):
        timestamp = int(timestamp)
        # try with current user info
        user = self.statement.select()\
            .fields(COLUMN_ROWID, COLUMN_TIMESTAMP_ADDED)\
            .table(USER.table)\
            .where(Condition(COLUMN_USER_ID, OPERATOR_EQUAL, ":user_id"))\
            .execute(user_id=user_id)\
            .first()
        if user is None:
            # if the user is not in the user table, we do not know about their
            raise Exception("unknown user: {user_id}".format(user_id=user_id))
        last_added = user[COLUMN_TIMESTAMP_ADDED]
        if self.__was_valid_at(timestamp, last_added):
            rowid = user[COLUMN_ROWID]
            return USER.table, rowid
        # now iterate the user_history entries for that user
        user_history = self.statement.select()\
            .fields(COLUMN_ROWID, COLUMN_TIMESTAMP_ADDED, COLUMN_TIMESTAMP_REMOVED)\
            .table(USER_HISTORY.table)\
            .where(Condition(COLUMN_USER_ID_USER_HISTORY, OPERATOR_EQUAL, ":user_id"))\
            .order_by(Cast(COLUMN_TIMESTAMP_REMOVED, TYPE_INTEGER), ORDER_DESC)\
            .execute(user_id=user_id)
        for user in user_history:
            added = user[COLUMN_TIMESTAMP_ADDED]
            removed = user[COLUMN_TIMESTAMP_REMOVED]
            if self.__was_valid_at(timestamp, added, removed):
                rowid = user[COLUMN_ROWID]
                return USER_HISTORY.table, rowid
        raise Exception("user {user_id} was unknown at {timestamp}".format(user_id=user_id, timestamp=timestamp))

    @staticmethod
    def __was_valid_at(timestamp: int, timestamp_added: str, timestamp_removed: str = None):
        if timestamp_removed is None:
            return int(timestamp_added) <= timestamp
        else:
            return int(timestamp_added) <= timestamp <= int(timestamp_removed)
