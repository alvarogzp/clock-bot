from clock.storage.data_source.data_sources.sqlite.sql.item.base import SimpleItem


class OrderMode(SimpleItem):
    pass


ORDER_ASC = OrderMode("asc")
ORDER_DESC = OrderMode("desc")
