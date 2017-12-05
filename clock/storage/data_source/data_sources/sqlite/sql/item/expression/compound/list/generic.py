from clock.storage.data_source.data_sources.sqlite.sql.item.expression.compound.base import CompoundExpression
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.compound.list.parsed import ParsedExpressionList, \
    DEFAULT_SEPARATOR, DEFAULT_BEFORE, DEFAULT_AFTER
from clock.storage.data_source.data_sources.sqlite.sql.item.expression.parser import EXPRESSION_TYPE


class ExpressionList(ParsedExpressionList, CompoundExpression):
    def __init__(self, *expressions: EXPRESSION_TYPE, separator: str = DEFAULT_SEPARATOR,
                 before: str = DEFAULT_BEFORE, after: str = DEFAULT_AFTER):
        parsed_expressions = (self.parse(expr) for expr in expressions)
        super().__init__(*parsed_expressions, separator=separator, before=before, after=after)
