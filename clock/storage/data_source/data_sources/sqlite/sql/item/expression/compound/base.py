from clock.storage.data_source.data_sources.sqlite.sql.item.expression.base import Expression
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.parser import ExpressionParser


class CompoundExpression(Expression):
    def str(self):
        raise NotImplementedError()

    @staticmethod
    def parse(expr):
        return ExpressionParser.parse(expr)
