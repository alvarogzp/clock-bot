class BaseClause:
    def __init__(self):
        # call super as these classes will be used as mix-in
        # and we want the init chain to reach all extended classes in the user of these mix-in
        # Update: Its main purpose is to make IDE hint children constructors to call base one,
        # as not calling it in an overridden constructor breaks the chain. But not having a
        # constructor at all doesn't break it, it rather continues with the next defined
        # constructor in the chain.
        super().__init__()
