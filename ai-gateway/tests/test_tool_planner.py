import json

from app.reasoning.tool_planner import ToolPlanner


print("\n=== Tool Planner Test ===\n")

planner = ToolPlanner()

# -------------------------------------------------
# Initial State
# -------------------------------------------------

print("Initializing Tool Planner\n")

print(
    json.dumps(
        planner.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Add Tools
# -------------------------------------------------

print("\nAdding Tools\n")

planner.add(
    tool="github.list_repositories",
    priority=100,
)

planner.add(
    tool="filesystem.search",
    arguments={
        "path": "/docs",
    },
    priority=90,
    parallel=True,
)

planner.add(
    tool="memory.search",
    arguments={
        "query": "repositories",
    },
    priority=80,
    parallel=True,
    depends_on="github.list_repositories",
)

print(
    json.dumps(
        planner.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Build Plan
# -------------------------------------------------

print("\nExecution Plan\n")

print(
    json.dumps(
        planner.build(),
        indent=2,
    )
)

# -------------------------------------------------
# Parallel Tasks
# -------------------------------------------------

print("\nParallel Tasks\n")

print(
    json.dumps(
        planner.parallel_groups(),
        indent=2,
    )
)

# -------------------------------------------------
# Sequential Tasks
# -------------------------------------------------

print("\nSequential Tasks\n")

print(
    json.dumps(
        planner.sequential_tasks(),
        indent=2,
    )
)

# -------------------------------------------------
# Checks
# -------------------------------------------------

print("\nHas Parallel\n")

print(
    planner.has_parallel()
)

print("\nHas Dependencies\n")

print(
    planner.has_dependencies()
)

# -------------------------------------------------
# Statistics
# -------------------------------------------------

print("\nStatistics\n")

print(
    json.dumps(
        planner.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Export
# -------------------------------------------------

print("\nExport\n")

print(
    json.dumps(
        planner.export(),
        indent=2,
    )
)

# -------------------------------------------------
# Cleanup
# -------------------------------------------------

print("\nCleanup\n")

planner.clear()

print(
    json.dumps(
        planner.statistics(),
        indent=2,
    )
)

print("\nTool Planner Test Passed ✓")