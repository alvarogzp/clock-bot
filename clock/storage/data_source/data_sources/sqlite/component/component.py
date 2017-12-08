from sqlite3 import Connection

from clock.storage.data_source.data_sources.sqlite.sql.item.table import Table
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.alter_table import AlterTable
from clock.storage.data_source.data_sources.sqlite.sql.statement.builder.create_table import CreateTable
from clock.storage.data_source.data_sources.sqlite.sql.statement.executor import StatementExecutor
from clock.storage.data_source.data_sources.sqlite.sql.statement.statement import SingleSqlStatement, SqlStatement


class SqliteStorageComponent:
    def __init__(self, name: str, version: int):
        self.name = name
        self.version = version
        self.tables = []
        self.connection = None  # type: Connection

    # SETUP METHODS

    def managed_tables(self, *tables: Table):
        self.tables.extend(tables)

    def set_connection(self, connection: Connection):
        self.connection = connection

    # MIGRATION METHODS

    def create(self):
        self.__check_there_are_managed_tables()
        for table in self.tables:
            create_statement = CreateTable().from_definition(table).build()
            self.statement(create_statement).execute()

    def upgrade(self, old_version: int, new_version: int):
        self.__check_there_are_managed_tables()
        if not isinstance(old_version, int) or not isinstance(new_version, int):
            raise Exception("old and new version must be integers")
        version_diff = new_version - old_version
        if version_diff > 1:
            self.upgrade(old_version, new_version-1)
        elif version_diff != 1:
            raise Exception("unexpected version diff: {diff}".format(diff=version_diff))
        self._upgrade_tables(new_version)

    def __check_there_are_managed_tables(self):
        if len(self.tables) == 0:
            raise NotImplementedError(
                "you must override migration methods when no delegating table management to base component"
            )

    def _upgrade_tables(self, version: int):
        for table in self.tables:
            alter_statement = AlterTable().from_definition(table, version).build()
            self.statement(alter_statement).execute()

    # SQL EXECUTION METHODS

    def statement(self, statement: SqlStatement):
        return StatementExecutor(self.connection, statement)

    def sql(self, sql: str, *qmark_params, **named_params):
        """
        :deprecated: use self.statement to execute properly-formatted sql statements
        """
        statement = SingleSqlStatement(sql)
        return self.statement(statement).execute(*qmark_params, **named_params)

    def _sql(self, sql: str, params=()):
        """
        :deprecated: use self.sql instead
        """
        statement = SingleSqlStatement(sql)
        return self.statement(statement).execute_for_params(params).cursor

    # UTIL METHODS

    @staticmethod
    def _empty_if_none(field: str):
        return field if field is not None else ""
