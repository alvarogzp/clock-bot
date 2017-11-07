from bot.action.core.action import Action

from clock.storage.api import StorageApi


class SaveMessageAction(Action):
    def __init__(self):
        super().__init__()
        self.storage = None  # type: StorageApi

    def post_setup(self):
        self.storage = self.cache.storage

    def process(self, event):
        self.storage.save_message(event.message)
