from typing import Union, Optional

from babel import Locale
from bot.api.domain import ApiObject

from clock.bot.commands.start import NO_RESULTS_PARAMETER
from clock.bot.inline.query.result.inline import InlineResult
from clock.domain.country import Country
from clock.domain.time import TimePoint
from clock.domain.zone import Zone
from clock.result.factory import ResultFactory


class InlineResultGenerator:
    @classmethod
    def generate(cls, time_point: TimePoint, locale: Locale, zones: list):
        return [cls._get_inline_result(time_point, zone, locale) for zone in zones]

    @staticmethod
    def _get_inline_result(time_point: TimePoint, zone: Union[Zone, Country], locale: Locale):
        result = ResultFactory.get(time_point, zone, locale)
        return InlineResult.from_result(result)


class AnswerInlineQueryResultGenerator:
    @staticmethod
    def generate(query: ApiObject, results: list, next_offset: Optional[str]):
        result = {
            "inline_query_id": query.id,
            "results": results,
            "next_offset": next_offset,
            "cache_time": 0,
            "is_personal": True
        }
        if len(results) == 0:
            result["switch_pm_text"] = "☹ No results for '{query}' ☹".format(query=query.query)
            result["switch_pm_parameter"] = NO_RESULTS_PARAMETER
        return result
