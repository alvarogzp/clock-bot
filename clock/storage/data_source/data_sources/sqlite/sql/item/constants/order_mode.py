from clock.storage.data_source.data_sources.sqlite.sql.item.base import NamedItem


class OrderMode(NamedItem):
    pass


ASC = OrderMode("asc")
DESC = OrderMode("desc")
