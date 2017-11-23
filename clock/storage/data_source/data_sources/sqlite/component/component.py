from sqlite3 import Connection


class SqliteStorageComponent:
    def __init__(self, name: str, version: int):
        self.name = name
        self.version = version
        self.connection = None  # type: Connection

    def set_connection(self, connection: Connection):
        self.connection = connection

    def create(self):
        raise NotImplementedError()

    def _add_columns(self, table: str, *columns: str):
        """
        IMPORTANT:
        Table name and column definitions are added to the sql statement in an unsafe way!
        So, untrusted input MUST NOT be passed to them.
        Their values should ideally be static string literals.
        If computed at runtime, they MUST come from a TOTALLY trusted source (like another module string constant
        or an admin-controlled configuration value).
        """
        for column in columns:
            # table name and column definitions cannot be (safely) parametrized by the sqlite engine
            # but as we trust the input, we can format the statement in an unsafe way
            sql = "alter table {table} add column {column}".format(table=table, column=column)
            self.sql(sql)

    def sql(self, sql: str, *qmark_params, **named_params):
        there_are_qmark_params = len(qmark_params) > 0
        there_are_named_params = len(named_params) > 0
        if there_are_qmark_params and there_are_named_params:
            raise Exception("all params must be of the same type (qmark or named) for a single query")
        params = qmark_params
        if there_are_named_params:
            params = named_params
        return self._sql(sql, params)

    def _sql(self, sql: str, params=()):
        return self.connection.execute(sql, params)

    @staticmethod
    def _empty_if_none(field: str):
        return field if field is not None else ""
