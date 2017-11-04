from bot.action.core.action import Action

from clock.bot.commands.util import messages


NO_RESULTS_PARAMETER = "no_results"


class StartAction(Action):
    def __init__(self):
        super().__init__()
        self.start_message = None  # initialized in post_setup

    def post_setup(self):
        self.start_message = messages.start(self.cache.bot_info)

    def process(self, event):
        if event.command_args == NO_RESULTS_PARAMETER:
            message = messages.troubleshoot(event.message.from_, self.cache.zone_finder)
        else:
            message = self.start_message.copy()
        self.api.async.send_message(message.to_chat_replying(event.message))
