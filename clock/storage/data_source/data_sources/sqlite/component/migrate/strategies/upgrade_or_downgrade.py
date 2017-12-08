import inspect

from clock.storage.data_source.data_sources.sqlite.component.component import SqliteStorageComponent
from clock.storage.data_source.data_sources.sqlite.component.migrate.exception import SqliteComponentMigratorException
from clock.storage.data_source.data_sources.sqlite.component.migrate.strategy import SqliteMigrationStrategy


class SqliteUpgradeOrDowngradeMigration(SqliteMigrationStrategy):
    def migrate(self):
        for func, to_version in self.get_migrate_path():
            self.do_migration(func, to_version)

    def get_migrate_path(self):
        try:
            return self._chained_migrate_path()
        except NoMigratePathFoundException as e:
            generic_migrate_path = self._generic_migrate_path()
            if generic_migrate_path is not None:
                return generic_migrate_path
            raise e

    def _generic_migrate_path(self):
        # if a generic migrate function exists, call it passing the old and new versions
        generic_migrate_func = self.get_migrate_func()
        if self.is_compatible(generic_migrate_func, number_of_args=2):
            return [
                (lambda: generic_migrate_func(self.old_version, self.new_version), self.new_version)
            ]

    def _chained_migrate_path(self):
        # build the most direct path to migrate from old to new version
        migrate_path = []
        current_version = self.old_version
        while current_version != self.new_version:
            func, current_version = self._get_best_migrate_from(current_version)
            migrate_path.append((func, current_version))
        return migrate_path

    def _get_best_migrate_from(self, old_version: int):
        # initialize the best distance to the distance from the old version to the destination version
        # we are searching for migration functions with a distance lower than this, so that we get closer
        # to the destination version
        best_distance = abs(self.new_version - old_version)
        best_version = None
        best_func = None
        for func, new_version in self._get_available_migrates_from(old_version):
            if self._is_between_migration_versions(new_version):
                distance = abs(self.new_version - new_version)
                if distance < best_distance:
                    best_distance = distance
                    best_version = new_version
                    best_func = func
        if best_func is None:
            # no func to get closer from old_version to the destination version (without passing it) was found
            self._raise_no_path_found()
        return best_func, best_version

    def _get_available_migrates_from(self, version: int):
        migrate_func_start_name = "{type}_from_{old}_to_".format(type=self.migration_type, old=version)
        # iterate over all members of the component
        for name, value in inspect.getmembers(self.component):
            if name.startswith(migrate_func_start_name) and self.is_compatible(value, number_of_args=0):
                # it matches the name start and is a compatible function
                # try to get the destination version this migration function gives us to
                migrates_to_version = self._get_destination_version(name, len(migrate_func_start_name))
                if migrates_to_version is not None:
                    # got a valid destination version, yield it
                    yield value, migrates_to_version

    @staticmethod
    def _get_destination_version(migration_func_name: str, destination_version_starts_at: int):
        try:
            return int(migration_func_name[destination_version_starts_at:])
        except ValueError:
            # not a valid migration function
            return

    def _is_between_migration_versions(self, version: int):
        return self.old_version <= version <= self.new_version or \
               self.old_version >= version >= self.new_version

    def _raise_no_path_found(self):
        raise NoMigratePathFoundException(
            self.component, self.migration_type, self.old_version, self.new_version
        )


class NoMigratePathFoundException(SqliteComponentMigratorException):
    def __init__(self, component: SqliteStorageComponent, migration_type: str, old_version: int, new_version: int):
        super().__init__(
            component, migration_type,
            "no valid path to fully {migration_type} from version {old} to {new} was found"
            .format(migration_type=migration_type, old=old_version, new=new_version)
        )
