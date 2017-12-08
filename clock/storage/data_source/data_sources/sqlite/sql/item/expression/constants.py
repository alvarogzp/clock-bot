from clock.storage.data_source.data_sources.sqlite.sql.item.expression.simple import Literal


NULL = Literal("null")

CURRENT_UNIX_TIMESTAMP = Literal("strftime('%s', 'now')")
