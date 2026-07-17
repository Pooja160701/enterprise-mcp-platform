import json

from app.reasoning.reasoning_engine import ReasoningEngine


print("\n=== Reasoning Engine Test ===\n")

engine = ReasoningEngine()

# -------------------------------------------------
# Initial State
# -------------------------------------------------

print("Initializing Reasoning Engine\n")

print(
    json.dumps(
        engine.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Run Reasoning
# -------------------------------------------------

print("\nRunning Reasoning\n")

engine.reason(
    "List all GitHub repositories."
)

# -------------------------------------------------
# Query
# -------------------------------------------------

print("Query\n")

print(
    engine.query()
)

# -------------------------------------------------
# Goal
# -------------------------------------------------

print("\nGoal\n")

print(
    engine.goal()
)

# -------------------------------------------------
# Execution Plan
# -------------------------------------------------

print("\nExecution Plan\n")

print(
    json.dumps(
        engine.plan(),
        indent=2,
    )
)

# -------------------------------------------------
# Reasoning Steps
# -------------------------------------------------

print("\nReasoning Steps\n")

print(
    json.dumps(
        engine.steps(),
        indent=2,
    )
)

# -------------------------------------------------
# Completed
# -------------------------------------------------

print("\nCompleted\n")

print(
    engine.completed()
)

# -------------------------------------------------
# Statistics
# -------------------------------------------------

print("\nStatistics\n")

print(
    json.dumps(
        engine.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Export
# -------------------------------------------------

print("\nExport\n")

print(
    json.dumps(
        engine.export(),
        indent=2,
    )
)

# -------------------------------------------------
# Clear
# -------------------------------------------------

print("\nCleanup\n")

engine.clear()

print(
    json.dumps(
        engine.statistics(),
        indent=2,
    )
)

print("\nReasoning Engine Test Passed")