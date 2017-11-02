class ResultFormatter:
    def id(self):
        raise NotImplementedError()

    def title(self):
        raise NotImplementedError()

    def description(self):
        raise NotImplementedError()

    def message(self):
        raise NotImplementedError()

    def image_url(self):
        raise NotImplementedError()

    def result(self):
        return {
            "type": "article",
            "id": self.id(),
            "title": self.title(),
            "input_message_content": {
                "message_text": self.message(),
                "parse_mode": "HTML",
                "disable_web_page_preview": True
            },
            "description": self.description(),
            "thumb_url": self.image_url()
        }
