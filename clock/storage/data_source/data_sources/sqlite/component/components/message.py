from clock.storage.data_source.data_sources.sqlite.component.component import SqliteStorageComponent
from clock.storage.data_source.data_sources.sqlite.sql.item.column import Column
from clock.storage.data_source.data_sources.sqlite.sql.item.constants.type import INTEGER, TEXT
from clock.storage.data_source.data_sources.sqlite.sql.item.table import Table


NAME = "message"
VERSION = 2


ID = Column("id", INTEGER, "primary key", "not null")  # automatically filled
TIMESTAMP = Column("timestamp", TEXT)
CHAT_ID = Column("chat_id", INTEGER)
MESSAGE_ID = Column("message_id", INTEGER)
USER_ID = Column("user_id", INTEGER)
DATE = Column("date", INTEGER)
IS_FORWARD = Column("is_forward", INTEGER)  # boolean
REPLY_TO_MESSAGE = Column("reply_to_message", INTEGER)  # references: message_id column
IS_EDIT = Column("is_edit", INTEGER)  # boolean
MESSAGE_TEXT = Column("text", TEXT)
NEW_CHAT_MEMBER = Column("new_chat_member", INTEGER)  # user_id
LEFT_CHAT_MEMBER = Column("left_chat_member", INTEGER)  # user_id
GROUP_CHAT_CREATED = Column("group_chat_created", INTEGER)  # boolean
MIGRATE_TO_CHAT_ID = Column("migrate_to_chat_id", INTEGER)
MIGRATE_FROM_CHAT_ID = Column("migrate_from_chat_id", INTEGER)

MESSAGE_ID_COMMAND = Column("message_id", INTEGER)  # references: message.id column
COMMAND_TEXT = Column("command", TEXT)
COMMAND_ARGS = Column("command_args", TEXT)


MESSAGE = Table("message")
MESSAGE.column(ID)
MESSAGE.column(TIMESTAMP)
MESSAGE.column(CHAT_ID)
MESSAGE.column(MESSAGE_ID)
MESSAGE.column(USER_ID)
MESSAGE.column(DATE)
MESSAGE.column(IS_FORWARD, version=2)
MESSAGE.column(REPLY_TO_MESSAGE, version=2)
MESSAGE.column(IS_EDIT, version=2)
MESSAGE.column(MESSAGE_TEXT)
MESSAGE.column(NEW_CHAT_MEMBER, version=2)
MESSAGE.column(LEFT_CHAT_MEMBER, version=2)
MESSAGE.column(GROUP_CHAT_CREATED, version=2)
MESSAGE.column(MIGRATE_TO_CHAT_ID, version=2)
MESSAGE.column(MIGRATE_FROM_CHAT_ID, version=2)

COMMAND = Table("command")
COMMAND.column(MESSAGE_ID_COMMAND)
COMMAND.column(COMMAND_TEXT)
COMMAND.column(COMMAND_ARGS)


class MessageSqliteComponent(SqliteStorageComponent):
    def __init__(self):
        super().__init__(NAME, VERSION)
        self.managed_tables(MESSAGE, COMMAND)

    def save_message(self, chat_id: int, message_id: int, user_id: int, date: int, is_forward: bool,
                     reply_to_message: int, is_edit: bool, text: str, new_chat_member: int, left_chat_member: int,
                     group_chat_created: bool, migrate_to_chat_id: int, migrate_from_chat_id: int):
        self._sql("insert into message "
                  "(timestamp, chat_id, message_id, user_id, date, is_forward, reply_to_message, is_edit, text, "
                  "new_chat_member, left_chat_member, group_chat_created, migrate_to_chat_id, migrate_from_chat_id) "
                  "values (strftime('%s', 'now'), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (chat_id, message_id, user_id, date, is_forward, reply_to_message, is_edit, text, new_chat_member,
                   left_chat_member, group_chat_created, migrate_to_chat_id, migrate_from_chat_id))

    def save_command(self, message_id: int, command: str, command_args: str):
        self._sql("insert into command "
                  "(message_id, command, command_args) "
                  "values (?, ?, ?)",
                  (message_id, command, command_args))

    def get_message_id(self, chat_id: int, message_id: int):
        return self._sql("select id from message where "
                         "chat_id = ? and message_id = ?",
                         (chat_id, message_id)).fetchone()["id"]
