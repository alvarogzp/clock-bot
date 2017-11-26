from clock.storage.data_source.data_sources.sqlite.sql.item.constants.type import Type
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.compound.base import CompoundExpression
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.parser import EXPRESSION_TYPE


class Cast(CompoundExpression):
    def __init__(self, expr: EXPRESSION_TYPE, type: Type):
        self.expr = self.parse(expr)
        self.type = type

    def str(self):
        return "cast({expr} as {type})".format(expr=self.expr.str(), type=self.type.str())
