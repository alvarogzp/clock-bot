from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.base import StatementBuilder
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.clauses.columns import ColumnsClause
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.clauses.table import TableClause
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.select import Select


class Insert(TableClause, ColumnsClause, StatementBuilder):
    def __init__(self):
        super().__init__()
        self._values = None
        self._select = None

    def values(self, *values: str):
        self._values = ", ".join(values)

    def select(self, select: Select):
        self._select = select.build_sql()

    def build_sql(self):
        columns = ", ".join(self._columns_names)
        sql = "insert into {table} ({columns})".format(table=self._table, columns=columns)
        if self._not_none(self._values):
            sql += " values ({values})".format(values=self._values)
        elif self._not_none(self._select):
            sql += " {select}".format(select=self._select)
        return sql
