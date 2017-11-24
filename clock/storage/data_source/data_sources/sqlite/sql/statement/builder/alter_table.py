from clock.storage.data_source.data_sources.sqlite.sql.item.column import Column
from clock.storage.data_source.data_sources.sqlite.sql.item.table import Table
from clock.storage.data_source.data_sources.sqlite.sql.schema.table import TableSchema
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.base import StatementBuilder


class AlterTableBuilder(StatementBuilder):
    """
    IMPORTANT:
    Table name and column definitions are added to the sql statement in an unsafe way!
    So, untrusted input MUST NOT be passed to them.
    Their values should ideally be static string literals.
    If computed at runtime, they MUST come from a TOTALLY trusted source (like another module string constant
    or an admin-controlled configuration value).
    """

    def __init__(self):
        super().__init__(multiple_statements=True)
        self._table = None
        self._columns = []

    def table(self, table: Table):
        self._table = table.str()
        return self

    def add_column(self, column: Column):
        self._columns.append(column.str())
        return self

    def from_schema(self, schema: TableSchema, version: int):
        """Add all columns from the schema added in the specified version"""
        self.table(schema.table)
        for column in schema.columns.get_with_version(version):
            self.add_column(column)
        return self

    def build_sql(self):
        return [
            "alter table {table} add column {column}".format(table=self._table, column=column)
            for column in self._columns
        ]
