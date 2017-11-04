from bot.action.core.action import Action

from clock.bot.commands.util import messages


class TroubleshootAction(Action):
    def process(self, event):
        message = messages.troubleshoot(event.message.from_, self.cache.zone_finder)
        self.api.async.send_message(message.to_chat_replying(event.message))
