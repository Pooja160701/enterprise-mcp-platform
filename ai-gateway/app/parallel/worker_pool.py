from concurrent.futures import ThreadPoolExecutor, Future
from threading import Lock
from typing import Callable, Dict, List, Optional
import uuid


class WorkerPool:
    """
    Enterprise Worker Pool

    Manages a pool of worker threads for executing tasks
    concurrently.

    Features

    ✓ Thread Pool
    ✓ Submit Tasks
    ✓ Track Running Tasks
    ✓ Wait for Completion
    ✓ Cancel Pending Tasks
    ✓ Statistics
    """

    DEFAULT_WORKERS = 8

    _executor: Optional[ThreadPoolExecutor] = None
    _futures: Dict[str, Future] = {}
    _lock = Lock()

    # -------------------------------------------------
    # Initialize
    # -------------------------------------------------

    @classmethod
    def initialize(
        cls,
        max_workers: int = DEFAULT_WORKERS,
    ):
        """
        Create the worker pool.
        """

        if cls._executor is None:
            cls._executor = ThreadPoolExecutor(
                max_workers=max_workers,
                thread_name_prefix="enterprise-worker",
            )

    # -------------------------------------------------
    # Submit Task
    # -------------------------------------------------

    @classmethod
    def submit(
        cls,
        func: Callable,
        *args,
        **kwargs,
    ) -> str:
        """
        Submit a task.

        Returns
        -------
        task_id
        """

        if cls._executor is None:
            cls.initialize()

        task_id = str(uuid.uuid4())

        future = cls._executor.submit(
            func,
            *args,
            **kwargs,
        )

        with cls._lock:
            cls._futures[task_id] = future

        return task_id

    # -------------------------------------------------
    # Future
    # -------------------------------------------------

    @classmethod
    def future(
        cls,
        task_id: str,
    ) -> Optional[Future]:

        with cls._lock:
            return cls._futures.get(task_id)

    # -------------------------------------------------
    # Result
    # -------------------------------------------------

    @classmethod
    def result(
        cls,
        task_id: str,
        timeout: Optional[float] = None,
    ):

        future = cls.future(task_id)

        if future is None:
            return None

        return future.result(timeout=timeout)

    # -------------------------------------------------
    # Done
    # -------------------------------------------------

    @classmethod
    def done(
        cls,
        task_id: str,
    ) -> bool:

        future = cls.future(task_id)

        if future is None:
            return False

        return future.done()

    # -------------------------------------------------
    # Cancel
    # -------------------------------------------------

    @classmethod
    def cancel(
        cls,
        task_id: str,
    ) -> bool:

        future = cls.future(task_id)

        if future is None:
            return False

        return future.cancel()

    # -------------------------------------------------
    # Wait All
    # -------------------------------------------------

    @classmethod
    def wait(
        cls,
    ):
        """
        Wait until every submitted task finishes.
        """

        with cls._lock:
            futures = list(cls._futures.values())

        for future in futures:
            try:
                future.result()
            except Exception:
                pass

    # -------------------------------------------------
    # Cleanup Completed
    # -------------------------------------------------

    @classmethod
    def cleanup(
        cls,
    ):
        """
        Remove completed tasks from memory.
        """

        with cls._lock:

            completed = [

                task_id

                for task_id, future in cls._futures.items()

                if future.done()

            ]

            for task_id in completed:
                del cls._futures[task_id]

    # -------------------------------------------------
    # Shutdown
    # -------------------------------------------------

    @classmethod
    def shutdown(
        cls,
        wait: bool = True,
    ):
        """
        Shutdown the worker pool.
        """

        if cls._executor:

            cls._executor.shutdown(
                wait=wait,
            )

        cls._executor = None

        with cls._lock:
            cls._futures.clear()

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    @classmethod
    def statistics(
        cls,
    ):

        with cls._lock:

            total = len(cls._futures)

            completed = sum(
                future.done()
                for future in cls._futures.values()
            )

            running = sum(
                future.running()
                for future in cls._futures.values()
            )

            pending = total - completed - running

        return {
            "workers": cls.DEFAULT_WORKERS,
            "tasks": total,
            "running": running,
            "completed": completed,
            "pending": pending,
        }

    # -------------------------------------------------
    # Active Task IDs
    # -------------------------------------------------

    @classmethod
    def task_ids(
        cls,
    ) -> List[str]:

        with cls._lock:
            return list(cls._futures.keys())

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @classmethod
    def clear(
        cls,
    ):

        with cls._lock:
            cls._futures.clear()