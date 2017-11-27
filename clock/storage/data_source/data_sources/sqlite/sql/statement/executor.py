from sqlite3 import Connection

from clock.storage.data_source.data_sources.sqlite.sql.result.result import SqlResult
from clock.storage.data_source.data_sources.sqlite.sql.statement.statement import SqlStatement, SingleSqlStatement, \
    CompoundSqlStatement


class StatementExecutor:
    def __init__(self, connection: Connection, statement: SqlStatement):
        self.connection = connection
        self.statement = statement

    def execute(self, *qmark_params, **named_params):
        params = self._get_params(qmark_params, named_params)
        return self.execute_for_params(params)

    def execute_for_params(self, params):
        return self._execute(params)

    @staticmethod
    def _get_params(qmark_params: tuple, named_params: dict):
        there_are_qmark_params = len(qmark_params) > 0
        there_are_named_params = len(named_params) > 0
        if there_are_qmark_params and there_are_named_params:
            raise Exception("all params must be of the same type (qmark or named) for an individual statement")
        params = qmark_params
        if there_are_named_params:
            params = named_params
        return params

    def _execute(self, params):
        raise NotImplementedError()

    def _execute_sql(self, sql: str, params):
        return SqlResult(self.connection.execute(sql, params))


class SingleStatementExecutor(StatementExecutor):
    def _execute(self, params):
        return self._execute_sql(self.statement.get_sql(), params)


class CompoundStatementExecutor(StatementExecutor):
    def _execute(self, params):
        # do not return anything
        for sql in self.statement.get_sql():
            self._execute_sql(sql, params)


class StatementExecutorFactory:
    def __init__(self, connection: Connection):
        self.connection = connection

    def executor(self, statement: SqlStatement):
        if isinstance(statement, SingleSqlStatement):
            return SingleStatementExecutor(self.connection, statement)
        elif isinstance(statement, CompoundSqlStatement):
            return CompoundStatementExecutor(self.connection, statement)
        raise Exception("unexpected statement type")
