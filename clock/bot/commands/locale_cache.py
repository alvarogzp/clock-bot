from bot.action.core.action import Action
from bot.action.util.textformat import FormattedText


class LocaleCacheAction(Action):
    def __init__(self):
        super().__init__()
        self.zone_finder_cache = None  # initialized in post_setup

    def post_setup(self):
        self.zone_finder_cache = self.cache.zone_finder_api.cache()

    def process(self, event):
        response = self.get_cached_locales()
        self.api.send_message(response.build_message().to_chat_replying(event.message))

    def get_cached_locales(self):
        cached_locales = self.zone_finder_cache.cached_locales()
        return FormattedText()\
            .concat(self.get_cached_locales_number(cached_locales))\
            .concat(self.get_cached_locales_names(cached_locales))

    @staticmethod
    def get_cached_locales_number(cached_locales: list):
        cached_locales_number = len(cached_locales)
        return FormattedText().normal("Cached locales: {number}")\
            .start_format().bold(number=cached_locales_number).end_format()

    @staticmethod
    def get_cached_locales_names(cached_locales: list):
        return FormattedText().join(
            [
                FormattedText().newline().normal(" - {name}").start_format().bold(name=locale).end_format()
                for locale in cached_locales
            ]
        )
