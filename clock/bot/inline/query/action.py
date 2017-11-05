from bot.action.core.action import Action
from bot.multithreading.work import Work

from clock.bot.inline.query.result.generator import InlineResultGenerator, AnswerInlineQueryResultGenerator
from clock.bot.locale_cache import LocaleCache
from clock.domain.time import TimePoint
from clock.finder.api import ZoneFinderApi
from clock.locale.getter import LocaleGetter
from clock.log.api import LogApi
from clock.storage.api import StorageApi


MAX_RESULTS_PER_QUERY = 25


class InlineQueryClockAction(Action):
    def __init__(self):
        super().__init__()
        self.zone_finder = None  # initialized in post_setup when we have access to config
        self.logger = None  # initialized in post_setup
        self.locale_cache = None  # initialized in post_setup

    def post_setup(self):
        self.zone_finder = ZoneFinderApi(bool(self.config.enable_countries))
        self.logger = LogApi.get(self.cache.logger)
        initial_locales_to_cache = self.config.locales_to_cache_on_startup
        self.locale_cache = LocaleCache(self.zone_finder.cache(), self.scheduler, self.logger, initial_locales_to_cache)
        # for others to use
        self.cache.zone_finder = self.zone_finder
        self.cache.locale_cache = self.locale_cache

    def process(self, event):
        current_time = TimePoint.current()

        query = event.query
        locale = LocaleGetter.from_user(query.from_)

        zones = self.zone_finder.find(query.query, locale, current_time)

        offset = self.__get_offset(query)
        offset_end = offset + MAX_RESULTS_PER_QUERY
        next_offset = self.__get_next_offset(len(zones), offset_end)

        results = InlineResultGenerator.generate(current_time, locale, zones[offset:offset_end])

        processing_time = TimePoint.current_timestamp() - current_time.timestamp

        result = AnswerInlineQueryResultGenerator.generate(query, results, next_offset)
        self.api.async.answerInlineQuery(**result)

        self.locale_cache.cache(locale)

        self.__storage_schedule_save_query(
            lambda: StorageApi.get().save_query(query, current_time, locale, zones, results, processing_time)
        )

        # event.logger is async
        self.logger.log_query(query, current_time, locale, zones, results, processing_time)

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

    def __storage_schedule_save_query(self, func: callable):
        self.scheduler.io(Work(func, "storage:save_query"))
