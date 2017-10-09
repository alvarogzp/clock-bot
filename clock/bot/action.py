from babel import Locale
from bot.action.core.action import Action

from clock.domain.datetimezone import DateTimeZone, DateTimeZoneFormatter
from clock.domain.time import TimePoint
from clock.domain.finder import ZoneFinder


class InlineClockAction(Action):
    def process(self, event):
        query_id = event.query.id

        current_time = TimePoint.current()

        user_locale_code = event.query.from_.language_code
        locale = Locale.parse(user_locale_code, sep="-")

        zones = ZoneFinder.from_locale(locale)

        results = []
        for zone in zones:
            date_time_zone = DateTimeZone(current_time, zone)
            date_time_zone_formatter = DateTimeZoneFormatter(date_time_zone, locale)
            inline_date_time_zone_result_formatter = InlineResultFormatter(date_time_zone_formatter)
            results.append(inline_date_time_zone_result_formatter.result())

        self.api.answerInlineQuery(inline_query_id=query_id, results=results, cache_time=0, is_personal=True)


class InlineResultFormatter:
    def __init__(self, date_time_zone_formatter: DateTimeZoneFormatter):
        self.date_time_zone_formatter = date_time_zone_formatter

    def id(self):
        return self.date_time_zone_formatter.id()

    def title(self):
        return self.date_time_zone_formatter.timezone()

    def description(self):
        return self.date_time_zone_formatter.datetime()

    def message(self):
        return "<b>{timezone}</b>\n{datetime}".format(
            timezone=self.date_time_zone_formatter.timezone(),
            datetime=self.date_time_zone_formatter.datetime()
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
