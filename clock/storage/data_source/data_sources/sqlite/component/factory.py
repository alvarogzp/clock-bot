from sqlite3 import Connection

from clock.storage.data_source.data_sources.sqlite.component.components.chat import ChatSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.message import MessageSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.query import QuerySqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.user import UserSqliteComponent


class SqliteStorageComponentFactory:
    def __init__(self, connection: Connection):
        self.connection = connection

    def user(self):
        return UserSqliteComponent(self.connection)

    def query(self):
        return QuerySqliteComponent(self.connection)

    def chat(self):
        return ChatSqliteComponent(self.connection)

    def message(self):
        return MessageSqliteComponent(self.connection)
