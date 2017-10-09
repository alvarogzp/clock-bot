import datetime

import pytz
import time

from clock.domain.zone import Zone


class TimePoint:
    def __init__(self, timestamp):
        self.timestamp = timestamp
        # this is the most direct way to get a UTC aware datetime from a timestamp
        self.utc = pytz.utc.localize(datetime.datetime.utcfromtimestamp(timestamp))

    def id(self):
        return str(self.timestamp)

    def at(self, zone: Zone):
        """:rtype: datetime.datetime"""
        return self.utc.astimezone(zone.timezone)

    @staticmethod
    def current():
        return TimePoint(time.time())
