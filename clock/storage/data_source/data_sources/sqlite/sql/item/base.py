class SqlItem:
    def str(self):
        raise NotImplementedError()


class SimpleItem(SqlItem):
    def __init__(self, name: str):
        self.name = name

    def str(self):
        return self.name
