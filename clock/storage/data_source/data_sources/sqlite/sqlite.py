import sqlite3
from sqlite3 import Connection

from clock.log.api import LogApi
from clock.storage.data_source.data_source import StorageDataSource
from clock.storage.data_source.data_sources.sqlite.component.components.active_chat import ActiveChatSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.chat import ChatSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.message import MessageSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.query import QuerySqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.user import UserSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.factory import ClockSqliteStorageComponentFactory
from clock.storage.data_source.data_sources.sqlite.sql.result.row import ResultRow


DATABASE_FILENAME = "state/clock.db"


class SqliteStorageDataSource(StorageDataSource):
    def __init__(self, logger: LogApi, debug: bool):
        self.logger = logger
        self.debug = debug
        self.inside_pending_context_manager = False
        # initialized in init to avoid creating sqlite objects outside the thread in which it will be operating
        self.connection = None  # type: Connection
        self.user = None  # type: UserSqliteComponent
        self.chat = None  # type: ChatSqliteComponent
        self.query = None  # type: QuerySqliteComponent
        self.message = None  # type: MessageSqliteComponent
        self.active_chat = None  # type: ActiveChatSqliteComponent

    def init(self):
        self._init_connection()
        self._init_components()

    def _init_connection(self):
        self.connection = sqlite3.connect(DATABASE_FILENAME)
        if self.debug:
            # print all sentences to stdout
            self.connection.set_trace_callback(lambda x: print(x))
        # disable implicit transactions as we are manually handling them
        self.connection.isolation_level = None
        # improved rows
        self.connection.row_factory = ResultRow
        if self.inside_pending_context_manager:
            self.__enter__()

    def _init_components(self):
        components = ClockSqliteStorageComponentFactory(self.connection, self.logger)
        self.user = components.user()
        self.chat = components.chat()
        self.query = components.query(self.user)
        self.message = components.message()
        self.active_chat = components.active_chat()

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

    def get_recent_queries_language_codes(self, *args):
        return self.query.get_recent_queries_language_codes(*args)

    def context_manager(self):
        return self

    def __enter__(self):
        if self.connection is not None:
            self.connection.execute("begin")
        else:
            # the first init() operation does not yet have the connection created
            # so delay the begin until we create it
            self.inside_pending_context_manager = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.inside_pending_context_manager:
            self.inside_pending_context_manager = False
        if exc_type is None and exc_val is None and exc_tb is None:
            # no error
            self.connection.execute("commit")
        else:
            self.connection.execute("rollback")
