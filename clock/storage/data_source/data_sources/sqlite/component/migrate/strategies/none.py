from clock.storage.data_source.data_sources.sqlite.component.migrate.strategy import SqliteMigrationStrategy


class SqliteNoMigration(SqliteMigrationStrategy):
    def migrate(self):
        # nothing to do
        pass
