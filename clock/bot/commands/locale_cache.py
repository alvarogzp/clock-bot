from babel import Locale
from bot.action.core.action import Action
from bot.action.util.textformat import FormattedText
from bot.api.domain import Message
from bot.logger.formatter.exception import ExceptionFormatter

from clock.bot.locale_cache import LocaleCache


class LocaleCacheAction(Action):
    def __init__(self):
        super().__init__()
        self.send_cached_locales_sub_action = None  # initialized in post_setup
        self.cache_locale_sub_action = None  # initialized in post_setup

    def post_setup(self):
        locale_cache = self.cache.locale_cache
        self.send_cached_locales_sub_action = SendCachedLocalesSubAction(locale_cache)
        self.cache_locale_sub_action = CacheLocaleSubAction(locale_cache)

    def process(self, event):
        send_formatted_text_func = self._get_send_formatted_text_func(event)
        if not event.command_args:
            self.send_cached_locales(send_formatted_text_func)
        else:
            self.cache_locale(event.command_args, send_formatted_text_func)

    def send_cached_locales(self, send_formatted_text_func: callable):
        self.send_cached_locales_sub_action.send(send_formatted_text_func)

    def cache_locale(self, locale: str, send_formatted_text_func: callable):
        self.cache_locale_sub_action.cache(locale, send_formatted_text_func)

    def _get_send_formatted_text_func(self, event):
        return lambda text: self._send_formatted_text(text, event.message)

    def _send_formatted_text(self, text: FormattedText, replying_to: Message):
        self.api.async.send_message(text.build_message().to_chat_replying(replying_to))


class LocaleCacheSubAction:
    def __init__(self, locale_cache: LocaleCache):
        self.locale_cache = locale_cache


class SendCachedLocalesSubAction(LocaleCacheSubAction):
    def send(self, send_formatted_text_func: callable):
        response = self.get_cached_locales()
        send_formatted_text_func(response)

    def get_cached_locales(self):
        cached_locales = self.locale_cache.cached_locales()
        return FormattedText()\
            .concat(self.get_cached_locales_number(cached_locales))\
            .concat(self.get_cached_locales_names(cached_locales))

    @staticmethod
    def get_cached_locales_number(cached_locales: list):
        cached_locales_number = len(cached_locales)
        return FormattedText().normal("Cached locales: {number}")\
            .start_format().bold(number=cached_locales_number).end_format()

    @staticmethod
    def get_cached_locales_names(cached_locales: list):
        return FormattedText().join(
            [
                FormattedText().newline().normal(" - {name}").start_format().bold(name=locale).end_format()
                for locale in cached_locales
            ]
        )


class CacheLocaleSubAction(LocaleCacheSubAction):
    def cache(self, locale: str, send_formatted_text_func: callable):
        try:
            locale = self._get_locale(locale)
        except Exception as e:
            self.__send_error(e, send_formatted_text_func)
        else:
            if self._is_cached(locale):
                self.__send_response_is_cached(locale, send_formatted_text_func)
            else:
                self._cache_locale(locale)
                self.__send_response_caching_scheduled(locale, send_formatted_text_func)

    @staticmethod
    def _get_locale(locale: str):
        return Locale.parse(locale)

    def _is_cached(self, locale: Locale):
        return self.locale_cache.is_cached(locale)

    def _cache_locale(self, locale: Locale):
        self.locale_cache.cache(locale)

    @staticmethod
    def __send_error(error: Exception, send_formatted_text_func: callable):
        response = FormattedText()\
            .normal("Error: {error}").start_format()\
            .bold(error=ExceptionFormatter.format(error)).end_format()
        send_formatted_text_func(response)

    @staticmethod
    def __send_response_is_cached(locale: Locale, send_formatted_text_func: callable):
        response = FormattedText()\
            .normal("Locale {locale} is already cached!").start_format()\
            .bold(locale=locale).end_format()
        send_formatted_text_func(response)

    @staticmethod
    def __send_response_caching_scheduled(locale: Locale, send_formatted_text_func: callable):
        response = FormattedText()\
            .normal("Caching of {locale} locale scheduled...").newline()\
            .normal("You will get notified on the log chat when it ends").start_format()\
            .bold(locale=str(locale)).end_format()
        send_formatted_text_func(response)
