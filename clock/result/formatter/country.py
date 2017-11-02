from typing import List

from clock.domain.country import CountryFormatter
from clock.domain.datetimezone import DateTimeZoneFormatter
from clock.domain.time import TimePoint
from clock.result.formatter import ResultFormatter


class CountryResultFormatter(ResultFormatter):
    def __init__(self, time_point: TimePoint, country_formatter: CountryFormatter,
                 date_time_zone_formatters: List[DateTimeZoneFormatter]):
        self.time_point = time_point
        self.country_formatter = country_formatter
        self.date_time_zone_formatters = date_time_zone_formatters

    def id(self):
        return self.time_point.id() + "@country:" + self.country_formatter.id()

    def title(self):
        return self.country_formatter.name()

    def description(self):
        return "{number_of_zones} 🕓".format(number_of_zones=len(self.date_time_zone_formatters))

    def message(self):
        return \
            "<b>🌍 {country} 🌎</b>\n\n" \
            "{zones}".format(
                country=self.country_formatter.name(),
                zones="\n\n".join(
                    "<b>📍 {timezone}</b>\n"
                    "<b>🕓 {time}\n📆 {date}</b>\n"
                    "<code>{zone}</code> | {tzname}".format(
                        timezone=date_time_zone_formatter.timezone_location(),
                        time=date_time_zone_formatter.time(format="full"),
                        date=date_time_zone_formatter.date(format="full"),
                        name=date_time_zone_formatter.timezone_name(),
                        tzname=date_time_zone_formatter.timezone_tzname(),
                        zone=date_time_zone_formatter.timezone_zone(),
                        offset=date_time_zone_formatter.timezone_offset()
                    )
                    for date_time_zone_formatter in self.date_time_zone_formatters
                )
            )

    def image_url(self):
        # "https://greenwichmeantime.com/static/app/world_clock/icon/world.svg" -- svg doesn't seem to work
        return "https://lh3.googleusercontent.com/zS00dXy7DXIjDmygytD5qC8GFF9uWxXIvu73-8CUISgZPeAR0c6JfEk26Yra-7Dh1w"
