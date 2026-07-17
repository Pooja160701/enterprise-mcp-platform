import json
import time

from app.observability.distributed_tracing import DistributedTracing


def pretty(data):

    print(
        json.dumps(
            data,
            indent=2,
        )
    )


print("\n=== Distributed Tracing Test ===\n")

# -------------------------------------------------
# Initialize
# -------------------------------------------------

print("Initializing Distributed Tracing\n")

tracer = DistributedTracing()

pretty(
    tracer.statistics()
)

# -------------------------------------------------
# Start Trace
# -------------------------------------------------

print("\nStarting Trace\n")

trace_id = tracer.start_trace(

    name="GitHub Repository Workflow",

    service="api-gateway",

)

print("Trace ID\n")
print(trace_id)

pretty(
    tracer.statistics()
)

# -------------------------------------------------
# Start Root Span
# -------------------------------------------------

print("\nStarting Root Span\n")

root_span = tracer.start_span(

    name="Handle User Request",

)

print(root_span)

time.sleep(0.1)

# -------------------------------------------------
# Start Child Span 1
# -------------------------------------------------

print("\nStarting Child Span 1\n")

github_span = tracer.start_span(

    name="GitHub MCP Tool",

    service="github-server",

    parent=root_span,

)

print(github_span)

time.sleep(0.1)

print("\nFinishing Child Span 1\n")

print(

    tracer.finish_span(

        github_span,

    )

)

# -------------------------------------------------
# Start Child Span 2
# -------------------------------------------------

print("\nStarting Child Span 2\n")

db_span = tracer.start_span(

    name="Database Lookup",

    service="database",

    parent=root_span,

)

print(db_span)

time.sleep(0.1)

print("\nFinishing Child Span 2\n")

print(

    tracer.finish_span(

        db_span,

    )

)

# -------------------------------------------------
# Finish Root Span
# -------------------------------------------------

print("\nFinishing Root Span\n")

print(

    tracer.finish_span(

        root_span,

    )

)

# -------------------------------------------------
# Finish Trace
# -------------------------------------------------

print("\nFinishing Trace\n")

print(
    tracer.finish_trace()
)

# -------------------------------------------------
# Statistics
# -------------------------------------------------

print("\nStatistics\n")

pretty(
    tracer.statistics()
)

# -------------------------------------------------
# Individual Span
# -------------------------------------------------

print("\nRoot Span\n")

pretty(
    tracer.span(root_span)
)

# -------------------------------------------------
# All Spans
# -------------------------------------------------

print("\nAll Spans\n")

pretty(
    tracer.spans()
)

# -------------------------------------------------
# Export
# -------------------------------------------------

print("\nExport\n")

pretty(
    tracer.export()
)

# -------------------------------------------------
# Cleanup
# -------------------------------------------------

print("\nCleanup\n")

tracer.clear()

pretty(
    tracer.statistics()
)

print("\nDistributed Tracing Test Passed")