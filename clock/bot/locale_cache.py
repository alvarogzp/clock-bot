import itertools
from babel import Locale
from bot.multithreading.scheduler import SchedulerApi
from bot.multithreading.work import Work

from clock.domain.time import TimePoint
from clock.finder.api import ZoneFinderLocaleCache
from clock.locale.getter import LocaleGetter
from clock.log.api import LogApi
from clock.storage.api import StorageApi


DEFAULT_RECENT_LOCALES_LIMIT = 10

DEFAULT_INITIAL_LOCALES_TO_CACHE = """
en-US
es-ES
"""


class LocaleCache:
    def __init__(self, zone_finder_locale_cache: ZoneFinderLocaleCache, scheduler: SchedulerApi, logger: LogApi,
                 storage: StorageApi, initial_locales_to_cache: str, recent_locales_limit: int):
        self.locale_cache = zone_finder_locale_cache
        self.logger = logger
        self.storage = storage

        # using only one background thread to avoid consuming too many resources for locale caching
        # this is a background cache, quickly processing queries is more important
        self.worker = scheduler.new_worker_pool("locale_cache", min_workers=0, max_workers=1, max_seconds_idle=60)

        initial_locales = self._parse_initial_locales(
            initial_locales_to_cache or DEFAULT_INITIAL_LOCALES_TO_CACHE
        )
        recent_language_codes = self._get_recent_language_codes(
            int(recent_locales_limit or DEFAULT_RECENT_LOCALES_LIMIT)
        )
        initial_language_codes = itertools.chain(initial_locales, recent_language_codes)
        self._cache_initial_language_codes(initial_language_codes)

    @staticmethod
    def _parse_initial_locales(initial_locales_to_cache: str):
        for line in initial_locales_to_cache.splitlines():
            for language_code in line.split():
                if language_code.startswith("#"):
                    # a comment was found, ignore until the next line
                    break
                yield language_code

    def _get_recent_language_codes(self, limit: int):
        return self.storage.get_recent_queries_language_codes(limit)

    def _cache_initial_language_codes(self, initial_language_codes_to_cache: iter):
        for language_code in initial_language_codes_to_cache:
            locale = LocaleGetter.from_language_code(language_code)
            self.cache(locale)

    def cache(self, locale: Locale):
        if not self.locale_cache.is_cached(locale):
            self.worker.post(Work(lambda: self._cache(locale), "cache_locale:" + str(locale)))

    def _cache(self, locale: Locale):
        start_time = TimePoint.current_timestamp()
        self.locale_cache.cache(locale)
        self.logger.log_locale_cache(locale, TimePoint.current_timestamp() - start_time)

    def is_cached(self, locale: Locale):
        return self.locale_cache.is_cached(locale)

    def cached_locales(self):
        return self.locale_cache.cached_locales()
