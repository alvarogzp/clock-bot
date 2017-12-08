from sqlite3 import Cursor


class SqlResult:
    def __init__(self, cursor: Cursor):
        self.cursor = cursor

    def first(self):
        return self.cursor.fetchone()

    def first_field(self):
        first = self.first()
        if first is not None:
            return first[0]

    def map_field(self):
        return (row[0] for row in self.cursor)

    def __iter__(self):
        # the cursor itself is iterable
        return self.cursor
