from sqlite_framework.session.session import SqliteSession

from clock.log.api import LogApi
from clock.storage.data_source.data_source import StorageDataSource
from clock.storage.data_source.data_sources.sqlite.component.components.active_chat import ActiveChatSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.chat import ChatSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.message import MessageSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.query import QuerySqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.components.user import UserSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.factory import ClockSqliteStorageComponentFactory
from clock.storage.data_source.data_sources.sqlite.logger import LogApiSqliteLogger


DATABASE_FILENAME = "state/clock.db"


class SqliteStorageDataSource(StorageDataSource):
    def __init__(self, logger: LogApi, debug: bool):
        self.session = SqliteSession(DATABASE_FILENAME, debug)
        self.logger = LogApiSqliteLogger(logger)
        # initialized in init to avoid creating sqlite objects outside the thread in which it will be operating
        self.user = None  # type: UserSqliteComponent
        self.chat = None  # type: ChatSqliteComponent
        self.query = None  # type: QuerySqliteComponent
        self.message = None  # type: MessageSqliteComponent
        self.active_chat = None  # type: ActiveChatSqliteComponent

    def init(self):
        self.session.init()
        self._init_components()

    def _init_components(self):
        components = ClockSqliteStorageComponentFactory(self.session, self.logger)
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
        return self.session.context_manager()
