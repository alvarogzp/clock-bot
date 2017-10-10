import pytz
from babel import Locale

from clock.domain.country import Country
from clock.domain.zone import Zone


class ZoneFinder:
    all_timezones_lower = [i.lower() for i in pytz.all_timezones]

    @classmethod
    def find(cls, query, locale: Locale):
        zones = []
        if not query:
            zones.extend(cls.from_locale(locale))
        else:
            zones.extend(cls.from_query(query))
        return zones

    @classmethod
    def from_locale(cls, locale: Locale):
        country_code = locale.territory
        return cls.__from_country(country_code)

    @staticmethod
    def __from_country(country_code):
        country = Country(country_code)
        timezones = pytz.country_timezones.get(country_code, default=[])
        return [Zone(timezone, country) for timezone in timezones]

    @classmethod
    def from_query(cls, query):
        query = query.lower()
        zones = []
        # first, try zone name exact match
        zone = cls.__from_zone_name(query)
        if zone is not None:
            zones.append(zone)
        # then, try country code exact match
        country_zones = cls.__from_country(query)
        zones.extend(country_zones)
        if len(zones) > 0:
            # if there are exact matches, return them
            return zones
        # now inexact search
        if len(query) > 2:
            zones.extend(cls.__incomplete_zone_names(query, fuzzy=True))
        return zones

    @classmethod
    def __from_zone_name(cls, zone_name):
        """
        :param zone_name: must be lowercase!
        """
        if zone_name in cls.all_timezones_lower:
            index = cls.all_timezones_lower.index(zone_name)
            return cls.__from_all_timezones_index(index)

    @classmethod
    def __incomplete_zone_names(cls, query, fuzzy=False):
        """
        :param query: must be lowercase!
        """
        zones_start = []
        zones_fuzzy = []
        for index, zone_name_lower in enumerate(cls.all_timezones_lower):
            if zone_name_lower.startswith(query):
                zones_start.append(cls.__from_all_timezones_index(index))
            elif fuzzy and query in zone_name_lower:
                zones_fuzzy.append(cls.__from_all_timezones_index(index))
        return zones_start + zones_fuzzy

    @staticmethod
    def __from_all_timezones_index(index):
        return Zone(pytz.all_timezones[index])
