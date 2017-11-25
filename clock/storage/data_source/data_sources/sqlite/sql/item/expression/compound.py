from clock.storage.data_source.data_sources.sqlite.sql.item.constants.operator import Operator
from clock.storage.data_source.data_sources.sqlite.sql.item.constants.type import Type
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.base import Expression
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.parser import ExpressionParser, EXPRESSION_TYPE


class CompoundExpression(Expression):
    def str(self):
        raise NotImplementedError()

    @staticmethod
    def parse(expr):
        return ExpressionParser.parse(expr)


class Condition(CompoundExpression):
    def __init__(self, left: EXPRESSION_TYPE, operator: Operator, right: EXPRESSION_TYPE):
        self.left = self.parse(left)
        self.operator = operator
        self.right = self.parse(right)

    def str(self):
        return "{left} {operator} {right}"\
            .format(left=self.left.str(), operator=self.operator.str(), right=self.right.str())


class Cast(CompoundExpression):
    def __init__(self, expr: EXPRESSION_TYPE, type: Type):
        self.expr = self.parse(expr)
        self.type = type

    def str(self):
        return "cast({expr} as {type})".format(expr=self.expr.str(), type=self.type.str())
