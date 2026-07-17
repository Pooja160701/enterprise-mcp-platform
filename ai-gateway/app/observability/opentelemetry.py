from copy import deepcopy
import time
import uuid


class OpenTelemetry:
    """
    Enterprise OpenTelemetry

    Lightweight tracing implementation compatible with
    ObservabilityManager and DistributedTracing.
    """

    OK = "OK"
    ERROR = "ERROR"

    def __init__(self):

        self.clear()

    # -------------------------------------------------
    # Trace
    # -------------------------------------------------

    def start_trace(
        self,
        name,
        service=None,
    ):

        self.clear()

        self._trace_id = str(uuid.uuid4())

        self._trace_name = name

        self._service = service or ""

        self._started = time.time()

        return self._trace_id

    def finish_trace(
        self,
        trace_id=None,
        **kwargs,
    ):

        # compatibility argument
        if trace_id is not None:
            self._trace_id = trace_id

        # close every active span
        for span_id, span in list(self._spans.items()):

            if span["ended_at"] is None:

                self.end_span(span_id)

        return self.export()

    # -------------------------------------------------
    # Span
    # -------------------------------------------------

    def start_span(
        self,
        name,
        trace_id=None,
        parent=None,
        parent_span=None,
        service=None,
        attributes=None,
    ):

        if trace_id is not None:

            self._trace_id = trace_id

        span_id = str(uuid.uuid4())

        span = {

            "span_id": span_id,

            "trace_id": self._trace_id,

            "service": service or self._service,

            "parent": parent if parent is not None else parent_span,

            "name": name,

            "attributes": deepcopy(
                attributes or {}
            ),

            "events": [],

            "status": self.OK,

            "started_at": time.time(),

            "ended_at": None,

            "duration": None,

        }

        self._spans[span_id] = span

        self._current = span_id

        return span_id

    def end_span(
        self,
        span_id=None,
        status=OK,
    ):

        span_id = span_id or self._current

        if span_id not in self._spans:

            return False

        span = self._spans[span_id]

        if span["ended_at"] is None:

            span["ended_at"] = time.time()

            span["duration"] = round(

                span["ended_at"]
                - span["started_at"],

                6,

            )

        span["status"] = status

        if self._current == span_id:

            self._current = None

        return True

    def finish_span(
        self,
        span_id=None,
        status=None,
        **kwargs,
    ):

        if status is None:

            status = self.OK

        return self.end_span(

            span_id=span_id,

            status=status,

        )
    
    # -------------------------------------------------
    # Attributes
    # -------------------------------------------------

    def attribute(
        self,
        key,
        value,
        span_id=None,
    ):

        span_id = span_id or self._current

        if span_id not in self._spans:

            return False

        self._spans[span_id]["attributes"][key] = deepcopy(value)

        return True

    def attributes(
        self,
        values,
        span_id=None,
    ):

        span_id = span_id or self._current

        if span_id not in self._spans:

            return False

        self._spans[span_id]["attributes"].update(
            deepcopy(values)
        )

        return True

    # -------------------------------------------------
    # Events
    # -------------------------------------------------

    def event(
        self,
        name,
        attributes=None,
        span_id=None,
    ):

        span_id = span_id or self._current

        if span_id not in self._spans:

            return False

        self._spans[span_id]["events"].append({

            "timestamp": time.time(),

            "name": name,

            "attributes": deepcopy(
                attributes or {}
            ),

        })

        return True

    def add_event(
        self,
        name,
        attributes=None,
        span_id=None,
    ):

        return self.event(

            name=name,

            attributes=attributes,

            span_id=span_id,

        )

    # -------------------------------------------------
    # Error
    # -------------------------------------------------

    def error(
        self,
        message,
        span_id=None,
    ):

        span_id = span_id or self._current

        if span_id not in self._spans:

            return False

        self.event(

            "error",

            {

                "message": message

            },

            span_id,

        )

        self._spans[span_id]["status"] = self.ERROR

        if self._spans[span_id]["ended_at"] is None:

            self.end_span(

                span_id,

                self.ERROR,

            )

        return True

    # -------------------------------------------------
    # Span Retrieval
    # -------------------------------------------------

    def current_span(
        self,
    ):

        if self._current is None:

            return None

        return deepcopy(

            self._spans[self._current]

        )

    def span(
        self,
        span_id,
    ):

        if span_id not in self._spans:

            return None

        return deepcopy(

            self._spans[span_id]

        )

    def spans(
        self,
    ):

        return deepcopy(

            list(

                self._spans.values()

            )

        )

    # -------------------------------------------------
    # Trace Info
    # -------------------------------------------------

    def trace_id(
        self,
    ):

        return self._trace_id

    def trace_name(
        self,
    ):

        return self._trace_name

    def service(
        self,
    ):

        return self._service

    def duration(
        self,
    ):

        if self._started is None:

            return 0.0

        return round(

            time.time() - self._started,

            6,

        )
    
    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ):

        completed = sum(

            span["ended_at"] is not None

            for span in self._spans.values()

        )

        active = len(self._spans) - completed

        return {

            "trace_id": self._trace_id,

            "trace_name": self._trace_name,

            "service": self._service,

            "spans": len(self._spans),

            "active_spans": active,

            "completed_spans": completed,

            "duration": self.duration(),

        }

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(
        self,
    ):

        return {

            "trace_id": self._trace_id,

            "trace_name": self._trace_name,

            "service": self._service,

            "started_at": self._started,

            "duration": self.duration(),

            "spans": deepcopy(

                list(

                    self._spans.values()

                )

            ),

        }

    # -------------------------------------------------
    # Reset
    # -------------------------------------------------

    def clear(
        self,
    ):

        self._trace_id = ""

        self._trace_name = ""

        self._service = ""

        self._started = None

        self._spans = {}

        self._current = None

    def reset(
        self,
    ):

        self.clear()

        return True

    # -------------------------------------------------
    # Compatibility Helpers
    # -------------------------------------------------

    def current_trace(
        self,
    ):

        return {

            "trace_id": self._trace_id,

            "trace_name": self._trace_name,

            "service": self._service,

            "started_at": self._started,

            "duration": self.duration(),

        }

    def trace(
        self,
    ):

        return self.current_trace()

    def traces(
        self,
    ):

        return [

            self.current_trace()

        ]

    def has_trace(
        self,
    ):

        return self._trace_id != ""

    def has_span(
        self,
        span_id,
    ):

        return span_id in self._spans

    # -------------------------------------------------
    # Factory
    # -------------------------------------------------

    @staticmethod
    def empty():

        return OpenTelemetry()