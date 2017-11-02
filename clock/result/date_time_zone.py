from clock.domain.datetimezone import DateTimeZoneFormatter
from clock.result import Result


class DateTimeZoneResult(Result):
    def __init__(self, date_time_zone_formatter: DateTimeZoneFormatter):
        self.date_time_zone_formatter = date_time_zone_formatter

    def id(self):
        return self.date_time_zone_formatter.id()

    def title(self):
        return self.date_time_zone_formatter.timezone_location()

    def description(self):
        return "{zone}\n{datetime}".format(
            datetime=self.date_time_zone_formatter.datetime(format="short"),
            zone=self.date_time_zone_formatter.timezone_zone()
        )

    def message(self):
        return \
            "<b>🌍 {timezone} 🌎</b>\n\n" \
            "<b>🕓 {time}\n📆 {date}</b>\n\n" \
            "{name} | {tzname}\n" \
            "<code>{zone}</code> | {offset}".format(
                timezone=self.date_time_zone_formatter.timezone_location(),
                time=self.date_time_zone_formatter.time(format="full"),
                date=self.date_time_zone_formatter.date(format="full"),
                name=self.date_time_zone_formatter.timezone_name(),
                tzname=self.date_time_zone_formatter.timezone_tzname(),
                zone=self.date_time_zone_formatter.timezone_zone(),
                offset=self.date_time_zone_formatter.timezone_offset()
            )

    def image_url(self):
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Icons8_flat_clock.svg/2000px-Icons8_flat_clock.svg.png"
