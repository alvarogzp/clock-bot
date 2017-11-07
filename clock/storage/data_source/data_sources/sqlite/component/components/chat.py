from clock.storage.data_source.data_sources.sqlite.component.component import SqliteStorageComponent


class ChatSqliteComponent(SqliteStorageComponent):
    def init(self):
        self._sql("create table if not exists chat ("
                  "chat_id integer primary key not null,"
                  "chat_type text,"
                  "title text,"
                  "username text,"
                  "timestamp_added text"
                  ")")
        self._sql("create table if not exists chat_history ("
                  "chat_id integer not null,"
                  "chat_type text,"
                  "title text,"
                  "username text,"
                  "timestamp_added text,"
                  "timestamp_removed text"
                  ")")

    def save_chat(self, chat_id: int, chat_type: str, title: str, username: str):
        chat_type = self._empty_if_none(chat_type)
        title = self._empty_if_none(title)
        username = self._empty_if_none(username)
        if not self.__is_chat_saved_equal(chat_id, chat_type, title, username):
            self.__add_to_chat_history(chat_id)
            self._sql("insert or replace into chat "
                      "(chat_id, chat_type, title, username, timestamp_added) "
                      "values (?, ?, ?, ?, strftime('%s', 'now'))",
                      (chat_id, chat_type, title, username))

    def __is_chat_saved_equal(self, chat_id: int, chat_type: str, title: str, username: str):
        return self._sql("select 1 from chat where "
                         "id = ? and type = ? and title = ? and username = ?",
                         (chat_id, chat_type, title, username)).fetchone()

    def __add_to_chat_history(self, chat_id: int):
        # if chat does not exists in chat table, nothing will be inserted into chat_history, as expected for new chats
        self._sql("insert into chat_history "
                  "(chat_id, chat_type, title, username, timestamp_added, timestamp_removed) "
                  "select chat_id, chat_type, title, username, timestamp_added, strftime('%s', 'now') "
                  "from chat where chat_id = ?", (chat_id,))
