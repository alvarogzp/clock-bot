from bot.action.core.action import Action
from bot.action.util.textformat import FormattedText


class HelpAction(Action):
    def process(self, event):
        message = self._get_message()
        message.data["reply_markup"] = self._get_reply_markup()
        self.api.async.send_message(message.to_chat_replying(event.message))

    def _get_message(self):
        text = FormattedText()\
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
        return text.build_message()

    def _get_reply_markup(self):
        return {
            "inline_keyboard": [
                [self.__button("Get the current times in your country", "")],
                [self.__button("Get all times in United States", "US")],
                [self.__button("Get the UTC time", "UTC")],
                [self.__button("Get Los Angeles time", "Los Angeles")],
                [self.__button("Get all zones using Central European Time (CET)", "CET")],
                [self.__button("Get all zones in GMT+07", "-gmt +07")],
                [self.__button("Get all zones where it is now 11 hours", "-time 11")],
                [self.__button("Send the London time to someone else", "London", current_chat=False)]
            ]
        }

    @staticmethod
    def __button(text: str, query: str, current_chat: bool = True):
        switch_inline_query_key = "switch_inline_query_current_chat" if current_chat else "switch_inline_query"
        return {
            "text": text,
            switch_inline_query_key: query
        }
