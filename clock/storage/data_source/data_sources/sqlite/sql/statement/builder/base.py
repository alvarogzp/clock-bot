from sqlite3 import Connection

from clock.storage.data_source.data_sources.sqlite.sql.statement.statement import CompoundSqlStatement, \
    SingleSqlStatement


class StatementBuilder:
    def __init__(self):
        self.multiple_statements = False
        self.connection = None  # type: Connection

    def set_connection(self, connection: Connection):
        self.connection = connection

    def build_sql(self):
        raise NotImplementedError()

    def build(self):
        sql = self.build_sql()
        if self.multiple_statements:
            return CompoundSqlStatement(self.connection, sql)
        return SingleSqlStatement(self.connection, sql)

    def execute(self, *args, **kwargs):
        """Convenience method that builds and executes the statement in a single call"""
        return self.build().execute(*args, **kwargs)

    @staticmethod
    def _not_none(clause):
        return clause is not None
