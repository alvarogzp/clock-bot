from bot.action.core.action import Action

from clock.storage.api import StorageApi


class SaveMessageAction(Action):
    def __init__(self):
        super().__init__()
        self.storage = None  # type: StorageApi

    def post_setup(self):
        self.storage = self.cache.storage

    def process(self, event):
        message = event.message
        self.storage.save_message(message)
        self._check_inactive(message)

    def _check_inactive(self, message):
        self._check_left_chat(message)
        self._check_chat_migrated(message)

    def _check_left_chat(self, message):
        left_chat_member = message.left_chat_member
        if left_chat_member is not None and left_chat_member.id == self.cache.bot_info.id:
            from_ = message.from_
            reason = "left, by: " + str(from_.id) if from_ is not None else "unknown"
            self.storage.set_inactive_chat(message.chat, reason)

    def _check_chat_migrated(self, message):
        migrate_to_chat_id = message.migrate_to_chat_id
        if migrate_to_chat_id is not None:
            reason = "migrated to: " + str(migrate_to_chat_id)
            self.storage.set_inactive_chat(message.chat, reason)
