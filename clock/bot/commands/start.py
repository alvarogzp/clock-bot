from bot.action.core.action import Action
from bot.action.util.textformat import FormattedText


class StartAction(Action):
    def process(self, event):
        response = FormattedText()\
            .bold("👋 Hello! 👋").newline().newline()\
            .normal("I am {name}.").newline()\
            .bold("I can tell you the current time of any place in the world.").newline()\
            .normal("You have to use me in inline mode.").newline().newline()\
            .bold("👇 Tap any button below to try me 👇")\
            .start_format().bold(name=self._get_bot_name()).end_format()
        message = response.build_message()
        message.data["reply_markup"] = self._get_reply_markup()
        self.api.async.send_message(message.to_chat_replying(event.message))

    def _get_bot_name(self):
        return self.cache.bot_info.first_name

    @staticmethod
    def _get_reply_markup():
        return {
            "inline_keyboard": [
                [
                    {
                        "text": "What time is it in New York?",
                        "switch_inline_query_current_chat": "New York"
                    },
                ],
                [
                    {
                        "text": "Send the current time to someone",
                        "switch_inline_query": ""
                    },
                ]
            ]
        }
