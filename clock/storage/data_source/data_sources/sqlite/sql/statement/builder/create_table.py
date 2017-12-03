from clock.storage.data_source.data_sources.sqlite.sql.item.table import Table
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.base import StatementBuilder
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.clauses.columns import ColumnsClause
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.clauses.table import TableClause


class CreateTable(TableClause, ColumnsClause, StatementBuilder):
    """
    IMPORTANT:
    Table name and column definitions are added to the sql statement in an unsafe way!
    So, untrusted input MUST NOT be passed to them.
    Their values should ideally be static string literals.
    If computed at runtime, they MUST come from a TOTALLY trusted source (like another module string constant
    or an admin-controlled configuration value).
    """

    def from_definition(self, table: Table):
        self.table(table)
        self.columns(*table.columns.get_all())
        return self

    def build_sql(self):
        columns = ", ".join(self._columns_definitions)
        return "create table {name} ({columns})".format(name=self._table, columns=columns)
