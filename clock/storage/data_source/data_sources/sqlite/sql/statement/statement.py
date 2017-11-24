from sqlite3 import Connection
from typing import List

from clock.storage.data_source.data_sources.sqlite.sql.result.result import SqlResult


class SqlStatement:
    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, *qmark_params, **named_params):
        params = self.__get_params(qmark_params, named_params)
        return self.execute_for_params(params)

    @staticmethod
    def __get_params(qmark_params: tuple, named_params: dict):
        there_are_qmark_params = len(qmark_params) > 0
        there_are_named_params = len(named_params) > 0
        if there_are_qmark_params and there_are_named_params:
            raise Exception("all params must be of the same type (qmark or named) for an individual statement")
        params = qmark_params
        if there_are_named_params:
            params = named_params
        return params

    def execute_for_params(self, params) -> SqlResult:
        raise NotImplementedError()

    def _execute_statement(self, statement: str, params):
        return SqlResult(self.connection.execute(statement, params))


class SingleSqlStatement(SqlStatement):
    def __init__(self, connection: Connection, statement: str):
        super().__init__(connection)
        self.statement = statement

    def execute_for_params(self, params):
        return self._execute_statement(self.statement, params)


class CompoundSqlStatement(SqlStatement):
    def __init__(self, connection: Connection, statements: List[str]):
        super().__init__(connection)
        self.statements = statements

    def execute_for_params(self, params):
        # do not return anything
        for statement in self.statements:
            self._execute_statement(statement, params)
