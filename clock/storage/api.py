from babel import Locale
from bot.api.domain import ApiObject

from clock.domain.time import TimePoint
from clock.storage.async.scheduler import StorageScheduler
from clock.storage.data_source.data_source import StorageDataSource


class StorageApi:
    def __init__(self, data_source: StorageDataSource, scheduler: StorageScheduler):
        self.data_source = data_source
        self.scheduler = scheduler
        self.init()

    def init(self):
        self.scheduler.schedule_no_result(self._init)

    def save_query(self, query: ApiObject, time_point: TimePoint, locale: Locale, results_found: list,
                   results_sent: list, processing_seconds: float):
        self.scheduler.schedule_no_result(
            lambda: self._save_query(query, time_point, locale, results_found, results_sent, processing_seconds)
        )

    def save_chosen_result(self, user: ApiObject, timestamp: str, chosen_zone_name: str, query: str,
                           choosing_seconds: float):
        self.scheduler.schedule_no_result(
            lambda: self._save_chosen_result(user, timestamp, chosen_zone_name, query, choosing_seconds)
        )

    def save_message(self, message: ApiObject):
        self.scheduler.schedule_no_result(
            lambda: self._save_message(message)
        )

    def _init(self):
        self.data_source.init()

    def _save_query(self, query: ApiObject, time_point: TimePoint, locale: Locale, results_found: list,
                    results_sent: list, processing_seconds: float):
        self._save_user(query.from_)
        self.data_source.save_query(query.from_.id, time_point.id(), query.query, query.offset, str(locale),
                                    len(results_found), len(results_sent), processing_seconds)
        self.data_source.commit()

    def _save_user(self, user: ApiObject):
        self.data_source.save_user(user.id, user.first_name, user.last_name, user.username, user.language_code)

    def _save_chosen_result(self, user: ApiObject, timestamp: str, chosen_zone_name: str, query: str,
                            choosing_seconds: float):
        # the query might have been retrieved from server-side cache and the user could be unknown for us
        self._save_user(user)
        self.data_source.save_chosen_result(user.id, timestamp, chosen_zone_name, query, choosing_seconds)
        self.data_source.commit()

    def _save_message(self, message: ApiObject):
        user_id = None
        user = message.from_
        if user:
            user_id = user.id
            self._save_user(user)
        chat = message.chat
        self._save_chat(chat)
        self.data_source.save_message(chat.id, message.message_id, user_id, message.date, message.text)
        self.data_source.commit()

    def _save_chat(self, chat: ApiObject):
        self.data_source.save_chat(chat.id, chat.type, chat.title, chat.username)
