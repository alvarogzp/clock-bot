from clock.storage.data_source.data_sources.sqlite.component.component import SqliteStorageComponent
from clock.storage.data_source.data_sources.sqlite.sql.item.column import Column, ROWID
from clock.storage.data_source.data_sources.sqlite.sql.item.constants.conflict_resolution import REPLACE
from clock.storage.data_source.data_sources.sqlite.sql.item.constants.operator import EQUAL, AND, OR, IS
from clock.storage.data_source.data_sources.sqlite.sql.item.constants.order_mode import DESC
from clock.storage.data_source.data_sources.sqlite.sql.item.constants.type import INTEGER, TEXT
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.compound.cast import Cast
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.compound.condition import Condition, \
    MultipleCondition
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.constants import NULL, CURRENT_UNIX_TIMESTAMP
from clock.storage.data_source.data_sources.sqlite.sql.item.table import Table
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.insert import Insert
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.select import Select


USER_ID = Column("user_id", INTEGER, "primary key", "not null")
FIRST_NAME = Column("first_name", TEXT)
LAST_NAME = Column("last_name", TEXT)
USERNAME = Column("username", TEXT)
LANGUAGE_CODE = Column("language_code", TEXT)
IS_BOT = Column("is_bot", INTEGER)  # boolean
TIMESTAMP_ADDED = Column("timestamp_added", TEXT)
USER_ID_USER_HISTORY = Column("user_id", INTEGER, "not null")
TIMESTAMP_REMOVED = Column("timestamp_removed", TEXT)


USER = Table("user")
USER.column(USER_ID)
USER.column(FIRST_NAME)
USER.column(LAST_NAME)
USER.column(USERNAME)
USER.column(LANGUAGE_CODE)
USER.column(IS_BOT, version=2)
USER.column(TIMESTAMP_ADDED)

USER_HISTORY = Table("user_history")
USER_HISTORY.column(USER_ID_USER_HISTORY)
USER_HISTORY.column(FIRST_NAME)
USER_HISTORY.column(LAST_NAME)
USER_HISTORY.column(USERNAME)
USER_HISTORY.column(LANGUAGE_CODE)
USER_HISTORY.column(IS_BOT, version=2)
USER_HISTORY.column(TIMESTAMP_ADDED)
USER_HISTORY.column(TIMESTAMP_REMOVED)


ADD_USER = Insert().or_(REPLACE)\
    .table(USER)\
    .columns(USER_ID, FIRST_NAME, LAST_NAME, USERNAME, LANGUAGE_CODE, IS_BOT, TIMESTAMP_ADDED)\
    .values(":user_id", ":first_name", ":last_name", ":username", ":language_code", ":is_bot", CURRENT_UNIX_TIMESTAMP)\
    .build()

GET_IS_USER_SAVED_EQUAL = Select()\
    .fields("1")\
    .table(USER)\
    .where(
        MultipleCondition(
            AND,
            Condition(USER_ID, EQUAL, ":user_id"),
            Condition(FIRST_NAME, EQUAL, ":first_name"),
            Condition(LAST_NAME, EQUAL, ":last_name"),
            Condition(USERNAME, EQUAL, ":username"),
            Condition(LANGUAGE_CODE, EQUAL, ":language_code"),
            Condition(
                Condition(IS_BOT, EQUAL, ":is_bot"),
                OR,
                Condition(
                    Condition(IS_BOT, IS, NULL),
                    AND,
                    Condition(":is_bot", IS, NULL)
                )
            )
        )
    )\
    .build()

# missing table, which is filled at runtime from either USER or USER_HISTORY
GET_LANGUAGE_CODE_BUILDER = Select()\
    .fields(LANGUAGE_CODE)\
    .where(Condition(ROWID, EQUAL, ":rowid"))

GET_ROWID_AND_TIMESTAMP_ADDED_FROM_USER = Select()\
    .fields(ROWID, TIMESTAMP_ADDED)\
    .table(USER)\
    .where(Condition(USER_ID, EQUAL, ":user_id"))\
    .build()

GET_ROWID_TIMESTAMP_ADDED_AND_REMOVED_FROM_USER_HISTORY = Select()\
    .fields(ROWID, TIMESTAMP_ADDED, TIMESTAMP_REMOVED)\
    .table(USER_HISTORY)\
    .where(Condition(USER_ID_USER_HISTORY, EQUAL, ":user_id"))\
    .order_by(Cast(TIMESTAMP_REMOVED, INTEGER), DESC)\
    .build()


class UserSqliteComponent(SqliteStorageComponent):
    version = 2

    def __init__(self):
        super().__init__("user", self.version)
        self.managed_tables(USER, USER_HISTORY)

    def save_user(self, user_id: int, first_name: str, last_name: str, username: str, language_code: str, is_bot: bool):
        first_name = self._empty_if_none(first_name)
        last_name = self._empty_if_none(last_name)
        username = self._empty_if_none(username)
        language_code = self._empty_if_none(language_code)
        if not self.__is_user_saved_equal(user_id, first_name, last_name, username, language_code, is_bot):
            self.__add_to_user_history(user_id)
            self.statement(ADD_USER).execute(
                user_id=user_id, first_name=first_name, last_name=last_name, username=username,
                language_code=language_code, is_bot=is_bot
            )

    def __is_user_saved_equal(self, user_id: int, first_name: str, last_name: str, username: str, language_code: str,
                              is_bot: bool):
        return self.statement(GET_IS_USER_SAVED_EQUAL).execute(
            user_id=user_id, first_name=first_name, last_name=last_name, username=username, language_code=language_code,
            is_bot=is_bot
        ).first()

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
        statement = GET_LANGUAGE_CODE_BUILDER.copy()\
            .table(table)\
            .build()
        return self.statement(statement)\
            .execute(rowid=rowid)\
            .first_field()

    def _find_user_at(self, user_id: int, timestamp: str):
        timestamp = int(timestamp)
        # try with current user info
        user = self.statement(GET_ROWID_AND_TIMESTAMP_ADDED_FROM_USER)\
            .execute(user_id=user_id)\
            .first()
        if user is None:
            # if the user is not in the user table, we do not know about their
            raise Exception("unknown user: {user_id}".format(user_id=user_id))
        last_added = user[TIMESTAMP_ADDED]
        if self.__was_valid_at(timestamp, last_added):
            rowid = user[ROWID]
            return USER, rowid
        # now iterate the user_history entries for that user
        user_history = self.statement(GET_ROWID_TIMESTAMP_ADDED_AND_REMOVED_FROM_USER_HISTORY)\
            .execute(user_id=user_id)
        for user in user_history:
            added = user[TIMESTAMP_ADDED]
            removed = user[TIMESTAMP_REMOVED]
            if self.__was_valid_at(timestamp, added, removed):
                rowid = user[ROWID]
                return USER_HISTORY, rowid
        raise Exception("user {user_id} was unknown at {timestamp}".format(user_id=user_id, timestamp=timestamp))

    @staticmethod
    def __was_valid_at(timestamp: int, timestamp_added: str, timestamp_removed: str = None):
        if timestamp_removed is None:
            return int(timestamp_added) <= timestamp
        else:
            return int(timestamp_added) <= timestamp <= int(timestamp_removed)
