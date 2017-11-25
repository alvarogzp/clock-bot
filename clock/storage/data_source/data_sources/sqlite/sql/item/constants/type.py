from clock.storage.data_source.data_sources.sqlite.sql.item.base import SqlItem


class Type(SqlItem):
    def __init__(self, name: str):
        self.name = name

    def str(self):
        return self.name


TYPE_INTEGER = Type("integer")
TYPE_TEXT = Type("text")
TYPE_REAL = Type("real")
