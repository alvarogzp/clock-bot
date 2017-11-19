from bot.action.core.action import Action

from clock.log.api import LogApi
from clock.storage.api import StorageApi


class SaveMessageAction(Action):
    def __init__(self):
        super().__init__()
        self.storage = None  # type: StorageApi
        self.logger = None  # type: LogApi

    def post_setup(self):
        self.storage = self.cache.storage
        self.logger = self.cache.log_api

    def process(self, event):
        message = event.message
        self.storage.save_message(message)
        self._check_inactive(message)
        self.logger.log_message(message)

    def _check_inactive(self, message):
        self._check_left_chat(message)
        self._check_chat_migrated(message)

    def _check_left_chat(self, message):
        left_chat_member = message.left_chat_member
        if left_chat_member is not None and left_chat_member.id == self.cache.bot_info.id:
            self.storage.set_inactive_chat(message.chat, "left")

    def _check_chat_migrated(self, message):
        migrate_to_chat_id = message.migrate_to_chat_id
        if migrate_to_chat_id is not None:
            self.storage.set_inactive_chat(message.chat, "migrated")
