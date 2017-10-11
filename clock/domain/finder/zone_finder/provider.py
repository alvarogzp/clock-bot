import pytz
from babel import Locale

from clock.domain.finder.zone_finder.zone_finders.country import CountryZoneFinder
from clock.domain.finder.zone_finder.zone_finders.localized import LocalizedZoneFinder
from clock.domain.finder.zone_finder.zone_finders.localized_date_time import LocalizedDateTimeZoneFinder
from clock.domain.finder.zone_finder.zone_finders.name import NameZoneFinder
from clock.domain.time import TimePoint
from clock.domain.zone import Zone
from clock.util import Cache


class ZoneFindersProvider:
    def __init__(self):
        zone_names = pytz.all_timezones
        self.zones = self.__build_zones(zone_names)
        self.name_zone_finder = NameZoneFinder(self.zones)
        self.country_zone_finder = CountryZoneFinder(self.name_zone_finder, pytz.country_timezones)
        self._localized_zone_finder_cache = Cache()

    @staticmethod
    def __build_zones(zone_names: list):
        return [Zone(zone_name) for zone_name in zone_names]

    def localized_zone_finder(self, locale: Locale):
        """:rtype: LocalizedZoneFinder"""
        return self._localized_zone_finder_cache\
            .get_or_generate(str(locale), lambda: self.__create_localized_zone_finder(locale))

    def __create_localized_zone_finder(self, locale):
        return LocalizedZoneFinder(self.zones, locale)

    def localized_date_time_zone_finder(self, locale: Locale, time_point: TimePoint):
        return LocalizedDateTimeZoneFinder(self.zones, locale, time_point)
