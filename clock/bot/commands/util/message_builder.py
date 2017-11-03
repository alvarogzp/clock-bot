class MessageWithReplyMarkupBuilder:
    def get_message(self):
        text = self.get_text()
        message = text.build_message()
        message.data["reply_markup"] = self.get_reply_markup()
        return message

    def get_text(self):
        raise NotImplementedError()

    def get_reply_markup(self):
        raise NotImplementedError()

    @staticmethod
    def switch_inline_button(text: str, query: str, current_chat: bool = True):
        switch_inline_query_key = "switch_inline_query_current_chat" if current_chat else "switch_inline_query"
        return {
            "text": text,
            switch_inline_query_key: query
        }
