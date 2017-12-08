from typing import Union

from clock.storage.data_source.data_sources.sqlite.sql.item.column import Column


class ColumnUtil:
    @staticmethod
    def name_if_column(value: Union[str, Column]):
        if isinstance(value, Column):
            return value.name
        return value
