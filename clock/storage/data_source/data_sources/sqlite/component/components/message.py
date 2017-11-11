from clock.storage.data_source.data_sources.sqlite.component.component import SqliteStorageComponent


class MessageSqliteComponent(SqliteStorageComponent):
    version = 1

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
                  "text text"
                  ")")
        self._sql("create table if not exists command ("
                  "message_id integer,"
                  "command text,"
                  "command_args text"
                  ")")

    def save_message(self, chat_id: int, message_id: int, user_id: int, date: int, text: str):
        self._sql("insert into message "
                  "(timestamp, chat_id, message_id, user_id, date, text) "
                  "values (strftime('%s', 'now'), ?, ?, ?, ?, ?)",
                  (chat_id, message_id, user_id, date, text))

    def save_command(self, message_id: int, command: str, command_args: str):
        self._sql("insert into command "
                  "(message_id, command, command_args) "
                  "values (?, ?, ?)",
                  (message_id, command, command_args))

    def get_message_id(self, chat_id: int, message_id: int):
        return self._sql("select id from message where "
                         "chat_id = ? and message_id = ?",
                         (chat_id, message_id)).fetchone()["id"]
