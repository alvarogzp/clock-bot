import pytz
from babel import Locale

from clock.domain.country import Country
from clock.domain.zone import Zone


class ZoneFinder:
    @staticmethod
    def from_locale(locale: Locale):
        language = locale.language
        country = Country(language)
        timezones = pytz.country_timezones.get(language, default=[])
        return [Zone(timezone, country) for timezone in timezones]
