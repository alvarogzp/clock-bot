from bot.action.core.action import Action

from clock.bot.commands.util import messages


class HelpAction(Action):
    def __init__(self):
        super().__init__()
        self.help_message = None  # initialized in post_setup

    def post_setup(self):
        self.help_message = messages.help(self.cache.bot_info)

    def process(self, event):
        self.api.async.send_message(self.help_message.copy().to_chat_replying(event.message))
