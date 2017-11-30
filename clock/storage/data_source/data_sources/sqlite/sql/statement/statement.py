from typing import Iterable, Sequence


class SqlStatement:
    pass


class SingleSqlStatement(SqlStatement):
    def __init__(self, statement: str):
        self.statement = statement

    def get_sql(self):
        return self.statement


class CompoundSqlStatement(SqlStatement):
    def __init__(self, statements: Sequence[SqlStatement]):
        self.statements = statements

    def get_statements(self):
        return self.statements

    @staticmethod
    def from_sql(sql_list: Iterable[str]):
        return CompoundSqlStatement([SingleSqlStatement(sql) for sql in sql_list])

    @staticmethod
    def from_statements(*statements: SqlStatement):
        return CompoundSqlStatement(statements)
