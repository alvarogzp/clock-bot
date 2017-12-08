from clock.storage.data_source.data_sources.sqlite.sql.item.base import NamedItem


class Operator(NamedItem):
    pass


# operators ordered by precedence (from highest to lowest)
# an empty line means a precedence jump

EQUAL = Operator("=")
IS = Operator("is")

AND = Operator("and")

OR = Operator("or")
