from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# =====================================================
# Structured Logging Models
# =====================================================

class LogEntry(BaseModel):
    timestamp: float
    level: str
    message: str
    correlation_id: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class LoggerStatistics(BaseModel):
    logs: int = 0
    debug: int = 0
    info: int = 0
    warning: int = 0
    error: int = 0
    critical: int = 0
    correlation_id: str = ""


# =====================================================
# Metrics Models
# =====================================================

class Metric(BaseModel):
    name: str
    value: float
    labels: Dict[str, str] = Field(default_factory=dict)
    timestamp: float


class CounterMetric(Metric):
    pass


class GaugeMetric(Metric):
    pass


class HistogramMetric(Metric):
    buckets: List[float] = Field(default_factory=list)


class SummaryMetric(Metric):
    quantiles: Dict[str, float] = Field(default_factory=dict)


class MetricsStatistics(BaseModel):
    counters: int = 0
    gauges: int = 0
    histograms: int = 0
    timers: int = 0
    running_timers: int = 0
    last_updated: Optional[float] = None

# =====================================================
# OpenTelemetry Models
# =====================================================

class SpanEvent(BaseModel):
    timestamp: float
    name: str
    attributes: Dict[str, Any] = Field(default_factory=dict)


class Span(BaseModel):
    span_id: str
    trace_id: str
    service: str = ""
    parent: Optional[str] = None
    name: str
    attributes: Dict[str, Any] = Field(default_factory=dict)
    events: List[SpanEvent] = Field(default_factory=list)
    status: str = "OK"
    started_at: float
    ended_at: Optional[float] = None
    duration: Optional[float] = None


class Trace(BaseModel):
    trace_id: str
    trace_name: str
    service: str = ""
    started_at: Optional[float] = None
    duration: float = 0.0
    spans: List[Span] = Field(default_factory=list)


class TraceStatistics(BaseModel):
    trace_id: str = ""
    trace_name: str = ""
    service: str = ""
    spans: int = 0
    active_spans: int = 0
    completed_spans: int = 0
    duration: float = 0.0


# =====================================================
# Distributed Tracing Models
# =====================================================

class DistributedTraceStatistics(BaseModel):
    trace_id: str = ""
    trace_name: str = ""
    service: str = ""
    spans: int = 0
    completed_spans: int = 0
    running_spans: int = 0
    duration: float = 0.0

# =====================================================
# Grafana Dashboard Models
# =====================================================

class DashboardVariable(BaseModel):
    name: str
    query: str
    label: str = ""
    variable_type: str = "query"


class DashboardAnnotation(BaseModel):
    name: str
    datasource: str = ""
    enabled: bool = True
    icon_color: str = "rgba(0, 211, 255, 1)"


class DashboardPanel(BaseModel):
    id: int = 0
    title: str
    panel_type: str = "timeseries"
    datasource: str = "Prometheus"
    grid_pos: Dict[str, int] = Field(default_factory=dict)
    targets: List[Dict[str, Any]] = Field(default_factory=list)
    options: Dict[str, Any] = Field(default_factory=dict)


class Dashboard(BaseModel):
    title: str
    uid: str
    refresh: str = "30s"
    timezone: str = "browser"
    schema_version: int = 39
    version: int = 1
    panels: List[DashboardPanel] = Field(default_factory=list)
    variables: List[DashboardVariable] = Field(default_factory=list)
    annotations: List[DashboardAnnotation] = Field(default_factory=list)
    created_at: float


class DashboardStatistics(BaseModel):
    title: str = ""
    uid: str = ""
    panels: int = 0
    variables: int = 0
    annotations: int = 0
    refresh: str = "30s"
    created_at: Optional[float] = None


# =====================================================
# Prometheus Models
# =====================================================

class PrometheusStatistics(BaseModel):
    metrics: int = 0
    counters: int = 0
    gauges: int = 0
    histograms: int = 0
    summaries: int = 0

# =====================================================
# Enterprise Observability Models
# =====================================================

class ObservabilityStatistics(BaseModel):
    structured_logger: LoggerStatistics
    metrics: MetricsStatistics
    opentelemetry: TraceStatistics
    prometheus: PrometheusStatistics
    grafana: DashboardStatistics
    distributed_tracing: DistributedTraceStatistics


class ObservabilityExport(BaseModel):
    structured_logger: List[LogEntry] = Field(default_factory=list)
    metrics: List[Metric] = Field(default_factory=list)
    opentelemetry: Trace
    prometheus: Dict[str, Any] = Field(default_factory=dict)
    grafana: Dashboard
    distributed_tracing: Trace


# =====================================================
# Generic API Response Models
# =====================================================

class StatusResponse(BaseModel):
    success: bool = True
    message: str = ""


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    details: Optional[Dict[str, Any]] = None


class HealthResponse(BaseModel):
    status: str = "healthy"
    timestamp: float
    services: Dict[str, str] = Field(default_factory=dict)


# =====================================================
# Module Exports
# =====================================================

__all__ = [
    # Logging
    "LogEntry",
    "LoggerStatistics",

    # Metrics
    "Metric",
    "CounterMetric",
    "GaugeMetric",
    "HistogramMetric",
    "SummaryMetric",
    "MetricsStatistics",

    # Tracing
    "SpanEvent",
    "Span",
    "Trace",
    "TraceStatistics",
    "DistributedTraceStatistics",

    # Dashboard
    "DashboardVariable",
    "DashboardAnnotation",
    "DashboardPanel",
    "Dashboard",
    "DashboardStatistics",

    # Prometheus
    "PrometheusStatistics",

    # Enterprise
    "ObservabilityStatistics",
    "ObservabilityExport",

    # API
    "StatusResponse",
    "ErrorResponse",
    "HealthResponse",
]