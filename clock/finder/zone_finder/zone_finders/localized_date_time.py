import babel.dates
from babel import Locale

from clock.domain.time import TimePoint
from clock.domain.zone import ZoneFormatter
from clock.finder.zone_finder.find_util import FindUtil


class LocalizedDateTimeZoneFinder:
    def __init__(self, zones: iter, locale: Locale, time_point: TimePoint):
        self.zones = zones
        self.locale = locale
        self.time_point = time_point

    def match_time_lower(self, query_lower):
        return FindUtil.match_key(self.__get_time_lower(), query_lower, search_fuzzy=False)

    def __get_time_lower(self):
        return [(babel.dates.format_time(self.time_point.at(zone), locale=self.locale).lower(), zone)
                for zone in self.zones]

    def match_gmt_lower(self, query_lower):
        return FindUtil.match_key(self.__get_zone_gmt_lower(), query_lower)

    def __get_zone_gmt_lower(self):
        for zone in self.zones:
            datetime = self.time_point.at(zone)
            yield (ZoneFormatter.gmt_offset(datetime, self.locale).lower(), zone)
            yield (ZoneFormatter.gmt_offset(datetime, self.locale, short=True).lower(), zone)
            yield (ZoneFormatter.gmt_offset(datetime, self.locale, return_z=True).lower(), zone)

    def match_tzname_lower(self, query_lower):
        return FindUtil.match_key(self.__get_tzname_lower(), query_lower)

    def __get_tzname_lower(self):
        return [(ZoneFormatter.tzname(self.time_point.at(zone)).lower(), zone) for zone in self.zones]
