from sqlite3 import Connection
from typing import Iterable

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

    def select(self, fields: Iterable[str] = ("*",), table: str = None,
               where: str = None, group_by: str = None, order_by: str = None, limit: int = None, other: str = None,
               *qmark_params, **named_params):
        """
        IMPORTANT:
        All arguments except qmark_params and named_params are added to the sql statement in an unsafe way!
        So, untrusted input MUST NOT be passed to them.
        Their values should ideally be static string literals.
        If computed at runtime, they MUST come from a TOTALLY trusted source (like another module string constant
        or an admin-controlled configuration value).

        :deprecated: use self.statement.select() instead
        """
        return self.statement.select()\
            .fields(*fields)\
            .table(Table(table))\
            .where(where)\
            .group_by(group_by)\
            .order_by(order_by)\
            .limit(limit)\
            .other(other)\
            .execute(*qmark_params, **named_params)

    def select_field(self, field: str, *args, **kwargs):
        """
        Return a list with the field values for the query.

        IMPORTANT:
        Same precautions as :func:`select` must be taken.

        :deprecated: use self.statement.select()...execute().map_field() instead
        """
        return self.select(fields=(field,), *args, **kwargs).map_field()

    def select_field_one(self, field: str, *args, **kwargs):
        """
        Return the field value for the first result.

        IMPORTANT:
        Same precautions as :func:`select` must be taken.

        :deprecated: use self.statement.select()...execute().first_field() instead
        """
        return self.select(fields=(field,), *args, **kwargs).first_field()

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
