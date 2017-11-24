from sqlite3 import Connection
from typing import Iterable

from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.factory import StatementBuilderFactory
from clock.storage.data_source.data_sources.sqlite.sql.statement.statement import SingleSqlStatement


class SqliteStorageComponent:
    def __init__(self, name: str, version: int):
        self.name = name
        self.version = version
        self.connection = None  # type: Connection
        self.statement = None  # type: StatementBuilderFactory

    def set_connection(self, connection: Connection):
        self.connection = connection
        self.statement = StatementBuilderFactory(connection)

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
        """
        clauses = []
        fields = ", ".join(fields)
        clauses.append("select {fields}".format(fields=fields))  # unsafe formatting
        if table is not None:
            clauses.append("from {table}".format(table=table))  # unsafe formatting
        if where is not None:
            clauses.append("where {where}".format(where=where))  # unsafe formatting
        if group_by is not None:
            clauses.append("group by {group_by}".format(group_by=group_by))  # unsafe formatting
        if order_by is not None:
            clauses.append("order by {order_by}".format(order_by=order_by))  # unsafe formatting
        if limit is not None:
            clauses.append("limit {limit}".format(limit=limit))  # unsafe formatting
        if other is not None:
            clauses.append("{other}".format(other=other))  # unsafe formatting
        sql = " ".join(clauses)
        return self.sql(sql, *qmark_params, **named_params)

    def select_field(self, field: str, *args, **kwargs):
        """
        Return a list with the field values for the query.

        IMPORTANT:
        Same precautions as :func:`select` must be taken.
        """
        return (row[field] for row in self.select(fields=(field,), *args, **kwargs))

    def select_field_one(self, field: str, *args, **kwargs):
        """
        Return the field value for the first result.

        IMPORTANT:
        Same precautions as :func:`select` must be taken.
        """
        row = self.select(fields=(field,), *args, **kwargs).fetchone()
        if row:
            return row[field]

    def add_columns(self, table: str, *columns: str):
        """
        IMPORTANT:
        Table name and column definitions are added to the sql statement in an unsafe way!
        So, untrusted input MUST NOT be passed to them.
        Their values should ideally be static string literals.
        If computed at runtime, they MUST come from a TOTALLY trusted source (like another module string constant
        or an admin-controlled configuration value).
        """
        for column in columns:
            # table name and column definitions cannot be (safely) parametrized by the sqlite engine
            # but as we trust the input, we can format the statement in an unsafe way
            sql = "alter table {table} add column {column}".format(table=table, column=column)
            self.sql(sql)

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
