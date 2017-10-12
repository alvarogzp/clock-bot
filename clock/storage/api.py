from babel import Locale
from bot.api.domain import ApiObject

from clock.domain.time import TimePoint
from clock.storage.data_source.data_sources.sqlite import SqliteStorageDataSource


class StorageApi:
    _instance = None

    @classmethod
    def get(cls):
        """:rtype: StorageApi"""
        if cls._instance is None:
            cls._instance = StorageApi()
        return cls._instance

    def __init__(self):
        self.data_source = SqliteStorageDataSource()

    def save_query(self, query: ApiObject, time_point: TimePoint, locale: Locale, results_found: list,
                   results_sent: list):
        self._save_user(query.from_)
        self.data_source.save_query(query.from_.id, time_point.id(), query.query, query.offset, str(locale),
                                    len(results_found), len(results_sent))
        self.data_source.commit()

    def _save_user(self, user: ApiObject):
        self.data_source.save_user(user.id, user.first_name, user.last_name, user.username, user.language_code)

    def save_chosen_result(self, user: ApiObject, timestamp: str, chosen_zone_name: str, query: str):
        self.data_source.save_chosen_result(user.id, timestamp, chosen_zone_name, query)
        self.data_source.commit()
