import json

from app.reasoning.goal_tracker import GoalTracker


print("\n=== Goal Tracker Test ===\n")

tracker = GoalTracker()

# -------------------------------------------------
# Initial State
# -------------------------------------------------

print("Initializing Goal Tracker\n")

print(
    json.dumps(
        tracker.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Add Goals
# -------------------------------------------------

print("\nAdding Goals\n")

goal1 = tracker.add(
    "List GitHub repositories",
    priority=100,
)

goal2 = tracker.add(
    "Search documentation",
    priority=90,
)

goal3 = tracker.add(
    "Summarize results",
    priority=80,
    depends_on=goal2,
)

print(goal1)
print(goal2)
print(goal3)

print(
    json.dumps(
        tracker.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Start Goals
# -------------------------------------------------

print("\nStarting Goals\n")

tracker.start(goal1)
tracker.start(goal2)

print(
    json.dumps(
        tracker.running(),
        indent=2,
    )
)

# -------------------------------------------------
# Update Progress
# -------------------------------------------------

print("\nUpdating Progress\n")

tracker.update(goal1, 50)
tracker.update(goal2, 80)

print(
    tracker.progress()
)

# -------------------------------------------------
# Complete Goals
# -------------------------------------------------

print("\nCompleting Goals\n")

tracker.complete(goal1)
tracker.complete(goal2)

print(
    json.dumps(
        tracker.completed(),
        indent=2,
    )
)

# -------------------------------------------------
# Fail Goal
# -------------------------------------------------

print("\nFailing Goal\n")

tracker.fail(goal3)

print(
    json.dumps(
        tracker.failed(),
        indent=2,
    )
)

# -------------------------------------------------
# Get Goal
# -------------------------------------------------

print("\nGet Goal\n")

print(
    json.dumps(
        tracker.get(goal1),
        indent=2,
    )
)

# -------------------------------------------------
# Pending Goals
# -------------------------------------------------

print("\nPending Goals\n")

print(
    json.dumps(
        tracker.pending(),
        indent=2,
    )
)

# -------------------------------------------------
# Statistics
# -------------------------------------------------

print("\nStatistics\n")

print(
    json.dumps(
        tracker.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Export
# -------------------------------------------------

print("\nExport\n")

print(
    json.dumps(
        tracker.export(),
        indent=2,
    )
)

# -------------------------------------------------
# Cleanup
# -------------------------------------------------

print("\nCleanup\n")

tracker.clear()

print(
    json.dumps(
        tracker.statistics(),
        indent=2,
    )
)

print("\nGoal Tracker Test Passed ✓")