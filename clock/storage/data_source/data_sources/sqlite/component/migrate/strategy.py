from inspect import signature

from clock.log.api import LogApi
from clock.storage.data_source.data_sources.sqlite.component.component import SqliteStorageComponent
from clock.storage.data_source.data_sources.sqlite.component.components.version_info import VersionInfoSqliteComponent


class SqliteMigrationStrategy:
    def __init__(self, component: SqliteStorageComponent, version_info: VersionInfoSqliteComponent, logger: LogApi,
                 migration_type: str, old_version: int, new_version: int):
        self.component = component
        self.version_info = version_info
        self.logger = logger
        self.migration_type = migration_type
        self.old_version = old_version
        self.new_version = new_version

    def migrate(self):
        raise NotImplementedError()

    def do_migration(self, func: callable, to_version: int):
        self._log_migration(to_version)
        func()
        self.version_info.set_version(self.component.name, to_version)

    def _log_migration(self, migrating_to_version: int):
        self.logger.log_sqlite_component_migration(
            self.component.name, self.migration_type, self.old_version, self.new_version, migrating_to_version
        )

    def get_migrate_func(self, name: str = None):
        if name is None:
            # generic migration function, eg. create(), upgrade()
            name = self.migration_type
        return getattr(self.component, name, None)

    @staticmethod
    def is_compatible(func: callable, number_of_args: int):
        return callable(func) and len(signature(func).parameters) == number_of_args
