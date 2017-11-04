from babel import Locale

from clock.domain.zone import Zone
from clock.finder.api import ZoneFinderApi
from clock.locale.country_code import CountryCode


class LocaleToZone:
    @classmethod
    def get_zone_from_locale(cls, locale: Locale, zone_finder: ZoneFinderApi):
        country_code = CountryCode.from_locale(locale)
        country_zones = zone_finder.country_finder().get_country_zones(country_code)
        for zone in country_zones:
            if isinstance(zone, Zone):
                return zone
        return cls.get_any_zone(zone_finder)

    @staticmethod
    def get_any_zone(zone_finder: ZoneFinderApi):
        return zone_finder.zones()[0]
