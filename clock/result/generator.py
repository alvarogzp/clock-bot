from typing import Union

from babel import Locale

from clock.domain.country import Country
from clock.domain.time import TimePoint
from clock.domain.zone import Zone
from clock.result.formatter.factory import ResultFormatterFactory


class ResultGenerator:
    @classmethod
    def generate(cls, time_point: TimePoint, locale: Locale, zones: list):
        return [cls._get_result_formatter(time_point, zone, locale).result() for zone in zones]

    @staticmethod
    def _get_result_formatter(time_point: TimePoint, zone: Union[Zone, Country], locale: Locale):
        return ResultFormatterFactory.get(time_point, zone, locale)
