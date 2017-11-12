from babel import Locale
from bot.api.domain import ApiObject

from clock.domain.time import TimePoint
from clock.storage.async.scheduler import StorageScheduler
from clock.storage.data_source.data_source import StorageDataSource


class StorageApi:
    def __init__(self, data_source: StorageDataSource, scheduler: StorageScheduler):
        self.data_source = data_source
        self.scheduler = scheduler
        scheduler.set_context_manager(data_source.context_manager())
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

    def save_command(self, message: ApiObject, command: str, command_args: str):
        self.scheduler.schedule_no_result(
            lambda: self._save_command(message, command, command_args)
        )

    def set_inactive_chat(self, chat: ApiObject, reason: str):
        self.scheduler.schedule_no_result(
            lambda: self._set_inactive_chat(chat, reason)
        )

    def _init(self):
        self.data_source.init()

    def _save_query(self, query: ApiObject, time_point: TimePoint, locale: Locale, results_found: list,
                    results_sent: list, processing_seconds: float):
        self._save_user(query.from_)
        self.data_source.save_query(query.from_.id, time_point.id(), query.query, query.offset, str(locale),
                                    len(results_found), len(results_sent), processing_seconds)

    def _save_user(self, user: ApiObject):
        self.data_source.save_user(user.id, user.first_name, user.last_name, user.username, user.language_code)

    def _save_chosen_result(self, user: ApiObject, timestamp: str, chosen_zone_name: str, query: str,
                            choosing_seconds: float):
        # the query might have been retrieved from server-side cache and the user could be unknown for us
        self._save_user(user)
        self.data_source.save_chosen_result(user.id, timestamp, chosen_zone_name, query, choosing_seconds)

    def _save_message(self, message: ApiObject):
        user_id = None
        user = message.from_
        if user:
            user_id = user.id
            self._save_user(user)
        chat = message.chat
        self._save_chat(chat)
        self._set_active_chat(chat)
        is_forward = True if message.forward_date is not None else None
        reply_to_message = message.reply_to_message
        if reply_to_message:
            reply_to_message = reply_to_message.message_id
        is_edit = True if message.edit_date is not None else None
        left_chat_member = message.left_chat_member
        if left_chat_member:
            left_chat_member = left_chat_member.id
        new_chat_members = message.new_chat_members or [None]
        for new_chat_member in new_chat_members:
            if new_chat_member:
                new_chat_member = new_chat_member.id
            self.data_source.save_message(
                chat.id,
                message.message_id,
                user_id,
                message.date,
                is_forward,
                reply_to_message,
                is_edit,
                message.text,
                new_chat_member,
                left_chat_member,
                message.group_chat_created,
                message.migrate_to_chat_id,
                message.migrate_from_chat_id
            )

    def _save_chat(self, chat: ApiObject):
        self.data_source.save_chat(chat.id, chat.type, chat.title, chat.username)

    def _save_command(self, message: ApiObject, command: str, command_args: str):
        message_id = self.data_source.get_message_id(message.chat.id, message.message_id)
        self.data_source.save_command(message_id, command, command_args)

    def _set_active_chat(self, chat: ApiObject):
        self.data_source.set_active_chat(chat.id)

    def _set_inactive_chat(self, chat: ApiObject, reason: str):
        self.data_source.set_inactive_chat(chat.id, reason)
