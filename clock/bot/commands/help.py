from bot.action.util.textformat import FormattedText

from clock.bot.commands.util.static_response import StaticResponseAction


class HelpAction(StaticResponseAction):
    def build_message(self):
        text = self._get_text()
        message = text.build_message()
        message.data["reply_markup"] = self._get_reply_markup()
        return message

    def _get_text(self):
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

    def _get_reply_markup(self):
        return {
            "inline_keyboard": [
                [self.switch_inline_button("Get the current times in your country", "")],
                [self.switch_inline_button("Get all times in United States", "US")],
                [self.switch_inline_button("Get the UTC time", "UTC")],
                [self.switch_inline_button("Get the time in Los Angeles", "Los Angeles")],
                [self.switch_inline_button("Get all zones using Central European Time (CET)", "CET")],
                [self.switch_inline_button("Get all zones in GMT+07", "-gmt +07")],
                [self.switch_inline_button("Get all zones where it is now 11 hours", "-time 11")],
                [self.switch_inline_button("Send the London time to someone else", "London", current_chat=False)]
            ]
        }
