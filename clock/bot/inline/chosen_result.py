from bot.action.core.action import Action
from bot.multithreading.work import Work

from clock.domain.datetimezone import DateTimeZone
from clock.domain.time import TimePoint
from clock.log.api import LogApi
from clock.storage.api import StorageApi


class ChosenInlineResultClockAction(Action):
    def process(self, event):
        chosen_result = event.chosen_result
        user = chosen_result.from_
        timestamp, chosen_zone_name = self.__get_timestamp_and_chosen_zone_name_from_result_id(chosen_result.result_id)
        query = chosen_result.query
        choosing_seconds = self.__get_choosing_seconds(timestamp)

        self.scheduler.io(Work(
            lambda: StorageApi.get().save_chosen_result(user, timestamp, chosen_zone_name, query),
            "storage:save_chosen_result"
        ))

        # event.logger is async
        LogApi.get(event.logger).log_chosen_result(user, timestamp, chosen_zone_name, query, choosing_seconds)

    @staticmethod
    def __get_timestamp_and_chosen_zone_name_from_result_id(result_id):
        extracted_items = DateTimeZone.extract_items_from_id(result_id)
        if len(extracted_items) < 2:
            return extracted_items[0], ""
        return extracted_items

    @staticmethod
    def __get_choosing_seconds(timestamp: str):
        try:
            return TimePoint.current_timestamp() - float(timestamp)
        except ValueError:
            return 0
