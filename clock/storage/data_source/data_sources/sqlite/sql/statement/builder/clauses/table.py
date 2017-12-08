from clock.storage.data_source.data_sources.sqlite.sql.item.table import Table
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.clauses.base import BaseClause


class TableClause(BaseClause):
    def __init__(self):
        super().__init__()
        self._table = None

    def table(self, table: Table):
        self._table = table.str()
        return self
