import json
import time
from bot.action.core.action import Action


class InlineClockAction(Action):
    def process(self, event):
        query_id = event.query.id
        timestamp = time.asctime(time.gmtime())
        result = {
            "type": "article",
            "id": "current_time",
            "title": "UTC",
            "input_message_content": {
                "message_text": timestamp,
                "disable_web_page_preview": True
            },
            "description": timestamp,
            "thumb_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Icons8_flat_clock.svg/2000px-Icons8_flat_clock.svg.png"
        }
        results = json.dumps([result], separators=(',', ':'))
        self.api.answerInlineQuery(inline_query_id=query_id, results=results, cache_time=0, is_personal=True)
