from bot.action.core.action import Action

from clock.bot.commands.util import messages


class PrivacyAction(Action):
    def __init__(self):
        super().__init__()
        self.privacy_message = None  # initialized in post_setup

    def post_setup(self):
        self.privacy_message = messages.privacy(self.cache.bot_info)

    def process(self, event):
        self.api.async.send_message(self.privacy_message.copy().to_chat_replying(event.message))
