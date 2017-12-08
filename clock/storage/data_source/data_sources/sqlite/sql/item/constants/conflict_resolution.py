from clock.storage.data_source.data_sources.sqlite.sql.item.base import NamedItem


class ConflictResolution(NamedItem):
    pass


REPLACE = ConflictResolution("replace")
