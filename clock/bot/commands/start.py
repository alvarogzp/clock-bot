from bot.action.core.action import Action

from clock.bot.commands.util.messages.start import StartMessageBuilder


class StartAction(Action):
    def __init__(self):
        super().__init__()
        self.start_message = None  # initialized in post_setup

    def post_setup(self):
        self.start_message = StartMessageBuilder(self.cache).get_message()

    def process(self, event):
        self.api.async.send_message(self.start_message.copy().to_chat_replying(event.message))
