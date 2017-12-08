from clock.storage.data_source.data_sources.sqlite.sql.item.base import SqlItem


class Expression(SqlItem):
    def str(self):
        raise NotImplementedError()
