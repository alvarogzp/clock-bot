from bot.multithreading.worker import Worker

from clock.storage.api import StorageApi
from clock.storage.async.scheduler import StorageScheduler
from clock.storage.data_source.data_sources.sqlite.sqlite import SqliteStorageDataSource


class StorageApiFactory:
    @classmethod
    def with_worker(cls, worker: Worker):
        data_source = cls._get_default_data_source()
        scheduler = cls._get_scheduler_for(worker)
        return StorageApi(data_source, scheduler)

    @staticmethod
    def _get_default_data_source():
        return SqliteStorageDataSource()

    @staticmethod
    def _get_scheduler_for(worker: Worker):
        return StorageScheduler(worker)
