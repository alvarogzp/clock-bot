from sqlite_framework.log.logger import SqliteLogger

from clock.log.api import LogApi


class LogApiSqliteLogger(SqliteLogger):
    def __init__(self, logger: LogApi):
        self.logger = logger

    def migration(self, component: str, migration_type: str, old_version: int, new_version: int,
                  about_to_migrate_to_version: int):
        self.logger.log_sqlite_component_migration(
            component, migration_type, old_version, new_version, about_to_migrate_to_version
        )
