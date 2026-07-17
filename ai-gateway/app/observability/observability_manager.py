from copy import deepcopy

from app.observability.structured_logger import StructuredLogger
from app.observability.metrics import Metrics
from app.observability.opentelemetry import OpenTelemetry
from app.observability.prometheus_metrics import PrometheusMetrics
from app.observability.grafana_dashboard import GrafanaDashboard
from app.observability.distributed_tracing import DistributedTracing


class ObservabilityManager:
    """
    Enterprise Observability Manager

                     Observability Manager
                              │
        ┌────────────┬────────────┬────────────┐
        │            │            │            │
      Logging      Metrics   OpenTelemetry  Tracing
        │            │            │            │
        └────────────┼────────────┼────────────┘
                     │
               Prometheus
                     │
                 Grafana

    Central observability layer for the
    Enterprise MCP Platform.
    """

    def __init__(self):

        self.logger = StructuredLogger()

        self.metrics = Metrics()

        self.opentelemetry = OpenTelemetry()

        self.prometheus = PrometheusMetrics()

        self.grafana = GrafanaDashboard()

        self.tracing = DistributedTracing()

    # -------------------------------------------------
    # Logging
    # -------------------------------------------------

    def log(
        self,
        level,
        message,
        **kwargs,
    ):

        return self.logger.log(
            level=level,
            message=message,
            **kwargs,
        )

    def debug(
        self,
        message,
        **kwargs,
    ):

        return self.logger.debug(
            message,
            **kwargs,
        )

    def info(
        self,
        message,
        **kwargs,
    ):

        return self.logger.info(
            message,
            **kwargs,
        )

    def warning(
        self,
        message,
        **kwargs,
    ):

        return self.logger.warning(
            message,
            **kwargs,
        )

    def error(
        self,
        message,
        **kwargs,
    ):

        return self.logger.error(
            message,
            **kwargs,
        )

    def critical(
        self,
        message,
        **kwargs,
    ):

        return self.logger.critical(
            message,
            **kwargs,
        )

    # -------------------------------------------------
    # Metrics
    # -------------------------------------------------

    def counter(
        self,
        name,
        value=1,
        labels=None,
    ):

        return self.prometheus.counter(
            name,
            value=value,
            labels=labels,
        )

    def gauge(
        self,
        name,
        value,
        labels=None,
    ):

        return self.prometheus.gauge(
            name,
            value,
            labels=labels,
        )

    def histogram(
        self,
        name,
        value,
        labels=None,
    ):

        return self.prometheus.histogram(
            name,
            value,
            labels=labels,
        )

    def summary(
        self,
        name,
        value,
        labels=None,
    ):

        return self.prometheus.summary(
            name,
            value,
            labels=labels,
        )

    # -------------------------------------------------
    # Distributed Tracing
    # -------------------------------------------------

    def start_trace(
        self,
        name,
        service="gateway",
    ):

        return self.tracing.start_trace(
            name=name,
            service=service,
        )

    def start_span(
        self,
        name,
        trace_id=None,
        parent=None,
        parent_span=None,
        service=None,
        attributes=None,
        **kwargs,
    ):

        return self.opentelemetry.start_span(
            name=name,
            trace_id=trace_id,
            parent=parent,
            parent_span=parent_span,
            service=service,
            attributes=attributes,
        )

    def finish_span(
        self,
        span_id=None,
        status=None,
    ):

        if status is None:
            status = self.opentelemetry.OK

        return self.opentelemetry.finish_span(
            span_id=span_id,
            status=status,
        )

    def finish_trace(
        self,
        trace_id=None,
    ):

        return self.opentelemetry.finish_trace(
            trace_id=trace_id,
        )

    # -------------------------------------------------
    # Dashboard
    # -------------------------------------------------

    def dashboard(
        self,
    ):

        return self.grafana.dashboard()

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ):

        return {

            "structured_logger": deepcopy(
                self.logger.statistics()
            ),

            "metrics": deepcopy(
                self.metrics.statistics()
            ),

            "opentelemetry": deepcopy(
                self.opentelemetry.statistics()
            ),

            "prometheus": deepcopy(
                self.prometheus.statistics()
            ),

            "grafana": deepcopy(
                self.grafana.statistics()
            ),

            "distributed_tracing": deepcopy(
                self.tracing.statistics()
            ),

        }

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(
        self,
    ):

        return {

            "structured_logger": deepcopy(
                self.logger.export()
            ),

            "metrics": deepcopy(
                self.metrics.export()
            ),

            "opentelemetry": deepcopy(
                self.opentelemetry.export()
            ),

            "prometheus": deepcopy(
                self.prometheus.export()
            ),

            "grafana": deepcopy(
                self.grafana.export()
            ),

            "distributed_tracing": deepcopy(
                self.tracing.export()
            ),

        }

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(
        self,
    ):

        self.logger.clear()

        self.metrics.clear()

        self.opentelemetry.clear()

        self.prometheus.clear()

        self.grafana.clear()

        self.tracing.clear()

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @staticmethod
    def empty():

        return ObservabilityManager()