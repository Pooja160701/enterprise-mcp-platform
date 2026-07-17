from copy import deepcopy
from collections import Counter
import json
import time
import uuid


class StructuredLogger:
    """
    Enterprise Structured Logger

    JSON-based structured logging for enterprise
    AI agents, workflows and MCP services.

    Features

    ✓ JSON Structured Logs
    ✓ INFO / WARNING / ERROR / DEBUG
    ✓ Correlation IDs
    ✓ Request IDs
    ✓ Custom Context
    ✓ Search
    ✓ Export
    ✓ Statistics

    Used by

    - Observability Manager
    - Agent Service
    - Tool Executor
    - Workflow Engine
    - API Gateway
    """

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

    def __init__(self):

        self.clear()

    # -------------------------------------------------
    # Generic Log
    # -------------------------------------------------

    def log(
        self,
        level,
        message,
        **kwargs,
    ):

        level = str(level).upper()

        if level == self.DEBUG:
            return self.debug(message, **kwargs)

        if level == self.INFO:
            return self.info(message, **kwargs)

        if level == self.WARNING:
            return self.warning(message, **kwargs)

        if level == self.ERROR:
            return self.error(message, **kwargs)

        if level == self.CRITICAL:
            return self.critical(message, **kwargs)

        raise ValueError(f"Unknown log level: {level}")

    # -------------------------------------------------
    # Internal Log
    # -------------------------------------------------

    def _log(
        self,
        level,
        message,
        *,
        service=None,
        component=None,
        correlation_id=None,
        request_id=None,
        metadata=None,
        **extra,
    ):

        metadata = deepcopy(metadata or {})
        metadata.update(extra)

        entry = {

            "id": len(self._logs) + 1,

            "timestamp": time.time(),

            "level": level,

            "message": message,

            "service": service,

            "component": component,

            "correlation_id": (
                correlation_id
                or self._correlation_id
            ),

            "request_id": (
                request_id
                or str(uuid.uuid4())
            ),

            "metadata": metadata,

        }

        self._logs.append(entry)

        self._counter[level] += 1

        self._last = deepcopy(entry)

        return deepcopy(entry)

    # -------------------------------------------------
    # Debug
    # -------------------------------------------------

    def debug(
        self,
        message,
        **kwargs,
    ):

        return self._log(
            self.DEBUG,
            message,
            **kwargs,
        )

    # -------------------------------------------------
    # Info
    # -------------------------------------------------

    def info(
        self,
        message,
        **kwargs,
    ):

        return self._log(
            self.INFO,
            message,
            **kwargs,
        )

    # -------------------------------------------------
    # Warning
    # -------------------------------------------------

    def warning(
        self,
        message,
        **kwargs,
    ):

        return self._log(
            self.WARNING,
            message,
            **kwargs,
        )

    # -------------------------------------------------
    # Error
    # -------------------------------------------------

    def error(
        self,
        message,
        **kwargs,
    ):

        return self._log(
            self.ERROR,
            message,
            **kwargs,
        )

    # -------------------------------------------------
    # Critical
    # -------------------------------------------------

    def critical(
        self,
        message,
        **kwargs,
    ):

        return self._log(
            self.CRITICAL,
            message,
            **kwargs,
        )

    # -------------------------------------------------
    # Correlation ID
    # -------------------------------------------------

    def set_correlation_id(
        self,
        correlation_id=None,
    ):

        self._correlation_id = (

            correlation_id

            or str(uuid.uuid4())

        )

        return self._correlation_id

    # -------------------------------------------------
    # Search by Level
    # -------------------------------------------------

    def by_level(
        self,
        level,
    ):

        return [

            deepcopy(log)

            for log in self._logs

            if log["level"] == level

        ]

    # -------------------------------------------------
    # Search by Service
    # -------------------------------------------------

    def by_service(
        self,
        service,
    ):

        return [

            deepcopy(log)

            for log in self._logs

            if log["service"] == service

        ]

    # -------------------------------------------------
    # Search Text
    # -------------------------------------------------

    def search(
        self,
        keyword,
    ):

        keyword = str(keyword).lower()

        return [

            deepcopy(log)

            for log in self._logs

            if keyword in log["message"].lower()

        ]

    # -------------------------------------------------
    # Latest
    # -------------------------------------------------

    def latest(
        self,
    ):

        if not self._logs:

            return None

        return deepcopy(

            self._logs[-1]

        )

    # -------------------------------------------------
    # Logs
    # -------------------------------------------------

    def logs(
        self,
    ):

        return deepcopy(

            self._logs

        )

    # -------------------------------------------------
    # JSON Export
    # -------------------------------------------------

    def to_json(
        self,
        indent=2,
    ):

        return json.dumps(

            self._logs,

            indent=indent,

        )

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ):

        return {

            "logs": len(
                self._logs
            ),

            "debug": self._counter[
                self.DEBUG
            ],

            "info": self._counter[
                self.INFO
            ],

            "warning": self._counter[
                self.WARNING
            ],

            "error": self._counter[
                self.ERROR
            ],

            "critical": self._counter[
                self.CRITICAL
            ],

            "correlation_id": self._correlation_id,

        }

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(
        self,
    ):

        return {

            "correlation_id": self._correlation_id,

            "logs": deepcopy(
                self._logs
            ),

            "last": deepcopy(
                self._last
            ),

        }

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(
        self,
    ):

        self._logs = []

        self._counter = Counter()

        self._last = None

        self._correlation_id = str(
            uuid.uuid4()
        )

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @staticmethod
    def empty():

        return StructuredLogger()