from sqlite3 import Connection


class SqliteStorageComponent:
    def __init__(self, connection: Connection):
        self.connection = connection

    def init(self):
        raise NotImplementedError()

    def _sql(self, sql: str, params=()):
        return self.connection.execute(sql, params)
