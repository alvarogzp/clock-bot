from bot.action.util.reply_markup.inline_keyboard.button import InlineKeyboardButton
from bot.action.util.reply_markup.inline_keyboard.markup import InlineKeyboardMarkup
from bot.action.util.textformat import FormattedText
from bot.api.domain import ApiObject

from clock.bot.commands.util.message_builder import MessageWithReplyMarkupBuilder


class StartMessageBuilder(MessageWithReplyMarkupBuilder):
    def __init__(self, bot_user: ApiObject):
        self.bot_name = bot_user.first_name

    def get_text(self):
        return FormattedText()\
            .bold("👋 Hello! 👋").newline().newline()\
            .normal("I am {name}.").newline()\
            .bold("I can tell you the current time of any place in the world.").newline()\
            .normal("You have to use me in inline mode.").newline().newline()\
            .normal("👉 Use the /help command to get more info and cool examples.").newline().newline()\
            .bold("👇 Tap any button below to try me 👇")\
            .start_format()\
            .bold(name=self.bot_name)\
            .end_format()

    def get_reply_markup(self):
        switch_inline_button = InlineKeyboardButton.switch_inline_query
        return InlineKeyboardMarkup.with_fixed_columns(1)\
            .add(switch_inline_button("What time is it in New York?", "New York", current_chat=True))\
            .add(switch_inline_button("Send the current time to someone", "", current_chat=False))
