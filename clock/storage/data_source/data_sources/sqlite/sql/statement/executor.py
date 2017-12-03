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
        return StatementExecution(self.connection, self.statement, params).execute()


class StatementExecution:
    def __init__(self, connection: Connection, statement: SqlStatement, params):
        self.connection = connection
        self.statement = statement
        self.params = params

    def execute(self):
        return self._execute_statement(self.statement)

    def _execute_statement(self, statement: SqlStatement):
        if isinstance(statement, SingleSqlStatement):
            return self._execute_single_statement(statement)
        elif isinstance(statement, CompoundSqlStatement):
            return self._execute_compound_statement(statement)
        elif isinstance(statement, SqlStatement):
            raise Exception("unknown sql statement type")
        raise Exception("expecting a SqlStatement, got: {type}".format(type=type(statement)))

    def _execute_compound_statement(self, statement: CompoundSqlStatement):
        # do not return anything
        for statement in statement.get_statements():
            self._execute_statement(statement)

    def _execute_single_statement(self, statement: SingleSqlStatement):
        sql = statement.get_sql()
        return self._execute_sql(sql)

    def _execute_sql(self, sql: str):
        return SqlResult(self.connection.execute(sql, self.params))
