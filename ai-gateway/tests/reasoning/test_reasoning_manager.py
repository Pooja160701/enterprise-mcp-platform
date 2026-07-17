import json

from app.reasoning.reasoning_manager import ReasoningManager


print("\n=== Reasoning Manager Test ===\n")

manager = ReasoningManager()

# -------------------------------------------------
# Initial State
# -------------------------------------------------

print("Initializing Reasoning Manager\n")

print(
    json.dumps(
        manager.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Goal Management
# -------------------------------------------------

print("\nAdding Goals\n")

goal1 = manager.add_goal(
    "List GitHub repositories",
    priority=100,
)

goal2 = manager.add_goal(
    "Search documentation",
    priority=90,
)

print(goal1)
print(goal2)

print(
    json.dumps(
        manager.goal_statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Run Reasoning
# -------------------------------------------------

print("\nRunning Reasoning\n")

query = "List all GitHub repositories."

result = manager.run(query)

# -------------------------------------------------
# Reasoning
# -------------------------------------------------

print("\nReasoning\n")

print(
    json.dumps(
        result["reasoning"],
        indent=2,
    )
)

# -------------------------------------------------
# Decision
# -------------------------------------------------

print("\nDecision\n")

print(
    json.dumps(
        result["decision"],
        indent=2,
    )
)

# -------------------------------------------------
# Tool Plan
# -------------------------------------------------

print("\nTool Plan\n")

print(
    json.dumps(
        result["tool_plan"],
        indent=2,
    )
)

# -------------------------------------------------
# Reflection
# -------------------------------------------------

print("\nReflection\n")

print(
    json.dumps(
        result["reflection"],
        indent=2,
    )
)

# -------------------------------------------------
# Self Critique
# -------------------------------------------------

print("\nSelf Critique\n")

print(
    json.dumps(
        result["critique"],
        indent=2,
    )
)

# -------------------------------------------------
# Trace
# -------------------------------------------------

print("\nReasoning Trace\n")

print(
    json.dumps(
        result["trace"],
        indent=2,
    )
)

# -------------------------------------------------
# Statistics
# -------------------------------------------------

print("\nStatistics\n")

print(
    json.dumps(
        manager.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Export
# -------------------------------------------------

print("\nExport\n")

print(
    json.dumps(
        manager.export(),
        indent=2,
    )
)

# -------------------------------------------------
# Cleanup
# -------------------------------------------------

print("\nCleanup\n")

manager.clear()

print(
    json.dumps(
        manager.statistics(),
        indent=2,
    )
)

print("\nReasoning Manager Test Passed")