from typing import Union

from clock.storage.data_source.data_sources.sqlite.sql.item.base import SqlItem
from clock.storage.data_source.data_sources.sqlite.sql.item.column import Column
from clock.storage.data_source.data_sources.sqlite.sql.util.column import ColumnUtil


class Expression(SqlItem):
    def __init__(self, value: Union[str, Column]):
        self.value = value

    def str(self):
        return ColumnUtil.name_if_column(self.value)
