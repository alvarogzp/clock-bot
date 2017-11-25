from typing import Union

from clock.storage.data_source.data_sources.sqlite.sql.item.column import Column
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.base import StatementBuilder
from clock.storage.data_source.data_sources.sqlite.sql.item.table import Table
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.clauses.where import WhereClause
from clock.storage.data_source.data_sources.sqlite.sql.util.column import ColumnUtil


class SelectBuilder(WhereClause, StatementBuilder):
    """
    IMPORTANT:
    All arguments are added to the sql statement in an unsafe way!
    So, untrusted input MUST NOT be passed to them.
    Their values should ideally be static string literals.
    If computed at runtime, they MUST come from a TOTALLY trusted source (like another module string constant
    or an admin-controlled configuration value).
    """

    def __init__(self):
        super().__init__()
        self._fields = "*"
        self._from = None
        self._group_by = None
        self._order_by = None
        self._limit = None
        self._other = None

    def fields(self, *fields: Union[str, Column]):
        self._fields = ", ".join((ColumnUtil.name_if_column(field) for field in fields))
        return self

    def table(self, table: Table):
        self._from = "from {table}".format(table=table.str())  # unsafe formatting
        return self

    def group_by(self, expr: str):
        self._group_by = "group by {expr}".format(expr=expr)  # unsafe formatting
        return self

    def order_by(self, order_by: str):
        self._order_by = "order by {order_by}".format(order_by=order_by)  # unsafe formatting
        return self

    def limit(self, number: int):
        self._limit = "limit {number}".format(number=number)  # unsafe formatting
        return self

    def other(self, clauses: str):
        self._other = clauses  # unsafe formatting
        return self

    def build_sql(self):
        select = "select {fields}".format(fields=self._fields)  # unsafe formatting
        clauses = [
            select,
            self._from,
            self._where,
            self._group_by,
            self._order_by,
            self._limit,
            self._other
        ]
        clauses = filter(self._not_none, clauses)
        return " ".join(clauses)
