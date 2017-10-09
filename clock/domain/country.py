import pytz


class Country:
    def __init__(self, country_code):
        self.country_code = country_code

    @property
    def name(self):
        return pytz.country_names[self.country_code]


class UnknownCountry(Country):
    def __init__(self):
        super().__init__("")

    @property
    def name(self):
        return ""
