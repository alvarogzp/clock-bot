from sqlite3 import OperationalError

from clock.storage.data_source.data_sources.sqlite.component.component import SqliteStorageComponent


class VersionInfoSqliteComponent(SqliteStorageComponent):
    """
    Take special care with updating the version of this component,
    as its migrations may be problematic.
    To avoid errors, they should be as direct as possible.
    """

    version = 1

    def __init__(self):
        super().__init__("version_info", self.version)
        self.initialized = False

    def migrate_if_necessary(self, version_info):
        result = super().migrate_if_necessary(version_info)
        self.initialized = True
        return result

    def create(self):
        self._sql("create table version_info ("
                  "component text primary key not null,"
                  "version integer"
                  ")")

    def set_version(self, component: str, version: int):
        self._sql("insert or replace into version_info "
                  "(component, version) "
                  "values (?, ?)",
                  (component, version))

    def get_version(self, component: str):
        try:
            row = self._sql("select version from version_info "
                            "where component = ?",
                            (component,)).fetchone()
        except OperationalError as e:
            if component == self.name and not self.initialized:
                # if the version of this module is being checked and it has not yet being initialized
                # it could fail as the table may not yet exist or has not been migrated from a previous
                # version
                row = None
            else:
                # if the error is for another reason, let it propagate
                raise e
        if row is not None:
            return row["version"]
