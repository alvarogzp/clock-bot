from babel import Locale
from bot.action.util.textformat import FormattedText
from bot.api.domain import ApiObject
from bot.logger.logger import Logger

from clock.domain.time import TimePoint
from clock.log.formatter import LogFormatter


LOG_TAG_QUERY = FormattedText().normal("QUERY")
LOG_TAG_CHOSEN_RESULT = FormattedText().bold("CHOSEN")
LOG_TAG_LOCALE_CACHE = FormattedText().bold("CACHE")
LOG_TAG_MESSAGE = FormattedText().normal("MESSAGE")
LOG_TAG_MIGRATION = FormattedText().bold("MIGRATION")


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
                  results_sent: list, processing_seconds: float, language_code: str):

        formatted_query = self.formatter.query_as_title(query.query, query.offset)
        formatted_user = self.formatter.user(query.from_)
        formatted_language_code = self.formatter.language_code(language_code)
        formatted_locale = self.formatter.locale(locale)
        formatted_time_point = self.formatter.time_point(time_point.id())
        formatted_processing_time = self.formatter.processing_time(processing_seconds)
        formatted_results_number = self.formatter.results(results_sent, results_found)

        formatted_message = self.formatter.message(
            formatted_query,
            formatted_user,
            formatted_language_code,
            formatted_locale,
            formatted_time_point,
            formatted_processing_time,
            formatted_results_number
        )

        self.logger.log(LOG_TAG_QUERY, formatted_message)

    def log_chosen_result(self, user: ApiObject, time_point: str, chosen_zone_name: str, query: str,
                          choosing_seconds: float):

        formatted_chosen_zone = self.formatter.chosen_zone_as_title(chosen_zone_name)
        formatted_user = self.formatter.user(user)
        formatted_query = self.formatter.query(query, "")
        formatted_time_point = self.formatter.time_point(time_point)
        formatted_choosing_time = self.formatter.choosing_time(choosing_seconds)

        formatted_message = self.formatter.message(
            formatted_chosen_zone,
            formatted_user,
            formatted_query,
            formatted_time_point,
            formatted_choosing_time
        )

        self.logger.log(LOG_TAG_CHOSEN_RESULT, formatted_message)

    def log_locale_cache(self, locale: Locale, caching_seconds: float):
        formatted_locale = self.formatter.locale_as_title(locale)
        formatted_caching_time = self.formatter.caching_time(caching_seconds)

        formatted_message = self.formatter.message(
            formatted_locale,
            formatted_caching_time
        )

        self.logger.log(LOG_TAG_LOCALE_CACHE, formatted_message)

    def log_message(self, message: ApiObject):
        formatted_text = self.formatter.text_as_title(message.text or "")
        formatted_user = self._if(self.formatter.user, message.from_, pass_condition=True)
        formatted_chat = self.formatter.chat(message.chat)
        formatted_date = self.formatter.date(message.date)
        formatted_message_id = self.formatter.message_id(message.message_id)
        formatted_forward = self._if(self.formatter.forward, message.forward_date)
        formatted_reply = self._if(self.formatter.reply, message.reply_to_message)
        formatted_edit = self._if(self.formatter.edit, message.edit_date)
        formatted_join = self._list(self.formatter.user, message.new_chat_members, "New member", pass_condition=True)
        formatted_left = self._if(self.formatter.user, message.left_chat_member, "Left member", pass_condition=True)
        formatted_created = self._if(self.formatter.created, message.group_chat_created)
        formatted_migrated_to = self._if(self.formatter.migrated, message.migrate_to_chat_id, "to", pass_condition=True)
        formatted_migrated_from = self._if(self.formatter.migrated, message.migrate_from_chat_id, "from", pass_condition=True)

        formatted_items = (
                formatted_text,
                formatted_user,
                formatted_chat,
                formatted_date,
                formatted_message_id,
                formatted_forward,
                formatted_reply,
                formatted_edit,
                formatted_join,
                formatted_left,
                formatted_created,
                formatted_migrated_to,
                formatted_migrated_from
            )

        formatted_items = filter(None, formatted_items)

        formatted_message = self.formatter.message(*formatted_items)

        self.logger.log(LOG_TAG_MESSAGE, formatted_message)

    @staticmethod
    def _if(func: callable, condition, *additional_params, pass_condition: bool = False):
        if condition:
            args = (condition,) + additional_params if pass_condition else additional_params
            return func(*args)

    def _list(self, func: callable, condition_list, *additional_params, pass_condition: bool = False):
        items = []
        for condition in condition_list or []:
            item = self._if(func, condition, *additional_params, pass_condition=pass_condition)
            if item:
                items.append(item)
        return self.formatter.message(*items) if items else None

    def log_sqlite_component_migration(self, component: str, migration_type: str, old_version: int, new_version: int,
                                       about_to_migrate_to_version: int):
        formatted_about_to_migrate_to_version = self.formatter.about_to_migrate_to_version(about_to_migrate_to_version)
        formatted_component = self.formatter.component(component)
        formatted_migration_type = self.formatter.migration_type(migration_type)
        formatted_old_version = self.formatter.migration_old_version(old_version)
        formatted_new_version = self.formatter.migration_new_version(new_version)

        formatted_message = self.formatter.message(
            formatted_about_to_migrate_to_version,
            formatted_component,
            formatted_migration_type,
            formatted_old_version,
            formatted_new_version
        )

        self.logger.log(LOG_TAG_MIGRATION, formatted_message)
