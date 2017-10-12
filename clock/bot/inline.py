from babel import Locale
from bot.action.core.action import Action

from clock.domain.datetimezone import DateTimeZone, DateTimeZoneFormatter
from clock.domain.time import TimePoint
from clock.domain.finder.api import ZoneFinderApi

MAX_RESULTS_PER_QUERY = 50


class InlineClockAction(Action):
    def process(self, event):
        query_id = event.query.id

        current_time = TimePoint.current()

        locale = self.__get_locale(event)

        zones = ZoneFinderApi.find(event.query.query, locale, current_time)

        offset = self.__get_offset(event)
        offset_end = offset + MAX_RESULTS_PER_QUERY
        next_offset = self.__get_next_offset(len(zones), offset_end)

        zones = zones[offset:offset_end]

        results = []
        for zone in zones:
            date_time_zone = DateTimeZone(current_time, zone)
            date_time_zone_formatter = DateTimeZoneFormatter(date_time_zone, locale)
            inline_date_time_zone_result_formatter = InlineResultFormatter(date_time_zone_formatter)
            results.append(inline_date_time_zone_result_formatter.result())

        self.api.answerInlineQuery(
            inline_query_id=query_id,
            results=results,
            next_offset=next_offset,
            cache_time=0,
            is_personal=True
        )

    @staticmethod
    def __get_locale(event):
        user_locale_code = event.query.from_.language_code
        return Locale.parse(user_locale_code, sep="-")

    @staticmethod
    def __get_offset(event):
        offset = event.query.offset
        if offset and offset.isdigit():
            return int(offset)
        return 0

    @staticmethod
    def __get_next_offset(result_number, offset_end):
        if result_number > offset_end:
            return str(offset_end)
        return None


class InlineResultFormatter:
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

    def result(self):
        return {
            "type": "article",
            "id": self.id(),
            "title": self.title(),
            "input_message_content": {
                "message_text": self.message(),
                "parse_mode": "HTML",
                "disable_web_page_preview": True
            },
            "description": self.description(),
            "thumb_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Icons8_flat_clock.svg/2000px-Icons8_flat_clock.svg.png"
        }
