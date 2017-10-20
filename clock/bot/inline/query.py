from babel import Locale
from bot.action.core.action import Action
from bot.multithreading.work import Work

from clock.domain.datetimezone import DateTimeZone, DateTimeZoneFormatter
from clock.domain.time import TimePoint
from clock.domain.zone import Zone
from clock.finder.api import ZoneFinderApi
from clock.log.api import LogApi
from clock.storage.api import StorageApi

MAX_RESULTS_PER_QUERY = 50


class InlineQueryClockAction(Action):
    def process(self, event):
        current_time = TimePoint.current()

        query = event.query
        locale = self.__get_locale(query)

        zones = ZoneFinderApi.find(query.query, locale, current_time)

        offset = self.__get_offset(query)
        offset_end = offset + MAX_RESULTS_PER_QUERY
        next_offset = self.__get_next_offset(len(zones), offset_end)

        results = self.__get_results(current_time, locale, zones[offset:offset_end])

        processing_time = TimePoint.current_timestamp() - current_time.timestamp

        self.api.async.answerInlineQuery(
            inline_query_id=query.id,
            results=results,
            next_offset=next_offset,
            cache_time=0,
            is_personal=True
        )

        self.scheduler.io(Work(
            lambda: StorageApi.get().save_query(query, current_time, locale, zones, results, processing_time),
            "storage:save_query"
        ))

        # event.logger is async
        LogApi.get(event.logger).log_query(query, current_time, locale, zones, results, processing_time)

    @staticmethod
    def __get_locale(query):
        user_locale_code = query.from_.language_code
        return Locale.parse(user_locale_code, sep="-")

    @staticmethod
    def __get_offset(query):
        offset = query.offset
        if offset and offset.isdigit():
            return int(offset)
        return 0

    @staticmethod
    def __get_next_offset(result_number, offset_end):
        if result_number > offset_end:
            return str(offset_end)
        return None

    def __get_results(self, time_point: TimePoint, locale: Locale, zones: list):
        return [self.__get_result(time_point, zone, locale) for zone in zones]

    @staticmethod
    def __get_result(time_point: TimePoint, zone: Zone, locale: Locale):
        date_time_zone = DateTimeZone(time_point, zone)
        date_time_zone_formatter = DateTimeZoneFormatter(date_time_zone, locale)
        inline_date_time_zone_result_formatter = InlineResultFormatter(date_time_zone_formatter)
        return inline_date_time_zone_result_formatter.result()


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
