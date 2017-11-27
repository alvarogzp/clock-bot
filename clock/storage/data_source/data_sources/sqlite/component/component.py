from sqlite3 import Connection

from clock.storage.data_source.data_sources.sqlite.sql.item.column import Column
from clock.storage.data_source.data_sources.sqlite.sql.item.table import Table
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.factory import StatementFactory
from clock.storage.data_source.data_sources.sqlite.sql.statement.statement import SingleSqlStatement


class SqliteStorageComponent:
    def __init__(self, name: str, version: int):
        self.name = name
        self.version = version
        self.connection = None  # type: Connection
        self.statement = None  # type: StatementFactory

    def set_connection(self, connection: Connection):
        self.connection = connection
        self.statement = StatementFactory(connection)

    def create(self):
        raise NotImplementedError()

    def add_columns(self, table: str, *columns: str):
        """
        IMPORTANT:
        Table name and column definitions are added to the sql statement in an unsafe way!
        So, untrusted input MUST NOT be passed to them.
        Their values should ideally be static string literals.
        If computed at runtime, they MUST come from a TOTALLY trusted source (like another module string constant
        or an admin-controlled configuration value).

        :deprecated: use self.statement.alter_table() instead
        """
        alter_table = self.statement.alter_table().table(Table(table))
        for column in columns:
            alter_table.add_column(Column(*column.split(" ")))
        alter_table.execute()

    def sql(self, sql: str, *qmark_params, **named_params):
        return SingleSqlStatement(self.connection, sql).execute(*qmark_params, **named_params)

    def _sql(self, sql: str, params=()):
        """
        :deprecated: use self.sql instead
        """
        return SingleSqlStatement(self.connection, sql).execute_for_params(params).cursor

    @staticmethod
    def _empty_if_none(field: str):
        return field if field is not None else ""
