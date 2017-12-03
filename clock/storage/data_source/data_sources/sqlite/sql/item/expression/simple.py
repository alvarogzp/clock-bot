from clock.storage.data_source.data_sources.sqlite.sql.item.base import StringItem
from clock.storage.data_source.data_sources.sqlite.sql.item.column import Column
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.base import Expression


class Literal(StringItem, Expression):
    def __init__(self, literal):
        super().__init__(str(literal))


class ColumnName(StringItem, Expression):
    def __init__(self, column: Column):
        super().__init__(column.name)
