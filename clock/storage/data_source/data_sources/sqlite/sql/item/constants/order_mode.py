from clock.storage.data_source.data_sources.sqlite.sql.item.base import NamedItem


class OrderMode(NamedItem):
    pass


ORDER_ASC = OrderMode("asc")
ORDER_DESC = OrderMode("desc")
