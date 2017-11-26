from clock.storage.data_source.data_sources.sqlite.sql.item.constants.operator import Operator
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.compound.base import CompoundExpression
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.parser import EXPRESSION_TYPE


class Condition(CompoundExpression):
    def __init__(self, left: EXPRESSION_TYPE, operator: Operator, right: EXPRESSION_TYPE):
        self.left = self.parse(left)
        self.operator = operator
        self.right = self.parse(right)

    def str(self):
        return "({left} {operator} {right})"\
            .format(left=self.left.str(), operator=self.operator.str(), right=self.right.str())
