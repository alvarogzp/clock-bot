import sqlite3

from clock.storage.data_source.data_sources.sqlite.sql.util.column import ColumnUtil


class ResultRow(sqlite3.Row):
    def __getitem__(self, item):
        item = ColumnUtil.name_if_column(item)
        return super().__getitem__(item)
