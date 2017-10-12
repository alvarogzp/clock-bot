from clock.finder.zone_finder.zone_finders.name import NameZoneFinder


class CountryZoneFinder:
    def __init__(self, name_zone_finder: NameZoneFinder, country_timezones: dict):
        self.name_zone_finder = name_zone_finder
        self.country_timezones = country_timezones

    def get_country_zones(self, country_code: str):
        zone_names = self.country_timezones.get(country_code, default=[])
        return self.name_zone_finder.get_multiple(zone_names)
