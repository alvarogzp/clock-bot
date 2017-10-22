from clock.domain.country import Country
from clock.finder.zone_finder.zone_finders.name import NameZoneFinder


class CountryZoneFinder:
    def __init__(self, name_zone_finder: NameZoneFinder, country_timezones: dict, find_countries: bool):
        self.name_zone_finder = name_zone_finder
        self.country_timezones = country_timezones
        self.find_countries = find_countries

    def get_country_zones(self, country_code: str):
        zone_names = self.country_timezones.get(country_code, default=[])
        zones = self.name_zone_finder.get_multiple(zone_names)
        if len(zone_names) > 0 and self.find_countries:
            country = Country(country_code, zones)
            # creating a copy to avoid inserting the country in the country itself
            zones = [country] + zones
        return zones
