import threading
import time
import uuid
from copy import deepcopy

from app.parallel.worker_pool import WorkerPool


class TaskScheduler:
    """
    Enterprise Task Scheduler

    Schedules work on top of WorkerPool.

    Features

    ✓ Immediate Tasks
    ✓ Delayed Tasks
    ✓ Periodic Tasks
    ✓ Cancel Tasks
    ✓ Wait Tasks
    ✓ Statistics
    """

    _scheduled = {}
    _lock = threading.Lock()

    # -------------------------------------------------
    # Initialize
    # -------------------------------------------------

    @classmethod
    def initialize(cls):
        """
        Initialize the scheduler.
        """
        WorkerPool.initialize()
        return cls


    # -------------------------------------------------
    # Shutdown
    # -------------------------------------------------

    @classmethod
    def shutdown(cls):
        """
        Shutdown scheduler and worker pool.
        """
        cls.clear()
        WorkerPool.shutdown()


    # -------------------------------------------------
    # Result
    # -------------------------------------------------

    @classmethod
    def result(
        cls,
        task_id,
        timeout=None,
    ):
        """
        Return the result of a task.
        """

        with cls._lock:
            task = cls._scheduled.get(task_id)

        if not task:
            return None

        worker = task.get("worker_task", task_id)

        return WorkerPool.result(
            worker,
            timeout=timeout,
        )


    # -------------------------------------------------
    # Done
    # -------------------------------------------------

    @classmethod
    def done(
        cls,
        task_id,
    ):
        """
        True if task has completed.
        """

        with cls._lock:
            task = cls._scheduled.get(task_id)

        if not task:
            return False

        worker = task.get("worker_task", task_id)

        return WorkerPool.done(worker)


    # -------------------------------------------------
    # Task IDs
    # -------------------------------------------------

    @classmethod
    def task_ids(cls):
        """
        Return all scheduled task IDs.
        """

        with cls._lock:
            return list(cls._scheduled.keys())
    
    # -------------------------------------------------
    # Schedule Immediate Task
    # -------------------------------------------------

    @classmethod
    def submit(
        cls,
        func,
        *args,
        **kwargs,
    ):

        WorkerPool.initialize()

        task_id = WorkerPool.submit(
            func,
            *args,
            **kwargs,
        )

        with cls._lock:

            cls._scheduled[task_id] = {

                "type": "immediate",

                "status": "submitted",

                "created_at": time.time(),

            }

        return task_id

    # -------------------------------------------------
    # Delayed Task
    # -------------------------------------------------

    @classmethod
    def schedule(
        cls,
        delay,
        func,
        *args,
        **kwargs,
    ):

        task_id = str(uuid.uuid4())

        def runner():

            time.sleep(delay)

            WorkerPool.initialize()

            worker_task = WorkerPool.submit(

                func,

                *args,

                **kwargs,

            )

            with cls._lock:

                cls._scheduled[task_id]["worker_task"] = worker_task

                cls._scheduled[task_id]["status"] = "running"

        thread = threading.Thread(

            target=runner,

            daemon=True,

        )

        with cls._lock:

            cls._scheduled[task_id] = {

                "type": "delayed",

                "delay": delay,

                "status": "scheduled",

                "created_at": time.time(),

                "thread": thread,

            }

        thread.start()

        return task_id

    # -------------------------------------------------
    # Repeating Task
    # -------------------------------------------------

    @classmethod
    def every(
        cls,
        interval,
        func,
        *args,
        **kwargs,
    ):

        task_id = str(uuid.uuid4())

        stop_event = threading.Event()

        def loop():

            while not stop_event.is_set():

                WorkerPool.submit(

                    func,

                    *args,

                    **kwargs,

                )

                stop_event.wait(interval)

        thread = threading.Thread(

            target=loop,

            daemon=True,

        )

        with cls._lock:

            cls._scheduled[task_id] = {

                "type": "periodic",

                "interval": interval,

                "status": "running",

                "thread": thread,

                "stop_event": stop_event,

                "created_at": time.time(),

            }

        thread.start()

        return task_id

    # -------------------------------------------------
    # Cancel
    # -------------------------------------------------

    @classmethod
    def cancel(
        cls,
        task_id,
    ):

        with cls._lock:

            task = cls._scheduled.get(task_id)

            if not task:

                return False

            #
            # Periodic Task
            #

            if task["type"] == "periodic":

                task["stop_event"].set()

                task["status"] = "cancelled"

                return True

            #
            # Immediate / Delayed
            #

            worker = task.get("worker_task")

            if worker:

                WorkerPool.cancel(worker)

                task["status"] = "cancelled"

                return True

            task["status"] = "cancelled"

            return True

    # -------------------------------------------------
    # Status
    # -------------------------------------------------

    @classmethod
    def status(
        cls,
        task_id,
    ):

        with cls._lock:

            return deepcopy(

                cls._scheduled.get(

                    task_id,

                    {},

                )

            )

    # -------------------------------------------------
    # Wait
    # -------------------------------------------------

    @classmethod
    def wait(
        cls,
        task_id=None,
        timeout=None,
    ):
        """
        Wait for one task or all tasks.
        """

        if task_id is None:
            WorkerPool.wait()
            return

        with cls._lock:
            task = cls._scheduled.get(task_id)

        if not task:
            return None

        worker = task.get("worker_task", task_id)

        return WorkerPool.result(
            worker,
            timeout=timeout,
        )

    # -------------------------------------------------
    # Wait All
    # -------------------------------------------------

    @classmethod
    def wait_all(
        cls,
    ):

        WorkerPool.wait()

    # -------------------------------------------------
    # Cleanup
    # -------------------------------------------------

    @classmethod
    def cleanup(cls):

        WorkerPool.cleanup()

        with cls._lock:

            remove = []

            for task_id in cls._scheduled:

                if WorkerPool.done(task_id):
                    remove.append(task_id)

            for task_id in remove:
                cls._scheduled.pop(task_id, None)

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    @classmethod
    def statistics(
        cls,
    ):

        with cls._lock:

            total = len(cls._scheduled)

            periodic = sum(

                task["type"] == "periodic"

                for task in cls._scheduled.values()

            )

            delayed = sum(

                task["type"] == "delayed"

                for task in cls._scheduled.values()

            )

            immediate = sum(

                task["type"] == "immediate"

                for task in cls._scheduled.values()

            )

        return {

            "total": total,

            "immediate": immediate,

            "delayed": delayed,

            "periodic": periodic,

            "worker_pool": WorkerPool.statistics(),

        }

    # -------------------------------------------------
    # All Tasks
    # -------------------------------------------------

    @classmethod
    def tasks(
        cls,
    ):

        with cls._lock:

            return deepcopy(

                cls._scheduled,

            )

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    @classmethod
    def clear(
        cls,
    ):

        with cls._lock:

            for task in cls._scheduled.values():

                if task.get("type") == "periodic":

                    task["stop_event"].set()

            cls._scheduled.clear()