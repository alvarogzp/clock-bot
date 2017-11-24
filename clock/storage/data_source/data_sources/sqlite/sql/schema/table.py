from collections import OrderedDict, defaultdict

from clock.storage.data_source.data_sources.sqlite.sql.item.column import Column
from clock.storage.data_source.data_sources.sqlite.sql.item.table import Table


class TableSchema:
    def __init__(self):
        self.table = None  # type: Table
        self.columns = ColumnListSchema()

    def column(self, column: Column, version: int = 1):
        self.columns.add(column, version)

    def column_from(self, schema: __class__, column_name: str):
        self.columns.add_from(schema.columns, column_name)


class ColumnListSchema:
    def __init__(self):
        self._columns = OrderedDict()
        self._versions = defaultdict(list)

    def add(self, column: Column, version: int):
        self._columns[column.name] = column
        self._versions[version].append(column)

    def add_from(self, columns: __class__, column_name: str):
        column = columns._columns[column_name]
        for version, columns in columns._versions.items():
            if column in columns:
                break
        else:
            raise Exception("original column version was not found")
        self.add(column, version)

    def get_all(self):
        return self._columns.values()

    def get_with_version(self, version: int):
        return self._versions[version]
