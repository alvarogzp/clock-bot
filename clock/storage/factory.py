from bot.multithreading.worker import Worker

from clock.storage.api import StorageApi
from clock.storage.async.scheduler import StorageScheduler
from clock.storage.data_source.data_sources.sqlite.sqlite import SqliteStorageDataSource


class StorageApiFactory:
    def with_worker(self, worker: Worker, debug: bool):
        data_source = self._get_default_data_source(debug)
        scheduler = self._get_scheduler_for(worker)
        return StorageApi(data_source, scheduler)

    @staticmethod
    def _get_default_data_source(debug: bool):
        return SqliteStorageDataSource(debug)

    @staticmethod
    def _get_scheduler_for(worker: Worker):
        return StorageScheduler(worker)
