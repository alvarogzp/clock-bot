from clock.storage.data_source.data_sources.sqlite.sql.item.base import SqlItem


class Table(SqlItem):
    def __init__(self, name: str):
        self.name = name

    def str(self):
        return self.name
