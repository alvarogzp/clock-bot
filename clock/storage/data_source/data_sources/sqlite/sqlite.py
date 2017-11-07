import sqlite3

from clock.storage.data_source.data_source import StorageDataSource
from clock.storage.data_source.data_sources.sqlite.component.component import SqliteStorageComponent
from clock.storage.data_source.data_sources.sqlite.component.components.chat import ChatSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.message import MessageSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.query import QuerySqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.user import UserSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.factory import SqliteStorageComponentFactory


DATABASE_FILENAME = "state/clock.db"


class SqliteStorageDataSource(StorageDataSource):
    def __init__(self):
        # initialized in init to avoid creating sqlite objects outside the thread in which it will be operating
        self.connection = None
        self.user = None  # type: UserSqliteComponent
        self.chat = None  # type: ChatSqliteComponent
        self.query = None  # type: QuerySqliteComponent
        self.message = None  # type: MessageSqliteComponent

    def init(self):
        self.connection = sqlite3.connect(DATABASE_FILENAME)
        self.connection.row_factory = sqlite3.Row  # improved rows
        components = SqliteStorageComponentFactory(self.connection)
        self.user = self._get_and_init(components.user())
        self.chat = self._get_and_init(components.chat())
        self.query = self._get_and_init(components.query())
        self.message = self._get_and_init(components.message())

    @staticmethod
    def _get_and_init(component: SqliteStorageComponent):
        component.init()
        return component

    def save_user(self, user_id: int, first_name: str, last_name: str, username: str, language_code: str):
        self.user.save_user(user_id, first_name, last_name, username, language_code)

    def save_chat(self, chat_id: int, chat_type: str, title: str, username: str):
        self.chat.save_chat(chat_id, chat_type, title, username)

    def save_query(self, user_id: int, timestamp: str, query: str, offset: str, locale: str, results_found_len: int,
                   results_sent_len: int, processing_seconds: float):
        self.query.save_query(
            user_id, timestamp, query, offset, locale, results_found_len, results_sent_len, processing_seconds
        )

    def save_chosen_result(self, user_id: int, timestamp: str, chosen_zone_name: str, query: str,
                           choosing_seconds: float):
        self.query.save_chosen_result(user_id, timestamp, chosen_zone_name, query, choosing_seconds)

    def save_message(self, chat_id: int, message_id: int, user_id: int, date: int, text: str):
        self.message.save_message(chat_id, message_id, user_id, date, text)

    def commit(self):
        self.connection.commit()