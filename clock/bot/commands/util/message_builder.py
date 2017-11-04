class MessageWithReplyMarkupBuilder:
    def get_message(self):
        text = self.get_text()
        reply_markup = self.get_reply_markup()
        return text.build_message().with_reply_markup(reply_markup)

    def get_text(self):
        raise NotImplementedError()

    def get_reply_markup(self):
        raise NotImplementedError()
