from bot.action.util.textformat import FormattedText

from clock.bot.commands.util.static_response import StaticResponseAction


class StartAction(StaticResponseAction):
    def build_message(self):
        text = self._get_text()
        message = text.build_message()
        message.data["reply_markup"] = self._get_reply_markup()
        return message

    def _get_text(self):
        return FormattedText()\
            .bold("👋 Hello! 👋").newline().newline()\
            .normal("I am {name}.").newline()\
            .bold("I can tell you the current time of any place in the world.").newline()\
            .normal("You have to use me in inline mode.").newline().newline()\
            .bold("👇 Tap any button below to try me 👇")\
            .start_format().bold(name=self._get_bot_name()).end_format()

    def _get_bot_name(self):
        return self.cache.bot_info.first_name

    def _get_reply_markup(self):
        return {
            "inline_keyboard": [
                [self.switch_inline_button("What time is it in New York?", "New York", current_chat=True)],
                [self.switch_inline_button("Send the current time to someone", "", current_chat=False)]
            ]
        }
