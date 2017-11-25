from clock.storage.data_source.data_sources.sqlite.sql.item.column import Column
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.base import Expression


class Literal(Expression):
    def __init__(self, literal: str):
        self.literal = literal

    def str(self):
        return self.literal


class ColumnName(Expression):
    def __init__(self, column: Column):
        self.column = column

    def str(self):
        return self.column.name
