class BaseClause:
    def __init__(self):
        # call super as these classes will be used as mix-in
        # and we want the init chain to reach all extended classes in the user of these mix-in
        super().__init__()
