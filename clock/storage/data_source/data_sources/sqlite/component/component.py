from sqlite3 import Connection


class SqliteStorageComponent:
    def __init__(self):
        self.connection = None  # type: Connection

    def set_connection(self, connection: Connection):
        self.connection = connection

    def init(self):
        raise NotImplementedError()

    def _sql(self, sql: str, params=()):
        return self.connection.execute(sql, params)

    def sql(self, sql: str, *params):
        return self.connection.execute(sql, params)

    @staticmethod
    def _empty_if_none(field: str):
        return field if field is not None else ""
