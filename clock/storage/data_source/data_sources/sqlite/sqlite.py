import sqlite3

from sqlite3 import Connection

from clock.storage.data_source.data_source import StorageDataSource
from clock.storage.data_source.data_sources.sqlite.component.component import SqliteStorageComponent
from clock.storage.data_source.data_sources.sqlite.component.components.active_chat import ActiveChatSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.chat import ChatSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.message import MessageSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.query import QuerySqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.user import UserSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.factory import SqliteStorageComponentFactory


DATABASE_FILENAME = "state/clock.db"


class SqliteStorageDataSource(StorageDataSource):
    def __init__(self):
        # initialized in init to avoid creating sqlite objects outside the thread in which it will be operating
        self.connection = None  # type: Connection
        self.user = None  # type: UserSqliteComponent
        self.chat = None  # type: ChatSqliteComponent
        self.query = None  # type: QuerySqliteComponent
        self.message = None  # type: MessageSqliteComponent
        self.active_chat = None  # type: ActiveChatSqliteComponent

    def init(self):
        self.connection = sqlite3.connect(DATABASE_FILENAME)
        self.connection.row_factory = sqlite3.Row  # improved rows
        components = SqliteStorageComponentFactory(self.connection)
        self.user = self._get_and_init(components.user())
        self.chat = self._get_and_init(components.chat())
        self.query = self._get_and_init(components.query())
        self.message = self._get_and_init(components.message())
        self.active_chat = self._get_and_init(components.active_chat())

    @staticmethod
    def _get_and_init(component: SqliteStorageComponent):
        component.init()
        return component

    def save_user(self, *args):
        self.user.save_user(*args)

    def save_chat(self, *args):
        self.chat.save_chat(*args)

    def save_query(self, *args):
        self.query.save_query(*args)

    def save_chosen_result(self, *args):
        self.query.save_chosen_result(*args)

    def save_message(self, *args):
        self.message.save_message(*args)

    def save_command(self, *args):
        self.message.save_command(*args)

    def get_message_id(self, *args):
        return self.message.get_message_id(*args)

    def set_active_chat(self, *args):
        return self.active_chat.set_active(*args)

    def set_inactive_chat(self, *args):
        return self.active_chat.set_inactive(*args)

    def commit(self):
        self.connection.commit()
