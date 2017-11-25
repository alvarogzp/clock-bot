from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.clauses.base import BaseClause


class WhereClause(BaseClause):
    def __init__(self):
        super().__init__()
        self._where = None

    def where(self, expr: str):
        self._where = "where {expr}".format(expr=expr)  # unsafe formatting
        return self
