from copy import deepcopy

from app.parallel.worker_pool import WorkerPool


class ParallelGroup:
    """
    Enterprise Parallel Group
    """

    def __init__(self):

        WorkerPool.initialize()

        self._tasks = []
        self._task_ids = []
        self._results = []

    # -------------------------------------------------
    # Add Task
    # -------------------------------------------------

    def add(
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
        self._results.clear()

        for func, args, kwargs in self._tasks:

            task_id = WorkerPool.submit(
                func,
                *args,
                **kwargs,
            )

            self._task_ids.append(task_id)

        WorkerPool.wait()

        for task_id in self._task_ids:

            try:

                value = WorkerPool.result(task_id)

                self._results.append(value)

            except Exception as exc:

                self._results.append(exc)

        return deepcopy(self._results)

    # -------------------------------------------------
    # Wait
    # -------------------------------------------------

    def wait(self):

        WorkerPool.wait()

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
    # Clear
    # -------------------------------------------------

    def clear(self):

        self._tasks.clear()
        self._task_ids.clear()
        self._results.clear()

        WorkerPool.cleanup()

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(self):

        completed = 0

        for task_id in self._task_ids:

            if WorkerPool.done(task_id):
                completed += 1

        return {

            "tasks": len(self._tasks),

            "completed": completed,

        }

    # -------------------------------------------------
    # Successful Results
    # -------------------------------------------------

    def successful(self):

        return [

            r

            for r in self._results

            if not isinstance(r, Exception)

        ]

    # -------------------------------------------------
    # Failed Results
    # -------------------------------------------------

    def failed(self):

        return [

            r

            for r in self._results

            if isinstance(r, Exception)

        ]

    # -------------------------------------------------
    # Has Failures
    # -------------------------------------------------

    def has_failures(self):

        return len(self.failed()) > 0

    # -------------------------------------------------
    # All Successful
    # -------------------------------------------------

    def all_successful(self):

        return not self.has_failures()

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @staticmethod
    def empty():

        return ParallelGroup()