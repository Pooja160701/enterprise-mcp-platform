import json
import time

from app.observability.observability_manager import ObservabilityManager


def pretty(data):

    print(
        json.dumps(
            data,
            indent=2,
        )
    )


print("\n=== Observability Manager Test ===\n")

# -------------------------------------------------
# Initialize
# -------------------------------------------------

print("Initializing Observability Manager\n")

manager = ObservabilityManager()

pretty(
    manager.statistics()
)

# -------------------------------------------------
# Structured Logging
# -------------------------------------------------

print("\nStructured Logging\n")

manager.log(

    level="INFO",

    message="Enterprise MCP Platform Started",

    service="gateway",

    version="1.0.0",

)

manager.log(

    level="WARNING",

    message="High CPU Usage",

    cpu=91,

)

pretty(
    manager.logger.statistics()
)

# -------------------------------------------------
# Prometheus Metrics
# -------------------------------------------------

print("\nPrometheus Metrics\n")

manager.counter(
    "http_requests_total"
)

manager.counter(
    "http_requests_total",
    value=5,
)

manager.gauge(
    "cpu_usage_percent",
    67.8,
)

manager.histogram(
    "request_duration_seconds",
    0.213,
)

manager.summary(
    "llm_latency_seconds",
    1.45,
)

pretty(
    manager.prometheus.statistics()
)

# -------------------------------------------------
# OpenTelemetry
# -------------------------------------------------

print("\nOpenTelemetry\n")

trace_id = manager.opentelemetry.start_trace(

    "User Request"

)

span_id = manager.opentelemetry.start_span(

    "Gateway",

    trace_id=trace_id,

)

time.sleep(0.1)

manager.opentelemetry.finish_span(
    span_id
)

manager.opentelemetry.finish_trace(
    trace_id
)

pretty(
    manager.opentelemetry.statistics()
)

# -------------------------------------------------
# Distributed Tracing
# -------------------------------------------------

print("\nDistributed Tracing\n")

manager.start_trace(

    "Repository Search",

    service="gateway",

)

root = manager.start_span(

    "Gateway",

)

child = manager.start_span(

    "GitHub Tool",

    service="github",

    parent=root,

)

time.sleep(0.1)

manager.finish_span(
    child
)

manager.finish_span(
    root
)

manager.finish_trace()

pretty(
    manager.tracing.statistics()
)

# -------------------------------------------------
# Grafana Dashboard
# -------------------------------------------------

print("\nGrafana Dashboard\n")

manager.grafana.configure(

    title="Enterprise Dashboard",

)

manager.grafana.add_panel(

    title="CPU",

    panel_type="timeseries",

)

manager.grafana.add_panel(

    title="Memory",

    panel_type="timeseries",

)

manager.grafana.add_variable(

    "environment",

    "label_values(environment)",

)

manager.grafana.add_annotation(

    "Deployments",

)

pretty(
    manager.grafana.statistics()
)

# -------------------------------------------------
# Dashboard Preview
# -------------------------------------------------

print("\nDashboard\n")

pretty(
    manager.dashboard()
)

# -------------------------------------------------
# Statistics
# -------------------------------------------------

print("\nStatistics\n")

pretty(
    manager.statistics()
)

# -------------------------------------------------
# Export
# -------------------------------------------------

print("\nExport\n")

pretty(
    manager.export()
)

# -------------------------------------------------
# Cleanup
# -------------------------------------------------

print("\nCleanup\n")

manager.clear()

pretty(
    manager.statistics()
)

print("\nObservability Manager Test Passed")