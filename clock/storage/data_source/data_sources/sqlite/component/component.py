from sqlite3 import Connection

from clock.storage.data_source.data_sources.sqlite.component.components.version_info import VersionInfoSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.migrate.migrator import SqliteComponentMigrator


class SqliteStorageComponent:
    def __init__(self, name: str, version: int):
        self.name = name
        self.version = version
        self.connection = None  # type: Connection

    def set_connection(self, connection: Connection):
        self.connection = connection

    def migrate_if_necessary(self, version_info: VersionInfoSqliteComponent):
        SqliteComponentMigrator(self, version_info).migrate()

    def _sql(self, sql: str, params=()):
        return self.connection.execute(sql, params)

    def sql(self, sql: str, *params):
        return self.connection.execute(sql, params)

    @staticmethod
    def _empty_if_none(field: str):
        return field if field is not None else ""
