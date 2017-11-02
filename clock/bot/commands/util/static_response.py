from bot.action.core.action import Action


class StaticResponseAction(Action):
    def __init__(self, async_response: bool = True):
        super().__init__()
        self.async_response = async_response
        self.message = None  # built on post_setup, as access to config, state or cache may be necessary to build it

    def post_setup(self):
        self.message = self.build_message()
        if self.async_response:
            self.api = self.api.async

    def build_message(self):
        raise NotImplementedError()

    @staticmethod
    def switch_inline_button(text: str, query: str, current_chat: bool = True):
        switch_inline_query_key = "switch_inline_query_current_chat" if current_chat else "switch_inline_query"
        return {
            "text": text,
            switch_inline_query_key: query
        }

    def process(self, event):
        self.api.send_message(self.message.to_chat_replying(event.message))
