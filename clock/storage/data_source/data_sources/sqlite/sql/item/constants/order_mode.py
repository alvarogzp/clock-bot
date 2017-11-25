from clock.storage.data_source.data_sources.sqlite.sql.item.base import SqlItem


class OrderMode(SqlItem):
    def __init__(self, mode: str):
        self.mode = mode

    def str(self):
        return self.mode


ORDER_ASC = OrderMode("asc")
ORDER_DESC = OrderMode("desc")
