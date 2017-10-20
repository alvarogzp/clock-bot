from babel import Locale
from bot.action.util.textformat import FormattedText
from bot.api.domain import ApiObject
from bot.logger.logger import Logger

from clock.domain.time import TimePoint
from clock.log.formatter import LogFormatter


LOG_TAG_QUERY = FormattedText().normal("QUERY")
LOG_TAG_CHOSEN_RESULT = FormattedText().bold("CHOSEN")


class LogApi:
    _instance = None

    @classmethod
    def get(cls, logger: Logger):
        """:rtype: LogApi"""
        if cls._instance is None or logger is not cls._instance.logger:
            cls._instance = LogApi(logger, LogFormatter())
        return cls._instance

    def __init__(self, logger: Logger, formatter: LogFormatter):
        self.logger = logger
        self.formatter = formatter

    def log_query(self, query: ApiObject, time_point: TimePoint, locale: Locale, results_found: list,
                  results_sent: list, processing_seconds: float):

        formatted_time_point = self.formatter.time_point(time_point.id())
        formatted_user = self.formatter.user(query.from_)
        formatted_query = self.formatter.query(query.query, query.offset)
        formatted_locale = self.formatter.locale(locale)
        formatted_processing_time = self.formatter.processing_time(processing_seconds)
        formatted_results_number = self.formatter.results(results_sent, results_found)

        formatted_message = self.formatter.message(
            formatted_time_point,
            formatted_user,
            formatted_query,
            formatted_locale,
            formatted_processing_time,
            formatted_results_number
        )

        self.logger.log(LOG_TAG_QUERY, formatted_message)

    def log_chosen_result(self, user: ApiObject, time_point: str, chosen_zone_name: str, query: str,
                          choosing_seconds: float):

        formatted_time_point = self.formatter.time_point(time_point)
        formatted_user = self.formatter.user(user)
        formatted_query = self.formatter.query(query, "")
        formatted_chosen_zone = self.formatter.chosen_zone(chosen_zone_name)
        formatted_choosing_time = self.formatter.choosing_time(choosing_seconds)

        formatted_message = self.formatter.message(
            formatted_time_point,
            formatted_user,
            formatted_query,
            formatted_chosen_zone,
            formatted_choosing_time
        )

        self.logger.log(LOG_TAG_CHOSEN_RESULT, formatted_message)
