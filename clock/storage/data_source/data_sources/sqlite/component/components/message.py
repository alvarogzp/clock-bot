from clock.storage.data_source.data_sources.sqlite.component.component import SqliteStorageComponent


class MessageSqliteComponent(SqliteStorageComponent):
    version = 2

    def __init__(self):
        super().__init__("message", self.version)

    def create(self):
        self._sql("create table if not exists message ("
                  "id integer primary key not null,"  # automatically filled
                  "timestamp text,"
                  "chat_id integer,"
                  "message_id integer,"
                  "user_id integer,"
                  "date integer,"
                  "is_forward integer,"  # boolean
                  "reply_to_message integer,"  # references: message_id column
                  "is_edit integer,"  # boolean
                  "text text,"
                  "new_chat_member integer,"  # user_id
                  "left_chat_member integer,"  # user_id
                  "group_chat_created integer,"  # boolean
                  "migrate_to_chat_id integer,"
                  "migrate_from_chat_id integer"
                  ")")
        self._sql("create table if not exists command ("
                  "message_id integer,"
                  "command text,"
                  "command_args text"
                  ")")

    def upgrade_from_1_to_2(self):
        self.add_columns(
            "message",
            "is_forward integer", "reply_to_message integer", "is_edit integer",
            "new_chat_member integer", "left_chat_member integer",
            "group_chat_created integer", "migrate_to_chat_id integer", "migrate_from_chat_id integer"
        )

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
