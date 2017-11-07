from clock.storage.data_source.data_sources.sqlite.component.component import SqliteStorageComponent


class MessageSqliteComponent(SqliteStorageComponent):
    def init(self):
        self._sql("create table if not exists message ("
                  "timestamp text,"
                  "chat_id integer,"
                  "message_id integer,"
                  "user_id integer,"
                  "date integer,"
                  "text text"
                  ")")

    def save_message(self, chat_id: int, message_id: int, user_id: int, date: int, text: str):
        self._sql("insert into message "
                  "(timestamp, chat_id, message_id, user_id, date, text) "
                  "values (strftime('%s', 'now'), ?, ?, ?, ?, ?)",
                  (chat_id, message_id, user_id, date, text))
