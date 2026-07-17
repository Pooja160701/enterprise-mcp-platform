import json
import time

from app.reasoning.reasoning_trace import ReasoningTrace


print("\n=== Reasoning Trace Test ===\n")

trace = ReasoningTrace()

# -------------------------------------------------
# Initial State
# -------------------------------------------------

print("Initializing Reasoning Trace\n")

print(
    json.dumps(
        trace.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Start Trace
# -------------------------------------------------

print("\nStarting Trace\n")

trace.start(
    "List all GitHub repositories."
)

# -------------------------------------------------
# Add Reasoning Steps
# -------------------------------------------------

print("Adding Reasoning Steps\n")

trace.add_step(
    "Understand Request",
)

trace.add_step(
    "Select Tool",
    {
        "tool": "github.list_repositories",
    },
)

trace.add_step(
    "Execute Tool",
)

# -------------------------------------------------
# Decision
# -------------------------------------------------

print("Decision\n")

trace.decision(
    "tool",
    "GitHub API required.",
)

# -------------------------------------------------
# Tool Calls
# -------------------------------------------------

print("Recording Tool Call\n")

trace.tool_call(
    "github.list_repositories",
    {},
)

# -------------------------------------------------
# Tool Results
# -------------------------------------------------

print("Recording Tool Result\n")

trace.tool_result(
    "github.list_repositories",
    "Found 12 repositories.",
)

# -------------------------------------------------
# Reflection
# -------------------------------------------------

print("Reflection\n")

trace.reflection(
    {
        "successful": True,
        "summary": "Execution completed successfully.",
    }
)

# -------------------------------------------------
# Self Critique
# -------------------------------------------------

print("Self Critique\n")

trace.critique(
    {
        "approved": True,
        "confidence": 100,
    }
)

# Small delay so duration isn't always zero
time.sleep(0.05)

# -------------------------------------------------
# Final Response
# -------------------------------------------------

print("Final Response\n")

trace.response(
    "Found 12 GitHub repositories.",
)

# -------------------------------------------------
# Statistics
# -------------------------------------------------

print("Statistics\n")

print(
    json.dumps(
        trace.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Export
# -------------------------------------------------

print("\nExport\n")

print(
    json.dumps(
        trace.export(),
        indent=2,
    )
)

# -------------------------------------------------
# Cleanup
# -------------------------------------------------

print("\nCleanup\n")

trace.clear()

print(
    json.dumps(
        trace.statistics(),
        indent=2,
    )
)

print("\nReasoning Trace Test Passed")