from babel import Locale
from bot.multithreading.scheduler import SchedulerApi
from bot.multithreading.work import Work

from clock.domain.time import TimePoint
from clock.finder.api import ZoneFinderLocaleCache
from clock.log.api import LogApi


DEFAULT_INITIAL_LOCALES_TO_CACHE = """
en_US
es_ES
"""


class LocaleCache:
    def __init__(self, zone_finder_locale_cache: ZoneFinderLocaleCache, scheduler: SchedulerApi, log_api: LogApi,
                 initial_locales_to_cache: str):
        self.locale_cache = zone_finder_locale_cache
        # using only one background thread to avoid consuming too many resources for locale caching
        # this is a background cache, quickly processing queries is more important
        self.worker = scheduler.new_worker_pool("locale_cache", min_workers=0, max_workers=1, max_seconds_idle=60)
        self.log_api = log_api
        self._cache_initial_locales(self._parse_initial_locales(initial_locales_to_cache))

    @staticmethod
    def _parse_initial_locales(initial_locales_to_cache: str):
        if initial_locales_to_cache is None:
            initial_locales_to_cache = DEFAULT_INITIAL_LOCALES_TO_CACHE
        for line in initial_locales_to_cache.splitlines():
            for locale_code in line.split():
                if locale_code.startswith("#"):
                    # a comment was found, ignore until the next line
                    break
                yield Locale.parse(locale_code)

    def _cache_initial_locales(self, initial_locales_to_cache: iter):
        for locale in initial_locales_to_cache:
            self.cache(locale)

    def cache(self, locale: Locale):
        if not self.locale_cache.is_cached(locale):
            self.worker.post(Work(lambda: self._cache(locale), "cache_locale:" + str(locale)))

    def _cache(self, locale: Locale):
        start_time = TimePoint.current_timestamp()
        self.locale_cache.cache(locale)
        self.log_api.log_locale_cache(locale, TimePoint.current_timestamp() - start_time)

    def is_cached(self, locale: Locale):
        return self.locale_cache.is_cached(locale)

    def cached_locales(self):
        return self.locale_cache.cached_locales()
