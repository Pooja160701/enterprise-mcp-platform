import json
import time

from app.observability.metrics import Metrics


def pretty(data):
    print(json.dumps(data, indent=2))


print("\n=== Metrics Test ===\n")

# -------------------------------------------------
# Initialize
# -------------------------------------------------

print("Initializing Metrics\n")

metrics = Metrics()

pretty(
    metrics.statistics()
)

# -------------------------------------------------
# Counter
# -------------------------------------------------

print("\nCounter Metrics\n")

print(
    metrics.increment(
        "requests_total"
    )
)

print(
    metrics.increment(
        "requests_total",
        5,
    )
)

print(
    metrics.counter(
        "errors_total",
        labels={
            "service": "gateway"
        },
    )
)

print("\nCounter Values\n")

print(
    "requests_total"
)

print(
    metrics.counter_value(
        "requests_total"
    )
)

print(
    "\nerrors_total"
)

print(
    metrics.counter_value(
        "errors_total"
    )
)

# -------------------------------------------------
# Gauge
# -------------------------------------------------

print("\nGauge Metrics\n")

metrics.gauge(
    "cpu_usage",
    72.5,
    labels={
        "host": "server-01"
    },
)

metrics.gauge(
    "memory_usage",
    61.8,
)

print("\nGauge Values\n")

print("cpu_usage")

print(
    metrics.gauge_value(
        "cpu_usage"
    )
)

print("\nmemory_usage")

print(
    metrics.gauge_value(
        "memory_usage"
    )
)

# -------------------------------------------------
# Histogram
# -------------------------------------------------

print("\nHistogram Metrics\n")

metrics.histogram(
    "response_time",
    0.12,
)

metrics.histogram(
    "response_time",
    0.18,
)

metrics.histogram(
    "response_time",
    0.15,
)

print("\nHistogram Statistics\n")

pretty(
    metrics.histogram_statistics(
        "response_time"
    )
)

# -------------------------------------------------
# Timer
# -------------------------------------------------

print("\nTimer Metrics\n")

metrics.start_timer(
    "tool_execution"
)

time.sleep(0.2)

duration = metrics.stop_timer(
    "tool_execution"
)

print(duration)

print("\nTimer Statistics\n")

pretty(
    metrics.timer_statistics(
        "tool_execution"
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

print("\nMetrics Test Passed ✓")