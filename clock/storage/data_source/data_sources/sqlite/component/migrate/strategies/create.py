from clock.storage.data_source.data_sources.sqlite.component.component import SqliteStorageComponent
from clock.storage.data_source.data_sources.sqlite.component.migrate.exception import SqliteComponentMigratorException
from clock.storage.data_source.data_sources.sqlite.component.migrate.strategy import SqliteMigrationStrategy


class SqliteCreateMigration(SqliteMigrationStrategy):
    def migrate(self):
        migrate_func = self.get_migrate_func()
        if not self.is_compatible(migrate_func, number_of_args=0):
            raise NoValidCreateFunctionException(self.component, self.migration_type)
        self.do_migration(migrate_func, self.new_version)


class NoValidCreateFunctionException(SqliteComponentMigratorException):
    def __init__(self, component: SqliteStorageComponent, migration_type: str):
        super().__init__(
            component, migration_type,
            "create function not found or is not valid"
        )
