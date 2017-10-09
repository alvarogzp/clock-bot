import datetime

import babel.dates
import pytz
from babel import Locale


class Zone:
    def __init__(self, zone_name):
        self.zone_name = zone_name
        self.timezone = pytz.timezone(zone_name)

    def id(self):
        """
        Returns the zone name passed on the constructor.

        Example: 'Europe/Madrid'
        """
        return self.zone_name

    @property
    def zone(self):
        """
        Returns the zone name as stored by the timezone object (it should be equal to self.zone_name).

        Example: 'Europe/Madrid'
        """
        return self.timezone.zone

    def __str__(self):
        """
        Returns the timezone string representation, which should be equal to self.zone.

        Example: 'Europe/Madrid'
        """
        return self.timezone.__str__()

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

        Example: 'GMT-07:00', '-07' (short)
        """
        return babel.dates.get_timezone_gmt(date_time, locale=locale, width="short" if short else "long", return_z=return_z)

    def location(self, locale: Locale):
        """
        Returns the full location string of the timezone as provided by ``babel``.

        Example: 'hora de España (Madrid)'
        """
        return babel.dates.get_timezone_location(self.timezone, locale=locale)

    def location_city(self, locale: Locale):
        """
        Returns the main city for the timezone, provided by ``babel``.

        Example: 'Madrid'
        """
        return babel.dates.get_timezone_location(self.timezone, locale=locale, return_city=True)

    def name(self, locale: Locale, short=False, zone_variant=None):
        """
        Returns the default timezone name as provided by ``babel``, with no daylight saving consideration.

        Example: 'hora de Europa central', 'CET' (short)
        """
        return babel.dates.get_timezone_name(self.timezone, locale=locale, width="short" if short else "long", zone_variant=zone_variant)

    @staticmethod
    def name_at_a_date_time(date_time: datetime.datetime, locale: Locale, short=False):
        """
        Returns timezone name of the date_time as provided by ``babel``.
        It informs if the timezone is in daylight savings or not.

        Examples: 'hora de verano de Europa central', 'hora estándar de Europa central'
        """
        return babel.dates.get_timezone_name(date_time, locale=locale, width="short" if short else "long")

    def name_zone(self, locale: Locale):
        """
        Returns the zone name from ``babel``. Should match self.zone_name and self.zone.
        """
        return babel.dates.get_timezone_name(self.timezone, locale=locale, return_zone=True)

    @staticmethod
    def utc():
        """Returns the UTC zone"""
        return utc


utc = Zone("UTC")
