class Cache:
    def __init__(self):
        self.cache = {}

    def get_or_generate(self, key, generate_func: callable):
        value = self.cache.get(key)
        if value is None:
            self.cache[key] = value = generate_func()
        return value
