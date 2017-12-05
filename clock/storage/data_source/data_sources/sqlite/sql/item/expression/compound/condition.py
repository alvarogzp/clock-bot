from clock.storage.data_source.data_sources.sqlite.sql.item.constants.operator import Operator
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.compound.list.generic import ExpressionList
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.parser import EXPRESSION_TYPE


class BaseCondition(ExpressionList):
    def __init__(self, operator: Operator, *expressions: EXPRESSION_TYPE):
        super().__init__(*expressions, separator=self._separator(operator), before="(", after=")")

    @staticmethod
    def _separator(operator: Operator):
        return " {operator} ".format(operator=operator.str())


class Condition(BaseCondition):
    def __init__(self, left: EXPRESSION_TYPE, operator: Operator, right: EXPRESSION_TYPE):
        super().__init__(operator, left, right)


class MultipleCondition(BaseCondition):
    pass
