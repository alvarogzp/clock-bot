from bot.action.core.action import Action
from bot.api.domain import ApiObject

from clock.bot.commands.util import messages
from clock.locale.getter import LocaleGetter


NO_RESULTS_PARAMETER = "no_results"


class StartAction(Action):
    def __init__(self):
        super().__init__()
        self.start_message = None  # initialized in post_setup

    def post_setup(self):
        self.start_message = messages.start(self.cache.bot_info)

    def process(self, event):
        user = event.message.from_
        if event.command_args == NO_RESULTS_PARAMETER:
            message = messages.troubleshoot(user, self.cache.zone_finder)
        else:
            message = self.start_message.copy()
        self.api.async.send_message(message.to_chat_replying(event.message))
        self._cache_user_locale(user)

    def _cache_user_locale(self, user: ApiObject):
        locale = LocaleGetter.from_user(user)
        self.cache.locale_cache.cache(locale)
