from clock.storage.data_source.data_sources.sqlite.sql.item.base import NamedItem


class Type(NamedItem):
    pass


INTEGER = Type("integer")
TEXT = Type("text")
REAL = Type("real")
