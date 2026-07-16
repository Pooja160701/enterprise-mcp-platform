from copy import deepcopy

from app.parallel.worker_pool import WorkerPool
from app.parallel.task_scheduler import TaskScheduler
from app.parallel.parallel_group import ParallelGroup
from app.parallel.async_queue import AsyncQueue
from app.parallel.concurrency_limiter import ConcurrencyLimiter
from app.parallel.cancellation import Cancellation


class ParallelExecutor:
    """
    Enterprise Parallel Executor
    """

    def __init__(self):

        WorkerPool.initialize()

        self.queue = AsyncQueue()
        self.limiter = ConcurrencyLimiter()
        self.cancellation = Cancellation()

        self._tasks = []
        self._task_ids = []
        self._results = []

    # -------------------------------------------------
    # Submit
    # -------------------------------------------------

    def submit(
        self,
        func,
        *args,
        **kwargs,
    ):

        self._tasks.append(
            (
                func,
                args,
                kwargs,
            )
        )

        return self

    # -------------------------------------------------
    # Execute
    # -------------------------------------------------

    def run(self):

        self._task_ids.clear()

        for func, args, kwargs in self._tasks:

            task_id = WorkerPool.submit(
                func,
                *args,
                **kwargs,
            )

            self._task_ids.append(task_id)

        return self

    # -------------------------------------------------
    # Wait
    # -------------------------------------------------

    def wait(self):

        WorkerPool.wait()

        self._results = []

        for task_id in self._task_ids:

            self._results.append(
                WorkerPool.result(task_id)
            )

        return self

    # -------------------------------------------------
    # Results
    # -------------------------------------------------

    def results(self):

        return deepcopy(self._results)

    # -------------------------------------------------
    # Done
    # -------------------------------------------------

    def done(self):

        return all(

            WorkerPool.done(task_id)

            for task_id in self._task_ids

        )

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(self):

        completed = sum(

            WorkerPool.done(task_id)

            for task_id in self._task_ids

        )

        return {

            "submitted": len(self._task_ids),

            "completed": completed,

            "queued": len(self._tasks),

            "worker_pool": WorkerPool.statistics(),

            "queue": self.queue.statistics(),

            "limiter": self.limiter.statistics(),

            "cancellation": self.cancellation.statistics(),

        }

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(self):

        self._tasks.clear()

        self._task_ids.clear()

        self._results.clear()

        self.queue.clear()

        self.limiter.clear()

        self.cancellation.clear()

        WorkerPool.cleanup()

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @staticmethod
    def empty():

        return ParallelExecutor()