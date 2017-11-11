from clock.storage.data_source.data_sources.sqlite.component.component import SqliteStorageComponent


class SqliteComponentMigratorException(Exception):
    def __init__(self, component: SqliteStorageComponent, migration_type: str, message: str):
        super().__init__(
            "Component '{name}' {type} migration failed with error: {message}. "
            "Component was not migrated. "
            "Unexpected things may happen."
            .format(name=component.name, type=migration_type, message=message)
        )
