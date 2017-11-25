from sqlite3 import Connection

from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.alter_table import AlterTable
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.create_table import CreateTable
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.insert import Insert
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.select import Select
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.update import Update


class StatementFactory:
    def __init__(self, connection: Connection):
        self.connection = connection

    def select(self) -> Select:
        return self._initialized(Select())

    def create_table(self) -> CreateTable:
        return self._initialized(CreateTable())

    def alter_table(self) -> AlterTable:
        return self._initialized(AlterTable())

    def update(self) -> Update:
        return self._initialized(Update())

    def insert(self) -> Insert:
        return self._initialized(Insert())

    def _initialized(self, builder):
        builder.set_connection(self.connection)
        return builder
