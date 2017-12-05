from typing import Union, Iterable

from clock.storage.data_source.data_sources.sqlite.sql.item.column import Column
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.base import Expression
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.compound.list.generic import ExpressionList
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.simple import ColumnName, Literal


SIMPLE_EXPRESSION_TYPE = Union[Expression, Column, str, int]
EXPRESSION_TYPE = Union[SIMPLE_EXPRESSION_TYPE, Iterable[SIMPLE_EXPRESSION_TYPE]]


class ExpressionParser:
    @staticmethod
    def parse(expr: EXPRESSION_TYPE):
        if isinstance(expr, Expression):
            return expr
        elif isinstance(expr, Column):
            return ColumnName(expr)
        elif isinstance(expr, (str, int)):
            return Literal(expr)
        elif isinstance(expr, Iterable):
            return ExpressionList(*expr)
        raise Exception("could not parse the expression")
