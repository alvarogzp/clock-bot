from typing import Union

from babel import Locale

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
