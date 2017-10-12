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
        return self.zone.id()


class DateTimeZoneFormatter:
    def __init__(self, date_time_zone: DateTimeZone, locale: Locale):
        self.date_time_zone = date_time_zone
        self.locale = locale

    def id(self):
        return self.date_time_zone.id()

    def date(self, format="medium"):
        return self.__title(babel.dates.format_date(self.date_time_zone.date_time, locale=self.locale, format=format))

    def time(self, format="medium"):
        return babel.dates.format_time(self.date_time_zone.date_time, locale=self.locale, format=format)

    def datetime(self, format="medium"):
        return babel.dates.format_datetime(self.date_time_zone.date_time, locale=self.locale, format=format)

    def timezone_location(self):
        return self.__title(ZoneFormatter.location(self.date_time_zone.zone, self.locale))

    def timezone_zone(self):
        return ZoneFormatter.zone_name(self.date_time_zone.zone)

    def timezone_tzname(self):
        return ZoneFormatter.tzname(self.date_time_zone.date_time)

    def timezone_name(self):
        return self.__title(ZoneFormatter.name(self.date_time_zone.zone, self.locale))

    def timezone_offset(self):
        return ZoneFormatter.gmt_offset(self.date_time_zone.date_time, self.locale)

    @staticmethod
    def __title(text):
        first_character = text[0]
        return first_character.upper() + text[1:]
