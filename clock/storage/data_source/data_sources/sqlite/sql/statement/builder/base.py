import copy

from clock.storage.data_source.data_sources.sqlite.sql.statement.statement import CompoundSqlStatement, \
    SingleSqlStatement


class StatementBuilder:
    def __init__(self):
        self.multiple_statements = False

    def build_sql(self):
        raise NotImplementedError()

    def build(self):
        sql = self.build_sql()
        if self.multiple_statements:
            return CompoundSqlStatement.from_sql(sql)
        return SingleSqlStatement(sql)

    def copy(self):
        """
        Return a copy of the builder with the same state.
        Further modifications to either the original or the copy won't be seen by the other.
        """
        return copy.copy(self)

    @staticmethod
    def _not_none(clause):
        return clause is not None
