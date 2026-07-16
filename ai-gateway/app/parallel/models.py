from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import time
import uuid


# -------------------------------------------------
# Task
# -------------------------------------------------

@dataclass
class ParallelTask:
    """
    Represents a single executable task.
    """

    func: Callable
    args: tuple = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)

    id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    name: str = ""

    priority: int = 0

    created_at: float = field(
        default_factory=time.time
    )


# -------------------------------------------------
# Task Result
# -------------------------------------------------

@dataclass
class TaskResult:
    """
    Result of a completed task.
    """

    task_id: str

    status: str

    result: Any = None

    error: Optional[str] = None

    started_at: float = 0.0

    completed_at: float = 0.0

    execution_time: float = 0.0


# -------------------------------------------------
# Queue Item
# -------------------------------------------------

@dataclass
class QueueItem:
    """
    Item stored in AsyncQueue.
    """

    task: ParallelTask

    queued_at: float = field(
        default_factory=time.time
    )


# -------------------------------------------------
# Scheduled Task
# -------------------------------------------------

@dataclass
class ScheduledTask:
    """
    Task managed by TaskScheduler.
    """

    id: str

    task: ParallelTask

    schedule_type: str

    delay: float = 0.0

    interval: float = 0.0

    status: str = "scheduled"

    worker_task: Optional[str] = None

    created_at: float = field(
        default_factory=time.time
    )


# -------------------------------------------------
# Parallel Group
# -------------------------------------------------

@dataclass
class ParallelGroupResult:
    """
    Collection of parallel task results.
    """

    results: List[TaskResult] = field(
        default_factory=list
    )

    started_at: float = field(
        default_factory=time.time
    )

    completed_at: float = 0.0

    @property
    def successful(self):

        return [

            r

            for r in self.results

            if r.status == "completed"

        ]

    @property
    def failed(self):

        return [

            r

            for r in self.results

            if r.status == "failed"

        ]

    @property
    def total(self):

        return len(self.results)


# -------------------------------------------------
# Cancellation Token
# -------------------------------------------------

@dataclass
class CancellationToken:
    """
    Cancellation state for a task.
    """

    task_id: str

    cancelled: bool = False

    created_at: float = field(
        default_factory=time.time
    )

    cancelled_at: Optional[float] = None


# -------------------------------------------------
# Concurrency Statistics
# -------------------------------------------------

@dataclass
class ConcurrencyStatistics:

    limit: int = 0

    running: int = 0

    available: int = 0

    utilization: float = 0.0

    full: bool = False


# -------------------------------------------------
# Worker Pool Statistics
# -------------------------------------------------

@dataclass
class WorkerPoolStatistics:

    workers: int = 0

    tasks: int = 0

    running: int = 0

    completed: int = 0

    pending: int = 0


# -------------------------------------------------
# Scheduler Statistics
# -------------------------------------------------

@dataclass
class SchedulerStatistics:

    total: int = 0

    immediate: int = 0

    delayed: int = 0

    periodic: int = 0


# -------------------------------------------------
# Queue Statistics
# -------------------------------------------------

@dataclass
class QueueStatistics:

    started: bool = False

    queued: int = 0

    submitted: int = 0

    processed: int = 0

    worker_alive: bool = False


# -------------------------------------------------
# Executor Statistics
# -------------------------------------------------

@dataclass
class ParallelExecutorStatistics:

    worker_pool: Dict[str, Any] = field(
        default_factory=dict
    )

    scheduler: Dict[str, Any] = field(
        default_factory=dict
    )

    queue: Dict[str, Any] = field(
        default_factory=dict
    )

    concurrency: Dict[str, Any] = field(
        default_factory=dict
    )

    cancellation: Dict[str, Any] = field(
        default_factory=dict
    )