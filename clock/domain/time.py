import datetime

import pytz
import time

from clock.domain.zone import Zone
from clock.util.cache import Cache


class TimePoint:
    def __init__(self, timestamp):
        self.timestamp = timestamp
        # this is the most direct way to get a UTC aware datetime from a timestamp
        self.utc = pytz.utc.localize(datetime.datetime.utcfromtimestamp(timestamp))
        self._at_cache = Cache()

    def id(self):
        return str(self.timestamp)

    def at(self, zone: Zone):
        """:rtype: datetime.datetime"""
        return self._at_cache.get_or_generate(zone.zone_name, lambda: self._at__no_cache(zone))

    def _at__no_cache(self, zone: Zone):
        return self.utc.astimezone(zone.timezone)

    @classmethod
    def current(cls):
        return TimePoint(cls.current_timestamp())

    @staticmethod
    def current_timestamp():
        return time.time()
