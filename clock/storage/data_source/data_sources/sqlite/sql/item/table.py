from collections import defaultdict

from clock.storage.data_source.data_sources.sqlite.sql.item.base import NamedItem
from clock.storage.data_source.data_sources.sqlite.sql.item.column import Column


class Table(NamedItem):
    def __init__(self, name: str):
        super().__init__(name)
        self.columns = ColumnList()
        self.column = self.columns.add


class ColumnList:
    def __init__(self):
        self._columns = []
        self._versions = defaultdict(list)

    def add(self, column: Column, version: int = 1):
        self._columns.append(column)
        self._versions[version].append(column)

    def get_all(self):
        return self._columns

    def get_with_version(self, version: int):
        return self._versions[version]
