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
            return CompoundSqlStatement(sql)
        return SingleSqlStatement(sql)

    @staticmethod
    def _not_none(clause):
        return clause is not None
