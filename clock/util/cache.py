import threading
from collections import defaultdict


class Cache:
    def __init__(self):
        self.cache = {}

    def get_or_generate(self, key, generate_func: callable):
        value = self.cache.get(key)
        if value is None:
            self.cache[key] = value = generate_func()
        return value


class SynchronizedCache(Cache):
    def __init__(self):
        super().__init__()
        # one lock per key
        self.locks = defaultdict(threading.Lock)

    def get_or_generate(self, key, generate_func: callable):
        # quick path: if value is in dict, return it
        value = self.cache.get(key)
        if value is not None:
            return value
        # slow path: value was not in dict, get lock to be sure to generate it only once
        with self.locks[key]:
            # with lock acquired we need to check again if key is in dict before inserting
            # because it could have been added between the unlocked check and the lock acquire
            return super().get_or_generate(key, generate_func)
