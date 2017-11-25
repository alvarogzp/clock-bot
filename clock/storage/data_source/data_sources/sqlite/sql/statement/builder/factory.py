from sqlite3 import Connection

from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.alter_table import AlterTableBuilder
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.create_table import CreateTableBuilder
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.select import SelectBuilder
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.update import UpdateBuilder


class StatementBuilderFactory:
    def __init__(self, connection: Connection):
        self.connection = connection

    def select(self) -> SelectBuilder:
        return self._initialized(SelectBuilder())

    def create_table(self) -> CreateTableBuilder:
        return self._initialized(CreateTableBuilder())

    def alter_table(self) -> AlterTableBuilder:
        return self._initialized(AlterTableBuilder())

    def update(self) -> UpdateBuilder:
        return self._initialized(UpdateBuilder())

    def _initialized(self, builder):
        builder.set_connection(self.connection)
        return builder
