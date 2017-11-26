from clock.storage.data_source.data_sources.sqlite.sql.item.base import NamedItem


class Operator(NamedItem):
    pass


# operators ordered by precedence (from highest to lowest)
# an empty line means a precedence jump

OPERATOR_EQUAL = Operator("=")
OPERATOR_IS = Operator("is")

OPERATOR_AND = Operator("and")

OPERATOR_OR = Operator("or")
