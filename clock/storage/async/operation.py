import queue

from bot.multithreading.work import Work
from bot.multithreading.worker import Worker


class StorageOperation:
    def __init__(self, worker: Worker, context_manager, func: callable, ignore_result: bool):
        self.worker = worker
        self.context_manager = context_manager
        self.func = func
        self.ignore_result = ignore_result
        self.result_queue = queue.Queue() if not ignore_result else None

    def execute(self):
        work = self._get_work()
        self.worker.post(work)
        if not self.ignore_result:
            # block until result is obtained, and return it
            return self.result_queue.get()

    def _get_work(self):
        func = self._wrapper_func
        name = "storage_operation"
        return Work(func, name)

    def _wrapper_func(self):
        result = None
        try:
            result = self._run_func_in_context_manager()
        finally:
            if not self.ignore_result:
                # always put a result, even if the operation crashes,
                # to avoid caller from getting deadlocked waiting for the result
                self.result_queue.put(result)

    def _run_func_in_context_manager(self):
        with self.context_manager:
            return self.func()
