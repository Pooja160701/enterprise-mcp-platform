from copy import deepcopy

from app.parallel.worker_pool import WorkerPool


class AsyncQueue:
    """
    Enterprise Async Queue

    Simple object-oriented async queue built on WorkerPool.
    """

    def __init__(self):
        WorkerPool.initialize()

        self._tasks = []
        self._task_ids = []
        self._results = []

    # -------------------------------------------------
    # Enqueue
    # -------------------------------------------------

    def enqueue(
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
    # Run
    # -------------------------------------------------

    def run(self):

        self._task_ids.clear()
        self._results.clear()

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
    # Task IDs
    # -------------------------------------------------

    def task_ids(self):

        return deepcopy(self._task_ids)

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(self):

        completed = sum(

            WorkerPool.done(task_id)

            for task_id in self._task_ids

        )

        return {

            "queued": len(self._tasks),

            "submitted": len(self._task_ids),

            "completed": completed,

        }

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(self):

        self._tasks.clear()
        self._task_ids.clear()
        self._results.clear()

        WorkerPool.cleanup()

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @staticmethod
    def empty():

        return AsyncQueue()