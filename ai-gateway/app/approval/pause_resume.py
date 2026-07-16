from threading import Event, Lock
from copy import deepcopy
import time


class PauseResume:
    """
    Enterprise Pause / Resume Controller

    Controls execution state for workflows,
    tools and agents.

    Features

    ✓ Pause Execution
    ✓ Resume Execution
    ✓ Wait While Paused
    ✓ Stop Execution
    ✓ Reset
    ✓ Statistics

    Used by

    - Approval Manager
    - Workflow Engine
    - Parallel Executor
    - Agent Service
    """

    def __init__(self):

        self._lock = Lock()

        self._pause_event = Event()
        self._pause_event.set()

        self._paused = False
        self._stopped = False

        self._pause_count = 0
        self._resume_count = 0

        self._paused_at = None
        self._resumed_at = None

    # -------------------------------------------------
    # Pause
    # -------------------------------------------------

    def pause(self):

        with self._lock:

            if self._paused:
                return False

            self._paused = True

            self._pause_count += 1

            self._paused_at = time.time()

            self._pause_event.clear()

        return True

    # -------------------------------------------------
    # Resume
    # -------------------------------------------------

    def resume(self):

        with self._lock:

            if not self._paused:
                return False

            self._paused = False

            self._resume_count += 1

            self._resumed_at = time.time()

            self._pause_event.set()

        return True

    # -------------------------------------------------
    # Wait
    # -------------------------------------------------

    def wait(self):

        self._pause_event.wait()

    # -------------------------------------------------
    # Stop
    # -------------------------------------------------

    def stop(self):

        with self._lock:

            self._stopped = True

            self._pause_event.set()

    # -------------------------------------------------
    # Paused
    # -------------------------------------------------

    def paused(self):

        return self._paused

    # -------------------------------------------------
    # Running
    # -------------------------------------------------

    def running(self):

        return not self._paused and not self._stopped

    # -------------------------------------------------
    # Stopped
    # -------------------------------------------------

    def stopped(self):

        return self._stopped

    # -------------------------------------------------
    # Reset
    # -------------------------------------------------

    def reset(self):

        with self._lock:

            self._paused = False
            self._stopped = False

            self._pause_count = 0
            self._resume_count = 0

            self._paused_at = None
            self._resumed_at = None

            self._pause_event.set()

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(self):

        return {

            "paused": self._paused,

            "running": self.running(),

            "stopped": self._stopped,

            "pause_count": self._pause_count,

            "resume_count": self._resume_count,

        }

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(self):

        return {

            "paused": self._paused,

            "running": self.running(),

            "stopped": self._stopped,

            "pause_count": self._pause_count,

            "resume_count": self._resume_count,

            "paused_at": self._paused_at,

            "resumed_at": self._resumed_at,

        }

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @staticmethod
    def empty():

        return PauseResume()