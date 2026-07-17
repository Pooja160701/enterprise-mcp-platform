from copy import deepcopy
import time
import uuid


class DistributedTracing:
    """
    Enterprise Distributed Tracing

    Tracks requests across multiple services using
    trace IDs and spans.

    Features

    ✓ Create Trace
    ✓ Start Span
    ✓ Finish Span
    ✓ Parent/Child Relationships
    ✓ Service Tracking
    ✓ Duration Calculation
    ✓ Statistics
    ✓ Export

    Used by

    - API Gateway
    - Tool Executor
    - Workflow Engine
    - OpenTelemetry
    - Observability Manager
    """

    def __init__(self):

        self.clear()

    # -------------------------------------------------
    # Start Trace
    # -------------------------------------------------

    def start_trace(
        self,
        name,
        service="gateway",
    ):

        self._trace_id = str(
            uuid.uuid4()
        )

        self._trace_name = name

        self._service = service

        self._trace_started = time.time()

        return self._trace_id

    # -------------------------------------------------
    # Start Span
    # -------------------------------------------------

    def start_span(
        self,
        name,
        service=None,
        parent=None,
    ):

        span = {

            "id": str(uuid.uuid4()),

            "parent": parent,

            "name": name,

            "service": service or self._service,

            "start": time.time(),

            "end": None,

            "duration": 0.0,

            "status": "running",

        }

        self._spans.append(span)

        return span["id"]

    # -------------------------------------------------
    # Finish Span
    # -------------------------------------------------

    def finish_span(
        self,
        span_id,
        status="completed",
    ):

        for span in self._spans:

            if span["id"] == span_id:

                if span["end"] is not None:

                    return False

                span["end"] = time.time()

                span["duration"] = round(

                    span["end"] - span["start"],

                    3,

                )

                span["status"] = status

                return True

        return False

    # -------------------------------------------------
    # Finish Trace
    # -------------------------------------------------

    def finish_trace(
        self,
    ):

        self._trace_finished = time.time()

        self._trace_duration = round(

            self._trace_finished -

            self._trace_started,

            3,

        )

        return True

    # -------------------------------------------------
    # Trace ID
    # -------------------------------------------------

    def trace_id(
        self,
    ):

        return self._trace_id

    # -------------------------------------------------
    # Spans
    # -------------------------------------------------

    def spans(
        self,
    ):

        return deepcopy(
            self._spans
        )

    # -------------------------------------------------
    # Find Span
    # -------------------------------------------------

    def span(
        self,
        span_id,
    ):

        for span in self._spans:

            if span["id"] == span_id:

                return deepcopy(span)

        return None

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ):

        completed = sum(

            span["status"] == "completed"

            for span in self._spans

        )

        running = sum(

            span["status"] == "running"

            for span in self._spans

        )

        return {

            "trace_id": self._trace_id,

            "trace_name": self._trace_name,

            "service": self._service,

            "spans": len(self._spans),

            "completed_spans": completed,

            "running_spans": running,

            "duration": self._trace_duration,

        }

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(
        self,
    ):

        return {

            "trace": {

                "id": self._trace_id,

                "name": self._trace_name,

                "service": self._service,

                "started_at": self._trace_started,

                "finished_at": self._trace_finished,

                "duration": self._trace_duration,

            },

            "spans": deepcopy(
                self._spans
            ),

        }

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(
        self,
    ):

        self._trace_id = ""

        self._trace_name = ""

        self._service = ""

        self._trace_started = None

        self._trace_finished = None

        self._trace_duration = 0.0

        self._spans = []

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @staticmethod
    def empty():

        return DistributedTracing()