import sqlite3

from clock.storage.data_source.data_sources.sqlite.sql.item.column import Column


class ResultRow(sqlite3.Row):
    def __getitem__(self, item):
        if isinstance(item, Column):
            item = item.name
        return super().__getitem__(item)
