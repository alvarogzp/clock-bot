from bot.action.util.textformat import FormattedText
from bot.api.domain import ApiObject

from clock.bot.commands.util.message_builder import MessageWithReplyMarkupBuilder


class PrivacyMessageBuilder(MessageWithReplyMarkupBuilder):
    def __init__(self, bot_user: ApiObject):
        self.bot_name = bot_user.first_name

    def get_text(self):
        return FormattedText()\
            .bold("🤝  Thanks for using {bot_name}  🤝")\
            .newline().newline()\
            .normal("We take privacy very seriously and want to make sure you understand where the information "
                    "we receive about you comes from, and how we use it to give you the best experience.")\
            .newline().newline()\
            .normal("You can read the information that the bot receives and how it is used on the following link:")\
            .newline()\
            .normal("👉 https://github.com/alvarogzp/clock-bot/wiki/Privacy")\
            .newline().newline()\
            .normal("You can check the information we are receiving from your Telegram profile with the following "
                    "command:")\
            .newline()\
            .normal("👉 /me")\
            .start_format()\
            .normal(bot_name=self.bot_name)\
            .end_format()
