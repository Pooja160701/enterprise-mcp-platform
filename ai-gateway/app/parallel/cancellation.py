import time
import uuid
from copy import deepcopy

from app.parallel.worker_pool import WorkerPool


class Cancellation:
    """
    Enterprise Cancellation

    Supports:

    ✓ Submit Tasks
    ✓ Cancel Tasks
    ✓ Wait
    ✓ Results
    ✓ Statistics
    ✓ Cleanup
    """

    def __init__(self):

        WorkerPool.initialize()

        self._tasks = {}
        self._results = {}
        self._cancelled = set()

    # -------------------------------------------------
    # Submit
    # -------------------------------------------------

    def submit(
        self,
        func,
        *args,
        **kwargs,
    ):

        task_id = str(uuid.uuid4())

        worker_id = WorkerPool.submit(
            func,
            *args,
            **kwargs,
        )

        self._tasks[task_id] = worker_id

        return task_id

    # -------------------------------------------------
    # Cancel
    # -------------------------------------------------

    def cancel(
        self,
        task_id,
    ):

        worker_id = self._tasks.get(task_id)

        if worker_id is None:
            return False

        WorkerPool.cancel(worker_id)

        self._cancelled.add(task_id)

        return True

    # -------------------------------------------------
    # Wait
    # -------------------------------------------------

    def wait(self):

        WorkerPool.wait()

        self._results.clear()

        for task_id, worker_id in self._tasks.items():

            if task_id in self._cancelled:

                self._results[task_id] = "Cancelled"

                continue

            try:

                self._results[task_id] = WorkerPool.result(worker_id)

            except Exception:

                self._results[task_id] = None

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

            WorkerPool.done(worker_id)

            for worker_id in self._tasks.values()

        )

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(self):

        completed = 0

        for worker_id in self._tasks.values():

            if WorkerPool.done(worker_id):

                completed += 1

        return {

            "registered": len(self._tasks),

            "cancelled": len(self._cancelled),

            "active": len(self._tasks) - completed,

            "global_cancel": False,

        }

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(self):

        self._tasks.clear()

        self._results.clear()

        self._cancelled.clear()

        WorkerPool.cleanup()

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @staticmethod
    def empty():

        return Cancellation()