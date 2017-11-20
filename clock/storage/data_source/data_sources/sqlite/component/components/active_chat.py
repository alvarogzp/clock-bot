from clock.storage.data_source.data_sources.sqlite.component.component import SqliteStorageComponent


class ActiveChatSqliteComponent(SqliteStorageComponent):
    version = 1

    def __init__(self):
        super().__init__("active_chat", self.version)

    def create(self):
        self._sql("create table if not exists active_chat ("
                  "chat_id integer primary key not null,"
                  "timestamp_added text"
                  ")")
        self._sql("create table if not exists inactive_chat ("
                  "chat_id integer not null,"
                  "inactive_reason text,"
                  "timestamp_added text,"
                  "timestamp_removed text"
                  ")")

    def set_active(self, chat_id: int):
        self._sql("insert or ignore into active_chat "
                  "(chat_id, timestamp_added) "
                  "values (?, strftime('%s', 'now'))",
                  (chat_id,))

    def set_inactive(self, chat_id: int, reason: str):
        if self.is_active(chat_id):
            # insert into inactive from active
            self._sql("insert into inactive_chat "
                      "(chat_id, inactive_reason, timestamp_added, timestamp_removed) "
                      "select chat_id, ?, timestamp_added, strftime('%s', 'now') "
                      "from active_chat where chat_id = ?",
                      (reason, chat_id,))
            # now remove the active row
            self._delete_active_chat(chat_id)
        else:
            # add to inactive with timestamp_added set to null
            self._sql("insert into inactive_chat "
                      "(chat_id, inactive_reason, timestamp_added, timestamp_removed) "
                      "values (?, ?, null, strftime('%s', 'now'))",
                      (chat_id, reason))

    def is_active(self, chat_id: int):
        return self._sql("select 1 from active_chat where "
                         "chat_id = ?",
                         (chat_id,)).fetchone() is not None

    def _delete_active_chat(self, chat_id: int):
        self._sql("delete from active_chat "
                  "where chat_id = ?",
                  (chat_id,))
