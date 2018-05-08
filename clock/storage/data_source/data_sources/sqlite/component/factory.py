from sqlite_framework.component.factory import SqliteStorageComponentFactory

from clock.storage.data_source.data_sources.sqlite.component.components.active_chat import ActiveChatSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.chat import ChatSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.message import MessageSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.query import QuerySqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.user import UserSqliteComponent


class ClockSqliteStorageComponentFactory(SqliteStorageComponentFactory):
    def user(self):
        return self._initialized(UserSqliteComponent())

    def query(self, user: UserSqliteComponent):
        return self._initialized(QuerySqliteComponent(user))

    def chat(self):
        return self._initialized(ChatSqliteComponent())

    def message(self):
        return self._initialized(MessageSqliteComponent())

    def active_chat(self):
        return self._initialized(ActiveChatSqliteComponent())
