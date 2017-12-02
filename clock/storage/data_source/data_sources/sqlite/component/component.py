from sqlite3 import Connection

from clock.storage.data_source.data_sources.sqlite.sql.item.column import Column
from clock.storage.data_source.data_sources.sqlite.sql.item.table import Table
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.alter_table import AlterTable
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.create_table import CreateTable
from clock.storage.data_source.data_sources.sqlite.sql.statement.executor import StatementExecutor
from clock.storage.data_source.data_sources.sqlite.sql.statement.statement import SingleSqlStatement, SqlStatement


class SqliteStorageComponent:
    def __init__(self, name: str, version: int):
        self.name = name
        self.version = version
        self.tables = []
        self.connection = None  # type: Connection

    def managed_tables(self, *tables: Table):
        self.tables.extend(tables)

    def set_connection(self, connection: Connection):
        self.connection = connection

    def create(self):
        for table in self.tables:
            create_statement = CreateTable().from_definition(table).build()
            self.statement(create_statement).execute()

    def statement(self, statement: SqlStatement):
        return StatementExecutor(self.connection, statement)

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
        alter_table = AlterTable().table(Table(table))
        alter_table.add_columns(*(Column(*column.split(" ")) for column in columns))
        self.statement(alter_table).execute()

    def sql(self, sql: str, *qmark_params, **named_params):
        statement = SingleSqlStatement(sql)
        return self.statement(statement).execute(*qmark_params, **named_params)

    def _sql(self, sql: str, params=()):
        """
        :deprecated: use self.sql instead
        """
        statement = SingleSqlStatement(sql)
        return self.statement(statement).execute_for_params(params).cursor

    @staticmethod
    def _empty_if_none(field: str):
        return field if field is not None else ""
