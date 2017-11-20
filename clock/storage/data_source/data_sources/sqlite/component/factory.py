from sqlite3 import Connection

from clock.storage.data_source.data_sources.sqlite.component.component import SqliteStorageComponent
from clock.storage.data_source.data_sources.sqlite.component.components.active_chat import ActiveChatSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.chat import ChatSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.message import MessageSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.query import QuerySqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.user import UserSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.version_info import VersionInfoSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.migrate.migrator import SqliteComponentMigrator


class SqliteStorageComponentFactory:
    def __init__(self, connection: Connection):
        self.connection = connection
        self.version_info = self._version_info()  # type: VersionInfoSqliteComponent

    def _version_info(self):
        # set self.version_info now to not fail on _migrate
        self.version_info = VersionInfoSqliteComponent()
        return self._initialized(self.version_info)

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
        self._migrate(component)
        return component

    def _migrate(self, component: SqliteStorageComponent):
        SqliteComponentMigrator(component, self.version_info).migrate()
