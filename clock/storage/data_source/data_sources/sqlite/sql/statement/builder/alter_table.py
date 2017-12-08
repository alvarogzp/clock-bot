from clock.storage.data_source.data_sources.sqlite.sql.item.table import Table
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.base import StatementBuilder
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.clauses.columns import ColumnsClause
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.clauses.table import TableClause


class AlterTable(TableClause, ColumnsClause, StatementBuilder):
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
        self.multiple_statements = True

    def from_definition(self, table: Table, version: int):
        """Add all columns from the table added in the specified version"""
        self.table(table)
        self.add_columns(*table.columns.get_with_version(version))
        return self

    def build_sql(self):
        return [
            "alter table {table} add column {column}".format(table=self._table, column=column)
            for column in self._columns_definitions
        ]
