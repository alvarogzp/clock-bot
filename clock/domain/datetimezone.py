import babel.dates
from babel import Locale

from clock.domain.time import TimePoint
from clock.domain.zone import Zone, ZoneFormatter


class DateTimeZone:
    def __init__(self, time_point: TimePoint, zone: Zone):
        self.time_point = time_point
        self.zone = zone
        self.date_time = time_point.at(self.zone)

    def id(self):
        return self.time_point.id() + "@" + self.zone.id()


class DateTimeZoneFormatter:
    def __init__(self, date_time_zone: DateTimeZone, locale: Locale):
        self.date_time_zone = date_time_zone
        self.locale = locale

    def id(self):
        return self.date_time_zone.id()

    def datetime(self):
        return babel.dates.format_datetime(self.date_time_zone.date_time, locale=self.locale)

    def timezone(self):
        return self.__title(ZoneFormatter.location(self.date_time_zone.zone, self.locale))

    @staticmethod
    def __title(text):
        first_character = text[0]
        return first_character.upper() + text[1:]
