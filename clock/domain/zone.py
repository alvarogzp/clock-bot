import datetime

import babel.dates
import pytz
from babel import Locale

from clock.util.cache import Cache


class Zone:
    def __init__(self, zone_name):
        self.zone_name = zone_name
        self.timezone = pytz.timezone(zone_name)
        # un-synchronized cache: generation is quick and does not compensate the lock overhead of a synchronized cache
        self._name_cache = Cache()
        self._location_cache = Cache()

    def id(self):
        """
        Returns the zone name passed on the constructor.

        Example: 'Europe/Madrid'
        """
        return self.zone_name

    def name(self, locale: Locale):
        return self._name_cache.get_or_generate(str(locale), lambda: self._name__no_cache(locale))

    def _name__no_cache(self, locale: Locale):
        return ZoneFormatter.name(self, locale)

    def location(self, locale: Locale):
        return self._location_cache.get_or_generate(str(locale), lambda: self._location__no_cache(locale))

    def _location__no_cache(self, locale: Locale):
        return ZoneFormatter.location(self, locale)

    @staticmethod
    def utc():
        """Returns the UTC zone"""
        return utc


utc = Zone("UTC")


class ZoneFormatter:
    @staticmethod
    def zone_name(zone: Zone):
        """
        Returns the zone name passed to the zone constructor.

        Example: 'Europe/Madrid'
        """
        return zone.zone_name

    @staticmethod
    def zone(zone: Zone):
        """
        Returns the zone name as stored by the timezone object (it should be equal to zone.zone_name).

        Example: 'Europe/Madrid'
        """
        return zone.timezone.zone

    @staticmethod
    def zone_str(zone: Zone):
        """
        Returns the timezone string representation, which should be equal to the result of self.zone.

        Example: 'Europe/Madrid'
        """
        return zone.timezone.__str__()

    @staticmethod
    def tzname(date_time: datetime.datetime):
        """
        Returns the result of calling tzname on the date_time object (must be timezone-aware to return other than None).
        Its representation usually differs from the timezone.zone representation.

        Example: 'CEST'
        """
        return date_time.tzname()

    @staticmethod
    def gmt_offset(date_time: datetime.datetime, locale: Locale, short=False, return_z=False):
        """
        Uses ``babel.dates.get_timezone_gmt`` to get the GMT offset of the date_time.
        See its doc for more info.

        Example: 'GMT+02:00', '+0200' (short)
        """
        return babel.dates.get_timezone_gmt(date_time, locale=locale, width="short" if short else "long", return_z=return_z)

    @staticmethod
    def location(zone: Zone, locale: Locale):
        """
        Returns the full location string of the timezone as provided by ``babel``.

        Example: 'hora de España (Madrid)'
        """
        return babel.dates.get_timezone_location(zone.timezone, locale=locale)

    @staticmethod
    def location_city(zone: Zone, locale: Locale):
        """
        Returns the main city for the timezone, provided by ``babel``.

        Example: 'Madrid'
        """
        return babel.dates.get_timezone_location(zone.timezone, locale=locale, return_city=True)

    @staticmethod
    def name(zone: Zone, locale: Locale, short=False, zone_variant=None):
        """
        Returns the default timezone name as provided by ``babel``.
        Daylight saving is not taken into account, unless you specify a ``zone_variant``.

        Example: 'hora de Europa central', 'CET' (short)
        """
        return babel.dates.get_timezone_name(zone.timezone, locale=locale, width="short" if short else "long", zone_variant=zone_variant)

    @staticmethod
    def name_at_a_date_time(date_time: datetime.datetime, locale: Locale, short=False):
        """
        Returns timezone name of the date_time as provided by ``babel``.
        It informs if the timezone is in daylight savings or not.

        Examples: 'hora de verano de Europa central', 'hora estándar de Europa central'
        """
        return babel.dates.get_timezone_name(date_time, locale=locale, width="short" if short else "long")

    @staticmethod
    def name_zone(zone: Zone, locale: Locale):
        """
        Returns the zone name from ``babel``. Should match self.zone_name and self.zone.

        Example: 'Europe/Madrid'
        """
        return babel.dates.get_timezone_name(zone.timezone, locale=locale, return_zone=True)
