import json

from app.observability.prometheus_metrics import PrometheusMetrics


def pretty(data):

    print(
        json.dumps(
            data,
            indent=2,
        )
    )


print("\n=== Prometheus Metrics Test ===\n")

# -------------------------------------------------
# Initialize
# -------------------------------------------------

print("Initializing Prometheus Metrics\n")

metrics = PrometheusMetrics()

pretty(
    metrics.statistics()
)

# -------------------------------------------------
# Counter
# -------------------------------------------------

print("\nCounter Metrics\n")

print(
    metrics.counter(
        "http_requests_total"
    )
)

print(
    metrics.counter(
        "http_requests_total",
        value=4,
    )
)

print(
    metrics.counter(
        "tool_calls_total",
        labels={
            "tool": "github.search",
        },
    )
)

pretty(
    metrics.statistics()
)

# -------------------------------------------------
# Gauge
# -------------------------------------------------

print("\nGauge Metrics\n")

metrics.gauge(
    "cpu_usage_percent",
    72.5,
)

metrics.gauge(
    "memory_usage_percent",
    61.2,
)

metrics.gauge(
    "active_sessions",
    18,
)

pretty(
    metrics.statistics()
)

# -------------------------------------------------
# Histogram
# -------------------------------------------------

print("\nHistogram Metrics\n")

metrics.histogram(
    "request_duration_seconds",
    0.18,
)

metrics.histogram(
    "request_duration_seconds",
    0.42,
)

metrics.histogram(
    "request_duration_seconds",
    0.25,
)

pretty(
    metrics.metric(
        "request_duration_seconds"
    )
)

# -------------------------------------------------
# Summary
# -------------------------------------------------

print("\nSummary Metrics\n")

metrics.summary(
    "llm_latency_seconds",
    1.15,
)

metrics.summary(
    "llm_latency_seconds",
    0.94,
)

metrics.summary(
    "llm_latency_seconds",
    1.37,
)

pretty(
    metrics.metric(
        "llm_latency_seconds"
    )
)

# -------------------------------------------------
# Exists
# -------------------------------------------------

print("\nMetric Exists\n")

print(
    "cpu_usage_percent"
)

print(
    metrics.exists(
        "cpu_usage_percent"
    )
)

print()

print(
    "unknown_metric"
)

print(
    metrics.exists(
        "unknown_metric"
    )
)

# -------------------------------------------------
# Statistics
# -------------------------------------------------

print("\nStatistics\n")

pretty(
    metrics.statistics()
)

# -------------------------------------------------
# Prometheus Scrape
# -------------------------------------------------

print("\nPrometheus Scrape\n")

print(
    metrics.scrape()
)

# -------------------------------------------------
# Export
# -------------------------------------------------

print("\nExport\n")

pretty(
    metrics.export()
)

# -------------------------------------------------
# Cleanup
# -------------------------------------------------

print("\nCleanup\n")

metrics.clear()

pretty(
    metrics.statistics()
)

print("\nPrometheus Metrics Test Passed")