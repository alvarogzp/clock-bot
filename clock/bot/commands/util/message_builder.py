class MessageWithReplyMarkupBuilder:
    def get_message(self):
        text = self.get_text()
        message = text.build_message()
        reply_markup = self.get_reply_markup()
        if reply_markup is not None:
            message.with_reply_markup(reply_markup)
        return message

    def get_text(self):
        raise NotImplementedError()

    def get_reply_markup(self):
        return None
