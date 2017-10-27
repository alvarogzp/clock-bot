import pytz
from babel import Locale

from clock.domain.time import TimePoint
from clock.domain.zone import Zone
from clock.finder.zone_finder.zone_finders.country import CountryZoneFinder
from clock.finder.zone_finder.zone_finders.localized import LocalizedZoneFinder
from clock.finder.zone_finder.zone_finders.localized_date_time import LocalizedDateTimeZoneFinder
from clock.finder.zone_finder.zone_finders.name import NameZoneFinder
from clock.util.cache import SynchronizedCache


class ZoneFindersProvider:
    def __init__(self, find_countries: bool):
        zone_names = pytz.all_timezones
        self.zones = self.__build_zones(zone_names)
        self.name_zone_finder = NameZoneFinder(self.zones)
        self.country_zone_finder = CountryZoneFinder(self.name_zone_finder, pytz.country_timezones, find_countries)
        self._localized_zone_finder_cache = LocalizedZoneFinderCache(self.__create_localized_zone_finder)

    @staticmethod
    def __build_zones(zone_names: list):
        return [Zone(zone_name) for zone_name in zone_names]

    def localized_zone_finder(self, locale: Locale):
        """:rtype: LocalizedZoneFinder"""
        return self._localized_zone_finder_cache.get_or_generate(locale)

    def __create_localized_zone_finder(self, locale):
        return LocalizedZoneFinder(self.zones, locale)

    def localized_date_time_zone_finder(self, locale: Locale, time_point: TimePoint):
        return LocalizedDateTimeZoneFinder(self.zones, locale, time_point)


class LocalizedZoneFinderCache:
    def __init__(self, create_func: callable):
        self.create_func = create_func
        self.cache = SynchronizedCache()

    def get_or_generate(self, locale: Locale):
        return self.cache.get_or_generate(self._key(locale), lambda: self.create_func(locale))

    @staticmethod
    def _key(locale: Locale):
        return str(locale)
