from clock.storage.data_source.data_sources.sqlite.sql.item.expression.compound.base import CompoundExpression
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.parser import EXPRESSION_TYPE


DEFAULT_SEPARATOR = ", "
DEFAULT_BEFORE = ""
DEFAULT_AFTER = ""


class ExpressionList(CompoundExpression):
    def __init__(self, *expressions: EXPRESSION_TYPE, separator: str = DEFAULT_SEPARATOR,
                 before: str = DEFAULT_BEFORE, after: str = DEFAULT_AFTER):
        self.expressions = [self.parse(expr) for expr in expressions]
        self.separator = separator
        self.before = before
        self.after = after

    def str(self):
        expressions = (
            "{expr}".format(expr=expr.str())
            for expr in self.expressions
        )
        expressions = self.separator.join(expressions)
        return "{before}{expressions}{after}"\
            .format(before=self.before, expressions=expressions, after=self.after)
