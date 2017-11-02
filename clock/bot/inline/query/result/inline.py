from clock.result import Result


class InlineResult:
    @staticmethod
    def from_result(result: Result):
        return {
            "type": "article",
            "id": result.id(),
            "title": result.title(),
            "input_message_content": {
                "message_text": result.message(),
                "parse_mode": "HTML",
                "disable_web_page_preview": True
            },
            "description": result.description(),
            "thumb_url": result.image_url()
        }
