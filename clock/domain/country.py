from typing import List

from babel import Locale

from clock.domain.zone import Zone


class Country:
    def __init__(self, country_code: str, zones: List[Zone]):
        self.country_code = country_code.upper()
        self.zones = zones

    def id(self):
        return self.country_code


class CountryFormatter:
    def __init__(self, country: Country, locale: Locale):
        self.country = country
        self.locale = locale

    def id(self):
        return self.country.id()

    def name(self):
        return self.locale.territories[self.country.country_code]
