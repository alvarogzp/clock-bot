from clock.storage.data_source.data_sources.sqlite.component.component import SqliteStorageComponent
from clock.storage.data_source.data_sources.sqlite.sql.item.column import Column
from clock.storage.data_source.data_sources.sqlite.sql.item.constants.type import INTEGER, TEXT
from clock.storage.data_source.data_sources.sqlite.sql.item.table import Table


NAME = "message"
VERSION = 2


MESSAGE = Table("message")
MESSAGE.column(Column("id", INTEGER, "primary key", "not null"))  # automatically filled
MESSAGE.column(Column("timestamp", TEXT))
MESSAGE.column(Column("chat_id", INTEGER))
MESSAGE.column(Column("message_id", INTEGER))
MESSAGE.column(Column("user_id", INTEGER))
MESSAGE.column(Column("date", INTEGER))
MESSAGE.column(Column("is_forward", INTEGER), version=2)  # boolean
MESSAGE.column(Column("reply_to_message", INTEGER), version=2)  # references: message_id column
MESSAGE.column(Column("is_edit", INTEGER), version=2)  # boolean
MESSAGE.column(Column("text", TEXT))
MESSAGE.column(Column("new_chat_member", INTEGER), version=2)  # user_id
MESSAGE.column(Column("left_chat_member", INTEGER), version=2)  # user_id
MESSAGE.column(Column("group_chat_created", INTEGER), version=2)  # boolean
MESSAGE.column(Column("migrate_to_chat_id", INTEGER), version=2)
MESSAGE.column(Column("migrate_from_chat_id", INTEGER), version=2)

COMMAND = Table("command")
COMMAND.column(Column("message_id", INTEGER))  # references: message.id column
COMMAND.column(Column("command", TEXT))
COMMAND.column(Column("command_args", TEXT))


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
