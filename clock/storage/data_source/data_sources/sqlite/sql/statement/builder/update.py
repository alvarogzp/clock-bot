from clock.storage.data_source.data_sources.sqlite.sql.item.column import Column
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.parser import EXPRESSION_TYPE, ExpressionParser
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.base import StatementBuilder
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.clauses.table import TableClause
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.clauses.where import WhereClause


class Update(TableClause, WhereClause, StatementBuilder):
    def __init__(self):
        super().__init__()
        self._set = None

    def set(self, column: Column, expr: EXPRESSION_TYPE):
        expr = ExpressionParser.parse(expr)
        self._set = "set {column_name} = {expr}".format(column_name=column.name, expr=expr.str())
        return self

    def build_sql(self):
        sql = "update {table} {set}".format(table=self._table, set=self._set)
        if self._not_none(self._where):
            sql += " {where}".format(where=self._where)
        return sql
