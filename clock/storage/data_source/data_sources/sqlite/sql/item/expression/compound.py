from typing import Union, Any

from clock.storage.data_source.data_sources.sqlite.sql.item.expression.base import Expression
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.parser import ExpressionParser


OPERATOR_EQUAL = "="


class CompoundExpression(Expression):
    def str(self):
        raise NotImplementedError()

    @staticmethod
    def wrap(expr):
        return ExpressionParser.parse(expr)


class Condition(CompoundExpression):
    def __init__(self, left: Union[Expression, Any], operator: str, right: Union[Expression, Any]):
        self.left = self.wrap(left)
        self.operator = operator
        self.right = self.wrap(right)

    def str(self):
        return "{left} {operator} {right}"\
            .format(left=self.left.str(), operator=self.operator, right=self.right.str())
