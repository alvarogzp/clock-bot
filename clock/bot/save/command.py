from bot.action.core.action import Action

from clock.storage.api import StorageApi


class SaveCommandAction(Action):
    def __init__(self):
        super().__init__()
        self.storage = None  # type: StorageApi

    def post_setup(self):
        self.storage = self.cache.storage

    def process(self, event):
        self.storage.save_command(event.message, event.command, event.command_args)
