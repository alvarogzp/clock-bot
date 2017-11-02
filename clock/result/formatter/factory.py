from typing import Union

from babel import Locale

from clock.domain.country import Country, CountryFormatter
from clock.domain.datetimezone import DateTimeZone, DateTimeZoneFormatter
from clock.domain.time import TimePoint
from clock.domain.zone import Zone
from clock.result.formatter.country import CountryResultFormatter
from clock.result.formatter.date_time_zone import DateTimeZoneResultFormatter


class ResultFormatterFactory:
    @classmethod
    def get(cls, time_point: TimePoint, zone: Union[Zone, Country], locale: Locale):
        if isinstance(zone, Country):
            return cls.get_for_country(time_point, zone, locale)
        else:
            return cls.get_for_zone(time_point, zone, locale)

    @classmethod
    def get_for_zone(cls, time_point: TimePoint, zone: Zone, locale: Locale):
        date_time_zone_formatter = cls._get_date_time_zone_formatter(time_point, zone, locale)
        return DateTimeZoneResultFormatter(date_time_zone_formatter)

    @staticmethod
    def _get_date_time_zone_formatter(time_point: TimePoint, zone: Zone, locale: Locale):
        date_time_zone = DateTimeZone(time_point, zone)
        return DateTimeZoneFormatter(date_time_zone, locale)

    @classmethod
    def get_for_country(cls, time_point: TimePoint, country: Country, locale: Locale):
        country_formatter = CountryFormatter(country, locale)
        date_time_zone_formatters = [cls._get_date_time_zone_formatter(time_point, zone, locale)
                                     for zone in country.zones]
        return CountryResultFormatter(time_point, country_formatter, date_time_zone_formatters)
