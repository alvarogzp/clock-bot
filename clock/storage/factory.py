from bot.multithreading.worker import Worker

from clock.log.api import LogApi
from clock.storage.api import StorageApi
from clock.storage.async.scheduler import StorageScheduler
from clock.storage.data_source.data_sources.sqlite.sqlite import SqliteStorageDataSource


class StorageApiFactory:
    def __init__(self, logger: LogApi, debug: bool):
        self.logger = logger
        self.debug = debug

    def with_worker(self, worker: Worker):
        data_source = self._get_default_data_source()
        scheduler = self._get_scheduler_for(worker)
        return StorageApi(data_source, scheduler)

    def _get_default_data_source(self):
        return SqliteStorageDataSource(self.debug)

    @staticmethod
    def _get_scheduler_for(worker: Worker):
        return StorageScheduler(worker)
