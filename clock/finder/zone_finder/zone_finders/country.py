from clock.domain.country import Country
from clock.finder.zone_finder.zone_finders.name import NameZoneFinder


class CountryZoneFinder:
    def __init__(self, name_zone_finder: NameZoneFinder, country_timezones: dict, find_countries: bool):
        self.countries_lower = self.__build_countries_lower(name_zone_finder, country_timezones, find_countries)

    @classmethod
    def __build_countries_lower(cls, name_zone_finder: NameZoneFinder, country_timezones: dict, find_countries: bool):
        countries = {}
        for country_code, country_zone_names in country_timezones.items():
            country_zones = name_zone_finder.get_multiple(country_zone_names)
            cls.__add_country_if_necessary(country_code, country_zones, find_countries)
            countries[country_code.lower()] = country_zones
        return countries

    @staticmethod
    def __add_country_if_necessary(country_code: str, country_zones: list, find_countries: bool):
        if find_countries and len(country_zones) > 0:
            # create a copy of the zones to avoid inserting the country in the country itself
            country = Country(country_code, country_zones[:])
            country_zones.insert(0, country)

    def get_country_zones(self, country_code: str):
        return self.countries_lower.get(country_code.lower(), [])
