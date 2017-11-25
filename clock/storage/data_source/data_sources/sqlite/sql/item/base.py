class SqlItem:
    def str(self):
        raise NotImplementedError()


class StringItem(SqlItem):
    def __init__(self, string: str):
        self.string = string

    def str(self):
        return self.string


class NamedItem(StringItem):
    def __init__(self, name: str):
        super().__init__(name)
