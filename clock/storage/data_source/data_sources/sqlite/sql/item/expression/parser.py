from typing import Union

from clock.storage.data_source.data_sources.sqlite.sql.item.column import Column
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.base import Expression
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.simple import ColumnName, Literal


EXPRESSION_TYPE = Union[Expression, Column, str, int]


class ExpressionParser:
    @staticmethod
    def parse(expr: EXPRESSION_TYPE):
        if isinstance(expr, Expression):
            return expr
        elif isinstance(expr, Column):
            return ColumnName(expr)
        elif isinstance(expr, (str, int)):
            return Literal(expr)
        raise Exception("could not parse the expression")
