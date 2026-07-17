import json
import time

from app.observability.opentelemetry import OpenTelemetry


def pretty(data):
    print(json.dumps(data, indent=2))


print("\n=== OpenTelemetry Test ===\n")

# -------------------------------------------------
# Initialize
# -------------------------------------------------

print("Initializing OpenTelemetry\n")

otel = OpenTelemetry()

pretty(
    otel.statistics()
)

# -------------------------------------------------
# Start Trace
# -------------------------------------------------

print("\nStarting Trace\n")

trace_id = otel.start_trace(
    "Enterprise MCP Request"
)

print(trace_id)

print("\nTrace ID\n")

print(
    otel.trace_id()
)

# -------------------------------------------------
# Root Span
# -------------------------------------------------

print("\nStarting Root Span\n")

root = otel.start_span(
    "API Gateway"
)

print(root)

# -------------------------------------------------
# Attributes
# -------------------------------------------------

print("\nAdding Attributes\n")

otel.attribute(
    "user",
    "alice",
)

otel.attribute(
    "request_id",
    "REQ-001",
)

otel.attribute(
    "service",
    "gateway",
)

pretty(
    otel.current_span()
)

# -------------------------------------------------
# Events
# -------------------------------------------------

print("\nAdding Events\n")

otel.event(
    "request_received"
)

otel.event(
    "authentication_success",
    {
        "role": "admin"
    },
)

pretty(
    otel.current_span()
)

# -------------------------------------------------
# Child Span
# -------------------------------------------------

print("\nStarting Child Span\n")

child = otel.start_span(
    "GitHub Tool",
    parent=root,
)

print(child)

otel.attribute(
    "tool",
    "github.list_repositories",
)

otel.event(
    "tool_execution_started"
)

time.sleep(0.1)

otel.event(
    "tool_execution_finished"
)

otel.end_span(
    child
)

print("\nChild Span\n")

pretty(
    otel.span(
        child
    )
)

# -------------------------------------------------
# Error Span
# -------------------------------------------------

print("\nCreating Error Span\n")

error_span = otel.start_span(
    "Database"
)

otel.error(
    "Connection timeout"
)

otel.end_span(
    error_span,
    status=OpenTelemetry.ERROR,
)

pretty(
    otel.span(
        error_span
    )
)

# -------------------------------------------------
# End Root Span
# -------------------------------------------------

print("\nEnding Root Span\n")

time.sleep(0.1)

otel.end_span(
    root
)

pretty(
    otel.span(
        root
    )
)

# -------------------------------------------------
# Statistics
# -------------------------------------------------

print("\nStatistics\n")

pretty(
    otel.statistics()
)

# -------------------------------------------------
# Export
# -------------------------------------------------

print("\nExport\n")

pretty(
    otel.export()
)

# -------------------------------------------------
# Cleanup
# -------------------------------------------------

print("\nCleanup\n")

otel.clear()

pretty(
    otel.statistics()
)

print("\nOpenTelemetry Test Passed")