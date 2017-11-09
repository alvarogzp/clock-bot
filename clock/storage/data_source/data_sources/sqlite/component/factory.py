from sqlite3 import Connection

from clock.storage.data_source.data_sources.sqlite.component.component import SqliteStorageComponent
from clock.storage.data_source.data_sources.sqlite.component.components.active_chat import ActiveChatSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.chat import ChatSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.message import MessageSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.query import QuerySqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.user import UserSqliteComponent


class SqliteStorageComponentFactory:
    def __init__(self, connection: Connection):
        self.connection = connection

    def user(self):
        return self._initialized(UserSqliteComponent())

    def query(self):
        return self._initialized(QuerySqliteComponent())

    def chat(self):
        return self._initialized(ChatSqliteComponent())

    def message(self):
        return self._initialized(MessageSqliteComponent())

    def active_chat(self):
        return self._initialized(ActiveChatSqliteComponent())

    def _initialized(self, component: SqliteStorageComponent):
        component.set_connection(self.connection)
        return component
