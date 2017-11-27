from clock.storage.data_source.data_sources.sqlite.sql.item.expression.compound.base import CompoundExpression
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.parser import EXPRESSION_TYPE


class ExpressionList(CompoundExpression):
    def __init__(self, *expressions: EXPRESSION_TYPE):
        self.expressions = [self.parse(expr) for expr in expressions]

    def str(self):
        expressions = (
            "{expr}".format(expr=expr.str())
            for expr in self.expressions
        )
        return ", ".join(expressions)
