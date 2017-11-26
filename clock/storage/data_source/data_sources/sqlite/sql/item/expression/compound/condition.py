from clock.storage.data_source.data_sources.sqlite.sql.item.constants.operator import Operator
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.compound.base import CompoundExpression
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.parser import EXPRESSION_TYPE


class BaseCondition(CompoundExpression):
    def __init__(self, operator: Operator, *expressions: EXPRESSION_TYPE):
        self.operator = operator
        self.expressions = [self.parse(expr) for expr in expressions]

    def str(self):
        operator = " {operator} ".format(operator=self.operator.str())
        expressions = (
            "{expr}".format(expr=expr.str())
            for expr in self.expressions
        )
        conditions = operator.join(expressions)
        return "({conditions})".format(conditions=conditions)


class Condition(BaseCondition):
    def __init__(self, left: EXPRESSION_TYPE, operator: Operator, right: EXPRESSION_TYPE):
        super().__init__(operator, left, right)
