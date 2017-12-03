from clock.storage.data_source.data_sources.sqlite.sql.item.column import Column
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.clauses.base import BaseClause


class ColumnsClause(BaseClause):
    def __init__(self):
        super().__init__()
        self._columns = ()

    @property
    def _columns_definitions(self):
        return (column.str() for column in self._columns)

    @property
    def _columns_names(self):
        return (column.name for column in self._columns)

    def columns(self, *columns: Column):
        self._columns = columns
        return self

    add_columns = columns  # for alter_table, it is a more user-friendly name
