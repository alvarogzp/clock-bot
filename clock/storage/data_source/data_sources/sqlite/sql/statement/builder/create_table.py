from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.base import StatementBuilder
from clock.storage.data_source.data_sources.sqlite.sql.item.column import Column
from clock.storage.data_source.data_sources.sqlite.sql.item.table import Table


class CreateTableBuilder(StatementBuilder):
    """
    IMPORTANT:
    Table name and column definitions are added to the sql statement in an unsafe way!
    So, untrusted input MUST NOT be passed to them.
    Their values should ideally be static string literals.
    If computed at runtime, they MUST come from a TOTALLY trusted source (like another module string constant
    or an admin-controlled configuration value).
    """

    def __init__(self):
        super().__init__()
        self._table = None
        self._columns = []

    def table(self, table: Table):
        self._table = table.str()
        return self

    def column(self, column: Column):
        self._columns.append(column.str())
        return self

    def build_sql(self):
        columns = ", ".join(self._columns)
        return "create table {name} ({columns})".format(name=self._table, columns=columns)
