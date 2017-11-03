from bot.action.util.reply_markup.inline_keyboard.button import InlineKeyboardButton
from bot.action.util.reply_markup.inline_keyboard.markup import InlineKeyboardMarkup
from bot.action.util.textformat import FormattedText
from bot.storage import Cache

from clock.bot.commands.util.message_builder import MessageWithReplyMarkupBuilder


class HelpMessageBuilder(MessageWithReplyMarkupBuilder):
    def __init__(self, cache: Cache):
        self.cache = cache

    def get_text(self):
        return FormattedText()\
            .bold("📎 Here you have some tips on how to use the bot correctly").newline().newline()\
            .normal("👉 First of all, you have to use the bot in inline mode.").newline()\
            .normal("{inline_bots_telegram_url}.").newline().newline()\
            .normal("👉 To get the current time in your country, make an inline request without query, "
                    "that is, just type the username of the bot ({bot_username}) "
                    "and add an empty space.").newline()\
            .normal("Send the result you want to the chat by tapping on it.").newline().newline()\
            .normal("👉 To get the time of another place, just type a country, a time-zone location "
                    "or a time-zone name. Type them in your language.").newline().newline()\
            .normal("👉 For more info and advanced search options, see the {search_page} "
                    "of the bot wiki.").newline().newline()\
            .bold("👇 Try any of the buttons below to get some examples 👇").newline()\
            .normal("Pay attention to what appears on the search box to learn how to do it by yourself!")\
            .start_format()\
            .url(
                "Click here to learn how to use Telegram bots in inline mode",
                "https://telegram.org/blog/inline-bots#how-does-it-work",
                "inline_bots_telegram_url"
            )\
            .code_inline(bot_username="@" + self.cache.bot_info.username)\
            .url(
                "search documentation page",
                "https://github.com/alvarogzp/clock-bot/wiki/Search",
                "search_page"
            )\
            .end_format()

    def get_reply_markup(self):
        switch_inline_button = InlineKeyboardButton.switch_inline_query
        return InlineKeyboardMarkup.with_fixed_columns(1)\
            .add(switch_inline_button("Get the current times in your country", ""))\
            .add(switch_inline_button("Get all times in United States", "US"))\
            .add(switch_inline_button("Get the UTC time", "UTC"))\
            .add(switch_inline_button("Get the time in Los Angeles", "Los Angeles"))\
            .add(switch_inline_button("Get all zones using Central European Time (CET)", "CET"))\
            .add(switch_inline_button("Get all zones in GMT+07", "-gmt +07"))\
            .add(switch_inline_button("Get all zones where it is now 11 hours", "-time 11"))\
            .add(switch_inline_button("Send the London time to someone else", "London", current_chat=False))
