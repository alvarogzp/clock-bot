from typing import Union, Any

from clock.storage.data_source.data_sources.sqlite.sql.item.base import SqlItem
from clock.storage.data_source.data_sources.sqlite.sql.item.column import Column
from clock.storage.data_source.data_sources.sqlite.sql.util.column import ColumnUtil


OPERATOR_EQUAL = "="


class Expression(SqlItem):
    def __init__(self, value: Union[str, Column]):
        self.value = value

    def str(self):
        return ColumnUtil.name_if_column(self.value)


class Condition(Expression):
    def __init__(self, left: Union[Expression, Any], operator: str, right: Union[Expression, Any]):
        super().__init__("")  # value is not used
        self.left = self._wrap_if_not_expression(left)
        self.operator = operator
        self.right = self._wrap_if_not_expression(right)

    @staticmethod
    def _wrap_if_not_expression(value):
        if isinstance(value, Expression):
            return value
        return Expression(value)

    def str(self):
        return "{left} {operator} {right}"\
            .format(left=self.left.str(), operator=self.operator, right=self.right.str())
