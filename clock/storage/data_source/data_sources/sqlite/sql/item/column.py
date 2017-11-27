from clock.storage.data_source.data_sources.sqlite.sql.item.base import SqlItem
from clock.storage.data_source.data_sources.sqlite.sql.item.constants.type import Type, INTEGER


class Column(SqlItem):
    def __init__(self, name: str, type: Type, *constraints: str):
        self.name = name
        self.type = type
        self.constraints = constraints

    def str(self):
        column = "{name} {type}".format(name=self.name, type=self.type.str())
        if self.constraints:
            constraints = " ".join(self.constraints)
            column += " {constraints}".format(constraints=constraints)
        return column


ROWID = Column("rowid", INTEGER, "primary key", "not null")
